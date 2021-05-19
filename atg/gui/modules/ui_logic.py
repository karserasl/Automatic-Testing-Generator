# @Author: Administrator
# @Date:   19/05/2021 06:11
from PySide6.QtCore import QDir
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QFileDialog

import main
from gui.modules import UIFunctions


class UiLogic(main.MainWindow):
    def open_file_btn(self):
        name = QFileDialog.getOpenFileName(self, 'Open File', dir=QDir("../mockapp").absolutePath(),
                                           filter="Python file (*.py)")
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
        func_selected = str(self.ui.combo_functions.currentText())
        sel_func_params = self.core.get_params[func_selected]
        print(sel_func_params)  # TODO: Remove this
        if len(sel_func_params) > 2:
            # TODO: PAIRWISE
            pass
        self.populate_table(func_params_columns=sel_func_params)

    def populate_table(self, func_params_columns, pairwise_choices=None):
        # numrows = len(func_params)
        numcols = len(func_params_columns)
        self.ui.process_user_input_table.setColumnCount(numcols + 1)
        self.ui.process_user_input_table.setHorizontalHeaderLabels(
            [*(f'Input for "{f}" Variable' for f in func_params_columns),
             'Expected Output'])  # generator comprehensions

    def process_input_table(self):
        pass
