import sys
import smp_qrc

from PyQt5.QtCore import (
    QDir,
    Qt,
    QUrl,
    QTime
)
from PyQt5.QtGui import (
    QIcon,
    QKeySequence,
    QPalette,
    QColor,
    QCursor,
    QFontDatabase,
    QFont
)
from PyQt5.QtMultimedia import (
    QMediaContent,
    QMediaPlayer
)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *


class SMPWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SMPWindow, self).__init__(parent)
        self.setWindowTitle("Simple Media Player")
        self.setWindowIcon(QIcon(":smp.ico"))
        self.setAnimated(True)

        self.widescreen = True

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        self.replay_button = QPushButton()
        self.replay_button.setIcon(QIcon(":replay_10_black_48dp.svg"))
        self.replay_button.setEnabled(False)
        self.replay_button.clicked.connect(self.replay_10)
        # self.replay_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.play_pause_button = QPushButton()
        self.play_pause_button.setEnabled(False)
        self.play_pause_button.setIcon(QIcon(":play_arrow_black_48dp.svg"))
        self.play_pause_button.clicked.connect(self.play)
        # self.play_pause_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.forward_button = QPushButton()
        self.forward_button.setEnabled(False)
        self.forward_button.setIcon(QIcon(":forward_30_black_48dp.svg"))
        self.forward_button.clicked.connect(self.forward_30)
        # self.forward_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.start_time = QLabel()
        self.start_time.setAlignment(Qt.AlignBottom)
        self.start_time.setText("0:00")
        self.start_time.setUpdatesEnabled(True)
        self.start_time.setEnabled(False)

        self.progress_bar = QSlider(Qt.Horizontal, self)
        self.progress_bar.setEnabled(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.sliderMoved.connect(self.setPosition)
        self.progress_bar.setSingleStep(2)
        self.progress_bar.setPageStep(20)
        self.progress_bar.setStyleSheet(self.stylesheet())
        # self.progress_bar.setAttribute(Qt.WA_TranslucentBackground, True)

        self.end_time = QLabel()
        self.end_time.setAlignment(Qt.AlignBottom)
        self.end_time.setText("0:00")
        self.end_time.setUpdatesEnabled(True)
        self.end_time.setEnabled(False)

        self.volume_button = QPushButton()
        self.volume_button.setEnabled(False)
        self.volume_button.setIcon(QIcon(":volume_up_black_48dp.svg"))
        self.volume_button.clicked.connect(self.toggleVolume)
        # self.volume_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.full_screen_button = QPushButton()
        self.full_screen_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.full_screen_button.setIcon(QIcon(":fullscreen_black_48dp.svg"))
        self.full_screen_button.clicked.connect(self.fullScreen)
        # self.full_screen_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.key_open_file = QShortcut(QKeySequence("ctrl+o"), self)
        self.key_open_file.activated.connect(self.showOpenFileDialog)

        self.key_replay = QShortcut(QKeySequence("j"), self)
        self.key_replay.activated.connect(self.replay_10)

        self.key_play_pause = QShortcut(QKeySequence("k"), self)
        self.key_play_pause.activated.connect(self.play)

        self.key_forward = QShortcut(QKeySequence("l"), self)
        self.key_forward.activated.connect(self.forward_30)

        self.key_mute_unmute = QShortcut(QKeySequence("m"), self)
        self.key_mute_unmute.activated.connect(self.toggleVolume)

        self.key_vol_inc = QShortcut(QKeySequence("Up"), self)
        self.key_vol_inc.activated.connect(self.volumeUp)

        self.key_vol_dec = QShortcut(QKeySequence("Down"), self)
        self.key_vol_dec.activated.connect(self.volumeDown)

        self.key_full_screen = QShortcut(QKeySequence("f"), self)
        self.key_full_screen.activated.connect(self.fullScreen)

        self.key_exit = QShortcut(QKeySequence("ctrl+x"), self)
        self.key_exit.activated.connect(self.exitCall)

        open_action = QAction(self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.showOpenFileDialog)

        exit_action = QAction(self)
        exit_action.setShortcut("Ctrl+X")
        exit_action.triggered.connect(self.exitCall)

        about_action = QAction(self)
        about_action.triggered.connect(self.showAboutDialog)

        # Create a widget for window contents
        root_widget = QWidget(self)
        root_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(root_widget)

        h_layout_mcon = QHBoxLayout()
        h_layout_mcon.setContentsMargins(8, 0, 8, 8)
        h_layout_mcon.addWidget(self.replay_button)
        h_layout_mcon.addWidget(self.play_pause_button)
        h_layout_mcon.addWidget(self.forward_button)
        h_layout_mcon.addWidget(self.start_time, 0, Qt.AlignBottom)
        h_layout_mcon.addWidget(self.progress_bar, 0, Qt.AlignBottom)
        h_layout_mcon.addWidget(self.end_time, 0, Qt.AlignBottom)
        h_layout_mcon.addWidget(self.volume_button)
        h_layout_mcon.addWidget(self.full_screen_button)
        v_layout_stack = QVBoxLayout()
        v_layout_stack.setContentsMargins(0, 0, 0, 0)
        # v_layout_stack.setSpacing(0)
        # v_layout_stack.setStretchFactor()
        v_layout_stack.addWidget(self.video_widget)
        v_layout_stack.addLayout(h_layout_mcon)

        # Set widget to contain window contents
        root_widget.setLayout(v_layout_stack)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.mediaStateChanged)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.error.connect(self.showErrorDialog)

    def activateHandCursorOnButtons(self):
        self.progress_bar.setCursor(QCursor(Qt.PointingHandCursor))
        self.replay_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.play_pause_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.forward_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.volume_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.full_screen_button.setCursor(QCursor(Qt.PointingHandCursor))

    def showOpenFileDialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Media", QDir.homePath())

        if file != "":
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.progress_bar.setEnabled(True)
            self.replay_button.setEnabled(True)
            self.play_pause_button.setEnabled(True)
            self.forward_button.setEnabled(True)
            self.volume_button.setEnabled(True)
            self.end_time.setEnabled(True)
            self.start_time.setEnabled(True)
            self.activateHandCursorOnButtons()
            self.media_player.play()

    @staticmethod
    def exitCall():
        sys.exit(app.exec_())

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def mediaStateChanged(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_pause_button.setIcon(QIcon(":pause_black_48dp.svg"))
        else:
            self.play_pause_button.setIcon(QIcon(":play_arrow_black_48dp.svg"))

    def positionChanged(self, position):
        self.progress_bar.setValue(position)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.media_player.position())
        self.start_time.setText(mtime.toString())

    def durationChanged(self, duration):
        self.progress_bar.setRange(0, duration)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.media_player.duration())
        self.end_time.setText(mtime.toString())

    def setPosition(self, position):
        self.media_player.setPosition(position)

    def forward_30(self):
        self.media_player.setPosition(self.media_player.position() + 30000)

    def replay_10(self):
        self.media_player.setPosition(self.media_player.position() - 10000)

    def adjustVolumeIcon(self):
        vol = self.media_player.volume()

        if vol >= 70:
            self.volume_button.setIcon(QIcon(":volume_up_black_48dp.svg"))

        elif 0 < vol < 70:
            self.volume_button.setIcon(QIcon(":volume_down_black_48dp.svg"))

        else:
            self.volume_button.setIcon(QIcon(":volume_mute_black_48dp.svg"))

    def volumeUp(self):
        if self.media_player.volume() < 100:
            self.media_player.setMuted(False)
            self.media_player.setVolume(self.media_player.volume() + 10)
            self.adjustVolumeIcon()

    def volumeDown(self):
        if self.media_player.volume() > 0:
            self.media_player.setMuted(False)
            self.media_player.setVolume(self.media_player.volume() - 10)
            self.adjustVolumeIcon()

    def toggleVolume(self):
        if self.media_player.isMuted():
            self.media_player.setMuted(False)
            self.adjustVolumeIcon()
        else:
            self.media_player.setMuted(True)
            self.volume_button.setIcon(QIcon(":volume_mute_black_48dp.svg"))

    def fullScreen(self):
        if self.windowState() == Qt.WindowFullScreen:
            self.start_time.show()
            self.progress_bar.show()
            self.end_time.show()
            self.full_screen_button.show()
            self.volume_button.show()
            self.replay_button.show()
            self.forward_button.show()
            self.play_pause_button.show()
            QApplication.restoreOverrideCursor()
            self.showNormal()
        else:
            self.showFullScreen()
            self.start_time.hide()
            self.progress_bar.hide()
            self.end_time.hide()
            self.full_screen_button.hide()
            self.volume_button.hide()
            self.forward_button.hide()
            self.replay_button.hide()
            self.play_pause_button.hide()
            QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))

    def mouseDoubleClickEvent(self, event):
        self.fullScreen()

    @staticmethod
    def showAboutDialog():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.NoIcon)
        msg_box.setWindowIcon(QIcon(":smp.png"))
        msg_box.setWindowTitle("About")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        msg_box.setText("<h2>Simple Media Player</h2>")
        msg_box.setInformativeText(
            '<p>Devloped by Shubham and Bivas</p>'
            '<p><a href="https://www.github.com/v3rma9579/MediaPlayer">View on GitHub</a></p>')
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    @staticmethod
    def showShortcutsDialog():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.NoIcon)
        msg_box.setWindowIcon(QIcon(":smp.png"))
        msg_box.setWindowTitle("Shortcuts")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(
            '<tr>'
            '<td>Ctrl+O</td>'
            '<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>'
            '<td>Open File</td>'
            '</tr>'
            '<tr>'
            '<td>J</td>'
            '<td>&#9;</td>'
            '<td>Replay</td>'
            '</tr>'
            '<tr>'
            '<td>K</td>'
            '<td></td>'
            '<td>Play Pause</td>'
            '</tr>'
            '<tr>'
            '<td>L</td>'
            '<td></td>'
            '<td>Forward</td>'
            '</tr>'
            '<tr>'
            '<td>&uarr;</td>'
            '<td></td>'
            '<td>Raise Volume</td>'
            '</tr>'
            '<tr>'
            '<td>&darr;</td>'
            '<td></td>'
            '<td>Lower Volume</td>'
            '</tr>'
            '<tr>'
            '<td>M</td>'
            '<td></td>'
            '<td>Mute Unmute</td>'
            '</tr>'
            '<tr>'
            '<td>F</td>'
            '<td></td>'
            '<td>Go Full Screen</td>'
            '</tr>'
            '<tr>'
            '<td>Ctrl+X</td>'
            '<td></td>'
            '<td>Exit</td>'
            '</tr>'
        )
        msg_box.exec()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        action_open_file = context_menu.addAction(QIcon(":file_open_black_48dp.svg"), "Open File\tCtrl+O")
        action_full_screen = context_menu.addAction(QIcon(":fullscreen_black_48dp.svg"), "Full Screen\tF")
        action_view_about = context_menu.addAction(QIcon(":info_black_48dp.svg"), "About")
        action_view_shortcuts = context_menu.addAction(QIcon(":help_outline_black_48dp.svg"), "Shortcuts")
        action_quit = context_menu.addAction(QIcon(":close_black_48dp.svg"), "Exit\tCtrl+X")
        if self.windowState() == Qt.WindowFullScreen:
            context_menu.hide()
            return
        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == action_quit:
            self.close()
        elif action == action_open_file:
            self.showOpenFileDialog()
        elif action == action_full_screen:
            self.fullScreen()
        elif action == action_view_about:
            self.showAboutDialog()
        elif action == action_view_shortcuts:
            self.showShortcutsDialog()

    def showErrorDialog(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowIcon(QIcon(":smp.png"))
        msg_box.setText("Unsupported file format")
        msg_box.setWindowTitle("Playback Error")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Retry)
        user_response = msg_box.exec()
        if user_response == QMessageBox.Ok:
            pass
        else:
            self.showOpenFileDialog()

    @staticmethod
    def stylesheet():
        return """
        QSlider::handle:horizontal{background:#ffffff;width:8px;}
        QSlider::groove:horizontal{border:0px;height:10px;background:#322b3a;}
        QSlider::sub-page:horizontal{background:#c088ff;border:0px;height:10px;}
        QSlider::handle:horizontal:hover{background:#ff0000;}
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(":Roboto-Regular.ttf")
    app.setApplicationName("Simple Media Player")
    app.setStyle("Fusion")
    font = QFont(":Roboto")
    font.setPointSize(10)
    app.setFont(font)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(18, 18, 18))
    palette.setColor(QPalette.WindowText, QColor(232, 232, 232))
    palette.setColor(QPalette.Base, QColor(46, 46, 46))
    palette.setColor(QPalette.Text, QColor(232, 232, 232))
    palette.setColor(QPalette.Button, QColor(33, 34, 34))
    palette.setColor(QPalette.ButtonText, QColor(194, 139, 254))
    palette.setColor(QPalette.Highlight, QColor(50, 43, 58))
    palette.setColor(QPalette.HighlightedText, QColor(188, 134, 249))
    palette.setColor(QPalette.Link, QColor(194, 139, 254))
    app.setPalette(palette)
    smp = SMPWindow()
    smp.resize(1280, 720)
    smp.show()
    sys.exit(app.exec_())
