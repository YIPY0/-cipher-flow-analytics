"""
CIPHER-FLOW ANALYTICS — Live Packet Capture
Captures packets using Scapy and feeds them to the FlowBuilder.
"""
import threading
import time
import logging

from scapy.all import sniff, IP, TCP, UDP, conf

from capture.flow_builder import FlowBuilder
from config import settings

logger = logging.getLogger(__name__)


class PacketCapture:
    """
    Runs Scapy sniff in a background thread.
    Feeds captured packets into FlowBuilder.
    Also runs a periodic expiration thread.
    """

    def __init__(self, flow_builder: FlowBuilder, interface: str | None = None):
        self.flow_builder = flow_builder
        self.interface = interface or settings.CAPTURE_INTERFACE
        self._running = False
        self._capture_thread: threading.Thread | None = None
        self._expire_thread: threading.Thread | None = None
        self.packet_count = 0
        self.encrypted_count = 0

    def _process_packet(self, pkt):
        """Callback for each captured packet."""
        if not pkt.haslayer(IP):
            return

        ip = pkt[IP]
        src_ip = ip.src
        dst_ip = ip.dst
        proto = ip.proto
        length = len(pkt)
        ts = float(pkt.time)
        header_size = ip.ihl * 4

        src_port = 0
        dst_port = 0
        flags = {}
        win = 0

        if pkt.haslayer(TCP):
            tcp = pkt[TCP]
            src_port = tcp.sport
            dst_port = tcp.dport
            win = tcp.window
            f = tcp.flags
            flags = {
                "FIN": bool(f & 0x01),
                "SYN": bool(f & 0x02),
                "RST": bool(f & 0x04),
                "PSH": bool(f & 0x08),
                "ACK": bool(f & 0x10),
                "URG": bool(f & 0x20),
            }
            header_size += tcp.dataofs * 4
            # TLS detection: port 443 or payload starts with 0x16/0x17
            if dst_port == 443 or src_port == 443:
                self.encrypted_count += 1
        elif pkt.haslayer(UDP):
            udp = pkt[UDP]
            src_port = udp.sport
            dst_port = udp.dport
            header_size += 8

        self.packet_count += 1

        self.flow_builder.add_packet(
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=src_port,
            dst_port=dst_port,
            protocol=proto,
            length=length,
            header_size=header_size,
            timestamp=ts,
            flags=flags,
            window_size=win,
        )

    def _expire_loop(self):
        """Periodically check for timed-out flows."""
        while self._running:
            time.sleep(10)
            self.flow_builder.expire_flows()

    def start(self):
        """Start packet capture in background threads."""
        if self._running:
            return
        self._running = True

        logger.info(
            "Starting packet capture on interface=%s",
            self.interface or "default",
        )

        self._capture_thread = threading.Thread(
            target=self._sniff_loop, daemon=True, name="pkt-capture"
        )
        self._expire_thread = threading.Thread(
            target=self._expire_loop, daemon=True, name="flow-expire"
        )
        self._capture_thread.start()
        self._expire_thread.start()

    def _sniff_loop(self):
        """Run Scapy sniff (blocking)."""
        try:
            sniff(
                iface=self.interface,
                prn=self._process_packet,
                store=False,
                filter=settings.CAPTURE_BPF_FILTER,
                stop_filter=lambda _: not self._running,
            )
        except PermissionError:
            logger.error(
                "Permission denied — run with administrator/root privileges "
                "for live packet capture"
            )
        except Exception as e:
            logger.error("Capture error: %s", e)

    def stop(self):
        """Stop capture."""
        self._running = False
        self.flow_builder.flush_all()
        logger.info("Packet capture stopped. Total packets: %d", self.packet_count)

    @property
    def stats(self) -> dict:
        return {
            "total_packets": self.packet_count,
            "encrypted_sessions": self.encrypted_count,
            "active_flows": self.flow_builder.active_flow_count,
        }