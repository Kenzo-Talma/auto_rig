# import sys
# import maya.cmds as cmds
import maya.OpenMayaUI as mui  # type: ignore
from PySide2 import QtCore, \
    QtWidgets\
    # QtGui,
import shiboken2
# import importlib
# from modules.module_reader import Reader_Module


def maya_main_window():
    main_window_port = mui.MQtUtil.mainWindow()
    return (shiboken2.wrapInstance(int(main_window_port), QtWidgets.QWidget))


class Module_Win(QtWidgets.QDialog):

    def __init__(self, module, parent=maya_main_window()):
        # super method
        super(Module_Win, self).__init__(parent)

        # windowns setting
        self.setWindowTitle("type extention list")
        self.setMinimumWidth(290)
        self.setMinimumHeight(320)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        # init functions
        # test
        self.module_info = {
            'inputs': {
                'data_input': None,
                'space_input_type': list,
                'space_input': ['test1', 'test2', 'test3']
            },
            'outputs': {
                'data_ouput': None,
                'space_ouput_type': None,
                'space_ouput': None
            }
        }
        # self.module_info = self.module_read(module)
        self.create_ui()

    def create_ui(self):
        # create layouts add widgets
        self.main_widget = QtWidgets.QWidget(self)

        self.main_layout = QtWidgets.QVBoxLayout(self)

        # self.scroll_area = QtWidgets.QScrollArea(self)

        # add input
        input_dic = self.module_info['inputs']

        # add space input
        space_input_type = input_dic['space_input_type']
        self.space_input = input_dic['space_input']

        if space_input_type == list:
            self.space_input_index = 0
            space_input_ui = self.create_list_ui(len(self.space_input))

        self.main_layout.addWidget(space_input_ui)

        # add main layout to main widget
        self.main_widget.setLayout(self.main_layout)

    def create_list_ui(self, input_number):
        # create list layout
        list_layout = QtWidgets.QVBoxLayout(self)
        button_layout = QtWidgets.QVBoxLayout(self)
        input_layout = QtWidgets.QVBoxLayout(self)

        # create input widget
        input_widget = QtWidgets.QWidget(self)

        # create scroll area
        input_scroll_area = QtWidgets.QScrollArea(self)
        input_scroll_area.setWidgetResizable(True)

        # create dic
        for i in range(input_number-1):
            self.add_space_input_func(
                list_layout,
                f'space input {self.space_input_index}'
            )

        # create add button
        add_line_button = QtWidgets.QPushButton('add space input')
        add_line_button.clicked.connect(
            lambda check=None,
            layout=list_layout,
            attribute=f'space input {self.space_input_index}':
            self.add_space_input_func(
                layout=layout,
                attribute=attribute
            )
        )

        button_layout.addWidget(add_line_button)

        # add to input layout
        input_layout.addLayout(list_layout)
        input_layout.addLayout(button_layout)

        # add to input widget
        input_widget.setLayout(input_layout)

        # add to input scroll area
        input_scroll_area.setWidget(input_widget)

        # return layout
        return input_scroll_area

    # def create_dic_ui(self):

    def module_read(self, module):
        # create reader object
        # self.reader_module = Reader_Module(module)

        # get data
        self.reader_module.get_space_input
        self.reader_module.get_space_output

        # return info dictionnary
        return {
            'inputs': {
                'data_input': self.reader_module.data_input,
                'space_input_type': self.reader_module.space_input_type,
                'space_input': self.reader_module.space_input
            },
            'outputs': {
                'data_ouput': self.reader_module.data_output,
                'space_ouput_type': self.reader_module.space_output_type,
                'space_ouput': self.reader_module.space_output
            }
        }

    def get_data(self, data):
        print('ok')

    def add_space_input_func(self, layout, attribute):
        # open line dictionnary
        button = QtWidgets.QPushButton(
            f'get {attribute}'
        )

        # create layout
        line_layout = QtWidgets.QHBoxLayout(self)

        # connect button
        button.clicked.connect(self.get_data)

        # create name
        name = QtWidgets.QLabel(attribute)
        name.setFrameStyle(6)

        # add widget to line layout
        line_layout.addWidget(name)
        line_layout.addWidget(button)

        # add line lyout to list layout
        layout.addLayout(line_layout)

        # increment spaceinput index
        self.increment_space_input_index()

    def increment_space_input_index(self):
        self.space_input_index += 1


##############################################################################
# test
##############################################################################


d = Module_Win(None)
d.show()
