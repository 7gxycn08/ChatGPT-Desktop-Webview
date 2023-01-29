from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow
from time import sleep
from sys import argv, exit

try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    sleep(3)
    pyi_splash.close()
except:
       pass

class ChatGPT_Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(1200,500,600,520)
        self.setWindowIcon(QIcon('Resources\\icon.ico'))
        self.setWindowTitle('ChatGPT Desktop Webview v1.0.0.4')
        self.profile = QWebEngineProfile('ChatGPTProfile')
        self.settings = self.profile.settings()
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard,True)
        self.webview = QWebEngineView(self.profile)
        self.setCentralWidget(self.webview)
        self.webview.setGeometry(1200,500,600,520)
        self.webview.setZoomFactor(0.7)
        self.url = QUrl("https://chat.openai.com/chat")
        self.webview.load(self.url)
        self.show()
        self.webview.show()

if __name__ == "__main__":
    app = QApplication(argv)
    run = ChatGPT_Main()
    exit(app.exec())
