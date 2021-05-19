# @Author: Administrator
# @Date:   19/05/2021 05:30
from PySide6.QtWidgets import QItemDelegate, QLineEdit


class TableValidator(QItemDelegate):
    def createEditor(self, parent, option, index):
        w = QLineEdit(parent)
        w.setInputMask("HH")
        return w
