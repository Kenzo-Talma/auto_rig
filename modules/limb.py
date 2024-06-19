import maya.cmds as cmds
from tools.create_node import create_node
from tools.matrix_constraint import matrix_constraint
from tools.create_control import create_control


class Ribbon_Module:
    # init method
    def __init__(
            self,
            space_input_list,
            data_input_list,
            name,
            side,
            limb_lenght=3,
            compound_name=None,
    ):
        # inputs
        self.space_input_list = space_input_list
        self.data_input_list = data_input_list

        # limb info
        self.limb_length = limb_lenght

        # def name
        if compound_name:
            self.name = f'{side}_{compound_name}_{name}'
        else:
            self.name = f'{side}_{name}'

        # module objects
        self.transfrom = None
        self.joint = None
        self.shapes = None
        self.control = None
        self.other_nodes = None

        # limb obects
        self.guide_list = None
        self.group_list = None

    def create_guides(self):
        for i in range(self.limb_length):
            # create guide
            loc = create_node('spaceLocator', n=f'{self.name}_{str(i)}_loc')
            cmds.setAttr(loc+'.translateX', i)

            # add loc to guide list
            if self.guide_list:
                self.guide_list.append(loc)
            else:
                self.guide_list = [loc]

            # parent guide
            if not i == 0:
                cmds.parent(loc, self.guide_list[i-1])

    def create_control(self):
        for n, guide in enumerate(self.guide_list):
            # create control
            ctrl, curve, grp, offset, joint = create_control(
                shape='circleX',
                name=guide.replace('_loc', '')
            )

            # add object to list
            if self.transfrom:
                self.transfrom.append(grp)
                self.transfrom.append(ctrl)
            else:
                self.transfrom = [grp, ctrl]

            if self.control:
                self.control.append(ctrl)
            else:
                self.control = [ctrl]

            if self.shapes:
                self.shapes.append(curve)
            else:
                self.shapes = [curve]

            if self.group_list:
                self.group_list.append(grp)
            else:
                self.group_list = [grp]

            # parent group
            if not n == 0:
                cmds.parent(grp, self.control[n-1])

    def create_joint(self):
        for n, ctrl in enumerate(self.control):
            # create joint
            joint = create_node('joint', n=ctrl.replace('ctrl', 'jnt'))

            # add joint to list
            if self.joint:
                self.joint.append(joint)
            else:
                self.joint = [joint]

            # parent joint
            if not n == 0:
                cmds.parent(joint, self.joint[n-1])

            # connect joint
            matrix_constraint(ctrl, joint)
