import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
import os
import json
import base64  # For encoding images

class EpubReaderApp(QMainWindow):
    def __init__(self, epub_file):
        super().__init__()
        self.epub_file = epub_file
        self.book = {}
        self.current_page = 1
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

        # Load and display EPUB content
        self.load_epub_content()

    def load_epub_content(self):
        try:
            self.book_file = os.path.join(self.epub_file, "book.json")
            with open(self.book_file, "r") as file:
                self.book_contents = json.load(file)
            page_num = 0
            for chapter in self.book_contents["chapters"]:
                for key, value in chapter["text"].items():
                    page_num += 1
                    self.book[page_num] = value
            self.display_current_page()
        except Exception as e:
            self.show_error_message(f"Error loading EPUB file: {str(e)}")

    def display_current_page(self):
        if self.book:
            if 1 <= self.current_page <= len(self.book):
                current_page_content = self.book[self.current_page]
                self.display_html_content(current_page_content)
            else:
                self.show_error_message("No more content available.")
        else:
            self.show_error_message("EPUB file not loaded.")

    def display_html_content(self, html_content):
        # Generate full HTML content with text and images
        html_page = "<html><head><style>img { max-width: 100%; height: auto; }</style></head><body>"
        
        # Check if the content is a dictionary (indicating it has text and images)
        if isinstance(html_content, dict):
            for key, value in html_content.items():
                if key == "text":
                    html_page += value
                elif key == "images":
                    for img_path in value:
                        # Encode image data to base64
                        with open(os.path.join(self.epub_file, img_path), "rb") as img_file:
                            img_data = base64.b64encode(img_file.read()).decode("utf-8")
                        # Embed image in HTML
                        html_page += f'<img src="data:image/jpeg;base64,{img_data}" /><br>'
        else:
            # If the content is not a dictionary, assume it's plain HTML text
            html_page += html_content
        
        html_page += "</body></html>"
        
        # Display HTML content in QWebEngineView
        self.web_view.setHtml(html_page)

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
    epub_file = '/Users/power_spy/Downloads/Spy School Goes South_conversion'
    app = QApplication(sys.argv)
    reader = EpubReaderApp(epub_file)
    reader.show()
    sys.exit(app.exec_())
