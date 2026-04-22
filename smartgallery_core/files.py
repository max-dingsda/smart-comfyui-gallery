from __future__ import annotations

import os
import shutil
import time


def safe_delete_file(filepath: str, delete_to: str | None, trash_folder: str | None) -> None:
    """Delete a file permanently or move it into the configured trash area."""
    if delete_to and trash_folder:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(filepath)
        trash_filename = f"{timestamp}_{filename}"
        trash_path = os.path.join(trash_folder, trash_filename)

        counter = 1
        while os.path.exists(trash_path):
            name_without_ext, ext = os.path.splitext(filename)
            trash_filename = f"{timestamp}_{name_without_ext}_{counter}{ext}"
            trash_path = os.path.join(trash_folder, trash_filename)
            counter += 1

        shutil.move(filepath, trash_path)
        print(f"INFO: Moved file to trash: {trash_path}")
        return

    os.remove(filepath)


def get_unique_filepath(destination_folder: str, filename: str) -> str:
    """Generate a non-conflicting file path using native path semantics."""
    base, ext = os.path.splitext(filename)
    counter = 1
    full_path = os.path.join(destination_folder, filename)

    while os.path.exists(full_path):
        new_filename = f"{base}({counter}){ext}"
        full_path = os.path.join(destination_folder, new_filename)
        counter += 1

    return full_path
