import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,QLabel,QLineEdit,QGridLayout,QLCDNumber,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
import demo


class UI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        #Button
        btn = QPushButton('Start', self)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        #Title_path
        title_path = QLabel('Path/IP')
        self.titleEdit = QLineEdit()
        #Title_people
        title_people = QLabel('People')
        #Display
        self.lcd_people = QLCDNumber(self)

        btn.clicked.connect(self.buttonClicked)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.lcd_people, 4, 0)
        grid.addWidget(title_people, 3, 0)
        grid.addWidget(btn,2,1)
        grid.addWidget(title_path, 1, 0)
        grid.addWidget(self.titleEdit, 1, 1)


        self.setLayout(grid)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Demo')
        self.show()

    def buttonClicked(self):
        path = self.titleEdit.text()
        demo.yolo_launcher(path,self)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    UI = UI()
    sys.exit(app.exec_())
    exit(app.exec_())

