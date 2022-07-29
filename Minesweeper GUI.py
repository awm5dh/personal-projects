from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
import Minesweeper


class MineField(QWidget):
    def __init__(self, array):
        super(MineField, self).__init__()
        self.button_collection = []
        self.button_collection_coordinates = []
        self.label_collection = []
        self.array = array
        index = 0
        for i in range(len(array[0])):
            for j in range(len(array)):
                label = QtWidgets.QLabel(self)
                label.setGeometry(25 + (19 * i), 25 + (19 * j), 20, 20)
                label.setAlignment(Qt.AlignCenter)
                label_value = str(array[j][i])
                if label_value == "-1":
                    label.setPixmap(QPixmap("mine_unexploded20x20.png"))
                    label.setStyleSheet("border: 1px solid black;")
                elif label_value == "0":
                    label.setText("")
                    label.setStyleSheet("border: 1px solid black;")
                elif label_value == "1":
                    label.setText("1")
                    label.setStyleSheet("border: 1px solid black; color: blue")
                elif label_value == "2":
                    label.setText("2")
                    label.setStyleSheet("border: 1px solid black; color: green")
                elif label_value == "3":
                    label.setText("3")
                    label.setStyleSheet("border: 1px solid black; color: red")
                elif label_value == "4":
                    label.setText("4")
                    label.setStyleSheet("border: 1px solid black; color: purple")
                elif label_value == "5":
                    label.setText("5")
                    label.setStyleSheet("border: 1px solid black; color: brown")
                elif label_value == "6":
                    label.setText("6")
                    label.setStyleSheet("border: 1px solid black; color: orange")
                elif label_value == "7":
                    label.setText("7")
                    label.setStyleSheet("border: 1px solid black; color: indigo")
                elif label_value == "8":
                    label.setText("8")
                    label.setStyleSheet("border: 1px solid black; color: gold")
                self.label_collection.append(label)

                button = QtWidgets.QPushButton(self)
                button.setGeometry(25+(19*i), 25+(19*j), 20, 20)
                button.clicked.connect(self.tile_clicked)
                button.setContextMenuPolicy(Qt.CustomContextMenu)
                button.customContextMenuRequested.connect(self.tile_right_clicked)
                button.setObjectName(label_value + "," + str(index))
                self.button_collection.append(button)
                self.button_collection_coordinates.append((i, j))

                index += 1

        self.button_relationships = {}
        for index, button in enumerate(self.button_collection):
            related_coordinates = Minesweeper.get_adjacent_cells((button.x()-25)/19, (button.y()-25)/19, len(array[0]), len(array))
            self.button_relationships[index] = []
            for pair in related_coordinates:
                self.button_relationships[index].append(self.button_collection_coordinates.index(pair))

        self.buttons_to_be_clicked = []
        self.adjustSize()

    def tile_clicked(self):
        self.buttons_to_be_clicked = []
        info = self.sender().objectName().split(",")[0], self.sender().objectName().split(",")[1]
        value, index = info[0], int(info[1])
        if value == "0":
            for i in self.button_relationships[index]:
                if not self.button_collection[i].isHidden():
                    self.buttons_to_be_clicked.append(self.button_collection[i])
            self.implied_click()
        if value == "-1":
            self.label_collection[index].setPixmap(QPixmap("mine_exploded_20x20.png"))
        self.sender().hide()

    def tile_right_clicked(self):
        if self.sender().icon().isNull():
            self.sender().setIcon(QIcon("flag_20x20.png"))
        else:
            self.sender().setIcon(QIcon())

    def implied_click(self):
        for button in self.buttons_to_be_clicked:
            info = button.objectName().split(",")[0], button.objectName().split(",")[1]
            value, index = info[0], int(info[1])
            if value == "0":
                for i in self.button_relationships[index]:
                    if not self.button_collection[i].isHidden():
                        self.buttons_to_be_clicked.append(self.button_collection[i])
            button.hide()


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
        self.adjustSize()
        self.setWindowTitle("Minesweeper by Aidan")

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("1")
        self.label.move(30, 20)


    def update(self):
        pass
        # self.label.adjustSize()


def clicked():
    print("clicked")


def window():
    app = QApplication(sys.argv)
    custom_font = QFont("Unispace")
    custom_font.setPointSize(9)
    custom_font.setBold(True)
    app.setFont(custom_font, "QLabel")
    # win = MyWindow()
    win = MineField(Minesweeper.create_field(16, 30, 99))
    win.show()
    sys.exit(app.exec_())

window()