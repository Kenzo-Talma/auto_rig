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
        self.edgeloop1 = None
        self.edgeloop2 = None
        self.setWindowTitle("Ribbon maker")
        # self.setMinimumWidth(200)
        # self.setMaximumWidth(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.setGeometry(200, 500, 400, 300)

        self.tool_box = QtWidgets.QToolBox(self)
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.type_dic = {}

        self.fill_dic()
        self.createWidget()

    def click_method(self, identifier):
        dic = self.widgets[identifier]
        line = dic['lineEdit']

        self.type_dic[identifier] = line.text()
        print(line.text)

    def close_func(self):
        path = 'D:/K.Work/git/auto_rig/ressources/type_dictionary.json'

        control_shape_file = open(Path(path))

        json.dump(self.type_dic, control_shape_file, indent=4)

    def fill_dic(self):
        path = 'D:/K.Work/git/auto_rig/ressources/type_dictionary.json'

        control_shape_file = open(Path(path))

        self.type_dic = json.load(control_shape_file)

    # widgets
    def createWidget(self):
        self.mainLayout.addWidget(self.tool_box)

        self.widgets = {}
        for ob_type in self.type_dic:
            identifier = ob_type
            label = QtWidgets.QLabel(ob_type)
            line = QtWidgets.QLineEdit(ob_type)
            self.widgets[identifier] = {
                'label': label,
                'lineEdit': line,
                'func': lambda check=None, a=identifier: self.click_method(a)
            }

        for widget in self.widgets:
            button_dic = self.widgets[widget]
            label = button_dic['label']
            line = button_dic['lineEdit']
            line.textEdited.connect(button_dic['func'])

            # self.mainLayout.addWidget(label)
            # self.mainLayout.addWidget(line)

            self.tool_box.addItem(label, widget)
            self.tool_box.insertItem(line, widget)

        self.close_button = QtWidgets.QPushButton('close')
        self.close_button.clicked.connect(self.close_func)
        # self.mainLayout.addWidget(self.close_button)
        self.tool_box.addItem(self.close_button, 'close')


##############################################################################
# test ui
##############################################################################

d = MainWin()
d.show()
