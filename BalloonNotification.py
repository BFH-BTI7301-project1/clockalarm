import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import Qt


if __name__ == '__main__':
    app = QApplication(sys.argv)

    icon = Qt.QIcon('ico/bfh_logo.png')

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowIcon(icon)
    w.setWindowTitle('Simple')
    w.show()

    systemtray_icon = Qt.QSystemTrayIcon(app)
    systemtray_icon.setIcon(icon)
    systemtray_icon.show()
    systemtray_icon.showMessage('New notification', 'Display a message')

    sys.exit(app.exec_())
