# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
import sys
import platform

# from PySide6 import QtWidgets

from gui.modules import *
from gui.widgets import *
from core.core import check

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "ATG - Automatic Test Generator"
        description = "Automatic Test Generator for Python code."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
        enable_right_button = False
        enable_left_button = True
        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.pushButton_5.clicked.connect(self.open_file_btn)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        if enable_left_button:
            widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
            widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

            widgets.btn_exit.clicked.connect(QApplication.quit)
        else:
            widgets.toggleLeftBox.hide()
            widgets.toggleLeftBox.setEnabled(False)
            widgets.extraCloseColumnBtn.hide()
            widgets.extraCloseColumnBtn.setEnabled(False)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, False)

        if enable_right_button:
            widgets.settingsTopBtn.clicked.connect(openCloseRightBox)
        else:
            widgets.settingsTopBtn.hide()
            widgets.settingsTopBtn.setEnabled(False)
        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        use_custom_theme = True
        theme_file = "themes/py_dracula_light.qss"

        # SET THEME AND HACKS
        if use_custom_theme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, theme_file, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btn_name = btn.objectName()

        # SHOW HOME PAGE
        if btn_name == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btn_name)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btn_name == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btn_name)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btn_name == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
            UIFunctions.resetStyle(self, btn_name)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        if btn_name == "btn_save":
            print('saved button pressed !')
            pass

        # PRINT BTN NAME
        # print(f'Button "{btn_name}" pressed!')

    # OPEN BUTTON
    # ///////////////////////////////////////////////////////////////
    def open_file_btn(self):
        name = QFileDialog.getOpenFileName(self, 'Open File', filter="Python file (*.py)")
        widgets.lineEdit_5.setText(name[0])
        widgets.stackedWidget.setCurrentWidget(widgets.widgets)
        UIFunctions.resetStyle(self, "btn_widgets")
        widgets.btn_widgets.setStyleSheet(UIFunctions.selectMenu(widgets.btn_widgets.styleSheet()))
        data = check(name[0], widgets)
        self.create_combo_box_items(data)
        print(data)

    def create_combo_box_items(self, data):
        self.model = QStandardItemModel()
        widgets.comboBox.setModel(self.model)
        widgets.comboBox_2.setModel(self.model)

        for k, v in data.items():
            cls = QStandardItem(k)
            self.model.appendRow(cls)
            for value in v:
                func = QStandardItem(value)
                cls.appendRow(func)
        widgets.comboBox_2.currentIndexChanged.connect(self.update_combo_box)
        self.update_combo_box(0)

    def update_combo_box(self, index):
        ind = self.model.index(index, 0, widgets.comboBox_2.rootModelIndex())
        widgets.comboBox.setRootModelIndex(ind)
        widgets.comboBox.setCurrentIndex(0)

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()
    #
    #     # PRINT MOUSE EVENTS
    #     if event.buttons() == Qt.LeftButton:
    #         print('Mouse click: LEFT CLICK')
    #     if event.buttons() == Qt.RightButton:
    #         print('Mouse click: RIGHT CLICK')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
