# @Author: Administrator
# @Date:   03/02/2021 14:26

from PySide6 import QtWidgets
import sys
import platform
from gui.modules import *
# from gui.modules import validator
from middleware import initializelogging
from middleware.core import ATG

# SET AS GLOBAL WIDGETS

widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SET AS GLOBAL WIDGETS

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.data = None
        self.core = ATG()
        self._pairwise = False
        self._result = None
        self._pw_ans = False
        # USE CUSTOM TITLE BAR

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME

        title = "ATG - Automatic Test Generator"
        description = "Automatic Test Generator for Python code."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU

        widgets.toggleButton.clicked.connect(lambda: FunctionsUi.toggle_menu(self, True))

        # SET UI DEFINITIONS

        FunctionsUi.funcs_ui_define(self)

        # SET UP VALIDATOR

        delegate = validator.Delegate(widgets.process_user_input_table)
        widgets.process_user_input_table.setItemDelegate(delegate)
        widgets.process_user_input_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # QTableWidget PARAMETERS

        widgets.process_user_input_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK

        enable_right_button = False
        enable_left_button = True
        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.button_click)
        widgets.btn_processing.clicked.connect(self.button_click)
        widgets.btn_output.clicked.connect(self.button_click)
        widgets.btn_save.clicked.connect(self.button_click)
        # SLIDE MENU
        widgets.github_btn.clicked.connect(self.github_btn)
        widgets.share_btn.clicked.connect(self.share_btn)
        # OPEN BUTTON
        widgets.open_btn.clicked.connect(self.open_file_btn)
        # TABLE BUTTONS
        widgets.new_row_btn.clicked.connect(self._add_row)
        widgets.remove_a_row.clicked.connect(self._remove_row)
        widgets.combo_functions.currentIndexChanged.connect(self.create_table_input)
        widgets.reset_table.clicked.connect(self.reset_table)
        # INFO BUTTON
        widgets.processing_info_btn.clicked.connect(self._information_btn)
        # NEXT BUTTON
        widgets.process_next_btn.clicked.connect(self.process_input_table)

        # EXTRA LEFT BOX
        def left_slide_open_close():
            FunctionsUi.toggle_left_slide(self, True)

        if enable_left_button:
            widgets.toggle_left_slide.clicked.connect(left_slide_open_close)
            widgets.extraCloseColumnBtn.clicked.connect(left_slide_open_close)

            widgets.btn_exit.clicked.connect(QApplication.quit)
        else:
            widgets.toggle_left_slide.hide()
            widgets.toggle_left_slide.setEnabled(False)
            widgets.extraCloseColumnBtn.hide()
            widgets.extraCloseColumnBtn.setEnabled(False)

        # EXTRA RIGHT BOX
        def right_slide_open_close():
            FunctionsUi.toggle_right_slide(self, False)

        if enable_right_button:
            widgets.settingsTopBtn.clicked.connect(right_slide_open_close)
        else:
            widgets.settingsTopBtn.hide()
            widgets.settingsTopBtn.setEnabled(False)
        # SHOW APP

        self.show()

        # SET CUSTOM THEME

        use_custom_theme = True
        theme_file = "gui/themes/light.qss"

        # SET THEME AND HACKS
        if use_custom_theme:
            # LOAD AND APPLY STYLE
            FunctionsUi.theme(self, theme_file, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(FunctionsUi.select_menu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK
    def github_btn(self):
        url = QUrl('https://github.com/karserasl/Automatic-Testing-Generator')
        QDesktopServices.openUrl(url)

    def share_btn(self):
        url = QUrl('https://twitter.com/intent/tweet?text=Automatic Test Generator in Python with PyQT!')
        QDesktopServices.openUrl(url)

    def button_click(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btn_name = btn.objectName()

        # SHOW HOME PAGE
        if btn_name == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            FunctionsUi.reset_styling(self, btn_name)
            btn.setStyleSheet(FunctionsUi.select_menu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btn_name == "btn_processing":
            widgets.stackedWidget.setCurrentWidget(widgets.processing)
            FunctionsUi.reset_styling(self, btn_name)
            btn.setStyleSheet(FunctionsUi.select_menu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btn_name == "btn_output":
            widgets.stackedWidget.setCurrentWidget(widgets.finalize)  # SET PAGE
            FunctionsUi.reset_styling(self, btn_name)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(FunctionsUi.select_menu(btn.styleSheet()))  # SELECT MENU

        if btn_name == "btn_save":
            output_txt = widgets.output_text.toPlainText()
            if output_txt:
                if widgets.append_checkbox.isChecked():
                    self.core.dump_output(output_txt, append=True)
                else:
                    self.core.dump_output(output_txt)

    # TABLE ADD/REMOVE BUTTONS
    def _add_row(self):
        rowCount = widgets.process_user_input_table.rowCount()
        widgets.process_user_input_table.insertRow(rowCount)

    def _remove_row(self):
        if widgets.process_user_input_table.rowCount() > 0:
            widgets.process_user_input_table.removeRow(widgets.process_user_input_table.rowCount() - 1)

    def _information_btn(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Information')
        msg.setText("""
        * The table below is populated with the names of variables from
            the selected function as its headers.
        * The columns are the inputs to that specific variable.
        * If the ATG detects that the selected function has 3 or more variables, 
            it will enable the pairwise algorithm.
        * Special symbols allowed are: " . : - ". Only 1 symbol per input allowed.
        """)
        msg.setInformativeText("""
        LIMITATIONS:
        1. Accepting only strings or integers.
        2. Boundary Value Analysis is happening only
            when the selected function has a single variable.
        3. Pairwise is happening only on 3 or more variables.
        """)
        msg.exec_()

    # RESIZE EVENTS

    def resizeEvent(self, event):
        # Update Size Grips
        FunctionsUi.resize_edges(self)

    # MOUSE CLICK EVENTS

    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    # UI LOGIC

    def open_file_btn(self):
        UiLogic.open_file_btn(self)

    def create_combo_box_items(self):
        UiLogic.create_combo_box_items(self)

    def create_table_input(self):
        UiLogic.create_table_input(self)

    def populate_table(self, func_params_columns, pairwise_results=None):
        UiLogic.populate_table(self, func_params_columns, pairwise_results=None)

    def process_input_table(self):
        UiLogic.process_input_table(self)

    def dump_output_helper(self):
        UiLogic.dump_output_helper(self)

    def reset_table(self):
        UiLogic.reset_table(self)


if __name__ == '__main__':
    initializelogging.setup_logging()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("gui/icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
