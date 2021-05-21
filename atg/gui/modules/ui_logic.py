# @Author: Administrator
# @Date:   19/05/2021 06:11
import re

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QDir
from PySide6.QtGui import QStandardItemModel, QStandardItem

import main
from gui.modules import FunctionsUi


class UiLogic(main.MainWindow):
    def open_file_btn(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', dir=QDir("../mockapp").absolutePath(),
                                                     filter="Python file (*.py)")
        if not name[0]: return
        self.core.analyse_file(name[0])
        self.data = self.core.get_data
        if self.core.check_if_exists():
            final_lbl = self.ui.final_label.text()
            new_final_lbl = f'{final_lbl}\nFound ATG config file in directory and loaded previously choices'
            self.ui.final_label.setText(new_final_lbl)
            self.dump_output_helper()
            self.create_combo_box_items()
            return

        if self.data and isinstance(self.data, dict):
            self.ui.path_line.setText(name[0])
            self.ui.stackedWidget.setCurrentWidget(self.ui.processing)
            FunctionsUi.reset_styling(self, "btn_processing")
            self.ui.btn_processing.setStyleSheet(FunctionsUi.select_menu(self.ui.btn_processing.styleSheet()))
            self.create_combo_box_items()

        else:
            self.ui.error_msg_label.setText(
                'Please select a Python File that has Classes with methods or functions, and they have some arguments')

    def create_combo_box_items(self):
        model = QStandardItemModel()
        self.ui.combo_classes.setModel(model)
        self.ui.combo_functions.setModel(model)
        for k, v in self.data.items():
            cls = QStandardItem(k)
            model.appendRow(cls)
            for value in v:
                func = QStandardItem(value)
                cls.appendRow(func)

        def update_combo_box(index):
            ind = model.index(index, 0, self.ui.combo_classes.rootModelIndex())
            self.ui.combo_functions.setRootModelIndex(ind)
            self.ui.combo_functions.show()
            self.ui.combo_functions.setCurrentIndex(0)

        self.ui.combo_classes.currentIndexChanged.connect(update_combo_box)

    def create_table_input(self):
        # Enable the edit on the table
        if self.ui.pairwise_check.isChecked():
            self.ui.pairwise_check.setChecked(False)
        self.ui.proc_error_label.setText('')
        self.ui.process_user_input_table.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.EditKeyPressed | QtWidgets.QAbstractItemView.AnyKeyPressed)
        func_selected = str(self.ui.combo_functions.currentText())
        cls_selected = str(self.ui.combo_classes.currentText())
        self.core.set_sel_function(func_selected)
        self.core.set_sel_cls(cls_selected)
        self._sel_func_params = self.core.get_params[func_selected]
        self.ui.process_user_input_table.clear()

        if len(self._sel_func_params) > 2:
            self._pairwise = True
            self.ui.pairwise_check.setChecked(True)
            self.ui.proc_error_label.setText(
                'Pairwise activated since more than 2 variables detected for the selected function')
            self.ui.invalid_choice.setEnabled(False)
            self.ui.invalid_choice.hide()
            self.ui.process_next_btn.setText('Process Pairwise')
        else:
            self._pairwise = False
            self.ui.invalid_choice.setEnabled(True)
            self.ui.invalid_choice.show()
            self.ui.process_next_btn.setText('Next')

        self.populate_table(func_params_columns=self._sel_func_params)

    def populate_table(self, func_params_columns, pairwise_results=None):
        pairwise_results = self._result

        num_cols = len(func_params_columns)
        if self._pairwise:
            self.ui.process_user_input_table.setColumnCount(num_cols)
            self.ui.process_user_input_table.setHorizontalHeaderLabels(
                [*(f'Input for "{f}" Variable' for f in func_params_columns)])
        else:
            self.ui.process_user_input_table.setColumnCount(num_cols + 1)
            self.ui.process_user_input_table.setHorizontalHeaderLabels(
                [*(f'Input for "{f}" Variable' for f in func_params_columns),
                 'Expected Output'])  # generator comprehensions
        if pairwise_results:
            num_rows = len(pairwise_results)
            self.ui.process_user_input_table.setRowCount(num_rows)
            # Loops to add values into QTableWidget
            for row in range(num_rows):
                for column in range(num_cols):
                    if isinstance(pairwise_results[row][column], int):
                        self.ui.process_user_input_table.setItem(row, column, QtWidgets.QTableWidgetItem(
                            str(pairwise_results[row][column])))
                    else:
                        self.ui.process_user_input_table.setItem(row, column, QtWidgets.QTableWidgetItem(
                            (pairwise_results[row][column])))

    def process_input_table(self):
        self.ui.proc_error_label.setText('')
        self.ui.output_text.clear()

        def error_dialog(msg):
            dlg = QtWidgets.QMessageBox(self)
            dlg.setIcon(QtWidgets.QMessageBox.Critical)
            dlg.setWindowModality(QtCore.Qt.WindowModal)
            dlg.setWindowTitle("ERROR")
            dlg.setText(msg)
            dlg.exec()

        def validator(text):

            if not re.fullmatch(r'^[a-zA-Z0-9\-.: ]*', text.strip()):
                error_dialog('Please check your inputs!')
                return True
            if re.search(r'[\-.:]{2,}', text):
                error_dialog('No more than 1 special symbol permitted')
                return True
            if '-' in text:
                try:
                    t = list(map(int, text.split('-')))
                    if t[0] > t[1]:
                        error_dialog('Please correct the ranges. It should be in ascending order!')
                        return True
                except ValueError as e:
                    self.ui.proc_error_label.setText(f'Error: {e}')
                    return

            return False

        inv_choice = self.ui.invalid_choice.text()
        cols = self.ui.process_user_input_table.columnCount()
        rows = self.ui.process_user_input_table.rowCount()
        outputs = []
        if self._pairwise:
            for col in range(cols):
                list_of_ans = []
                for row in range(rows):
                    item = self.ui.process_user_input_table.item(row, col)
                    if item and item.text():
                        list_of_ans.append(item.text().strip())
                        if validator(item.text()):
                            return
                outputs.append(list_of_ans)
        else:
            for row in range(rows):
                list_of_ans = []
                range_ans = False

                for col in range(cols):
                    item = self.ui.process_user_input_table.item(row, col)
                    if item and item.text():
                        list_of_ans.append(item.text().strip())
                        if validator(item.text()):
                            return
                        if '-' in item.text():
                            range_ans = True

                if list_of_ans:
                    if len(list_of_ans) != cols and not self._pairwise:
                        error_dialog('Please fill all the inputs and answer in a row!')
                        return
                    if len(list_of_ans) <= 2 and range_ans and not self._pairwise and not inv_choice:
                        error_dialog('Range input detected but did not provide an invalid choice!')
                        return

                    outputs.append(list_of_ans)
        if not outputs:
            self.ui.proc_error_label.setText('Please Fill at least 1 row!')
            return
        if sum([len(i) for i in outputs]) < 6 and self._pairwise:
            error_dialog('Need to provide more inputs for Pairwise algorithm to make sense!')
            return
        if any('-' in x for j in outputs for x in j) and max([len(a) for a in outputs]) > 2:
            error_dialog(
                'LIMITATION: Not able to process more than 1 BVA variable per function!\nOnly Equivalence Partitioning will run')

        self._result = self.core.run(outputs=outputs, inv_choice=inv_choice, pairwise=self._pairwise,
                                     pw_ans=self._pw_ans)
        print(outputs)
        print(self._result)
        print(self._pairwise)
        if isinstance(self._result, list) and self._result and self._pairwise:
            self._pairwise = False
            self._pw_ans = True
            self.populate_table(func_params_columns=self._sel_func_params, pairwise_results=self._result)
            return
        if not self._pairwise:
            self._pw_ans = False
            self.dump_output_helper()

    def dump_output_helper(self):
        self.core.dump()
        dumped_tests, count_tests = self.core.get_generator_dump
        if dumped_tests:
            self.ui.output_text.insertPlainText(dumped_tests)
            if not count_tests:
                self.ui.info_count_label.setText('')
            else:
                self.ui.info_count_label.setText(f'Number of Tests Generated: {str(count_tests)}')

            self.ui.stackedWidget.setCurrentWidget(self.ui.finalize)
            FunctionsUi.reset_styling(self, "btn_output")
            self.ui.btn_output.setStyleSheet(FunctionsUi.select_menu(self.ui.btn_output.styleSheet()))
