from pathlib import Path


def delete_file(file_path: Path = None) -> None:
    """
    This deletes a file from path (File System)
    """
    if file_path:
        file_path.unlink()
