import sys
import smp_qrc
from PyQt5.QtCore import QDir, Qt, QUrl, QTime
from PyQt5.QtGui import QIcon, QKeySequence, QPalette, QColor, QDesktopServices
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction


class SMPWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SMPWindow, self).__init__(parent)
        self.setWindowTitle("Simple Media Player")
        self.setWindowIcon(QIcon(":smp.ico"))
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        self.current_volume_level = 100
        self.widescreen = True

        # Button for rewind
        self.replay_button = QPushButton()
        self.replay_button.setIcon(QIcon(":replay_10_black_48dp.svg"))
        self.replay_button.setEnabled(False)
        self.replay_button.clicked.connect(self.replay_10)
        self.replay_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Button for forward
        self.forward_button = QPushButton()
        self.forward_button.setEnabled(False)
        self.forward_button.setIcon(QIcon(":forward_30_black_48dp.svg"))
        self.forward_button.clicked.connect(self.forward_30)
        self.forward_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Button for play/pause
        self.play_pause_button = QPushButton()
        self.play_pause_button.setEnabled(False)
        self.play_pause_button.setIcon(QIcon(":play_arrow_black_48dp.svg"))
        self.play_pause_button.clicked.connect(self.play)
        self.play_pause_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Time
        self.start_time = QLineEdit("0:00")
        self.start_time.setReadOnly(True)
        self.start_time.setFixedWidth(50)
        self.start_time.setUpdatesEnabled(True)
        self.start_time.setEnabled(False)
        # self.start_time.selectionChanged.connect(lambda: self.start_time.setSelection(0, 0))

        self.end_time = QLineEdit("0:00")
        self.end_time.setReadOnly(True)
        self.end_time.setFixedWidth(50)
        self.end_time.setUpdatesEnabled(True)
        self.end_time.setEnabled(False)
        # self.end_time.selectionChanged.connect(lambda: self.end_time.setSelection(0, 0))

        self.progress_bar = QSlider(Qt.Horizontal, self)
        self.progress_bar.setRange(0, 100)
        # self.progress_bar.sliderMoved.connect(self.setPosition)
        self.progress_bar.setSingleStep(2)
        self.progress_bar.setPageStep(20)
        self.progress_bar.setStyleSheet(self.stylesheet())
        # self.progress_bar.setAttribute(Qt.WA_TranslucentBackground, True)

        # Button for mute/unmute
        self.volume_button = QPushButton()
        self.volume_button.setEnabled(False)
        self.volume_button.setIcon(QIcon(":volume_up_black_48dp.svg"))
        self.volume_button.clicked.connect(self.muteVolume)
        self.volume_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Button for full screen
        self.full_screen_button = QPushButton()
        self.full_screen_button.setIcon(QIcon(":fullscreen_black_48dp.svg"))
        self.full_screen_button.clicked.connect(self.fullScreen)
        self.full_screen_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Shortcut for media player
        self.key_play_pause = QShortcut(QKeySequence("k"), self)
        self.key_play_pause.activated.connect(self.play)

        self.key_mute_unmute = QShortcut(QKeySequence("m"), self)
        self.key_mute_unmute.activated.connect(self.muteVolume)

        self.key_vol_inc = QShortcut(QKeySequence("Up"), self)
        self.key_vol_inc.activated.connect(self.volumeUp)

        self.key_vol_dec = QShortcut(QKeySequence("Down"), self)
        self.key_vol_dec.activated.connect(self.volumeDown)

        self.key_forward = QShortcut(QKeySequence("l"), self)
        self.key_forward.activated.connect(self.forward_30)

        self.key_replay = QShortcut(QKeySequence("j"), self)
        self.key_replay.activated.connect(self.replay_10)

        self.key_full_screen = QShortcut(QKeySequence("f"), self)
        self.key_full_screen.activated.connect(self.fullScreen)

        self.key_open_file = QShortcut(QKeySequence("ctrl+o"), self)
        self.key_open_file.activated.connect(self.showOpenFileDialog)

        self.key_exit = QShortcut(QKeySequence("ctrl+x"), self)
        self.key_exit.activated.connect(self.exitCall)

        # Create new action
        open_action = QAction("&Open File", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.showOpenFileDialog)

        # Create exit action
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+X")
        exit_action.triggered.connect(self.exitCall)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAboutDialog)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        h_layout_media_controls = QHBoxLayout()
        # h_layout_media_controls.setContentsMargins(0, 0, 0, 0)

        h_layout_media_controls.addWidget(self.replay_button, 0, Qt.AlignLeft)
        h_layout_media_controls.addWidget(self.play_pause_button, 0, Qt.AlignLeft)
        h_layout_media_controls.addWidget(self.forward_button, 0, Qt.AlignLeft)
        h_layout_media_controls.addWidget(self.volume_button, 0, Qt.AlignRight)
        h_layout_media_controls.addWidget(self.full_screen_button, 0, Qt.AlignRight)

        h_layout_progress_bar = QHBoxLayout()
        # h_layout_progress_bar.setContentsMargins(0, 0, 0, 0)
        h_layout_progress_bar.addWidget(self.progress_bar, 0, Qt.AlignLeft)
        h_layout_progress_bar.addWidget(self.start_time, 0, Qt.AlignLeft)
        h_layout_progress_bar.addWidget(self.end_time, 0, Qt.AlignRight)

        v_layout_stack = QVBoxLayout()
        v_layout_stack.addWidget(self.video_widget)
        v_layout_stack.addLayout(h_layout_progress_bar)
        v_layout_stack.addLayout(h_layout_media_controls)

        # Set widget to contain window contents
        wid.setLayout(v_layout_stack)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.mediaStateChanged)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.error.connect(self.showErrorDialog)

    def showOpenFileDialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Media", QDir.homePath())

        if file != "":
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.replay_button.setEnabled(True)
            self.play_pause_button.setEnabled(True)
            self.forward_button.setEnabled(True)
            self.volume_button.setEnabled(True)
            self.end_time.setEnabled(True)
            self.start_time.setEnabled(True)
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

    def adjustVolume(self):
        vol = self.media_player.volume()

        if vol >= 70:
            self.volume_button.setIcon(QIcon(":volume_up_black_48dp.svg"))

        elif 0 < vol < 70:
            self.volume_button.setIcon(QIcon(":volume_down_black_48dp.svg"))

        else:
            self.volume_button.setIcon(QIcon(":volume_mute_black_48dp.svg"))

    def volumeUp(self):
        if self.media_player.volume() != 100:
            self.media_player.setVolume(self.media_player.volume() + 10)
            self.current_volume_level = self.media_player.volume()
            self.adjustVolume()

    def volumeDown(self):
        if self.media_player.volume() != 0:
            self.media_player.setVolume(self.media_player.volume() - 10)
            self.current_volume_level = self.media_player.volume()
            self.adjustVolume()

    def getCurrentVolume(self):
        return self.media_player.volume()

    def muteVolume(self):
        if self.media_player.volume() > 0:
            self.current_volume_level = self.media_player.volume()
            self.media_player.setVolume(0)
            self.volume_button.setIcon(QIcon(":volume_mute_black_48dp.svg"))
        else:
            self.media_player.setVolume(self.current_volume_level)
            self.adjustVolume()

    def fullScreen(self):
        if self.windowState() == Qt.WindowFullScreen:
            self.full_screen_button.setVisible(True)
            self.volume_button.setVisible(True)
            self.replay_button.setVisible(True)
            self.forward_button.setVisible(True)
            self.play_pause_button.setVisible(True)
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.showNormal()
        else:
            self.showFullScreen()
            self.full_screen_button.setVisible(False)
            self.volume_button.setVisible(False)
            self.forward_button.setVisible(False)
            self.replay_button.setVisible(False)
            self.play_pause_button.setVisible(False)
            QApplication.setOverrideCursor(Qt.ArrowCursor)

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
            '<p><a href="https://www.github.com/AMD825301/MediaPlayer">View on GitHub</a></p>')
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
        action_open_file = context_menu.addAction("Open File\tCtrl+O")
        action_full_screen = context_menu.addAction("Full Screen\tF")
        action_view_about = context_menu.addAction("About")
        action_view_shortcuts = context_menu.addAction("Shortcuts")
        action_quit = context_menu.addAction("Exit\tCtrl+X")
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

    # @staticmethod
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
        QSlider::groove:horizontal{border:0px;height:8px;background:#322b3a;}
        QSlider::sub-page:horizontal{background:#121212;border:0px;height:8px;}
        QSlider::handle:horizontal:hover{background:#c088ff;}
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Simple Media Player")
    app.setStyle("Fusion")
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
    smp.setMinimumSize(1280, 720)
    smp.show()
    sys.exit(app.exec_())
