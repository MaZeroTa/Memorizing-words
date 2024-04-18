import sys
from StatForm_file import StatForm
from ListForm_file import ListForm
from PlayForm_file import PlayForm

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap

#  Открытие главного окна
class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(730, 200, 384, 683)
        btn_start = QPushButton('START TRAINING', self)
        btn_start.resize(350, 100)
        btn_start.move(19, 450)
        btn_stat = QPushButton('STATISTICS', self)
        btn_stat.resize(350, 50)
        btn_stat.move(19, 575)
        btn_list = QPushButton('≡', self)
        btn_list.resize(40, 40)
        btn_list.move(331, 15)

        pixmap = QPixmap('Kartinka.jpg')
        self.image = QLabel(self)
        self.image.move(19, 60)
        self.image.resize(370, 330)
        self.image.setPixmap(pixmap)

        btn_start.clicked.connect(self.open_training_form)
        btn_list.clicked.connect(self.open_list_form)
        btn_stat.clicked.connect(self.open_stat_form)

    #  Открытие нового окна, ссылаясь на класс PlayForm
    def open_training_form(self):
        self.new_form = PlayForm(self)
        self.new_form.show()

    #  Открытие нового окна, ссылаясь на класс ListForm
    def open_list_form(self):
        self.new_form = ListForm(self)
        self.new_form.show()

    #  Открытие нового окна, ссылаясь на класс StatForm
    def open_stat_form(self):
        self.new_form = StatForm(self)
        self.new_form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mm = MainMenu()
    mm.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())