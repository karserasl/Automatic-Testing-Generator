# @Author: Administrator
# @Date:   19/05/2021 05:30
from PySide6.QtGui import Qt, QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit, QStyledItemDelegate
from PySide6 import QtCore


class Delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = None

    # def createEditor(self, parent, option, index):
    # self.editor = QLineEdit(parent)
    # regExp = QtCore.QRegularExpression("[A-Za-z0-9\-\_\:\.]+")
    # validator = QRegularExpressionValidator(regExp)
    # self.editor.setValidator(validator)
    # return self.editor

    # def eventFilter(self, target, event):
    #     if event.type() == QtCore.QEvent.KeyPress:
    #         key = event.key()
    #         if key == QtCore.Qt.Key_Backspace:
    #             self.editor.setText(self.editor.text()[:-1])
    #             return True
    #         if key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
    #             self.editor.
    #             return True
    #     return False

    def setEditorData(self, editor, index):
        text = index.data(Qt.EditRole) or index.data(Qt.DisplayRole)
        editor.setText(text)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
