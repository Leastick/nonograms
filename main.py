import os
import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QGraphicsScene, QPushButton, QFrame, QGraphicsView, QLabel)
from PyQt5.QtGui import (QColor, QPen, QFont, QPixmap)
from PyQt5.QtCore import (Qt, pyqtSignal)

PATH = os.getcwd()
TEST_PATH = PATH + '/levels/level2'
to_pic = {'free': PATH + '/images/free_for_sure.png',
          'occupied': PATH + '/images/occupied.jpg',
          'unknown': None}


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


class Level:
    def __init__(self, path):
        self.rows = []
        self.columns = []
        with open(path, 'r') as f:
            self.n = int(f.readline())
            f.readline()
            for i in range(self.n):
                self.rows.append(list(map(int, f.readline().split())))
            f.readline()
            for i in range(self.n):
                self.columns.append(list(map(int, f.readline().split())))

    def row_iterator(self, field):
        for i in range(self.n):
            yield field[i]

    def column_iterator(self, field):
        for i in range(self.n):
            yield [field[j][i] for j in range(self.n)]

    def find_blocks(self, line):
        blocks = []
        block_len = 0
        for i in range(self.n):
            if line[i]:
                block_len += 1
            else:
                if block_len > 0:
                    blocks.append(block_len)
                block_len = 0
        return blocks

    def check_answer(self, field):
        for index, row in enumerate(self.row_iterator(field)):
            blocks = self.find_blocks(row)
            if blocks != self.rows[index]:
                return False
        for index, column in enumerate(self.column_iterator(field)):
            blocks = self.find_blocks(column)
            if blocks != self.columns[index]:
                return False
        return True


class Field(QGraphicsScene):
    def __init__(self, cell_side, level):
        super().__init__()
        self.cell_side = cell_side
        self.n = level.n
        self.widget_side = (5 + self.n) * self.cell_side
        self.setSceneRect(0, 0, self.widget_side, self.widget_side)
        self.level = level
        self.field = [[False] * level.n for _ in range(level.n)]
        self._init_ui()

    def make_labels(self):
        font = QFont('DejaVu Sans', 12, QFont.Bold)
        for index, blocks in enumerate(self.level.rows):
            s = '   '.join([str(block) for block in blocks]).rjust(25, ' ')
            text = self.addText(s, font)
            text.setPos(0, 5 * self.cell_side + index * self.cell_side)
        for index, blocks in enumerate(self.level.columns):
            s = '\n'.join([str(block) for block in blocks])
            text = self.addText(s, font)
            text.setPos(5 * self.cell_side + index * self.cell_side, 0)

    def _init_ui(self):
        self.setSceneRect(0, 0, self.widget_side, self.widget_side)
        self.cells = [[Cell(i, j, self) for j in range(self.level.n)] for i in range(self.level.n)]
        self.coors = [x for x in range(5 * self.cell_side, self.widget_side, self.cell_side)]
        thin_pen = QPen(Qt.gray, 2, Qt.SolidLine)
        bold_pen = QPen(Qt.gray, 4, Qt.SolidLine)
        for index, coor in enumerate(self.coors):
            current_pen = thin_pen if index % 5 != 0 else bold_pen
            self.addLine(coor, 0, coor, self.widget_side, current_pen)
            self.addLine(0, coor, self.widget_side, coor, current_pen)
        self.make_labels()

    def process_cell(self, x, y):
        cell_x_number = 0
        cell_y_number = 0
        while cell_x_number < len(self.coors) and self.coors[cell_x_number] < x:
            cell_x_number += 1
        while cell_y_number < len(self.coors) and self.coors[cell_y_number] < y:
            cell_y_number += 1
        cell_y_number -= 1
        cell_x_number -= 1
        if cell_y_number < 0 or cell_x_number < 0:
            return
        state = self.cells[cell_x_number][cell_y_number].switch_state()
        return cell_x_number, cell_y_number, state


class Viewer(QGraphicsView):
    def __init__(self, level):
        super().__init__()
        self.cell_side = 25
        self.field = Field(self.cell_side, level)
        self.setScene(self.field)
        self.setFixedSize(self.field.widget_side, self.field.widget_side)
        self.scene = []
        for i in range(level.n):
            self.scene.append([])
            for j in range(level.n):
                self.scene[i].append(ClickableLabel(self))
                self.scene[i][j].clicked.connect(lambda i=i, j=j: self.label_event(i, j))
        self.show()

    def update_picture(self, cell_x, cell_y, state):
        if state is None:
            self.scene[cell_x][cell_y].hide()
            return
        x = (cell_x + 5) * self.cell_side
        y = (cell_y + 5) * self.cell_side
        image = QPixmap(state)
        image = image.scaled(self.cell_side - 0.01, self.cell_side - 0.01)
        self.scene[cell_x][cell_y].setPixmap(image)
        self.scene[cell_x][cell_y].move(x + 0.01, y + 0.01)
        self.scene[cell_x][cell_y].setFixedSize(self.cell_side - 0.01, self.cell_side - 0.01)
        self.scene[cell_x][cell_y].show()
        self.update()

    def mousePressEvent(self, QMouseEvent):
        x, y = QMouseEvent.pos().x(), QMouseEvent.pos().y()
        cell_x, cell_y, state = self.field.process_cell(x, y)
        self.update_picture(cell_x, cell_y, state)

    def label_event(self, x, y):
        state = self.field.cells[x][y].switch_state()
        if state is None:
            self.scene[x][y].hide()
            return
        self.update_picture(x, y, state)


class Cell(QWidget):
    def __init__(self, x, y, host):
        super().__init__()
        self.host = host
        self.x = x
        self.y = y
        self.states = ['unknown', 'occupied', 'free']
        self.state_number = 0
        self._init_ui()

    def switch_state(self):
        self.state_number = (self.state_number + 1) % 3
        print(self.states[self.state_number])
        return to_pic[self.states[self.state_number]]

    def _init_ui(self):
        pass


def main():
    application = QApplication(sys.argv)
    window = Viewer(Level(TEST_PATH))
    application.exec_()


if __name__ == '__main__':
    main()