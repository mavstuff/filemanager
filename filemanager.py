import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        self.listwidget = QListWidget()
        #self.listwidget.insertItem(0, "My Computer")
        #self.listwidget.insertItem(1, "Documents")
        #self.listwidget.insertItem(2, "Pictures")
        #self.listwidget.insertItem(3, "Music")
        #self.listwidget.insertItem(4, "Videos")
        #self.listwidget.insertItem(5, "Downloads")
        #self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)

        self.listwidget.itemDoubleClicked.connect(self.doubleclicked)
    
    def listdir(self, dir):
        self.dir = dir
        self.setWindowTitle(dir)
        
        i = 0
        self.listwidget.clear()
        if not os.path.dirname(dir) == dir:
            item = QListWidgetItem()
            item.setText("[..]")
            item.setData(QtCore.Qt.UserRole, os.path.abspath(os.path.join(dir, os.pardir))) 
            self.listwidget.insertItem(i, item)
            i = i + 1

        for f in os.listdir(dir):
            fshow = f
            if (os.path.isdir(os.path.join(dir, f))):
                fshow = "[" + f + "]"
            item = QListWidgetItem()
            item.setText(fshow)
            item.setData(QtCore.Qt.UserRole, os.path.abspath(os.path.join(dir, f))) 
            self.listwidget.insertItem(i, item)
            i += 1


    def doubleclicked(self, qmodelindex):
        item = self.listwidget.currentItem()
        path = item.data(QtCore.Qt.UserRole)
        if (os.path.isdir(path)):
            self.listdir(path)


app = QApplication(sys.argv)
screen = Window()
screen.show()
screen.listdir("k:\\")
sys.exit(app.exec_())




