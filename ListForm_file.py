import sqlite3
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QScrollArea, QLineEdit, QComboBox, QMessageBox
import sqlite3


#  Отображение нового окна
class ListForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.load_database()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.resize(346, 590)
        self.scroll_area.move(21, 70)

#  Загрузка всей информации из базы данных, добавление ее в лайаут в виде кнопок
    def load_database(self):
        self.connection = sqlite3.connect("dict.sqlite")
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT * FROM word_list")
        rows = self.cur.fetchall()
        self.connection.close()

        for row in rows:
            each_word = QPushButton(f"{row[0]} {row[1].lower()} {row[2].lower()}")
            each_word.setStyleSheet('text-align:left')
            each_word.clicked.connect(self.button_clicked)
            self.scroll_layout.addWidget(each_word)

#  Отображение индивидуальной информации при нажатии на кнопку со словом, кнопка удалить
    def button_clicked(self):
        button = self.sender()
        button_text = button.text().split()
        connection = sqlite3.connect("dict.sqlite")
        num = button_text[0]
        cur = connection.cursor()
        cur.execute("SELECT * FROM word_list WHERE №=?", (num,))
        result = cur.fetchone()
        self.number = str(result[0])
        connection.close()

        self.info_button = QWidget()
        self.info_button.resize(284, 284)
        self.info_button.move(780, 270)
        button_ok = QPushButton('OK', self.info_button)
        button_ok.resize(60, 40)
        button_ok.move(19, 216)
        button_ok.clicked.connect(self.info_button.close)
        part_infow = QLabel(self.info_button)
        part_infot = QLabel(self.info_button)
        part_infop = QLabel(self.info_button)
        part_infor = QLabel(self.info_button)
        part_infowr = QLabel(self.info_button)
        part_infow.setText(str(result[1]).lower())
        part_infow.move(19, 19)
        part_infot.setText(str(result[2]).lower())
        part_infot.move(19, 58)
        part_infop.setText(str(result[3]))
        part_infop.move(19, 97)
        part_infop.adjustSize()
        right = QLabel(self.info_button)
        right.setText('right')
        right.move(19, 136)
        part_infor.setText(str(result[4]))
        part_infor.move(19, 176)
        wrong = QLabel(self.info_button)
        wrong.setText('wrong')
        wrong.move(140, 136)
        part_infowr.setText(str(result[5]))
        part_infowr.move(140, 176)
        button_delete = QPushButton('DELETE', self.info_button)
        button_delete.resize(180, 40)
        button_delete.move(89, 216)
        button_delete.clicked.connect(self.delete_word)
        self.info_button.show()

#  Удаление слова из базы данных
    def delete_word(self):
        connection = sqlite3.connect("dict.sqlite")
        cur = connection.cursor()
        cur.execute("DELETE FROM word_list WHERE №=?", (self.number,))
        connection.commit()
        connection.close()
        self.close()
        self.info_button.close()

    def initUI(self, *args):
        self.setGeometry(730, 200, 384, 683)
        btn_back = QPushButton('<-', self)
        btn_back.resize(40, 40)
        btn_back.move(19, 15)
        btn_add = QPushButton('ADD NEW WORD', self)
        btn_add.resize(300, 40)
        btn_add.move(71, 15)
        btn_back.clicked.connect(self.close)
        btn_add.clicked.connect(self.open_add_word_form)

#  Открытие новой формы, ссылаясь на класс AddForm
    def open_add_word_form(self):
        self.new_form = AddForm(self)
        self.new_form.show()
        self.close()


class AddForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

        self.connection = sqlite3.connect("dict.sqlite")

    def initUI(self, args):
        self.setGeometry(787, 380, 270, 340)
        add_new = QPushButton('ADD', self)
        add_new.resize(200, 40)
        add_new.move(35, 270)
        name_word_lab = QLabel(self)
        name_word_lab.setText('word')
        name_word_lab.move(27, 15)
        self.name_word = QLineEdit(self)
        self.name_word.resize(216, 40)
        self.name_word.move(27, 65)
        translation_lab = QLabel(self)
        translation_lab.setText('translation')
        translation_lab.move(27, 115)
        self.translation = QLineEdit(self)
        self.translation.resize(216, 40)
        self.translation.move(27, 165)
        self.part_of_speech = QComboBox(self)
        self.part_of_speech.addItem('noun')
        self.part_of_speech.addItem('pronoun')
        self.part_of_speech.addItem('adjective')
        self.part_of_speech.addItem('verb')
        self.part_of_speech.addItem('adverb')
        self.part_of_speech.addItem('numeral')
        self.part_of_speech.addItem('official part of speech')
        self.part_of_speech.resize(216, 40)
        self.part_of_speech.move(27, 220)

        add_new.clicked.connect(self.read_info)

#  Считывание информации с заполненных и выбранных пользователем полей, добавление её в бд
    def read_info(self):
        cur = self.connection.cursor()
        new_name = self.name_word.text().strip()
        new_translation = self.translation.text().strip()
        new_pof = self.part_of_speech.currentText()
        if not new_name or not new_translation:
            error_message = "Fill in all the lines!"
            QMessageBox.critical(None, "Error", error_message)
        else:
            cur.execute('INSERT INTO word_list(word, translation, type) VALUES(?, ?, ?)', (new_name, new_translation,
                                                                                           new_pof))
            self.connection.commit()
            self.close()
