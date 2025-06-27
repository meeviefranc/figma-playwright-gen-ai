def log_message(message: str) -> None:
    """Logs a message to the console."""
    print(f"[LOG] {message}")

def save_to_file(file_path: str, content: str) -> None:
    """Saves the given content to a specified file."""
    with open(file_path, 'w') as file:
        file.write(content)
    log_message(f"Content saved to {file_path}")

def read_from_file(file_path: str) -> str:
    """Reads content from a specified file."""
    with open(file_path, 'r') as file:
        content = file.read()
    log_message(f"Content read from {file_path}")
    return content

def validate_figma_credentials(access_token: str, file_key: str) -> bool:
    """Validates the provided Figma API credentials."""
    return bool(access_token) and bool(file_key)