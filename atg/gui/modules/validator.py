# @Author: Administrator
# @Date:   19/05/2021 05:30
from PySide6.QtGui import Qt, QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit, QStyledItemDelegate
from PySide6.QtCore import QRegularExpression


class Delegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        w = QLineEdit(parent)
        regExp = QRegularExpression("[A-Za-z0-9\-\_\:\.]+")
        validator = QRegularExpressionValidator(regExp)
        w.setValidator(validator)
        return w

    def setEditorData(self, editor, index):
        text = index.data(Qt.EditRole) or index.data(Qt.DisplayRole)
        editor.setText(text)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
