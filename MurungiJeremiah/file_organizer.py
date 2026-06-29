from pathlib import Path
import shutil


downloads_folder = Path.home() / "Downloads"

destination_maps: dict[str, list[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".sh", ".bat"],
    "Executables": [".exe", ".msi", ".app", ".deb"],
    "Others": []
}

def list_files_in_dir(dir: Path) -> list[Path]:
    return [f for f in dir.iterdir() if f.is_file()]

def move_files_to_destinations(source_dir: Path, maps: dict[str, list[str]]) -> None:
    files = list_files_in_dir(source_dir)
    for file in files:
        for dest_folder, extensions in maps.items():
            if file.suffix.lower() in extensions:
                dest_path = source_dir / dest_folder
                dest_path.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest_path / file.name))
                break
            else:
                # If the file's extension doesn't match any category, move it to "Others"
                if dest_folder == "Others":
                    dest_path = source_dir / dest_folder
                    dest_path.mkdir(exist_ok=True)
                    shutil.move(str(file), str(dest_path / file.name))
                    break

if __name__ == "__main__":
    move_files_to_destinations(downloads_folder, destination_maps)