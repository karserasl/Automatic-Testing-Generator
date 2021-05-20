import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

import main


# WITH ACCESS TO MAIN WINDOW WIDGETS

class AppFunctions(main.MainWindow):
    def setThemeHack(self):
        main.Settings.BTN_LEFT_BOX_COLOR = "background-color: #495474;"
        main.Settings.BTN_RIGHT_BOX_COLOR = "background-color: #495474;"
        main.Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
        background-color: #566388;
        """

        cwd = os.getcwd()
        print(cwd)
        # SET MANUAL STYLES
        self.ui.logo_label.setPixmap(QPixmap(f"{cwd}/gui/images/images/PythonLogoPNG.png"))
        self.ui.proc_error_label.setStyleSheet("color: #6272A4; font: 13pt 'Segoe UI';")
        self.ui.proc_error_label.setAlignment(Qt.AlignCenter)
        self.ui.path_line.setStyleSheet("background-color: #6272a4;")
        self.ui.open_btn.setStyleSheet("background-color: #6272a4;")
        self.ui.process_next_btn.setStyleSheet("background-color: #6272a4;")
        self.ui.new_row_btn.setStyleSheet("background-color: #6272a4;")
        self.ui.remove_a_row.setStyleSheet("background-color: #6272a4;")
        self.ui.output_text.setStyleSheet("background-color: #6272a4;")
        self.ui.process_user_input_table.setStyleSheet(
            "QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.combo_functions.setStyleSheet("background-color: #6272a4;")
        self.ui.combo_classes.setStyleSheet("background-color: #6272a4;")
        # self.ui.scrollArea.setStyleSheet(
        #     "QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        # self.ui.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        # self.ui.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        # self.ui.commandLinkButton.setStyleSheet("color: #ff79c6;")
