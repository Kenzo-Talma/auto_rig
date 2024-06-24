import maya.cmds as cmds
from tools.attr_lyb import edit_attr, connect_attr
from tools.create_control import create_control
from tools.list_lyb import append_list, extend_list


class Ribbon_Module:
    # init method
    def __init__(
            self,
            space_input_list,
            data_input_list,
            name,
            side,
            compound_name=None,
    ):
        # inputs
        self.space_input_list = space_input_list
        self.data_input_list = data_input_list

        # outputs
        self.space_output = None
        self.data_output = None

        # def name
        self.name = name
        self.side = side

        if compound_name:
            self.full_name = f'{side}_{compound_name}_{name}'
        else:
            self.full_name = f'{side}_{name}'

        # module objects
        self.transfrom = None
        self.joint = None
        self.shapes = None
        self.control = None
        self.other_nodes = None

    # create switch controller
    def create_switch(self):
        # create objects
        ctrl, curve, grp, offset, joint = create_control(
            shape='diamond',
            name=self.full_name
        )

        # add object to list
        extend_list(self.transfrom, [ctrl, grp])
        append_list(self.shape, curve)
        append_list(self.control, ctrl)

        # lock attribute
        for attr in ['translate', 'rotate', 'scale', 'v']:
            edit_attr(
                f'{ctrl}.{attr}',
                locked=True,
                channel_box=False,
                keyable=False
            )

    # attach switch to any tranform or joint
    def attach_switch(self, offset=[0, 0, 0]):
        connect_attr(
            self.space_input_list[0],
            self.transfrom[0]+'.offsetParentMatrix',
            f=True
        )
        cmds.setAttr(
            self.transfrom[0]+'.translate',
            offset[0],
            offset[1],
            offset[2]
        )
