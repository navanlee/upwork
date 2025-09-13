import shutil
from pathlib import Path


class FileOrganizer:
    def __init__(self, source_folder, destination_folder=None):
        self.source = Path(source_folder)
        self.destination = Path(destination_folder) if destination_folder else self.source

    def organize(self):
        """
        Step 1: Traverse all files (including subfolders).
        Step 2: Group files by type (pdf, image, excel, etc.)
        Step 3: Copy files into type folders inside destination
                with auto-renaming if duplicates exist.
        Step 4: Print sorted list by modification date
        """
        for file in self.source.rglob("*"):  # recursive: includes subfolders
            if file.is_file():
                # Step 1: Detect file type
                file_type = self.get_file_type(file.suffix.lower())
                type_folder = self.destination / file_type
                type_folder.mkdir(parents=True, exist_ok=True)

                # Step 2: Handle duplicate names
                target_path = self.get_unique_path(type_folder / file.name)

                # Step 3: Copy file
                shutil.copy2(str(file), target_path)  # copy2 preserves metadata
                print(f"Copied: {file} → {target_path}")

        # Step 4: Sort inside each folder by modification date
        for folder in self.destination.iterdir():
            if folder.is_dir():
                files = sorted(folder.iterdir(), key=lambda f: f.stat().st_mtime)
                print(f"\nSorted files in {folder.name}:")
                for f in files:
                    print(f"  {f.name}")

    @staticmethod
    def get_unique_path(path: Path) -> Path:
        """
        If file already exists, append (1), (2), etc.
        Example: file.pdf → file(1).pdf → file(2).pdf
        """
        if not path.exists():
            return path

        counter = 1
        stem, suffix = path.stem, path.suffix
        while True:
            new_path = path.with_name(f"{stem}({counter}){suffix}")
            if not new_path.exists():
                return new_path
            counter += 1

    @staticmethod
    def get_file_type(extension):
        """Categorize file by extension"""
        if extension in [".pdf"]:
            return "PDF"
        elif extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]:
            return "Images"
        elif extension in [".xls", ".xlsx", ".csv", ".ods"]:
            return "Excel"
        elif extension in [".doc", ".docx", ".txt", ".rtf", ".odt"]:
            return "Documents"
        elif extension in [".mp4", ".avi", ".mov", ".mkv"]:
            return "Videos"
        elif extension in [".mp3", ".wav", ".aac"]:
            return "Audio"
        else:
            return "Others"


if __name__ == "__main__":
    source = r"C:\Users\YourName\Downloads"   # Change this path
    destination = r"C:\Users\YourName\Organized"  # Change this path

    organizer = FileOrganizer(source, destination)
    organizer.organize()
