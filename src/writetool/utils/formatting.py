"""Human-readable formatting utilities."""


def format_size(size_bytes: int) -> str:
    """Convert bytes to human-readable string."""
    if size_bytes < 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    if unit_index == 0:
        return f"{int(size)} B"
    return f"{size:.1f} {units[unit_index]}"


def format_speed(bytes_per_sec: float) -> str:
    """Convert bytes/sec to human-readable speed string."""
    return f"{format_size(int(bytes_per_sec))}/s"


def truncate_hash(hash_str: str, length: int = 16) -> str:
    """Truncate a hash string for display."""
    if len(hash_str) <= length:
        return hash_str
    return hash_str[:length] + "..."
