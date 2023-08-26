def module_name(name: str) -> str:
    """Convert string to python module name."""
    return name.replace("-", "_").replace(".", "_").replace("/", "_").lower()
