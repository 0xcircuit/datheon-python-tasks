"""Organize files by extension. Dry-run is enabled by default for safety."""
from pathlib import Path
import shutil

# Change this to the folder you want to organize.
TARGET_DIR = Path.home() / "Downloads"
DRY_RUN = True
SKIP_DIRS = {".git", "__pycache__"}


def category_for(path):
    suffix = path.suffix.lower().lstrip(".")
    if not suffix:
        return "No_Extension"
    categories = {
        "Images": {"png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"},
        "Documents": {"pdf", "doc", "docx", "txt", "rtf", "odt"},
        "Spreadsheets": {"csv", "xls", "xlsx", "ods"},
        "Audio": {"mp3", "wav", "aac", "flac", "ogg"},
        "Video": {"mp4", "mkv", "mov", "avi", "webm"},
        "Archives": {"zip", "rar", "7z", "tar", "gz"},
        "Code": {"py", "js", "ts", "cpp", "c", "h", "java", "html", "css", "json"},
    }
    for category, extensions in categories.items():
        if suffix in extensions:
            return category
    return "Other"


def unique_destination(destination):
    """Avoid overwriting a file with the same name."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize(target_dir=TARGET_DIR, dry_run=DRY_RUN):
    target = Path(target_dir).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {target}")

    moves = []
    for item in target.iterdir():
        if not item.is_file() or item.name.startswith("."):
            continue
        category = category_for(item)
        destination_dir = target / category
        destination = unique_destination(destination_dir / item.name)
        moves.append((item, destination))

    if not moves:
        print(f"No files to organize in {target}")
        return []

    print(f"Folder: {target}")
    print("Mode:", "DRY RUN (no changes)" if dry_run else "LIVE")
    for source, destination in moves:
        print(f"{source.name} -> {destination.parent.name}/{destination.name}")
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
    if dry_run:
        print("\nReview this preview. To apply changes, set DRY_RUN = False in the script.")
    else:
        print(f"\nOrganized {len(moves)} file(s).")
    return moves


if __name__ == "__main__":
    try:
        organize()
    except (OSError, PermissionError) as exc:
        print(f"Could not organize folder: {exc}")
