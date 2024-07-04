import maya.cmds as cmds
from tools.matrix_constraint import matrix_constraint
from tools.create_node import create_node
from tools.create_control import create_control
from tools.transform_lib import match_transform
from tools.list_lib import append_list, extend_list
from tools.joint_lib import simple_joint_chain
from tools.space_switch import space_switch


class Limb_Module:
    # init method
    def __init__(
            self
    ):
        # inputs
        self.switch = None
        self.space_input_dic = {
            'limb_start_input': None,
            'limb_end_input': None
        }
        self.data_input_dic = {}

        # outputs
        self.space_output = None
        self.data_output = None

        # limb info
        self.limb_length = 3
        self.start_skip_attr = ['rotate', 'scale', 'shear']
        self.end_skip_attr = None

        # def name
        self.name = 'limb_1'
        self.side = 'C'
        self.compound_name = None

        if self.compound_name:
            self.full_name = f'{self.side}_{self.compound_name}_{self.name}'
        else:
            self.full_name = f'{self.side}_{self.name}'

        # module objects
        self.transfrom = None
        self.joint = None
        self.shapes = None
        self.control = None
        self.other_nodes = None

        # limb obects
        self.guide_list = None
        self.group_list = None

        self.fk_control = None
        self.fk_group = None
        self.fk_joint = None

        self.ik_control = None
        self.fk_group = None
        self.ik_joint = None

        self.main_joint = None

    def add_start_input(self, space_input_added):
        # get start space input list
        start_input_list = self.space_input_dic['limb_start_input']

        # add object to list
        start_input_list = append_list(start_input_list, space_input_added)

        # return list
        self.space_input_dic['limb_start_input'] = start_input_list

    def add_end_input(self, space_input_added):
        # get end space input list
        end_input_list = self.space_input_dic['limb_end_input']

        # add object to list
        end_input_list = append_list(end_input_list, space_input_added)

        # return list
        self.space_input_dic['limb_end_input'] = end_input_list

    def add_space_ouput(self):
        for i in range(self.limb_length):
            self.space_output = append_list(
                self.space_output,
                f'{self.full_name}_{str(i)}_main_jnt'
            )

    def create_guides(self):
        for i in range(self.limb_length):
            # create guide
            loc = create_node(
                'spaceLocator',
                n=f'{self.full_name}_{str(i)}_loc'
            )
            cmds.setAttr(loc+'.translateX', i)

            # add loc to guide list
            self.guide_list = append_list(self.guide_list, loc)

            # parent guide
            if not i == 0:
                cmds.parent(loc, self.guide_list[i-1])

    def create_ik_limb(self):
        # create joint list
        ik_joint_list = simple_joint_chain(
            self.guide_list,
            extention=['loc', 'ik_jnt']
        )

        # add joints to list
        self.joint = extend_list(self.joint, ik_joint_list)
        self.ik_joint = extend_list(self.ik_joint, ik_joint_list)

        # ik handle
        ik_handle, temp = cmds.ikHandle(
            sj=self.ik_joint[0],
            ee=self.ik_joint[-1],
            n=self.full_name+'_ikh'
        )

        # rename effector
        effector = cmds.rename(temp, self.full_name+'_effector')

        # create ik handle control
        ik_ctrl, ik_curve, ik_grp, ik_offset, ik_joint = create_control(
            name=ik_handle,
            shape='cube'
        )

        match_transform(ik_handle, ik_grp)
        cmds.parent(ik_handle, ik_ctrl)

        # add pole vector
        pv_ctrl, pv_curve, pv_grp, pv_offset, pv_joint = create_node(
            name=ik_handle.replace('ikh', 'pv'),
            shape='diamond'
        )
        match_transform(self.ik_joint[1], pv_grp)
        cmds.move(0, 0, 5, a=True)
        cmds.poleVectorConstraint(pv_ctrl, ik_handle)

        # connect last joint rotation
        or_cns = cmds.orientConstraint(ik_ctrl, self.ik_joint[-1])

        # add obect to list
        self.transfrom = extend_list(self.transfrom, [
                ik_ctrl,
                ik_grp,
                pv_ctrl,
                pv_grp
            ])
        self.ik_group = extend_list(self.ik_group, [ik_grp, pv_grp])
        self.ik_control = extend_list(self.ik_control, [ik_ctrl, pv_ctrl])
        self.shapes = extend_list(self.shapes, [ik_curve, pv_curve])
        self.transfrom = extend_list(self.transfrom, [
            ik_grp,
            pv_grp,
            ik_ctrl,
            pv_ctrl
        ])
        self.other_nodes = extend_list(self.other_nodes, [
            ik_handle,
            effector,
            or_cns
        ])

    def create_fk_limb(self):
        # create joint chain
        fk_joint_list = simple_joint_chain(
            self.guide_list,
            extention=['loc', 'fk_jnt']
        )

        # add joint to list
        self.joint = extend_list(self.joint, fk_joint_list)
        self.fk_joint = extend_list(self.fk_joint, fk_joint_list)

        for n, joint in enumerate(self.fk_joint):
            # create control
            ctrl, curve, grp, offset, joint = create_control(
                shape='circleX',
                name=joint.rpartition('_')[0]
            )

            # set position
            match_transform(ref=joint, target=grp)

            # add object to list
            self.transfrom = extend_list(self.transfrom, [grp, ctrl])
            self.fk_group = append_list(self.fk_group, grp)
            self.fk_control = append_list(self.fk_control, ctrl)
            self.shapes = append_list(self.shapes, curve)
            self.group_list = append_list(self.group_list, grp)

            # set position
            match_transform(joint, grp)

            # connect joint
            joint_mlm = matrix_constraint(ctrl, joint)
            self.other_nodes = append_list(self.other_nodes, joint_mlm)

            # parent group
            if not n == 0:
                cmds.parent(grp, self.fk_control[n-1])

    def create_ik_fk_switch(self):
        # create joint chain
        main_joint_list = simple_joint_chain(
            self.guide_list,
            extention=['loc', 'main_jnt']
        )

        # add joint to list
        self.joint = extend_list(self.joint, main_joint_list)
        self.main_joint = extend_list(self.main_joint, main_joint_list)

        # add switch
        self.switch.ik_fk_switch(
            self.main_joint,
            self.ik_joint,
            self.fk_joint,
            self.ik_control,
            self.fk_control
        )

    def connect_space_inputs(self):
        # connect start
        # get data list
        start_list = self.space_input_dic['limb_start_input']
        main_parent = start_list[0]
        start_list.remove(main_parent)

        # connect constraint
        self.switch.create_space_switch(
            follow_parent=main_parent,
            parent_list=start_list,
            target_list=[self.fk_group[0], self.ik_joint[0]],
            attribute_name=self.full_name+'_space_switch',
            attribute_list=None,
            skip_list=self.start_skip_attr
        )

        # connect start
        # get data list
        end_list = self.space_input_dic['limb_end_input']
        main_parent = end_list[0]
        end_list.remove(main_parent)

        # connect constraint
        space_switch(
            follow_parent=main_parent,
            parent_list=end_list,
            target_list=[self.ik_group[0]],
            attribute_name=self.ik_control+'_space_switch',
            attribute_list=None,
            skip_list=self.end_skip_attr,
            control=self.ik_control[0]
        )
