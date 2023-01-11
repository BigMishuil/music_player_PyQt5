# Let's listen to something ;)

import sys
import os
from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from player import Ui_MainWindow

        
class Player(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Player, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.play_icon = QIcon("icons/play.png")
        self.next_icon = QIcon("icons/next.png")
        self.back_icon = QIcon("icons/back.png")
        self.pause_icon = QIcon("icons/pause.png")
        self.stop_icon = QIcon("icons/stop.png")
        self.volume_icon = QIcon("icons/volume.png")
        self.mute_icon = QIcon("icons/mute.png")
        self.default_image = QPixmap("icons/icon.png")
        self.currentPlaylist = QMediaPlaylist()
        self.icon_button()
        self.setAcceptDrops(True)
        self.sound = True
        self.music = {}
        self.player = QMediaPlayer(self)
        self.player.mediaStatusChanged.connect(self.media_status_change)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.musicList.itemClicked.connect(self.on_item_clicked)
        self._buffer = QBuffer()
        self.musicProgress.setValue(0)
        self.musicProgress.setRange(0, 0)
        self.musicProgress.sliderMoved.connect(self.on_slider_moved)
        self.musicVolume.valueChanged.connect(self.volume_change)
        self.player.setPlaylist(self.currentPlaylist)
        self.volumeProgress.clicked.connect(self.on_sound_clicked)
        self.stopButton.clicked.connect(self.on_stop_clicked)
        self.nextButton.clicked.connect(self.on_next_clicked)
        self.backButton.clicked.connect(self.on_back_clicked)
        self.playButton.clicked.connect(self.on_play_clicked)
        self.pauseButton.clicked.connect(self.on_pause_clicked)
        self.musicVolume.setValue(50)
        self.index = 0
        self.item = ""
        
    def on_volume_change(self, value):
        self.player.setVolume(value)

    def on_next_clicked(self):
        self.player.playlist().next()
        index = self.player.playlist().currentIndex()

        try:
            self.musicList.item(index).setSelected(True)

        except:
            self.player.playlist().setCurrentIndex(0)
            self.musicList.item(0).setSelected(True)
            self.player.play()

    def on_back_clicked(self):
        self.player.playlist().previous()
        index = self.player.playlist().currentIndex()

        try:
            self.musicList.item(index).setSelected(True)

        except:
            self.player.playlist().setCurrentIndex(0)
            self.musicList.item(0).setSelected(True)
            self.player.play()
            
    def on_play_clicked(self):
        if self.currentPlaylist.mediaCount() == 0:
            self.open_file()
        if self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
        elif self.player.state() == QMediaPlayer.StoppedState:
            self.player.play()
        else:
            self.player.play()
            
    def open_file(self):
        file_choosen = QFileDialog.getOpenFileUrl(self, 'Open Music File', expanduser('~'),
                                                  'Audio (*.mp3 *.ogg *.wav)', '*.mp3 *.ogg *.wav')

        if file_choosen is not None:
            self.musicList.addItem(file_choosen[0].fileName())
            self.currentPlaylist.addMedia(QMediaContent(file_choosen[0]))
            
    def on_pause_clicked(self):
        if self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
        elif self.player.state() == QMediaPlayer.StoppedState:
            self.player.play()
        else:
            self.player.pause()
    
    def on_stop_clicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.stop()
        
    def on_sound_clicked(self):
        if self.sound:
            self.volumeProgress.setIcon(self.mute_icon)
            self.player.setVolume(0)
            self.sound = False
        else:
            self.sound = True
            self.player.setVolume(self.musicVolume.value())
            self.volumeProgress.setIcon(self.volume_icon)
        
    def duration_changed(self, duration):
        self.musicProgress.setRange(0, duration)
        
    def on_slider_moved(self, position):
        sender = self.sender()
        if isinstance(sender, QSlider):
            if self.player.isSeekable():
                self.player.setPosition(position)
                
    def on_item_clicked(self):
        data = self.musicList.selectedIndexes()[0]
        index = data.row()
        self.play_music(index=index)

    def play_music(self, index=0):
        self.player.setPlaylist(self.currentPlaylist)
        self.player.playlist().setCurrentIndex(index)
        self.player.play()
        self.player.setVolume(self.musicVolume.value())

    def volume_change(self, value):
        if value > 50:
            self.player.setVolume(value+1)
        else:
            self.player.setVolume(value)
        
    def position_changed(self, position):
        tm = '%d:%02d' % (int(position/60000), int((position/1000) % 60))
        self.startTime.setText(tm)
        self.musicProgress.setValue(position)
                
    def media_status_change(self):
        duration_t = self.player.duration()
        tm = "%d:%02d" % (int(duration_t / 60000), int((duration_t/1000) % 60))
        self.musicTime.setText(tm)
        index = self.player.playlist().currentIndex()
        try:
            self.musicList.item(index).setSelected(True)
        except:
            pass
        
    def icon_button(self):
        self.playButton.setIcon(self.play_icon)
        self.pauseButton.setIcon(self.pause_icon)
        self.nextButton.setIcon(self.next_icon)
        self.backButton.setIcon(self.back_icon)
        self.stopButton.setIcon(self.stop_icon)
        self.image.setPixmap(self.default_image)
        self.image.setAlignment(Qt.AlignCenter)
        self.volumeProgress.setIcon(self.volume_icon)

    def dropEvent(self, e):
        for x in e.mimeData().urls():
            name = x.fileName()
            path = x.toLocalFile()
            self.musicList.addItem(name)
            self.currentPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))

    def dragEnterEvent(self, e):
        for x in e.mimeData().urls():
            file_string = x.toString()
            if file_string.endswith(".mp3") or file_string.endswith(".MP3"):
                e.accept()
            else:
                e.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = Player()
    application.show()
    app.exec_()
