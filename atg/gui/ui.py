from __future__ import absolute_import

from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
# from techniques.pairwise import Pairwise
from allpairspy import AllPairs as Pairwise

from PyQt5.QtWidgets import QTableWidgetItem

data = [['John', datetime.datetime(2019, 5, 5, 0, 54), datetime.datetime(2019, 5, 26, 22, 51, 36)],
        ['Rex', datetime.datetime(2019, 5, 26, 22, 51, 36), datetime.datetime(2019, 6, 15, 10, 22, 48)],
        ['Watson', datetime.datetime(2019, 6, 15, 10, 22, 48), datetime.datetime(2019, 7, 8, 13, 33, 36)],
        ['Manila', datetime.datetime(2019, 7, 8, 13, 33, 36), datetime.datetime(2019, 7, 29, 6, 18)],
        ['Pete', datetime.datetime(2019, 7, 29, 6, 18), datetime.datetime(2019, 8, 6, 18, 50, 24)],
        ['Mathew', datetime.datetime(2019, 8, 6, 18, 50, 24), datetime.datetime(2019, 8, 31, 3, 14, 24)]]
parameters = [
    ["Ford", "Volvo", "BMW"],
    [20000, 40000, 50000],
    ["New", "Used"]
]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 90, 511, 301))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 430, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(440, 430, 75, 23))
        self.pushButton2.setObjectName("pushButton2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Variable1"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Variable2"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Variable3"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Output"))
        self.pushButton.setText(_translate("MainWindow", "Load"))
        self.pushButton.clicked.connect(self.onload)
        self.pushButton2.setText(_translate("MainWindow", "Read"))
        self.pushButton2.clicked.connect(self.read)

    def onload(self):
        pairs = [v for v in Pairwise(parameters)]
        numrows = len(pairs)  # 6 rows in your example
        numcols = len(pairs[0])  # 3 columns in your example
        print(pairs)
        # Set colums and rows in QTableWidget
        # self.tableWidget.setColumnCount(numcols)
        self.tableWidget.setRowCount(numrows)

        # Loops to add values into QTableWidget
        for row in range(numrows):
            for column in range(numcols):
                # Check if value datatime, if True convert to string
                if isinstance(pairs[row][column], int):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(pairs[row][column])))
                    print(pairs[row][column])
                else:
                    self.tableWidget.setItem(row, column, QTableWidgetItem((pairs[row][column])))

    def read(self):
        col = self.tableWidget.columnCount() - 1
        rows = self.tableWidget.rowCount()
        for row in range(rows):
            item = self.tableWidget.item(row, col)
            if item and item.text():
                print(self.tableWidget.item(row, col).text())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
#
# app = QApplication([])
#
#
# class PopupView(QWidget):
#     def __init__(self, parent=None):
#         super(PopupView, self).__init__(parent)
#         self.setWindowFlags(Qt.Popup)
#
#
# class ItemDelegate(QItemDelegate):
#     def __init__(self, parent):
#         super(ItemDelegate, self).__init__(parent)
#
#     def createEditor(self, parent, option, index):
#         return PopupView(parent)
#
#     def updateEditorGeometry(self, editor, option, index):
#         editor.move(QCursor.pos())
#
#
# class Model(QAbstractTableModel):
#     def __init__(self):
#         QAbstractTableModel.__init__(self)
#         self.items = [[1, 'one', 'ONE'], [2, 'two', 'TWO'], [3, 'three', 'THREE']]
#
#     def flags(self, index):
#         return Qt.ItemIsEnabled | Qt.ItemIsEditable
#
#     def rowCount(self, parent=QModelIndex()):
#         return 3
#
#     def columnCount(self, parent=QModelIndex()):
#         return 3
#
#     def data(self, index, role):
#         if not index.isValid():
#             return
#
#         if role in [Qt.DisplayRole, Qt.EditRole]:
#             return self.items[index.row()][index.column()]
#
#
# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self, parent)
#         self.clipboard = QApplication.clipboard()
#         mainWidget = QWidget()
#         self.setCentralWidget(mainWidget)
#         mainWidget.setLayout(QVBoxLayout())
#
#         view = QTableView()
#         view.setModel(Model())
#         view.setItemDelegate(ItemDelegate(view))
#         self.layout().addWidget(view)
#
#
# view = MainWindow()
# view.show()
# app.exec_()
