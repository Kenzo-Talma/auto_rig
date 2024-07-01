import maya.cmds as cmds
from tools.attr_lib import edit_attr, connect_attr, add_attr
from tools.create_control import create_control
from tools.list_lib import append_list, extend_list
from tools.create_node import create_node


class Switch_Module:
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
        self.transfrom = extend_list(self.transfrom, [ctrl, grp])
        self.shapes = append_list(self.shapes, curve)
        self.control = append_list(self.control, ctrl)

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

    def create_blend_matrix(self, input_list, output):
        # check if input list is instance
        if not isinstance(input_list, list):
            input_list = [input_list]

        # create blend matrix
        blm = create_node('blendMatrix', n=output.rpartition('_')[0]+'_blm')

        # create blend list
        blend_list = []

        # input loop
        for n, input in enumerate(input_list):
            # check if input got parent
            if cmds.listRelatives(input, p=True):
                # create mult matrix node
                input_mlm = create_node(
                    'multMatrix',
                    n=input.rpartition('_')[0]+'_mlm'
                )
                connect_attr(
                    input+'.worldMatrix',
                    input_mlm+'.matrixIn[0]',
                    f=True
                )
                connect_attr(
                    cmds.listRelatives(input, p=True)[0]+'.worldInverseMatrix',
                    input_mlm+'.matrixIn[1]',
                    f=True
                )
                connect_attr(
                    input_mlm+'.matrixSum',
                    f'{blm}.target[{str(n)}].targetMatrix',
                    f=True
                )
            else:
                connect_attr(
                    input+'.worldMatrix',
                    f'{blm}.target[{str(n)}].targetMatrix',
                    f=True
                )

            # connect output
            connect_attr(
                blm+'.outputMatrix',
                output+'.offsetParentMatrix',
                f=True
            )

            # add blend to blend list
            blend_list.append(f'{blm}.target[{str(n)}].weight')

        return blm, blend_list

    def ik_fk_switch(
        self,
        main_joint_list,
        ik_joint_list,
        fk_joint_list,
        ik_ctrl_list,
        fk_ctrl_list
    ):
        # create attribute
        ik_fk_attr = add_attr(
            node=self.control[0],
            long_name='switch_ik_fk',
            attribute_type='enum',
            enumName='ik:fk'
        )
        # create inverse node
        ik_fk_rev = create_node('reverse', n=self.full_name+'_ik_fk_rev')
        connect_attr(ik_fk_attr, ik_fk_rev+'.inputX', f=True)
        ik_fk_rev_attr = ik_fk_rev+'.outputX'

        # connect ik fk and main
        for main, ik, fk in zip(main_joint_list, ik_joint_list, fk_joint_list):
            blm, blend_list = self.create_blend_matrix([ik, fk], main)

            # connect attribute to blend matrix
            connect_attr(ik_fk_rev_attr, blend_list[0], f=True)
            connect_attr(ik_fk_attr, blend_list[1])

        # connect visibility
        for ctrl in ik_ctrl_list:
            for shape in cmds.listRelatives(ctrl, s=True):
                connect_attr(
                    ik_fk_attr,
                    shape+'.v',
                    f=True
                )

        for ctrl in fk_ctrl_list:
            for shape in cmds.listRelatives(ctrl, s=True):
                connect_attr(
                    ik_fk_rev_attr,
                    shape+'.v',
                    f=True
                )

    def create_attr(
        self,
        long_name,
        nice_name=None,
        attribute_type='float',
        keyable=True,
        locked=False,
        channel_box=True,
        default_value=None,
        max_value=None,
        min_value=None,
        force=True,
        **kwargs
    ):
        attribute = add_attr(
            node=self.full_name,
            long_name=long_name,
            nice_name=nice_name,
            attribute_type=attribute_type,
            keyable=keyable,
            locked=locked,
            channel_box=channel_box,
            default_value=default_value,
            max_value=max_value,
            min_value=min_value,
            force=force,
            **kwargs
        )

        return attribute
