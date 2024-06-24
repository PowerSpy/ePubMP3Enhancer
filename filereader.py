import sys
import os
import json
import base64
import vlc
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QTimer

class EpubReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.epub_folder = None
        self.book_contents = None
        self.book = {}
        self.current_page = 1
        self.soundtracks = {}
        self.current_soundtrack = None
        self.player = None  # Initialize the player attribute
        self.initUI()

    def initUI(self):
        self.setWindowTitle('EPUB Reader')
        self.setGeometry(100, 100, 816, 1056)  # Set initial window size

        # Central widget setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Create a layout to center the QWebEngineView
        center_layout = QHBoxLayout()
        layout.addLayout(center_layout)

        # WebEngineView for HTML content with fixed size
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(816, 1056)
        center_layout.addWidget(self.web_view, 0, Qt.AlignCenter)

        # Display an empty page initially
        self.web_view.setHtml("<html><body><h1>Select a converted ePub to display!</body></html>")

        # Set a timer to prompt the user for the EPUB folder after the main window is shown
        QTimer.singleShot(100, self.prompt_for_epub_folder)

    def prompt_for_epub_folder(self):
        self.epub_folder = QFileDialog.getExistingDirectory(None, "Select EPUB Folder")
        if not self.epub_folder:
            QMessageBox.critical(self, "Error", "No folder selected. The application will now exit.")
            sys.exit(-1)  # Exit if no folder selected

        # Load and display EPUB content
        self.load_epub_content()

    def load_epub_content(self):
        try:
            self.book_file = os.path.join(self.epub_folder, "book.json")
            with open(self.book_file, "r") as file:
                self.book_contents = json.load(file)
            
            # Extract soundtracks from book contents
            self.extract_soundtracks()

            page_num = 0
            for chapter in self.book_contents["chapters"]:
                for key, value in chapter["text"].items():
                    page_num += 1
                    self.book[page_num] = value

            self.display_current_page()
        except Exception as e:
            self.show_error_message(f"Error loading EPUB file: {str(e)}")

    def extract_soundtracks(self):
        if "soundtracks" in self.book_contents:
            self.soundtracks = self.book_contents["soundtracks"]

    def display_current_page(self):
        if self.book:
            if 1 <= self.current_page <= len(self.book):
                current_page_content = self.book[self.current_page]
                self.display_html_content(current_page_content)
                self.play_or_stop_soundtrack()
                self.update_window_title()  # Update window title with current page number
            else:
                self.show_error_message("No more content available.")
        else:
            self.show_error_message("EPUB file not loaded.")

    def display_html_content(self, html_content):
        # Generate full HTML content with text and images
        html_page = "<html><head><style>img { max-width: 100%; height: auto; }</style></head><body>"
        
        # Check if the content is a dictionary (indicating it has text and images)
        if isinstance(html_content, str):
            processed_html = self.process_html_with_images(html_content)
            html_page += processed_html
        else:
            # If the content is not as expected, show an error message
            self.show_error_message("Invalid content format. Unable to display.")

        html_page += "</body></html>"
        
        # Display HTML content in QWebEngineView
        self.web_view.setHtml(html_page)


    def process_html_with_images(self, html_content):
        img_pattern = r'<img\s+[^>]*src="([^"]+)"[^>]*>'  # Regex to extract image src
        processed_html = html_content

        # Track processed images to avoid duplicates
        processed_images = set()

        for match in re.finditer(img_pattern, html_content):
            img_tag = match.group(0)  # Get the entire img tag
            img_src = match.group(1)  # Get the src attribute value
            img_path = os.path.abspath(os.path.join(self.epub_folder, img_src.replace("../", "")))
            print("Checking Existing:", img_path)
            if os.path.exists(img_path):
                print("Exists:",img_path)
                if img_src not in processed_images:
                    with open(img_path, "rb") as img_file:
                        print(1)
                        img_data = base64.b64encode(img_file.read()).decode("utf-8")
                        print("Open Success:", img_path, "\n")
                    embedded_img_tag = f'<img src="data:image/jpeg;base64,{img_data}">'
                    processed_html = processed_html.replace(img_tag, embedded_img_tag, 1)  # Replace only once
                    processed_images.add(img_src)  # Add to processed images set
            else:
                print(f"Image not found: {img_path}")  # Print error if image not found

        return processed_html


    def play_or_stop_soundtrack(self):
        if self.soundtracks:
            for soundtrack_key, mp3_file in self.soundtracks.items():
                page_range = soundtrack_key.split('-')
                if len(page_range) == 2:
                    start_page, end_page = map(int, page_range)

                    if start_page <= self.current_page <= end_page:
                        if self.current_soundtrack != soundtrack_key:
                            self.stop_soundtrack()  # Stop any currently playing soundtrack
                            self.current_soundtrack = soundtrack_key
                            self.play_soundtrack(mp3_file)
                        return

            # No matching page range found, stop the soundtrack
            if self.current_soundtrack is not None:
                self.stop_soundtrack()
                self.current_soundtrack = None

    def play_soundtrack(self, soundtrack_path):
        if not self.player:
            self.player = vlc.MediaPlayer(soundtrack_path)
            self.player.play()
            self.player.audio_set_volume(100)  # Set volume to maximum when starting playback

    def stop_soundtrack(self):
        if self.player:
            self.player.stop()
            self.player.audio_set_volume(100)  # Reset volume to maximum
            self.player = None

    def update_window_title(self):
        self.setWindowTitle(f'EPUB Reader (Page: {self.current_page})')

    def next_page(self):
        if self.book:
            if self.current_page < len(self.book):
                self.current_page += 1
                self.display_current_page()

    def previous_page(self):
        if self.book:
            if self.current_page > 1:
                self.current_page -= 1
                self.display_current_page()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.next_page()
        elif event.key() == Qt.Key_Left:
            self.previous_page()

    def show_error_message(self, message):
        # Display error message in QWebEngineView
        error_html = f"<html><body><h1>{message}</h1></body></html>"
        self.web_view.setHtml(error_html)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = EpubReaderApp()
    reader.show()
    sys.exit(app.exec_())