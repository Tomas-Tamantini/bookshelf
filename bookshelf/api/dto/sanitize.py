def sanitize_name(name: str) -> str:
    alphanumeric = "".join(char for char in name if char.isalnum() or char.isspace())
    return " ".join(alphanumeric.split()).lower()
