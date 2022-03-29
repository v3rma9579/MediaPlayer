from PyQt5.QtCore import QDir, Qt, QUrl, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QKeySequence
import sys


class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Py Player")
        self.setWindowIcon(QIcon('xyz.png'))
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        # Button for backward slider
        self.backButton = QPushButton()
        self.backButton.setEnabled(False)
        self.backButton.setIcon(QIcon('rewind.png'))
        self.backButton.clicked.connect(self.backSlider10)

        # Button for forward slider
        self.forwardButton = QPushButton()
        self.forwardButton.setEnabled(False)
        self.forwardButton.setIcon(QIcon('forward.png'))
        self.forwardButton.clicked.connect(self.forwardSlider10)

        # Button for pause/play
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        # Time
        self.lbl = QLineEdit('00:00:00')
        self.lbl.setReadOnly(True)
        self.lbl.setFixedWidth(70)
        self.lbl.setUpdatesEnabled(True)
        self.lbl.selectionChanged.connect(lambda: self.lbl.setSelection(0, 0))

        self.elbl = QLineEdit('00:00:00')
        self.elbl.setReadOnly(True)
        self.elbl.setFixedWidth(70)
        self.elbl.setUpdatesEnabled(True)
        self.elbl.selectionChanged.connect(lambda: self.elbl.setSelection(0, 0))

        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setRange(0, 100)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setSingleStep(2)
        self.positionSlider.setPageStep(20)

        # Button for mute/ unmute
        self.volumeButton = QPushButton()
        self.volumeButton.setEnabled(False)
        self.volumeButton.setIcon(QIcon('volume-max.png'))

        if self.mediaPlayer.volume() != 0:
            self.volumeButton.clicked.connect(self.muteVolume)

        else:
            self.volumeButton.clicked.connect(self.unmuteVolume)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Shortcut for media player
        self.shortcut1 = QShortcut(QKeySequence('Space'), self)
        self.shortcut1.activated.connect(self.play)

        if self.mediaPlayer.volume() != 0:
            self.shortcut2 = QShortcut(QKeySequence('M'), self)
            self.shortcut2.activated.connect(self.muteVolume)

        else:
            self.shortcut2 = QShortcut(QKeySequence('M'), self)
            self.shortcut2.activated.connect(self.unmuteVolume)

        self.shortcut3 = QShortcut(QKeySequence('Up'), self)
        self.shortcut3.activated.connect(self.volumeUp)

        self.shortcut4 = QShortcut(QKeySequence('Down'), self)
        self.shortcut4.activated.connect(self.volumeDown)

        self.shortcut5 = QShortcut(QKeySequence('Right'), self)
        self.shortcut5.activated.connect(self.forwardSlider10)

        self.shortcut6 = QShortcut(QKeySequence('Left'), self)
        self.shortcut6.activated.connect(self.backSlider10)

        self.shortcut7 = QShortcut(QKeySequence('Enter'), self)
        self.shortcut7.activated.connect(self.fullScreen)

        self.shortcut7 = QShortcut(QKeySequence('H'), self)
        self.shortcut7.activated.connect(self.toggleSlider)

        # Create new action
        openAction = QAction(QIcon('folder.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open file')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('close.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.backButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.forwardButton)
        controlLayout.addWidget(self.lbl)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.elbl)
        controlLayout.addWidget(self.volumeButton)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.backButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.volumeButton.setEnabled(True)
            self.mediaPlayer.play()

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.position())
        self.lbl.setText(mtime.toString())

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def forwardSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000)

    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000)

    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)

        value = self.mediaPlayer.volume()

        if value == 0:
            self.volumeButton.setIcon(QIcon('volume-mute.png'))

        elif 0 < value <= 30:
            self.volumeButton.setIcon(QIcon('low-volume.png'))

        elif 30 < value <= 80:
            self.volumeButton.setIcon(QIcon('medium-volume.png'))

        else:
            self.volumeButton.setIcon(QIcon('volume-max.png'))

    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)

        value = self.mediaPlayer.volume()

        if value == 0:
            self.volumeButton.setIcon(QIcon('volume-mute.png'))

        elif 0 < value <= 30:
            self.volumeButton.setIcon(QIcon('low-volume.png'))

        elif 30 < value <= 80:
            self.volumeButton.setIcon(QIcon('medium-volume.png'))

        else:
            self.volumeButton.setIcon(QIcon('volume-max.png'))

    def getCurrentVolume(self):
        return self.mediaPlayer.volume()

    def muteVolume(self):
        self.mediaPlayer.setVolume(0)
        self.volumeButton.setIcon(QIcon('volume-mute.png'))
        return True

    def unmuteVolume(self):
        if self.muteVolume():
            self.mediaPlayer.setVolume(self.getCurrentVolume)
            self.volumeButton.setIcon(QIcon('volume.png'))

    def fullScreen(self):
        if self.windowState() & Qt.WindowFullScreen:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.showNormal()
        else:
            self.showFullScreen()
            QApplication.setOverrideCursor(Qt.BlankCursor)

    def mouseDoubleClickEvent(self, event):
        self.fullScreen()
        # self.toggleSlider()

    def hideSlider(self):
        self.playButton.hide()
        self.lbl.hide()
        self.positionSlider.hide()
        self.elbl.hide()
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        if self.widescreen:
            self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.778))
        else:
            self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.33))

    def showSlider(self):
        self.playButton.show()
        self.lbl.show()
        self.positionSlider.show()
        self.elbl.show()
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        if self.widescreen:
            self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.55))
        else:
            self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.33))

    def toggleSlider(self):
        if self.positionSlider.isVisible():
            self.hideSlider()
        else:
            self.showSlider()

    def menuRequested(self):
        menu = QMenu()
        actionFull = menu.addAction(QIcon.fromTheme("view-fullscreen"), "Fullscreen (f)")

        actionFull.triggered.connect(self.fullScreen)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(1200, 800)
    player.show()
    sys.exit(app.exec_())
