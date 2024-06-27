import maya.cmds as cmds
from tools.create_node import create_node
from tools.matrix_constraint import matrix_constraint
from tools.create_control import create_control
from tools.transform_lyb import match_transform
from tools.list_lyb import append_list, extend_list


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
        for n, guide in enumerate(self.guide_list):
            # create control
            ctrl, curve, grp, offset, joint = create_control(
                shape='circleX',
                name=guide.replace('loc', 'fk')
            )

            # add object to list
            self.transfrom = extend_list(self.transfrom, [grp, ctrl])
            self.fk_control = append_list(self.fk_control, ctrl)
            self.shapes = append_list(self.shapes, curve)
            self.group_list = append_list(self.group_list, grp)

            # set position
            match_transform(guide, grp)

            # parent group
            if not n == 0:
                cmds.parent(grp, self.fk_control[n-1])

    def create_ik_control(self):
        for n, guide in enumerate(self.guide_list):
            # create control
            ctrl, curve, grp, offset, joint = create_control(
                shape='circleX',
                name=guide.replace('loc', 'ik')
            )

            # add object to list
            self.transfrom = extend_list(self.transfrom, [grp, ctrl])
            self.ik_control = append_list(self.ik_control, ctrl)
            self.shapes = append_list(self.shapes, curve)
            self.group_list = append_list(self.group_list, grp)

            # set position
            match_transform(guide, grp)

    def create_joint(self):
        # test ik and fk
        if self.ik and self.fk:
            all_ctrl_list = [self.ik_control, self.fk_control]
        elif self.ik:
            all_ctrl_list = [self.ik_control]
        elif self.fk_control:
            all_ctrl_list = [self.fk_control]

        # ik fk loop
        for control_list in all_ctrl_list:
            # control loop
            for n, ctrl in enumerate(control_list):
                # create joint
                joint = create_node('joint', n=ctrl.replace('ctrl', 'jnt'))

                # add joint to list
                self.joint = append_list(self.joint, joint)

                if control_list == self.fk_control:
                    self.fk_joint = append_list(self.fk_joint, joint)
                elif control_list == self.ik_control:
                    self.ik_joint = append_list(self.ik_joint, joint)

                # parent joint
                if not n == 0:
                    if control_list == self.fk_control:
                        cmds.parent(joint, self.fk_joint[n-1])
                    elif control_list == self.ik_control:
                        cmds.parent(joint, self.ik_joint[n-1])

                # connect joint
                joint_mlm = matrix_constraint(ctrl, joint)

                # add multmatrix to list
                self.other_nodes = append_list(self.other_nodes, joint_mlm)

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
