# import sys
# import maya.cmds as cmds
import maya.OpenMayaUI as mui  # type: ignore
from PySide2 import QtCore, \
    QtWidgets\
    # QtGui,
import shiboken2
import json
from pathlib import Path
# import importlib


def mayaMainWindow():
    mainWindowPtr = mui.MQtUtil.mainWindow()
    return (shiboken2.wrapInstance(int(mainWindowPtr), QtWidgets.QWidget))


class MainWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(MainWin, self).__init__(parent)

        # windowns setting
        self.setWindowTitle("type extention list")
        self.setMinimumWidth(290)
        self.setMinimumHeight(320)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        # dictionary
        self.type_dic = {}
        self.line_dic = {}

        # init functions
        self.fill_dic()
        self.create_ui()

    def line_edit_func(self, identifier):
        dic = self.line_dic[identifier]
        line = dic['lineEdit']

        self.type_dic[identifier] = line.text()
        print(line.text())

    def write_func(self):
        path = 'D:/K.Work/git/auto_rig/ressources/type_dictionary.json'

        control_shape_file = open(Path(path), 'w')

        json.dump(self.type_dic, control_shape_file, indent=4)

    def fill_dic(self):
        path = 'D:/K.Work/git/auto_rig/ressources/type_dictionary.json'

        control_shape_file = open(Path(path))

        self.type_dic = json.load(control_shape_file)

    # widgets
    def create_ui(self):
        # create layouts ad widgets
        self.type_layout = QtWidgets.QVBoxLayout(self)

        self.main_widget = QtWidgets.QWidget(self)

        self.scroll_area = QtWidgets.QScrollArea(self)

        # type dictionary loop
        for ob_type in self.type_dic:
            # create line dictionary
            identifier = ob_type
            label = QtWidgets.QLabel(ob_type)
            line = QtWidgets.QLineEdit(self.type_dic[ob_type])

            # add entry
            self.line_dic[identifier] = {
                'label': label,
                'lineEdit': line,
                'func': lambda check=None, a=identifier: self.line_edit_func(a)
            }

        # create widgets
        for widget in self.line_dic:
            # open line dictionary
            button_dic = self.line_dic[widget]
            label = button_dic['label']
            line = button_dic['lineEdit']

            # define connect
            line.returnPressed.connect(button_dic['func'])

            # create layout
            layout = QtWidgets.QHBoxLayout(self)

            layout.addWidget(label)
            layout.addWidget(line)

            # add layout to main type layout
            self.type_layout.addLayout(layout)

        # set and add close button to close button layout
        self.close_button = QtWidgets.QPushButton('write extentions')
        self.close_button.clicked.connect(self.write_func)
        self.type_layout.addWidget(self.close_button)

        # add type layout to the type widget
        self.main_widget.setLayout(self.type_layout)

        # add scroll area
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_widget)


##############################################################################
# test ui
##############################################################################

d = MainWin()
d.show()
