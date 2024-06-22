# EPUB Book With Background Music and Text Reader

## Overview

This project consists of two main Python scripts: `createbook.py` and `textreader.py`. The purpose of these scripts is to allow users to convert ePub books to a JSON format with MP3 soundtracks and to read the converted content with soundtracks playing in the background.

### `createbook.py`

This script provides a graphical user interface (GUI) for converting ePub books to a JSON format. Users can add MP3 soundtracks to specified page ranges within the book. The converted book, along with its soundtracks, is saved in a specified directory.

#### Features
- Load ePub files.
- Add MP3 soundtracks to specified page ranges.
- Save the converted book and soundtracks as a JSON file.

#### Requirements
- Python 3.12
- ebooklib
- BeautifulSoup4
- tkinter
- tkinterhtml

#### How to Use
1. **Clone the GitHub repository**:
    ```bash
    git clone https://github.com/powerspyy/ePubMP3Enhancer.git
    cd ePubMP3Enhancer
    ```
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    On macOS, depending on your setup, use:
    ```bash
    pip3 install -r requirements.txt
    ```
3. **Run the script**:
    ```bash
    python createbook.py
    ```

    On macOS, use:
    ```bash
    python3 createbook.py
    ```

4. **Using the GUI**:
    - Click "Load ePub" to select and load an ePub file.
    - Navigate through the book using "Previous Page", "Next Page", "Previous Chapter", and "Next Chapter" buttons.
    - Add soundtracks by specifying a page range and selecting an MP3 file.
    - Save the JSON file with embedded soundtracks using the "Save JSON" button.

### `textreader.py`

This script provides a GUI to read the converted JSON book. It displays the book's content and plays the corresponding soundtracks for specified pages in the background.

#### Features
- Load and display JSON books.
- Play soundtracks for the current page range.

#### Requirements
- Python 3.12
- PyQt5

#### How to Use
1. **Clone the GitHub repository**:
    ```bash
    git clone https://github.com/powerspyy/ePubMP3Enhancer.git
    cd ePubMP3Enhancer
    ```
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    On macOS, depending on your setup, use:
    ```bash
    pip3 install -r requirements.txt
    ```
3. **Run the script**:
    ```bash
    python textreader.py
    ```

    On macOS, use:
    ```bash
    python3 textreader.py
    ```

4. **Using the GUI**:
    - Load the JSON book file.
    - Navigate through the book using the navigation buttons. (left and right arrow keys)
    - Soundtracks will play automatically for pages that have associated MP3 files.

## Additional Information

These scripts are designed to enhance the ePub reading experience by allowing the addition of soundtracks to specific page ranges. The `createbook.py` script handles the conversion and soundtrack embedding, while `textreader.py` provides a seamless reading and listening experience.

Feel free to contribute to the project or modify the scripts to suit your needs.
