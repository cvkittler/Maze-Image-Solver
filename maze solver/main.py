import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from screeninfo import get_monitors

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Load image in PySide2"
        self.setWindowTitle(self.title)

        label = QLabel(self)
        pixmap = QPixmap('maze.jpg')

        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

class ResizeableImage(QLabel):

    def __init__(self, imagePath):
        QLabel.__init__(self)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setStyleSheet("background-color:#ffffff;")

        pixelMap = QPixmap(imagePath)
        self.update_pixmap(self._pixmap2bytes(pixelMap))

    def resizeEvent(self, event):

        if event:
            x = event.size().width()
            y = event.size().height()
        else:
            x = self.width()
            y = self.height()

        self.current_pixmap = self._bytes2pixmap(self.bytes_image_edit)
        self.setPixmap(self.current_pixmap.scaled(x, y, Qt.KeepAspectRatio))
        self.resize(x, y)

    def update_pixmap(self, bytes_image):

        self.bytes_image_edit = bytes_image

        self.current_pixmap = self._bytes2pixmap(bytes_image)
        self.setPixmap(self.current_pixmap)

        self.resizeEvent(None)

    @staticmethod
    def _bytes2pixmap(raw_image):

        image = QImage()
        image.loadFromData(raw_image)
        return QPixmap(image)

    @staticmethod
    def _pixmap2bytes(pixmap):

        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, 'PNG')
        return byte_array.data()

    @property
    def image_dims(self):
        return self.width(), self.height()

    def force_resize(self, qsize):
        self.resizeEvent(QResizeEvent(qsize, qsize))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ResizeableImage('maze.jpg')
    sys.exit(app.exec_())