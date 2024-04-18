import sqlite3
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QMessageBox


#  Открытие новой формы
class PlayForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

        self.right_or_not = False

    def initUI(self, *args):
        self.setGeometry(730, 200, 384, 683)
        btn_back = QPushButton('<-', self)
        btn_back.resize(40, 40)
        btn_back.move(19, 15)
        btn_back.clicked.connect(self.close)

        self.translation_label = QLabel(self)
        self.translation_label.setText('Translation:')
        self.translation_label.move(19, 70)
        self.translation_word = QLabel(self)
        self.translation_word.move(19, 120)
        self.translation_word.resize(375, 40)
        self.word_edit = QLineEdit(self)
        self.word_edit.setPlaceholderText("Enter word")
        self.word_edit.move(19, 180)
        self.check_button = QPushButton("Check", self)
        self.check_button.resize(200, 40)
        self.check_button.move(19, 240)
        self.check_button.clicked.connect(self.check_answer)
        self.result_info = QLabel(self)
        self.result_info.move(19, 300)
        self.result_info.resize(346, 40)

        self.next_button = QPushButton("Next word", self)
        self.next_button.resize(346, 40)
        self.next_button.move(19, 400)
        connection = sqlite3.connect("dict.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM word_list")
        words_num = cursor.fetchone()[0]
        connection.close()
        if words_num < 10:
            error_message = "Please, add minimum 10 words"
            reply = QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                reply.close()
                self.close()
        else:
            self.next_button.clicked.connect(self.load_next_word)
        self.next_button_counter = 0
        self.right_count = []
        self.wrong_count = []
        self.in_training = [0]
        self.last_training = []
        self.change_last_training = []
        self.t_number = 0
        self.again = QPushButton("Restart", self)
        self.again.resize(346, 40)
        self.again.move(19, 400)
        self.again.clicked.connect(self.load_next_word)
        self.again.hide()

        self.sw_list1, self.sw_list2 = QWidget(self), QWidget(self)
        self.rtt, self.wrt = QLabel("You've answered right", self), QLabel("You've answered wrong", self)
        self.rtt.move(19, 57)
        self.wrt.move(184, 57)

        self.load_next_word()
        
#  Загрузка нового слова, учитывая впервые ли проводится тренировка или это повтор
    def load_next_word(self):
        self.rtt.hide()
        self.wrt.hide()
        self.sw_list1.hide()
        self.sw_list2.hide()
        self.next_button.hide()
        self.result_info.hide()
        self.word_edit.clear()
        self.next_button.hide()
        self.word_edit.setEnabled(True)
        self.check_button.setEnabled(True)
        connection = sqlite3.connect("dict.sqlite")
        cursor = connection.cursor()
        if self.change_last_training != []:
            self.translation_label.show()
            self.translation_word.show()
            self.word_edit.show()
            self.check_button.show()
            self.again.hide()
            cursor.execute("SELECT * FROM word_list WHERE №=?", (self.change_last_training[0],))
            self.change_last_training.pop(0)
            result = cursor.fetchone()
            self.t_number = str(result[0])
            self.t_word = str(result[1])
            self.t_translation = str(result[2])
            self.t_right = int(result[4])
            self.t_wrong = int(result[5])
            self.translation_word.setText(self.t_translation.lower())
            connection.close()
        else:
            while self.t_number in self.in_training:
                cursor.execute("SELECT * FROM word_list ORDER BY RANDOM() LIMIT 1")
                result = cursor.fetchone()
                self.t_number = str(result[0])
            self.in_training.append(self.t_number)
            self.last_training.append(self.t_number)
            self.t_word = str(result[1])
            self.t_translation = str(result[2])
            self.t_right = int(result[4])
            self.t_wrong = int(result[5])
            self.translation_word.setText(self.t_translation.lower())
            connection.close()

#  Проверка слова или вывод ошибки, если поле со словом пустое
    def check_answer(self):
        answer = self.word_edit.text()
        if not answer:
            error_message = "Write your answer"
            QMessageBox.critical(None, "Error", error_message)
        elif answer.lower().strip() == self.t_word.lower():
            self.result_info.setText("Correct translation")
            self.result_info.setStyleSheet('background: green;')
            self.result_info.show()
            self.right_or_not = True
            self.update_info()
            self.right_count.append(self.t_translation)
            self.show_result()
        else:
            self.result_info.setText("Incorrect translation")
            self.result_info.setStyleSheet('background: red;')
            self.result_info.show()
            self.right_or_not = False
            self.update_info()
            self.wrong_count.append(self.t_translation)
            self.show_result()

#  Обновление информации о слове о правильности ответа в базе данных
    def update_info(self):
        connection = sqlite3.connect("dict.sqlite")
        cursor = connection.cursor()
        if self.right_or_not:
            cursor.execute("UPDATE word_list SET right=? WHERE №=?", (self.t_right + 1, self.t_number))
        else:
            cursor.execute("UPDATE word_list SET wrong=? WHERE №=?", (self.t_wrong + 1, self.t_number))
        connection.commit()
        connection.close()

#  Проверка кол-ва слов, показанных до этого, появление кнопки для следующего слова или для результатов тренировки
    def show_result(self):
        if self.next_button_counter < 9:
            self.next_button_counter += 1
            self.word_edit.setEnabled(False)
            self.check_button.setEnabled(False)
            self.next_button.show()
        else:
            self.end_button = QPushButton('Show result', self)
            self.end_button.resize(346, 40)
            self.end_button.move(19, 400)
            self.end_button.clicked.connect(self.end_of_training)
            self.end_button.show()

#  Сохранение информации для статистики в базе данных, отображение результатов тренировки и кнопки рестарта
    def end_of_training(self):
        connection = sqlite3.connect("dict.sqlite")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO graph(rit, wrn) VALUES(?, ?)', (len(self.right_count), len(self.wrong_count)))
        connection.commit()
        self.end_button.hide()
        self.result_info.hide()
        self.next_button.hide()
        self.translation_label.hide()
        self.translation_word.hide()
        self.word_edit.hide()
        self.check_button.hide()

        sw_list1_ly, sw_list2_ly = QVBoxLayout(), QVBoxLayout()
        self.clear_layout(sw_list1_ly)
        self.clear_layout(sw_list2_ly)

        for i in self.right_count:
            cursor.execute("SELECT * FROM word_list WHERE translation=?", (i,))
            word = cursor.fetchone()
            rt_word = word[1]
            print_word = QLabel(rt_word)
            sw_list1_ly.addWidget(print_word)
        for j in self.wrong_count:
            cursor.execute("SELECT * FROM word_list WHERE translation=?", (j,))
            word = cursor.fetchone()
            wr_word = word[1]
            print_word = QLabel(wr_word)
            sw_list2_ly.addWidget(print_word)
        self.again.show()
        self.right_count, self.wrong_count = [], []
        self.change_last_training = self.last_training.copy()
        self.next_button_counter = 0

        self.rtt.show()
        self.wrt.show()
        self.sw_list1, self.sw_list2 = QWidget(self), QWidget(self)
        self.sw_list1.setLayout(sw_list1_ly)
        self.sw_list2.setLayout(sw_list2_ly)
        self.sw_list1.move(19, 70)
        self.sw_list2.move(184, 70)
        self.sw_list1.show()
        self.sw_list2.show()

#  Очищение лайаутов перед повторном их отображении
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
