"""
CIPHER-FLOW ANALYTICS — Flow Builder
Groups raw packets into bidirectional flows keyed by 5-tuple.
"""
import time
import threading
import logging
from collections import defaultdict
from dataclasses import dataclass, field

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class FlowRecord:
    """Accumulates packet-level data for one flow."""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: int
    start_time: float = 0.0
    last_time: float = 0.0

    # Forward = src→dst, Backward = dst→src
    fwd_packet_lengths: list = field(default_factory=list)
    bwd_packet_lengths: list = field(default_factory=list)
    fwd_timestamps: list = field(default_factory=list)
    bwd_timestamps: list = field(default_factory=list)
    fwd_header_sizes: list = field(default_factory=list)
    bwd_header_sizes: list = field(default_factory=list)

    # Flags
    fin_count: int = 0
    syn_count: int = 0
    rst_count: int = 0
    psh_count: int = 0
    ack_count: int = 0
    urg_count: int = 0
    fwd_psh_count: int = 0

    # Window sizes
    init_win_fwd: int = 0
    init_win_bwd: int = 0
    _first_fwd: bool = True
    _first_bwd: bool = True

    @property
    def flow_key(self) -> str:
        return f"{self.src_ip}:{self.src_port}-{self.dst_ip}:{self.dst_port}-{self.protocol}"

    @property
    def total_packets(self) -> int:
        return len(self.fwd_packet_lengths) + len(self.bwd_packet_lengths)


class FlowBuilder:
    """
    Maintains active flows and exports completed flows.
    Thread-safe for concurrent packet insertion.
    """

    def __init__(self, timeout: int = None, packet_threshold: int = None):
        self.timeout = timeout or settings.FLOW_TIMEOUT
        self.packet_threshold = packet_threshold or settings.FLOW_PACKET_THRESHOLD
        self.flows: dict[str, FlowRecord] = {}
        self._lock = threading.Lock()
        self._export_callbacks: list = []

    def on_export(self, callback):
        """Register a callback for when a flow is exported."""
        self._export_callbacks.append(callback)

    def _make_key(self, src_ip, dst_ip, src_port, dst_port, proto) -> tuple:
        """Canonical bidirectional key."""
        a = (src_ip, src_port)
        b = (dst_ip, dst_port)
        if a <= b:
            return (src_ip, src_port, dst_ip, dst_port, proto)
        return (dst_ip, dst_port, src_ip, src_port, proto)

    def add_packet(
        self,
        src_ip: str,
        dst_ip: str,
        src_port: int,
        dst_port: int,
        protocol: int,
        length: int,
        header_size: int,
        timestamp: float,
        flags: dict | None = None,
        window_size: int = 0,
    ):
        """Insert a packet into the appropriate flow."""
        key = self._make_key(src_ip, dst_ip, src_port, dst_port, protocol)
        key_str = f"{key[0]}:{key[1]}-{key[2]}:{key[3]}-{key[4]}"

        with self._lock:
            if key_str not in self.flows:
                self.flows[key_str] = FlowRecord(
                    src_ip=key[0],
                    dst_ip=key[2],
                    src_port=key[1],
                    dst_port=key[3],
                    protocol=key[4],
                    start_time=timestamp,
                    last_time=timestamp,
                )

            flow = self.flows[key_str]
            flow.last_time = timestamp

            # Determine direction
            is_forward = (src_ip == flow.src_ip and src_port == flow.src_port)

            if is_forward:
                flow.fwd_packet_lengths.append(length)
                flow.fwd_timestamps.append(timestamp)
                flow.fwd_header_sizes.append(header_size)
                if flow._first_fwd:
                    flow.init_win_fwd = window_size
                    flow._first_fwd = False
            else:
                flow.bwd_packet_lengths.append(length)
                flow.bwd_timestamps.append(timestamp)
                flow.bwd_header_sizes.append(header_size)
                if flow._first_bwd:
                    flow.init_win_bwd = window_size
                    flow._first_bwd = False

            # TCP flags
            if flags:
                if flags.get("FIN"): flow.fin_count += 1
                if flags.get("SYN"): flow.syn_count += 1
                if flags.get("RST"): flow.rst_count += 1
                if flags.get("PSH"):
                    flow.psh_count += 1
                    if is_forward:
                        flow.fwd_psh_count += 1
                if flags.get("ACK"): flow.ack_count += 1
                if flags.get("URG"): flow.urg_count += 1

            # Check export conditions
            if flow.total_packets >= self.packet_threshold:
                self._export_flow(key_str)

    def expire_flows(self):
        """Export all flows that have timed out."""
        now = time.time()
        expired = []
        with self._lock:
            for key_str, flow in self.flows.items():
                if now - flow.last_time > self.timeout:
                    expired.append(key_str)

        for key_str in expired:
            self._export_flow(key_str)

    def flush_all(self):
        """Export all active flows regardless of state."""
        with self._lock:
            keys = list(self.flows.keys())
        for k in keys:
            self._export_flow(k)

    def _export_flow(self, key_str: str):
        """Remove flow from active set and invoke callbacks."""
        with self._lock:
            flow = self.flows.pop(key_str, None)
        if flow and flow.total_packets >= 2:
            for cb in self._export_callbacks:
                try:
                    cb(flow)
                except Exception as e:
                    logger.error("Export callback error: %s", e)

    @property
    def active_flow_count(self) -> int:
        return len(self.flows)