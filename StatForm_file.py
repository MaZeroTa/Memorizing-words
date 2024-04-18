import sqlite3
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from pyqtgraph import GraphicsLayoutWidget


class StatForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

#  Отображение графика, который строится по данным из бд. кнопка назад
    def initUI(self, args):
        self.setGeometry(730, 200, 384, 683)
        btn_back = QPushButton('<-', self)
        btn_back.resize(40, 40)
        btn_back.move(19, 15)

        btn_back.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        self.graph_widget = GraphicsLayoutWidget(self)
        layout.addWidget(btn_back)
        layout.addWidget(self.graph_widget)

        connection = sqlite3.connect("dict.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT rit FROM graph")
        right_db = list(map(lambda x: x[0], cursor.fetchall()))
        cursor.execute("SELECT wrn FROM graph")
        wrong_db = list(map(lambda x: x[0], cursor.fetchall()))
        cursor.execute("SELECT COUNT(*) FROM graph WHERE rit IS NOT NULL")
        nm_trainings = cursor.fetchone()[0]
        connection.close()

        stat = self.graph_widget.addPlot()
        stat.showGrid(x=True, y=True)
        stat.addLegend()
        x = []
        for i in range(nm_trainings):
            x.append(i)

        stat.setLabel('left', 'The number of answers')
        stat.setLabel('bottom', 'The number of trainings')
        stat.setXRange(0, nm_trainings + 1)
        stat.setYRange(0, 11)
        wrong_line = stat.plot(x, wrong_db, pen='r', symbol='x', symbolPen='r', symbolBrush=0.2, name='wrong')
        right_line = stat.plot(x, right_db, pen='g', symbol='o', symbolPen='g', symbolBrush=0.2, name='right')
