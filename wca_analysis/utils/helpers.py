"""
Helper utility functions
"""

import pandas as pd
import numpy as np


def format_time(seconds):
    """Format time in seconds to readable format"""
    if seconds is None or pd.isna(seconds):
        return "N/A"
    if seconds < 60:
        return f"{seconds:.2f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:05.2f}"


def calculate_percentile(data, percentile):
    """Calculate percentile of data"""
    if len(data) == 0:
        return None
    return np.percentile(data, percentile)


def get_event_name(event_id, event_names):
    """Get event name from event ID"""
    return event_names.get(event_id, event_id)


def safe_divide(a, b):
    """Safe division that handles division by zero"""
    if b == 0:
        return 0
    return a / b
