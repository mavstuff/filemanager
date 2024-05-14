import os
import sys
import win32api
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore


class MyDirItem:
    def __init__(self):
        self.specialdir = None
        self.dir = None


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.myitem = MyDirItem()
        layout = QGridLayout()
        self.setLayout(layout)
        self.listwidget = QListWidget()
        #self.listwidget.insertItem(0, "My Computer")
        #self.listwidget.insertItem(1, "Documents")
        #self.listwidget.insertItem(2, "Pictures")
        #self.listwidget.insertItem(3, "Music")
        #self.listwidget.insertItem(4, "Videos")
        #self.listwidget.insertItem(5, "Downloads")
        
        layout.addWidget(self.listwidget)

        self.listwidget.itemDoubleClicked.connect(self.doubleclicked)

    def listmyitem(self, clickeditem: MyDirItem):
        self.myitem = clickeditem
        self.listwidget.clear()
        i = 0

        if (clickeditem.specialdir == "Desktop"):
            mynewitem = MyDirItem()
            mynewitem.specialdir = "My Computer"
            mynewitem.dir = None

            listitem = QListWidgetItem()
            listitem.setText(mynewitem.specialdir)
            listitem.setData(QtCore.Qt.UserRole, mynewitem) 
            self.listwidget.insertItem(i, listitem)
            i += 1


        if (clickeditem.specialdir == "My Computer"):
            all_drives = [i for i in win32api.GetLogicalDriveStrings().split('\x00') if i]
            
            for drive in all_drives:
                mynewitem = MyDirItem()
                mynewitem.specialdir = None
                mynewitem.dir = drive

                listitem = QListWidgetItem()
                listitem.setText("[%s]" % mynewitem.dir)
                listitem.setData(QtCore.Qt.UserRole, mynewitem) 
                self.listwidget.insertItem(i, listitem)
                i += 1

        elif (clickeditem.specialdir == None):

            if len(clickeditem.dir) >= 2 and clickeditem.dir[1] == ':':

                mynewitem = MyDirItem()
                mynewitem.specialdir = "My Computer"
                mynewitem.dir = None
                listitem = QListWidgetItem()
                listitem.setText("[..]")
                listitem.setData(QtCore.Qt.UserRole, mynewitem) 
                self.listwidget.insertItem(i, listitem)
                i = i + 1 

            if not os.path.dirname(clickeditem.dir) == self.myitem.dir:

                mynewitem = MyDirItem()
                mynewitem.specialdir = None
                mynewitem.dir = os.path.abspath(os.path.join(clickeditem.dir, os.pardir))
                listitem = QListWidgetItem()
                listitem.setText("[..]")
                listitem.setData(QtCore.Qt.UserRole, mynewitem) 
                self.listwidget.insertItem(i, listitem)
                i = i + 1 

                
            if os.path.isdir(clickeditem.dir):
                for f in os.listdir(clickeditem.dir):
                    fshow = f
                    if (os.path.isdir(os.path.join(clickeditem.dir, f))):
                        fshow = "[" + f + "]"

                    mynewitem = MyDirItem()
                    mynewitem.specialdir = None
                    mynewitem.dir = os.path.abspath(os.path.join(clickeditem.dir, f))

                    listitem = QListWidgetItem()
                    listitem.setText(fshow)
                    listitem.setData(QtCore.Qt.UserRole, mynewitem) 
                    self.listwidget.insertItem(i, listitem)
                    i += 1


    def doubleclicked(self, qmodelindex):
        listitem = self.listwidget.currentItem()
        myitem = listitem.data(QtCore.Qt.UserRole)
        self.listmyitem(myitem)


app = QApplication(sys.argv)
screen = Window()
screen.show()
myitem = MyDirItem()
myitem.dir = None
myitem.specialdir = "Desktop"
screen.listmyitem(myitem)
sys.exit(app.exec_())




