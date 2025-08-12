import os
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtWebEngineCore import (QWebEngineSettings, QWebEngineProfile, QWebEnginePage, QWebEngineNotification)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from sys import argv, exit
from win32api import EnumDisplaySettings
from win32con import ENUM_CURRENT_SETTINGS
import subprocess


def get_refresh_rate():
    # Get the current display settings
    settings = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)

    # Return the refresh rate (in Hz)
    return settings.DisplayFrequency

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
        self.popup_dialog.setWindowTitle("ChatGPT Desktop Webview v1.2")
        self.popup_dialog.setWindowIcon(QIcon('Resources/icon.ico'))
        self.popup_dialog.setCentralWidget(self.new_webview)
        self.popup_dialog.setGeometry(1200, 500, 600, 520)
        self.popup_dialog.show()

        return self.new_webview.page()

class CustomWebView(QWebEngineView):
    def __init__(self):
        super().__init__()

        # Set up fixed frame_rate
        self.fps = get_refresh_rate()  # get refresh rate
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        timer_value = 1000 / self.fps
        self.timer.start(int(timer_value))  # Get and trigger update for consistent latency
        self.is_dragging = False

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Start tracking drag state
        self.is_dragging = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # Stop tracking drag state
        self.is_dragging = False

    def update_frame(self):
        # Only update when not dragging to avoid excessive repaints during window move
        if not self.is_dragging:
            self.update()


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fps = get_refresh_rate()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        timer_value = 1000 / self.fps
        self.timer.start(int(timer_value))  # Trigger every 1/60th of a second
        self.is_dragging = False

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Start tracking drag state
        self.is_dragging = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # Stop tracking drag state
        self.is_dragging = False

    def update_frame(self):
        # Only update when not dragging to avoid excessive repaints during window move
        if not self.is_dragging:
            self.update()


class ChatGptMain(CustomMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(1200, 500, 600, 520)
        self.setWindowIcon(QIcon(r'Resources/icon.ico'))
        self.setWindowTitle('ChatGPT Desktop Webview v1.2')
        self.profile = QWebEngineProfile('ChatGPTProfile')
        self.profile.setPersistentStoragePath(fr"C:/Users/{os.getlogin()}/AppData/Local/ChatGPT")
        self.profile.setNotificationPresenter(self.handle_notification)
        self.settings = self.profile.settings()
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.ReadingFromCanvasEnabled, False)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.SpatialNavigationEnabled, True)
        self.webview = CustomWebView()
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
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setToolTip("ChatGPT Desktop Webview v1.2")
        self.tray_icon.setIcon(QIcon("Resources/icon.ico"))
        self.tray_icon.activated.connect(
            lambda reason: self.show() if reason == QSystemTrayIcon.ActivationReason.Trigger else None)
        if self.tray_icon is not None:
            self.tray_icon.hide()
        self.tray_menu = QMenu(self)
        self.restore_action = QAction("About", self)
        self.restore_action.triggered.connect(self.about_page)
        self.tray_menu.addAction(self.restore_action)

        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(QApplication.instance().quit)
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)

        self.tray_icon.show()
        self.webview.page().featurePermissionRequested.connect(self.on_feature_permission_requested)
        self.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def on_feature_permission_requested(self, security_origin, feature):
        if feature == QWebEnginePage.Feature.Notifications:
            self.webview.page().setFeaturePermission(
                security_origin,
                feature,
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )
        elif feature == QWebEnginePage.Feature.MediaAudioCapture:
            self.webview.page().setFeaturePermission(
                security_origin,
                feature,
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )

    def handle_notification(self, notification: QWebEngineNotification):
        self.tray_icon.showMessage(
            notification.title(),  # Title
            notification.message(),  # Message
            QIcon('Resources/icon.ico'),  # Icon
            5000  # Duration in milliseconds
        )

    def about_page(self):
        url = "https://github.com/7gxycn08/ChatGPT-Desktop-Webview"
        subprocess.Popen(f"start {url}", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    app = QApplication(argv)
    """Uncomment lines below to route traffic through Socks5Proxy of your choice"""
    # from PySide6 import QtNetwork
    # proxy = QtNetwork.QNetworkProxy()
    # proxy.setType(QtNetwork.QNetworkProxy.ProxyType.Socks5Proxy)
    # proxy.setHostName("127.0.0.1")
    # proxy.setPort(1080)
    # QtNetwork.QNetworkProxy.setApplicationProxy(proxy)
    run = ChatGptMain()
    exit(app.exec())
