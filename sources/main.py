import sys
import smp_qrc
from PyQt5.QtCore import QDir, Qt, QUrl, QTime
from PyQt5.QtGui import QIcon, QKeySequence, QPalette, QColor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction


class SMPWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SMPWindow, self).__init__(parent)
        self.setWindowTitle("SMP")
        self.setWindowIcon(QIcon(":smp.ico"))
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.current_volume_level = 100
        videoWidget = QVideoWidget()

        self.widescreen = True

        # self.about_SMP = f'Simple Media Player\nDeveloped by Shubham Verma & Bivas Kumar\
        self.shortcuts = "Open File\tCtrl+O" \
                         "\nPlay/Pause\tSpacebar" \
                         "\nRewind\t" \
                         "\nForward\t" \
                         "\nVolume Up\t" \
                         "\nVolume Down\t" \
                         "\nMute/Unmute\tM" \
                         "\nFull Screen\tF" \
                         "\nExit\tCtrl+X"

        # Button for rewind
        self.replayButton = QPushButton()
        self.replayButton.setIcon(QIcon(":replay_10_black_48dp.svg"))
        # self.replayButton.setEnabled(False)
        self.replayButton.clicked.connect(self.backSlider10)
        # self.replayButton.

        # Button for fastforward
        self.forwardButton = QPushButton()
        # self.forwardButton.setEnabled(False)
        self.forwardButton.setIcon(QIcon(":forward_30_black_48dp.svg"))
        self.forwardButton.clicked.connect(self.forwardSlider10)

        # Button for pause/play
        self.playButton = QPushButton()
        # self.playButton.setEnabled(False)
        self.playButton.setIcon(QIcon(""))
        self.playButton.clicked.connect(self.play)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Time
        self.lbl = QLineEdit("--:--")
        self.lbl.setReadOnly(True)
        self.lbl.setFixedWidth(70)
        self.lbl.setUpdatesEnabled(True)
        # self.lbl.setStyleSheet(stylesheet(self))
        self.lbl.setEnabled(False)
        # self.lbl.selectionChanged.connect(lambda: self.lbl.setSelection(0, 0))

        self.elbl = QLineEdit("--:--")
        self.elbl.setReadOnly(True)
        self.elbl.setFixedWidth(70)
        self.elbl.setUpdatesEnabled(True)
        # self.elbl.setStyleSheet(stylesheet(self))
        self.elbl.setEnabled(False)
        # self.elbl.selectionChanged.connect(lambda: self.elbl.setSelection(0, 0))

        self.progress_bar = QSlider(Qt.Horizontal, self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.sliderMoved.connect(self.setPosition)
        self.progress_bar.setSingleStep(2)
        self.progress_bar.setPageStep(20)
        self.progress_bar.setStyleSheet(stylesheet(self))
        self.progress_bar.setAttribute(Qt.WA_TranslucentBackground, True)

        # Button for mute/unmute
        self.volumeButton = QPushButton()
        # self.volumeButton.setEnabled(False)
        self.volumeButton.setIcon(QIcon(":volume_up_black_48dp.svg"))
        self.volumeButton.clicked.connect(self.muteVolume)

        # Button for full screen
        self.fullScreenButton = QPushButton()
        self.fullScreenButton.setIcon(QIcon(":fullscreen_black_48dp.svg"))
        self.fullScreenButton.clicked.connect(self.fullScreen)
        self.fullScreenButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Shortcut for media player
        self.shortcut1 = QShortcut(QKeySequence("Space"), self)
        self.shortcut1.activated.connect(self.play)

        self.shortcut2 = QShortcut(QKeySequence("M"), self)
        self.shortcut2.activated.connect(self.muteVolume)

        self.shortcut3 = QShortcut(QKeySequence("Up"), self)
        self.shortcut3.activated.connect(self.volumeUp)

        self.shortcut4 = QShortcut(QKeySequence("Down"), self)
        self.shortcut4.activated.connect(self.volumeDown)

        self.shortcut5 = QShortcut(QKeySequence("Right"), self)
        self.shortcut5.activated.connect(self.forwardSlider10)

        self.shortcut6 = QShortcut(QKeySequence("Left"), self)
        self.shortcut6.activated.connect(self.backSlider10)

        self.shortcut7 = QShortcut(QKeySequence("f"), self)
        self.shortcut7.activated.connect(self.fullScreen)

        self.shortcut8 = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut8.activated.connect(self.openFile)

        self.shortcut9 = QShortcut(QKeySequence("Ctrl+X"), self)
        self.shortcut9.activated.connect(self.exitCall)

        # Create new action
        openAction = QAction("&Open File", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+X")
        exitAction.triggered.connect(self.exitCall)

        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(self.handleInfo)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(512, 0, 512, 0)

        controlLayout.addWidget(self.replayButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.forwardButton)
        controlLayout.addWidget(self.volumeButton)
        controlLayout.addWidget(self.fullScreenButton)

        layout_stack_progress_bar = QHBoxLayout()
        layout_stack_progress_bar.setContentsMargins(5, 5, 10, 10)
        layout_stack_progress_bar.addWidget(self.lbl)
        layout_stack_progress_bar.addWidget(self.progress_bar)
        layout_stack_progress_bar.addWidget(self.elbl)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(layout_stack_progress_bar)
        layout.addLayout(controlLayout)
        # layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Media", QDir.homePath())

        if fileName != "":
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.replayButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.volumeButton.setEnabled(True)
            self.mediaPlayer.play()
            self.elbl.setEnabled(True)
            self.lbl.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(QIcon(":pause_black_48dp.svg"))
        else:
            self.playButton.setIcon(QIcon(":play_arrow_black_48dp.svg"))

    def positionChanged(self, position):
        self.progress_bar.setValue(position)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.position())
        self.lbl.setText(mtime.toString())

    def durationChanged(self, duration):
        self.progress_bar.setRange(0, duration)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def forwardSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000)

    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000)

    def volumeAdjust(self):
        vol = self.mediaPlayer.volume()

        if vol >= 75:
            self.volumeButton.setIcon(QIcon(":volume_up_black_48dp.svg"))

        elif 0 < vol < 75:
            self.volumeButton.setIcon(QIcon(":volume_down_black_48dp.svg"))

        else:
            self.volumeButton.setIcon(QIcon(":volume_mute_black_48dp.svg"))

    def volumeUp(self):
        if self.mediaPlayer.volume() != 100:
            self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
            self.current_volume_level = self.mediaPlayer.volume()
            self.volumeAdjust()

    def volumeDown(self):
        if self.mediaPlayer.volume() != 0:
            self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
            self.current_volume_level = self.mediaPlayer.volume()
            self.volumeAdjust()

    def getCurrentVolume(self):
        return self.mediaPlayer.volume()

    def muteVolume(self):
        if self.mediaPlayer.volume() > 0:
            self.current_volume_level = self.mediaPlayer.volume()
            self.mediaPlayer.setVolume(0)
            self.volumeButton.setIcon(QIcon(":volume_mute_black_48dp.svg"))
        else:
            self.mediaPlayer.setVolume(self.current_volume_level)
            self.volumeAdjust()

    def fullScreen(self):
        if self.windowState() == Qt.WindowFullScreen:
            self.fullScreenButton.setVisible(True)
            self.volumeButton.setVisible(True)
            self.backButton.setVisible(True)
            self.forwardButton.setVisible(True)
            self.playButton.setVisible(True)
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.showNormal()
        else:
            self.showFullScreen()
            self.fullScreenButton.setVisible(False)
            self.volumeButton.setVisible(False)
            self.forwardButton.setVisible(False)
            self.backButton.setVisible(False)
            self.playButton.setVisible(False)
            QApplication.setOverrideCursor(Qt.ArrowCursor)

    def mouseDoubleClickEvent(self, event):
        self.fullScreen()

    def handleInfo(self):
        about_SMP = QTextBrowser()
        about_SMP.setOpenExternalLinks(True)
        about_SMP.append('<a href=https://github.com/AMD825301/MediaPlayer>View on GitHub</a>')

        QMessageBox.about(about_SMP, "About", "")

    def showShortcuts(self):
        QMessageBox.about(self, "Shortcuts", self.shortcuts)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        action_open_file = context_menu.addAction("Open File\tCtrl+O")
        action_full_screen = context_menu.addAction("Full Screen\tF")
        action_view_about = context_menu.addAction("About")
        action_view_shortcuts = context_menu.addAction("Shortcuts")
        action_quit = context_menu.addAction("Exit\tCtrl+X")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == action_quit:
            self.close()
        elif action == action_open_file:
            self.openFile()
        elif action == action_full_screen:
            self.fullScreen()
        elif action == action_view_about:
            self.handleInfo()
        elif action == action_view_shortcuts:
            self.showShortcuts()

    def handleError(self):
        mbox = QMessageBox()
        mbox.setIcon()
        mbox.about(None, "Playback Error", "gandu")


def stylesheet(self):
    return """
QSlider::handle:horizontal {
  background: #ff0000;
  width: 8px;
}

QSlider::groove:horizontal {
  border: 0px;
  height: 8px;
  background: #585858;
}

QSlider::sub-page:horizontal {
  background: #ff0000;
  border: 0px;
  height: 8px;
}

QSlider::handle:horizontal:hover {
  background: #ffffff;
  height: 8px;
  width: 12px;
  border: 0px;
}

QSlider::sub-page:horizontal:disabled {
  background: #bbbbbb;
  border-color: #999999;
}

QSlider::add-page:horizontal:disabled {
  background: #2a82da;
  border-color: #999999;
}

QSlider::handle:horizontal:disabled {
  background: #2a82da;
}
QLineEdit {
  color: #585858;
  border: 0px;
  font-size: 8pt;
}

QMenu {
  border: 0px;
  margin: 0px;
}

QMenu::item {
  padding: 2px 25px 2px 20px;
}

QMenu::item:selected {
  background-color: #ff0000;
}
"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("SMP")
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(18, 18, 18, 255))
    palette.setColor(QPalette.WindowText, QColor(240, 244, 248))
    palette.setColor(QPalette.Base, QColor(36, 59, 83))
    palette.setColor(QPalette.Text, QColor(240, 244, 248))
    palette.setColor(QPalette.Button, QColor(185, 136, 250))
    palette.setColor(QPalette.ButtonText, QColor(59, 27, 97))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(255, 64, 129))
    palette.setColor(QPalette.HighlightedText, QColor(33, 33, 33))
    app.setPalette(palette)
    smp = SMPWindow()
    smp.setMinimumSize(640, 480)
    smp.show()
    sys.exit(app.exec_())
