import os
import zipfile
import shutil

def extract_images_from_epub(epub_file_path, output_folder):
    """
    Extracts images from an EPUB file located in any path containing 'images/' and saves them to the specified output folder.

    Parameters:
    - epub_file_path (str): Path to the EPUB file.
    - output_folder (str): Folder where extracted images will be saved.
    """
    try:
        with zipfile.ZipFile(epub_file_path, 'r') as epub_zip:
            for file_info in epub_zip.infolist():
                if 'images/' in file_info.filename and not file_info.is_dir():
                    # Extract image file
                    filename = os.path.basename(file_info.filename)
                    output_path = os.path.join(output_folder, filename)
                    with epub_zip.open(file_info) as source, open(output_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
                    print(f"Extracted: {filename} to {output_path}")
        print("Extraction completed successfully!")
    except Exception as e:
        print(f"Error extracting images from EPUB: {str(e)}")

if __name__ == "__main__":
    epub_file_path = '/Users/power_spy/Downloads/Spy School Goes South (Stuart Gibbs) (Z-Library).epub'  # Replace with your EPUB file path
    output_folder = '/Users/power_spy/Downloads/Spy School Goes South_conversion/images'  # Replace with the folder where you want to save the images

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extract_images_from_epub(epub_file_path, output_folder)
