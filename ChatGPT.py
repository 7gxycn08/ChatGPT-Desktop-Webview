import os
from PySide6.QtGui import QIcon
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import (QWebEngineSettings, QWebEngineProfile, QWebEnginePage)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow
from sys import argv, exit


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.popup_dialog = QMainWindow()
        self.new_webview = QWebEngineView()

    def createWindow(self, _type):
        self.new_webview.setPage(QWebEnginePage(self.profile(), self.new_webview))
        self.new_webview.page().action(self.new_webview.page().WebAction.SavePage).setVisible(False)
        self.new_webview.page().action(self.new_webview.page().WebAction.ViewSource).setVisible(False)
        self.new_webview.page().action(self.new_webview.page().WebAction.Cut).setVisible(True)
        self.new_webview.page().action(self.new_webview.page().WebAction.Copy).setVisible(True)
        self.new_webview.page().action(self.new_webview.page().WebAction.Paste).setVisible(True)
        self.new_webview.setZoomFactor(0.7)
        self.popup_dialog.setWindowTitle("ChatGPT Desktop Webview v1.0.0.7")
        self.popup_dialog.setWindowIcon(QIcon('Resources/icon.ico'))
        self.popup_dialog.setCentralWidget(self.new_webview)
        self.popup_dialog.setGeometry(1200, 500, 600, 520)
        self.popup_dialog.show()

        return self.new_webview.page()


class ChatGptMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(1200, 500, 600, 520)
        self.setWindowIcon(QIcon(r'Resources/icon.ico'))
        self.setWindowTitle('ChatGPT Desktop Webview v1.0.0.8')
        self.profile = QWebEngineProfile('ChatGPTProfile')
        self.profile.setPersistentStoragePath(fr"C:/Users/{os.getlogin()}/AppData/Local/ChatGPT")
        self.settings = self.profile.settings()
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.ReadingFromCanvasEnabled, False)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.SpatialNavigationEnabled, True)
        self.webview = QWebEngineView(self)
        self.setCentralWidget(self.webview)
        self.webview.setPage(CustomWebEnginePage(self.profile, self.webview))
        self.webview.setGeometry(1200, 500, 600, 520)
        self.webview.setZoomFactor(0.7)
        self.url = QUrl("https://chat.openai.com")
        self.webview.load(self.url)
        self.webview.page().action(self.webview.page().WebAction.SavePage).setVisible(False)
        self.webview.page().action(self.webview.page().WebAction.ViewSource).setVisible(False)
        self.webview.page().action(self.webview.page().WebAction.Cut).setVisible(True)
        self.webview.page().action(self.webview.page().WebAction.Copy).setVisible(True)
        self.webview.page().action(self.webview.page().WebAction.Paste).setVisible(True)
        self.show()


if __name__ == "__main__":
    app = QApplication(argv)
    run = ChatGptMain()
    exit(app.exec())