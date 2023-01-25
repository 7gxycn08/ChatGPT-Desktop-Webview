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

#Enable this class to set a different User Agent (Might cause issues with Cloudflare)
# class UserAgentInterceptor(QWebEngineUrlRequestInterceptor):
#     def interceptRequest(self, info: QWebEngineUrlRequestInfo):
#         user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/108.0 Mobile/15E148 Safari/605.1.15"
#         info.setHttpHeader(QByteArray(b"user-agent"), QByteArray.fromRawData(user_agent.encode()))

class ChatGPT_Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(1200,500,600,520)
        self.setWindowIcon(QIcon('Resources\\icon.ico'))
        self.setWindowTitle('ChatGPT Desktop Webview v1.0.0.3')
        self.webview = QWebEngineView()
        self.profile = QWebEngineProfile.defaultProfile()
        self.settings = self.profile.settings()
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard,True) #Fixes the copy button not working issue.
        self.setCentralWidget(self.webview)
        self.webview.setGeometry(1200,500,600,520)
        self.webview.setZoomFactor(1)
        self.url = QUrl("https://chat.openai.com")
        self.webview.load(self.url)
        self.show()
        self.webview.show()

if __name__ == "__main__":
    app = QApplication(argv)
    run = ChatGPT_Main()
    exit(app.exec())
