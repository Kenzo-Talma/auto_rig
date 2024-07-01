import maya.cmds as cmds
from tools.create_node import create_node
from tools.list_lib import append_list, extend_list
from tools.create_control import create_control
from tools.matrix_constraint import matrix_constraint
from tools.transform_lib import match_transform
from tools.joint_lib import simple_joint_chain


class Foot_Module:
    # init method
    def __init__(
            self,
            switch,
            space_input_list,
            data_input_list,
            name,
            side,
            ik=True,
            compound_name=None,
    ):
        # inputs
        self.switch = switch
        self.space_input_list = space_input_list
        self.data_input_list = data_input_list

        # outputs
        self.space_output = None
        self.data_output = None

        # hand info
        self.ik = ik

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

        # chain obects
        self.guide_dic = {
            f'{self.full_name}_finger_1': {
                f'{self.full_name}_finger_1_1_loc': (0, 0, 0),
                f'{self.full_name}_finger_1_2_loc': (0, 0, 0),
                f'{self.full_name}_finger_1_3_loc': (0, 0, 0),
                f'{self.full_name}_finger_1_4_loc': (0, 0, 0)
            },
            f'{self.full_name}_finger_2': {
                f'{self.full_name}_finger_2_1_loc': (0, 0, 0),
                f'{self.full_name}_finger_2_2_loc': (0, 0, 0),
                f'{self.full_name}_finger_2_3_loc': (0, 0, 0),
                f'{self.full_name}_finger_2_4_loc': (0, 0, 0),
                f'{self.full_name}_finger_2_5_loc': (0, 0, 0)
            },
            f'{self.full_name}_finger_3': {
                f'{self.full_name}_finger_3_1_loc': (0, 0, 0),
                f'{self.full_name}_finger_3_2_loc': (0, 0, 0),
                f'{self.full_name}_finger_3_3_loc': (0, 0, 0),
                f'{self.full_name}_finger_3_4_loc': (0, 0, 0),
                f'{self.full_name}_finger_3_5_loc': (0, 0, 0)
            },
            f'{self.full_name}_finger_4': {
                f'{self.full_name}_finger_4_1_loc': (0, 0, 0),
                f'{self.full_name}_finger_4_2_loc': (0, 0, 0),
                f'{self.full_name}_finger_4_3_loc': (0, 0, 0),
                f'{self.full_name}_finger_4_4_loc': (0, 0, 0),
                f'{self.full_name}_finger_4_5_loc': (0, 0, 0)
            },
            f'{self.full_name}_finger_5': {
                f'{self.full_name}_finger_5_1_loc': (0, 0, 0),
                f'{self.full_name}_finger_5_2_loc': (0, 0, 0),
                f'{self.full_name}_finger_5_3_loc': (0, 0, 0),
                f'{self.full_name}_finger_5_4_loc': (0, 0, 0),
                f'{self.full_name}_finger_5_5_loc': (0, 0, 0)
            }
        }

        self.ik_joint = None
        self.ik_control = None

        self.fk_control = None
        self.fk_group = None

        self.main_joint = None

    def create_guides(self):
        for guide_dic in self.guide_dic:
            for n, loc in enumerate(guide_dic):
                # create guide
                loc = create_node(
                    'spaceLocator',
                    n=loc
                )
                cmds.setAttr(loc+'.translate', guide_dic[loc])

                # parent guide
                if not n == 0:
                    cmds.parent(loc, self.guide_list[n-1])

    def create_ik_chain(self, guide_list):
        # create joint chain
        ik_joint_list = simple_joint_chain(guide_list)

        # add joint to list
        self.ik_joint = extend_list(self.ik_joint, ik_joint_list)

        # ik handle
        ik_handle, temp = cmds.ikHandle(
            sj=self.ik_joint[0],
            ee=self.ik_joint[-1],
            n=self.full_name+'_ikh',
            sol='ikSCsolver'
        )

        # rename effector
        effector = cmds.rename(temp, self.full_name+'_effector')

        # create ik handle control
        ik_ctrl, ik_curve, ik_grp, ik_offset, ik_joint = create_control(
            name=ik_handle,
            shape='cube'
        )

        # match ik control
        match_transform(ref=self.ik_joint[-1], target=ik_grp)

        # parent ik handle
        cmds.parent(ik_handle, ik_ctrl)

        # add object to list
        self.transfrom = extend_list(self.transfrom, [ik_grp, ik_ctrl])
        self.shapes = append_list(self.shapes, ik_curve)
        self.control = append_list(self.control, ik_ctrl)
        self.ik_control = append_list(self.ik_control, ik_ctrl)
        self.other_nodes = extend_list(self.other_nodes, [
            ik_handle,
            effector
        ])

    def create_fk_chain(self, guide_list):
        fk_ctrl_list = None

        # create joint chain
        main_joint_list = simple_joint_chain(guide_list)

        # add joint to list
        self.main_joint = extend_list(self.main_joint, main_joint_list)

        # create control
        for n, joint in enumerate(main_joint_list):
            ctrl, curve, grp, offset, jnt = create_control(
                name=joint.rpartition('_')[0],
                shape='circleX'
            )

            # set control position
            match_transform(ref=joint, target=grp)

            # add objects to list
            self.transfrom = extend_list(self.transfrom, [grp, ctrl])
            self.shapes = append_list(self.shapes, curve)
            self.control = append_list(self.control, ctrl)
            self.fk_control = append_list(self.fk_control, ctrl)
            self.fk_group = append_list(self.fk_group, grp)

            fk_ctrl_list = append_list(fk_ctrl_list, ctrl)

            # parent control
            if not n == 0:
                cmds.parent(grp, fk_ctrl_list[n-1])

        # constraint joint to ctrl
        for joint, ctrl in zip(main_joint_list, fk_ctrl_list):
            matrix_constraint(parent=ctrl, target=joint)

    def connect_chains(self):
        for ik_jnt in self.ik_joint:
            matrix_constraint(
                parent=ik_jnt,
                target=ik_jnt.replace('ik_jnt', 'fk_grp')
            )
