"""
CIPHER-FLOW ANALYTICS — Live Feature Extractor
Converts a FlowRecord into the same feature vector used for ML training.
"""
import numpy as np
import logging

from capture.flow_builder import FlowRecord

logger = logging.getLogger(__name__)


def _safe_stats(arr: list) -> dict:
    """Compute mean, std, max, min, total for a numeric list."""
    if not arr:
        return {"mean": 0, "std": 0, "max": 0, "min": 0, "total": 0}
    a = np.array(arr, dtype=float)
    return {
        "mean": float(np.mean(a)),
        "std": float(np.std(a)),
        "max": float(np.max(a)),
        "min": float(np.min(a)),
        "total": float(np.sum(a)),
    }


def _iat(timestamps: list) -> dict:
    """Compute inter-arrival time statistics."""
    if len(timestamps) < 2:
        return {"mean": 0, "std": 0, "max": 0, "min": 0, "total": 0}
    ts = np.array(sorted(timestamps))
    diffs = np.diff(ts) * 1e6  # convert to microseconds
    return {
        "mean": float(np.mean(diffs)),
        "std": float(np.std(diffs)),
        "max": float(np.max(diffs)),
        "min": float(np.min(diffs)),
        "total": float(np.sum(diffs)),
    }


def extract_features(flow: FlowRecord) -> dict:
    """
    Extract ML feature vector from a completed FlowRecord.
    Returns dict matching SELECTED_FEATURES ordering.
    """
    duration_us = max((flow.last_time - flow.start_time) * 1e6, 1.0)

    fwd_stats = _safe_stats(flow.fwd_packet_lengths)
    bwd_stats = _safe_stats(flow.bwd_packet_lengths)
    all_lengths = flow.fwd_packet_lengths + flow.bwd_packet_lengths
    all_stats = _safe_stats(all_lengths)

    fwd_iat = _iat(flow.fwd_timestamps)
    bwd_iat = _iat(flow.bwd_timestamps)
    all_iat = _iat(flow.fwd_timestamps + flow.bwd_timestamps)

    total_fwd = len(flow.fwd_packet_lengths)
    total_bwd = len(flow.bwd_packet_lengths)
    total_packets = total_fwd + total_bwd

    total_fwd_bytes = fwd_stats["total"]
    total_bwd_bytes = bwd_stats["total"]
    total_bytes = total_fwd_bytes + total_bwd_bytes

    features = {
        "flow_duration": duration_us,
        "total_fwd_packets": float(total_fwd),
        "total_bwd_packets": float(total_bwd),
        "total_length_fwd_packets": total_fwd_bytes,
        "total_length_bwd_packets": total_bwd_bytes,
        "fwd_packet_length_max": fwd_stats["max"],
        "fwd_packet_length_min": fwd_stats["min"],
        "fwd_packet_length_mean": fwd_stats["mean"],
        "fwd_packet_length_std": fwd_stats["std"],
        "bwd_packet_length_max": bwd_stats["max"],
        "bwd_packet_length_min": bwd_stats["min"],
        "bwd_packet_length_mean": bwd_stats["mean"],
        "bwd_packet_length_std": bwd_stats["std"],
        "flow_bytes_per_s": (total_bytes / duration_us) * 1e6 if duration_us > 0 else 0,
        "flow_packets_per_s": (total_packets / duration_us) * 1e6 if duration_us > 0 else 0,
        "flow_iat_mean": all_iat["mean"],
        "flow_iat_std": all_iat["std"],
        "flow_iat_max": all_iat["max"],
        "flow_iat_min": all_iat["min"],
        "fwd_iat_total": fwd_iat["total"],
        "fwd_iat_mean": fwd_iat["mean"],
        "fwd_iat_std": fwd_iat["std"],
        "fwd_iat_max": fwd_iat["max"],
        "fwd_iat_min": fwd_iat["min"],
        "bwd_iat_total": bwd_iat["total"],
        "bwd_iat_mean": bwd_iat["mean"],
        "bwd_iat_std": bwd_iat["std"],
        "bwd_iat_max": bwd_iat["max"],
        "bwd_iat_min": bwd_iat["min"],
        "fwd_psh_flags": float(flow.fwd_psh_count),
        "fwd_header_length": _safe_stats(flow.fwd_header_sizes)["mean"],
        "bwd_header_length": _safe_stats(flow.bwd_header_sizes)["mean"],
        "fwd_packets_per_s": (total_fwd / duration_us) * 1e6 if duration_us > 0 else 0,
        "bwd_packets_per_s": (total_bwd / duration_us) * 1e6 if duration_us > 0 else 0,
        "min_packet_length": all_stats["min"],
        "max_packet_length": all_stats["max"],
        "packet_length_mean": all_stats["mean"],
        "packet_length_std": all_stats["std"],
        "packet_length_variance": all_stats["std"] ** 2,
        "fin_flag_count": float(flow.fin_count),
        "syn_flag_count": float(flow.syn_count),
        "rst_flag_count": float(flow.rst_count),
        "psh_flag_count": float(flow.psh_count),
        "ack_flag_count": float(flow.ack_count),
        "average_packet_size": total_bytes / max(total_packets, 1),
        "avg_fwd_segment_size": fwd_stats["mean"],
        "avg_bwd_segment_size": bwd_stats["mean"],
        "init_win_bytes_forward": float(flow.init_win_fwd),
        "init_win_bytes_backward": float(flow.init_win_bwd),
        "active_mean": duration_us if total_packets > 0 else 0,
        "active_std": 0.0,
        "idle_mean": 0.0,
        "idle_std": 0.0,
    }

    # Metadata (not used by ML but stored in DB)
    metadata = {
        "src_ip": flow.src_ip,
        "dst_ip": flow.dst_ip,
        "src_port": flow.src_port,
        "dst_port": flow.dst_port,
        "protocol": flow.protocol,
    }

    return {"features": features, "metadata": metadata}