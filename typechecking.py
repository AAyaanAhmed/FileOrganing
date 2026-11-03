import os
import shutil
import hashlib
import logging
from pathlib import Path
from datetime import datetime


logging.basicConfig(
    filename="file_activity.log",
    level=logging.INFO,
    format="%(asctime)s : %(message)s"
)


FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"],
    "Code": [".py", ".java"]
}


def get_folder(extension):
    for folder, extensions in FILE_TYPES.items():
        if extension in extensions:
            return folder
    return "Others"


def generate_hash(file_path):
    checksum = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            checksum.update(chunk)

    return checksum.hexdigest()


def create_report(data):
    with open("file_report.txt", "w") as report:
        report.write("File Organizer Report\n")
        report.write(f"Created: {datetime.now()}\n\n")

        for name, count in data.items():
            report.write(f"{name}: {count} files\n")


def organize_files(directory):

    path = Path(directory)

    if not path.is_dir():
        print("Invalid folder path")
        return

    processed = set()
    report = {}

    for file in path.iterdir():

        if file.is_dir():
            continue

        try:
            file_id = generate_hash(file)

            if file_id in processed:
                logging.warning(f"Duplicate skipped: {file.name}")
                continue

            processed.add(file_id)

            folder_name = get_folder(file.suffix.lower())

            target = path / folder_name
            target.mkdir(exist_ok=True)

            shutil.move(
                str(file),
                str(target / file.name)
            )

            report[folder_name] = report.get(folder_name, 0) + 1

            logging.info(
                f"{file.name} moved to {folder_name}"
            )

        except Exception as error:
            logging.error(
                f"{file.name}: {error}"
            )

    create_report(report)

    print("\nOrganization Completed")
    print("---------------------")

    for folder, count in report.items():
        print(f"{folder}: {count}")

    print("\nReport created: file_report.txt")
    print("Log created: file_activity.log")


def main():

    folder = input("Enter folder location: ")

    organize_files(folder)


if __name__ == "__main__":
    main()
