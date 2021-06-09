import sys
import math
import random as rd
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRect, QPointF

STEPS = 1
HEIGHT = 200
WIDTH = 200
POLYGON_WINDOW = None
OFFSET = 50


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


class SubWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()

    def setup(self):
        global HEIGHT, WIDTH, STEPS, OFFSET
        self.setWindowTitle('Trójkąt Sierpińskiego by Patryk Wojtiuk')
        self.canvas = QRect(1, 1, WIDTH, HEIGHT)
        self.setMaximumSize(WIDTH+OFFSET, HEIGHT+OFFSET)
        self.setMinimumSize(WIDTH+OFFSET, HEIGHT+OFFSET)
        self.show()

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        self.paintTriangle(e, qp)
        qp.end()

    def start_gamepoint(self, p1, p2, p3):
        r1, r2 = sorted([rd.uniform(0.0, 1.0), rd.uniform(0.0, 1.0)])
        return QPointF(r1 * p1.x() + (r2 - r1)*p2.x() + (1-r2)*p3.x(), r1 * p1.y() + (r2 - r1)*p2.y() + (1-r2)*p3.y())

    def paintTriangle(self, e, qp):
        global OFFSET
        objClr = QColor(200, 30, 40)

        pen = QtGui.QPen(QColor(0, 0, 0))
        pen.setWidth(1)

        qp.setPen(pen)
        qp.setBrush(objClr)
        qp.setRenderHint(QPainter.Antialiasing)

        triangles = []

        p1 = QPointF(0 + OFFSET, HEIGHT)
        p2 = QPointF(WIDTH, HEIGHT)
        p3 = QPointF((WIDTH+OFFSET)/2, HEIGHT-(WIDTH*math.sqrt(3))/2)

        triangles.append(Triangle(p1, p2, p3))

        qp.drawLine(p1, p2)
        qp.drawLine(p2, p3)
        qp.drawLine(p1, p3)

        #GRA W CHAOS w tym przypadku Szczegółowość polecam na 200000
        # gamePoint = self.start_gamepoint(p1, p2, p3)
        # for i in range(STEPS):
        #     which_point = rd.choice([p1, p2, p3])
        #     qp.drawPoint(gamePoint)
        #     gamePoint = QPointF((gamePoint.x() + which_point.x()) / 2, (gamePoint.y() + which_point.y()) / 2)

        for i in range(STEPS - 1):
            after_triangles = []
            to_remove = []
            for t in triangles:
                p1 = QPointF((t.p1.x() + t.p2.x()) / 2, (t.p1.y() + t.p2.y()) / 2)
                p2 = QPointF((t.p1.x() + t.p3.x()) / 2, (t.p1.y() + t.p3.y()) / 2)
                p3 = QPointF((t.p2.x() + t.p3.x()) / 2, (t.p2.y() + t.p3.y()) / 2)

                qp.drawLine(p1, p2)
                qp.drawLine(p2, p3)
                qp.drawLine(p1, p3)

                after_triangles.append(Triangle(t.p1, p1, p2))
                after_triangles.append(Triangle(p1, t.p2, p3))
                after_triangles.append(Triangle(p2, p3, t.p3))

                to_remove.append(t)
            for t in to_remove:
                triangles.remove(t)
            for t in after_triangles:
                triangles.append(t)


class CreateButton(QPushButton):
    def __init__(self, fields=None):
        super(CreateButton, self).__init__()
        if fields is None:
            fields = []
        self.fields = fields

    def akcja(self):
        global STEPS, HEIGHT, WIDTH, POLYGON_WINDOW
        if self.text() == 'Stworz Trójkąt Sierpińskiego':
            if self.fields[0].text() and self.fields[1].text() and self.fields[2].text():
                HEIGHT = int(self.fields[0].text())
                WIDTH = int(self.fields[1].text())
                STEPS = int(self.fields[2].text())
                POLYGON_WINDOW = SubWindow()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup()

    def setup(self):
        self.setWindowTitle('Trójkąt Sierpińskiego by Patryk Wojtiuk')
        grid = QGridLayout()
        label1 = QLabel()
        label1.setText('Wyskokość: ')
        label2 = QLabel()
        label2.setText('Szerokość: ')
        heightEdit = QLineEdit()
        widthEdit = QLineEdit()
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(heightEdit, 0, 1)
        grid.addWidget(widthEdit, 1, 1)
        label3 = QLabel()
        label3.setText('Podaj stopień szczegółowości: ')
        complexityEdit = QLineEdit()
        grid.addWidget(label3, 2, 0)
        grid.addWidget(complexityEdit, 2, 1)
        createButton = CreateButton([heightEdit, widthEdit, complexityEdit])
        createButton.setText('Stworz Trójkąt Sierpińskiego')
        grid.addWidget(createButton, 3, 0, 1, 2)
        createButton.clicked.connect(createButton.akcja)
        self.setLayout(grid)
        self.show()


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
