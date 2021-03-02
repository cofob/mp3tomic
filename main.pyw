from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWinExtras import QWinTaskbarButton, QWinTaskbarProgress
import sys
import os
from mp3tomic import *
import design
import json

if not os.path.isfile('config'):
    with open('config', 'w') as f:
        f.write('{}')
try:
    with open('config', 'r') as f:
        config = json.load(f)
except json.JSONDecodeError:
    config = {}


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stopbtn.clicked.connect(self.stop_btn)
        self.ui.volumeSlider.valueChanged.connect(self.changed_volume)
        self.ui.pathEdit.textChanged.connect(self.path_changed)
        self.ui.listWidget.itemClicked.connect(self.selection_changed)
        self.player = Player()
        try:
            self.path = str(config.get('path', ''))
            self.volume = int(config.get('volume', 99))
            if self.volume > 99:
                self.volume = 99
            elif self.volume < 0:
                self.volume = 99
        except:
            self.volume = 99
            self.path = ''
            self.save()
        self.changed_volume(self.volume)
        self.ui.volumeSlider.setSliderPosition(self.volume)
        self.ui.pathEdit.setText(self.path)

    def save(self):
        config['path'] = self.path
        config['volume'] = self.volume
        with open('config', 'w') as f:
            json.dump(config, f)

    def selection_changed(self, name):
        self.player.play(os.path.join(self.path, name.text()))

    def path_changed(self, path):
        self.path = path
        self.save()
        self.ui.listWidget.clear()
        if os.path.isdir(path):
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path, i)):
                    self.ui.listWidget.addItem(i)

    def changed_volume(self, val):
        self.volume = val
        self.player.set_volume(val)
        self.save()

    def stop_btn(self):
        self.player.stop()


app = QtWidgets.QApplication([])
application = App()
application.setWindowIcon(QtGui.QIcon('icon.ico'))
application.show()
application.taskbar_button = QWinTaskbarButton()
application.taskbar_button.setWindow(application.windowHandle())
application.taskbar_button.setOverlayIcon(QtGui.QIcon('icon.ico'))

sys.exit(app.exec())
