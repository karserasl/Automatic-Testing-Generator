# @Author: Administrator
# @Date:   03/05/2021 03:55
import ast
import csv

from PySide6 import QtCore, QtGui, QtWidgets


class MyWindow(QtWidgets.QWidget):
    def __init__(self, fileName, parent=None):
        super(MyWindow, self).__init__(parent)
        self.fileName = fileName

        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.pushButtonLoad = QtWidgets.QPushButton(self)
        self.pushButtonLoad.setText("Load Csv File!")
        self.pushButtonLoad.clicked.connect(self.loadCsv(self.fileName))

        # self.pushButtonWrite = QtWidgets.QPushButton(self)
        # self.pushButtonWrite.setText("Write Csv File!")
        # self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.pushButtonLoad)
        # self.layoutVertical.addWidget(self.pushButtonWrite)

    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            node = ast.parse(fileInput.read())

            for row in node.body:
                if isinstance(row, ast.ClassDef):
                    items = [
                        QtGui.QStandardItem(field.name)
                        for field in row.body if isinstance(field, ast.FunctionDef)

                    ]
                    self.model.appendRow(items)
                    func = [
                        QtGui.QStandardItem(par.arg)
                        for fun in row.body if isinstance(fun, ast.FunctionDef) for par in fun.args.args
                    ]
                    self.model.appendRow(func)


# def writeCsv(self, fileName):
#     with open(fileName, "w") as fileOutput:
#         writer = csv.writer(fileOutput)
#         for rowNumber in range(self.model.rowCount()):
#             fields = [
#                 self.model.data(
#                     self.model.index(rowNumber, columnNumber),
#                     QtCore.Qt.DisplayRole
#                 )
#                 for columnNumber in range(self.model.columnCount())
#             ]
#             writer.writerow(fields)

# @QtCore.pyqtSlot()
# def on_pushButtonWrite_clicked(self):
#     self.writeCsv(self.fileName)

# @QtCore.Slot()
# def on_pushButtonLoad_clicked(self):
#     self.loadCsv(self.fileName)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow("main.py")
    main.show()

    sys.exit(app.exec_())
