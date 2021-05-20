# @Author: Administrator
# @Date:   19/05/2021 06:11
from PySide6.QtCore import QDir, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6 import QtWidgets, QtCore

import main
from gui.modules import UIFunctions


class UiLogic(main.MainWindow):
    def open_file_btn(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', dir=QDir("../mockapp").absolutePath(),
                                                     filter="Python file (*.py)")
        if not name[0]: return
        self.core.analyse_file(name[0])

        # TODO: Handle the case that .atg_config file exists (Re-running the app)
        if self.core.check_if_exists():
            return NotImplementedError

        self.data = self.core.get_data

        if self.data and isinstance(self.data, dict):
            self.ui.path_line.setText(name[0])
            self.ui.stackedWidget.setCurrentWidget(self.ui.processing)
            UIFunctions.resetStyle(self, "btn_processing")
            self.ui.btn_processing.setStyleSheet(UIFunctions.selectMenu(self.ui.btn_processing.styleSheet()))
            self.create_combo_box_items()

            print(self.data)  # TODO: Remove this
        else:
            self.ui.error_msg_label.setText(
                'Please select a Python File that has Classes with methods or functions, and they have some arguments')

    def create_combo_box_items(self):
        self.model = QStandardItemModel()
        self.ui.combo_functions.setModel(self.model)
        self.ui.combo_classes.setModel(self.model)

        def update_combo_box(index):
            ind = self.model.index(index, 0, self.ui.combo_classes.rootModelIndex())
            self.ui.combo_functions.setRootModelIndex(ind)
            self.ui.combo_functions.setCurrentIndex(0)

        self.ui.combo_classes.currentIndexChanged.connect(update_combo_box)
        update_combo_box(0)

        for k, v in self.data.items():
            cls = QStandardItem(k)
            self.model.appendRow(cls)
            for value in v:
                func = QStandardItem(value)
                cls.appendRow(func)

    def create_table_input(self):
        # Enable the edit on the table
        self.ui.process_user_input_table.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.EditKeyPressed | QtWidgets.QAbstractItemView.AnyKeyPressed)
        func_selected = str(self.ui.combo_functions.currentText())
        sel_func_params = self.core.get_params[func_selected]
        self.ui.process_user_input_table.clear()
        print(sel_func_params)  # TODO: Remove this
        if len(sel_func_params) > 2:
            # TODO: PAIRWISE
            pass
        self.populate_table(func_params_columns=sel_func_params)

    def populate_table(self, func_params_columns, pairwise=False):
        # numrows = len(func_params)
        numcols = len(func_params_columns)
        self.ui.process_user_input_table.setColumnCount(numcols + 1)
        self.ui.process_user_input_table.setHorizontalHeaderLabels(
            [*(f'Input for "{f}" Variable' for f in func_params_columns),
             'Expected Output'])  # generator comprehensions

    def process_input_table(self, pairwise=False):
        self.ui.proc_error_label.setText('')

        def error_dialog(msg):
            dlg = QtWidgets.QMessageBox(self)
            dlg.setIcon(QtWidgets.QMessageBox.Critical)
            dlg.setWindowModality(QtCore.Qt.WindowModal)
            dlg.setWindowTitle("ERROR")
            dlg.setText(msg)
            dlg.exec()

        def validator(text):
            if '-' in text:
                print(text)
                t = list(map(int, text.split('-')))
                if t[0] > t[1]:
                    error_dialog('Please correct the ranges. It should be in ascending order!')
                    return True

                if not inv_choice:
                    error_dialog('Range input detected but did not provide an invalid choice!')
                    return True

        answers_column = self.ui.process_user_input_table.columnCount() - 1
        inv_choice = self.ui.invalid_choice.text()
        cols = self.ui.process_user_input_table.columnCount()
        rows = self.ui.process_user_input_table.rowCount()
        outputs = []
        for row in range(rows):
            list_of_ans = []
            range_ans = False

            for col in range(cols):
                item = self.ui.process_user_input_table.item(row, col)
                if item and item.text():
                    list_of_ans.append(item.text())
                    if validator(item.text()):
                        return
                    if '-' in item.text():
                        range_ans = True

            if list_of_ans:
                if len(list_of_ans) != cols:
                    error_dialog('Please fill all the inputs and answer in a row!')
                    return
                if len(list_of_ans) > 2 and range_ans:
                    error_dialog(
                        'LIMITATION: Not able to process more than 1 BVA variable per function!\nOnly Equivalence Partitioning will run')
                outputs.append(list_of_ans)
        if not outputs:
            self.ui.proc_error_label.setText('Please Fill at least 1 row!')
            return

        result = self.core.run(outputs=outputs, inv_choice=inv_choice, pairwise=pairwise)

        if result:
            self.ui.stackedWidget.setCurrentWidget(self.ui.finalize)
            UIFunctions.resetStyle(self, "btn_output")
            self.ui.btn_output.setStyleSheet(UIFunctions.selectMenu(self.ui.btn_output.styleSheet()))
