def short_msg(val: str) -> str:
    """Shorten the message to 15 characters, adding '...' if longer."""
    if not isinstance(val, str):
        raise TypeError(f"Expected str, got {type(val)}")

    if not val:
        return ""
    return val[:15] + ("..." if len(val) > 15 else "")
