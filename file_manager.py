import os
import shutil
import logging

# Set up logging to a file
logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()

#  Correct path to the folder to organize 
target_directory = r"C:\\Users\\LENOVO\\Desktop\\py_test"

# File categories and their extensions
categories = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac"]
}

# Create folders if they don't exist
for folder in categories:
    os.makedirs(os.path.join(target_directory, folder), exist_ok=True)

os.makedirs(os.path.join(target_directory, "Others"), exist_ok=True)

# Organize files based on their type
def organize_files():
    for item in os.listdir(target_directory):
        item_path = os.path.join(target_directory, item)

        if os.path.isdir(item_path):
            continue

        moved = False
        try:
            for folder, extensions in categories.items():
                if item.lower().endswith(tuple(extensions)):
                    dest = os.path.join(target_directory, folder, item)
                    shutil.move(item_path, dest)
                    logger.info(f"{item} → {folder}")
                    moved = True
                    break

            if not moved:
                shutil.move(item_path, os.path.join(target_directory, "Others", item))
                logger.info(f"{item} → Others")

        except Exception as e:
            logger.error(f"Failed to move {item}: {e}")

if __name__ == "__main__":
    print("Organizing files. Please wait...")
    organize_files()
    print("Files have been organized successfully.")
    print("Check the target directory and 'file_organizer.log' for details.")
