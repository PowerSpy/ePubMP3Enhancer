import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from ebooklib import epub
import tempfile
import os

class EpubReaderApp(QMainWindow):
    def __init__(self, epub_file):
        super().__init__()
        self.epub_file = epub_file
        self.book = None
        self.items = []
        self.current_item_index = 0
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
            self.book = epub.read_epub(self.epub_file)
            self.items = list(self.book.get_items())
            self.display_current_item()
        except Exception as e:
            self.show_error_message(f"Error loading EPUB file: {str(e)}")

    def display_current_item(self):
        if self.items:
            if 0 <= self.current_item_index < len(self.items):
                current_item = self.items[self.current_item_index]
                if self.is_image_item(current_item):
                    self.display_image_content(current_item)
                else:
                    self.display_html_content(current_item.content.decode('utf-8'))
            else:
                self.show_error_message("No more content available.")
        else:
            self.show_error_message("EPUB file not loaded.")

    def is_image_item(self, item):
        # Check if the item is an image based on its media type
        return item.media_type.startswith('image/')

    def display_image_content(self, item):
        # Display image content in QWebEngineView
        image_data = self.book.read_item(item)
        image_filename = item.file_name.split('/')[-1]
        image_path = os.path.join(tempfile.gettempdir(), image_filename)
        with open(image_path, 'wb') as f:
            f.write(image_data)

        # Display image using HTML in QWebEngineView
        html_content = f'<html><body><img src="file://{image_path}"></body></html>'
        self.web_view.setHtml(html_content)

    def display_html_content(self, html_content):
        # Display HTML content in QWebEngineView
        self.web_view.setHtml(html_content)

    def next_page(self):
        if self.items:
            self.current_item_index += 1
            self.display_current_item()

    def previous_page(self):
        if self.items:
            self.current_item_index -= 1
            self.display_current_item()

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
    epub_file = '/Users/power_spy/Downloads/Spy School Goes South (Stuart Gibbs) (Z-Library).epub'
    app = QApplication(sys.argv)
    reader = EpubReaderApp(epub_file)
    reader.show()
    sys.exit(app.exec_())
