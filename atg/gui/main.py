# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
import ast
import inspect
import sys
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from PySide6 import QtGui, QtWidgets

from modules import *
from widgets import *
from allpairspy import AllPairs

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

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        def testFn():
            sys.exit(app.exec_())

        widgets.btn_exit.clicked.connect(testFn)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = True
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

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
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        def show_info(functionNode):
            print("Function name:", functionNode.name)
            print("Args:")
            for arg in functionNode.args.args:
                # import pdb; pdb.set_trace()
                print("\tParameter name:", arg.arg)

        def is_static_method(klass, attr, value=None):
            """Test if a value of a class is static method.

            example::

                class MyClass(object):
                    @staticmethod
                    def method():
                        ...

            :param klass: the class
            :param attr: attribute name
            :param value: attribute value
            """
            if value is None:
                value = getattr(klass, attr)
            assert getattr(klass, attr) == value

            for cls in inspect.getmro(klass):
                if inspect.isroutine(value):
                    if attr in cls.__dict__:
                        binded_value = cls.__dict__[attr]
                        if isinstance(binded_value, staticmethod):
                            return True
            return False

        classes = False
        functions = False
        if btnName == "btn_save":
            name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            # file = open(name, 'r')
            try:
                with open(name[0]) as f:
                    node = ast.parse(f.read())
                functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
            except Exception as e:
                print(e)

        if classes:
            for i, cls in enumerate(classes):
                clsName = cls.name
                widgets.comboBox.setItemText(i,
                                             QCoreApplication.translate("MainWindow", u"{}".format(f'{clsName} (Cls)'),
                                                                        None))
                methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
                for method in methods:
                    # is_static_method(cls, method.name)
                    show_info(method)
        if functions:
            classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
            for i, cls in enumerate(classes):
                clsName = cls.name
                widgets.comboBox.setItemText(i,
                                             QCoreApplication.translate("MainWindow", u"{}".format(f'{clsName} (Cls)'),
                                                                        None))
                methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
                for method in methods:
                    # is_static_method(cls, method.name)
                    show_info(method)
            for f in functions:
                show_info(f)
        # PRINT BTN NAME
        # print(f'Button "{btnName}" pressed!')

    parameters = [
        ["Brand X", "Brand Y"],
        ["98", "NT", "2000", "XP"],
        ["Internal", "Modem"],
        ["Salaried", "Hourly", "Part-Time", "Contr."],
        [6, 10, 15, 30, 60],
    ]
    pairs = AllPairs(parameters)

    numcols = len(pairs[0])  # ( to get number of columns, count number of values in first row( first row is data[0]))

    numrows = len(pairs)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
