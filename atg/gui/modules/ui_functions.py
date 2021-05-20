# MAIN FILE

import logging

logger = logging.getLogger(__name__)

from main import *

# GLOBALS

from gui.widgets import CustomGrip

GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True


class FunctionsUi(MainWindow):
    def __init__(self):
        self.left_edge = None
        self.right_edge = None
        self.top_edge = None
        self.bottom_edge = None
        self.left_slide = None
        self.right_slide = None
        self.animation = None
        self.sizegrip = None
        self.shadow = None

    # MAXIMIZE/RESTORE
    
    def maximize_restore(self):
        global GLOBAL_STATE
        if not self.isMaximized():
            self.showMaximized()
            GLOBAL_STATE = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            self.ui.frame_size_grip.hide()
            self.left_edge.hide()
            self.right_edge.hide()
            self.top_edge.hide()
            self.bottom_edge.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            self.ui.frame_size_grip.show()
            self.left_edge.show()
            self.right_edge.show()
            self.top_edge.show()
            self.bottom_edge.show()

    # RETURN STATUS
    
    @staticmethod
    def return_global():
        return GLOBAL_STATE

    # SET STATUS
    
    @staticmethod
    def set_status(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU
    
    def toggle_menu(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.leftMenuBg.width()
            max_extend = Settings.MENU_WIDTH
            standard = 60

            # SET MAX WIDTH
            if width == 60:
                width_extended = max_extend
            else:
                width_extended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")
            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(width_extended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    # TOGGLE LEFT BOX
    
    def toggle_left_slide(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraLeftBox.width()
            widthRightBox = self.ui.extraRightBox.width()
            maxExtend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.toggle_left_slide.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.toggle_left_slide.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = self.ui.settingsTopBtn.styleSheet()
                    self.ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.toggle_left_slide.setStyleSheet(style.replace(color, ''))

        FunctionsUi.start_box_animation(self, width, widthRightBox, "left")

    # TOGGLE RIGHT BOX
    
    def toggle_right_slide(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraRightBox.width()
            widthLeftBox = self.ui.extraLeftBox.width()
            maxExtend = Settings.RIGHT_BOX_WIDTH
            color = Settings.BTN_RIGHT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.settingsTopBtn.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.settingsTopBtn.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = self.ui.toggle_left_slide.styleSheet()
                    self.ui.toggle_left_slide.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.settingsTopBtn.setStyleSheet(style.replace(color, ''))

            FunctionsUi.start_box_animation(self, widthLeftBox, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 240
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 240
        else:
            right_width = 0

            # ANIMATION LEFT BOX
        self.left_slide = QPropertyAnimation(self.ui.extraLeftBox, b"minimumWidth")
        self.left_slide.setDuration(Settings.TIME_ANIMATION)
        self.left_slide.setStartValue(left_box_width)
        self.left_slide.setEndValue(left_width)
        self.left_slide.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX
        self.right_slide = QPropertyAnimation(self.ui.extraRightBox, b"minimumWidth")
        self.right_slide.setDuration(Settings.TIME_ANIMATION)
        self.right_slide.setStartValue(right_box_width)
        self.right_slide.setEndValue(right_width)
        self.right_slide.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.grp_animation = QParallelAnimationGroup()
        self.grp_animation.addAnimation(self.left_slide)
        self.grp_animation.addAnimation(self.right_slide)
        self.grp_animation.start()

    # SELECT/DESELECT MENU
    
    # SELECT
    def select_menu(self):
        select = self + Settings.MENU_SELECTED_STYLESHEET
        return select

    # DESELECT
    def deselect_menu(self):
        deselect = self.replace(Settings.MENU_SELECTED_STYLESHEET, "")
        return deselect

    # START SELECTION
    def select_button_menu(self, widget):
        for btn in self.ui.topMenu.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.setStyleSheet(FunctionsUi.select_menu(btn.styleSheet()))

    # RESET SELECTION
    def reset_styling(self, widget):
        for btn in self.ui.topMenu.findChildren(QPushButton):
            if btn.objectName() != widget:
                btn.setStyleSheet(FunctionsUi.deselect_menu(btn.styleSheet()))

    # IMPORT THEMES FILES QSS/CSS
    
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            try:
                with open(file, 'r') as f:
                    style_file = f.read()
                self.ui.styleSheet.setStyleSheet(style_file)
            except Exception as e:
                logger.error(f'Error reading style file :: {e}')

    # GUI FUNCTIONS DEFINITIONS
    
    def funcs_ui_define(self):
        def double_click_maximize(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: FunctionsUi.maximize_restore(self))

        self.ui.titleRightInfo.mouseDoubleClickEvent = double_click_maximize

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def move_window(event):

                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()

            self.ui.titleRightInfo.mouseMoveEvent = move_window

            # CUSTOM GRIPS
            self.left_edge = CustomGrip(self, Qt.LeftEdge, True)
            self.right_edge = CustomGrip(self, Qt.RightEdge, True)
            self.top_edge = CustomGrip(self, Qt.TopEdge, True)
            self.bottom_edge = CustomGrip(self, Qt.BottomEdge, True)

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.maximizeRestoreAppBtn.hide()
            self.ui.closeAppBtn.hide()
            self.ui.frame_size_grip.hide()

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self.ui.maximizeRestoreAppBtn.clicked.connect(lambda: FunctionsUi.maximize_restore(self))

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

    def resize_edges(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_edge.setGeometry(0, 10, 10, self.height())
            self.right_edge.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_edge.setGeometry(0, 0, self.width(), 10)
            self.bottom_edge.setGeometry(0, self.height() - 10, self.width(), 10)
