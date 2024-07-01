import maya.cmds as cmds
from tools.create_node import create_node
from tools.matrix_constraint import matrix_constraint
from tools.create_control import create_control
from tools.transform_lib import match_transform
from tools.list_lib import append_list, extend_list
from tools.joint_lib import simple_joint_chain


class Chain_Module:
    # init method
    def __init__(
            self,
            switch,
            space_input_list,
            data_input_list,
            name,
            side,
            fk=True,
            ik=True,
            chain_lenght=3,
            compound_name=None,
    ):
        # inputs
        self.switch = switch
        self.space_input_list = space_input_list
        self.data_input_list = data_input_list

        # outputs
        self.space_output = None
        self.data_output = None

        # chain info
        self.chain_length = chain_lenght
        self.ik = ik
        self.fk = fk

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
        self.guide_list = None
        self.group_list = None

        self.ik_control = None
        self.fk_control = None

        self.ik_joint = None
        self.fk_joint = None
        self.main_joint = None

    def create_guides(self):
        for i in range(self.chain_length):
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

    def create_fk_control(self):
        for n, joint in enumerate(self.fk_joint):
            # create control
            ctrl, curve, grp, offset, jnt = create_control(
                shape='circleX',
                name=joint.replace('loc', 'fk')
            )

            # add object to list
            self.transfrom = extend_list(self.transfrom, [grp, ctrl])
            self.fk_control = append_list(self.fk_control, ctrl)
            self.shapes = append_list(self.shapes, curve)
            self.group_list = append_list(self.group_list, grp)

            # set position
            match_transform(joint, grp)

            # parent group
            if not n == 0:
                cmds.parent(grp, self.fk_control[n-1])

            # constraint joint to controller
            matrix_constraint(parent=ctrl, target=joint)

    def create_ik_control(self):
        for joint in self.ik_joint:
            # create control
            ctrl, curve, grp, offset, jnt = create_control(
                shape='circleX',
                name=joint.replace('loc', 'ik')
            )

            # add object to list
            self.transfrom = extend_list(self.transfrom, [grp, ctrl])
            self.ik_control = append_list(self.ik_control, ctrl)
            self.shapes = append_list(self.shapes, curve)
            self.group_list = append_list(self.group_list, grp)

            # set position
            match_transform(ref=joint, target=grp)

            # constraint joint to controller
            matrix_constraint(parent=ctrl, target=joint)

    def create_joint(self):
        # create ik joints
        if self.ik:
            self.ik_joint = simple_joint_chain(
                self.guide_list,
                extention=['loc', 'ik_jnt']
            )

        # create fk joints
        if self.fk:
            self.fk_joint = simple_joint_chain(
                self.guide_list,
                extention=['loc', 'fk_jnt']
            )

    def create_ik_fk_switch(self):
        # create main limb
        for guide in self.guide_list:
            # create joint
            joint = create_node('joint', n=guide.replace('loc', 'main_jnt'))

            # add joint to list
            self.joint = append_list(self.joint, joint)
            self.main_joint = append_list(self.main_joint, joint)

            # add switch
            self.switch.ik_fk_switch(
                self.main_joint,
                self.ik_joint,
                self.fk_joint,
                self.ik_control,
                self.fk_control
            )
