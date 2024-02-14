from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout
from sys import argv, exit


class CustomWebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        self.new_webview = QWebEngineView()
        self.popup_dialog = QDialog()
        self.popup_dialog.setWindowTitle("ChatGPT Desktop Webview v1.0.0.5")
        self.popup_dialog.setWindowIcon(QIcon('Resources\\icon.ico'))
        self.popup_dialog.setLayout(QVBoxLayout())
        self.popup_dialog.layout().addWidget(self.new_webview)
        self.popup_dialog.setGeometry(1200, 500, 600, 520)
        self.popup_dialog.show()
        return self.new_webview.page()


class ChatGptMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(1200, 500, 600, 520)
        self.setWindowIcon(QIcon('Resources\\icon.ico'))
        self.setWindowTitle('ChatGPT Desktop Webview v1.0.0.5')
        self.profile = QWebEngineProfile('ChatGPTProfile')
        self.settings = self.profile.settings()
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.webview = QWebEngineView(self.profile)
        self.setCentralWidget(self.webview)
        self.webview.setPage(CustomWebEnginePage(self.webview))
        self.webview.setGeometry(1200, 500, 600, 520)
        self.webview.setZoomFactor(0.7)
        self.url = QUrl("https://chat.openai.com")
        self.webview.load(self.url)
        self.show()


if __name__ == "__main__":
    app = QApplication(argv)
    run = ChatGptMain()
    exit(app.exec())
