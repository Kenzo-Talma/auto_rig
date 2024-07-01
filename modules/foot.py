import maya.cmds as cmds
from tools.create_node import create_node
from tools.list_lib import append_list, extend_list
from tools.attr_lib import connect_attr
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
            fk=True,
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

        # foot info
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
        self.ik_guide_dic = {
            f'{self.full_name}_1_loc': (0, 0, 0),
            f'{self.full_name}_2_loc': (0, 0, 0),
            f'{self.full_name}_3_loc': (0, 0, 0),
            f'{self.full_name}_4_loc': (0, 0, 0),
            f'{self.full_name}_slide_1_loc': (0, 0, 0),
            f'{self.full_name}_slide_2_loc': (0, 0, 0),
            f'{self.full_name}_slide_3_loc': (0, 0, 0),
            f'{self.full_name}_side_in_loc': (0, 0, 0),
            f'{self.full_name}_side_out_loc': (0, 0, 0)
        }
        self.fk_guide_list = [
            f'{self.full_name}_1_loc',
            f'{self.full_name}_2_loc',
            f'{self.full_name}_3_loc'
        ]

        self.ik_joint = None
        self.ik_control = None
        self.ik_group = None
        self.ik_offset = None

        self.fk_joint = None
        self.fk_control = None
        self.fk_group = None
        self.fk_offset = None

        self.main_joint = None

    def create_guides(self):
        guide_list = []
        for n, loc in enumerate(self.ik_guide_dic):
            # create guide
            loc = create_node(
                'spaceLocator',
                n=loc
            )
            cmds.setAttr(loc+'.translate', self.ik_guide_dic[loc])

            # add loc to guide list
            guide_list = append_list(guide_list, loc)

            # parent guide
            if not n == 0:
                cmds.parent(loc, guide_list[n-1])

    def create_joint(self):
        # ik joint
        if self.ik:
            self.ik_joint = simple_joint_chain(
                self.fk_guide_list,
                extention=['loc', 'ik_jnt']
            )

        # fk joint
        if self.fk:
            self.fk_joint = simple_joint_chain(
                self.fk_guide_list,
                extention=['loc', 'fk_jnt']
            )

        # main list
        self.main_joint = simple_joint_chain(
                self.fk_guide_list,
                extention=['loc', 'main_jnt']
            )

    def create_ik_foot(self):
        # create object
        for n, loc in enumerate(self.ik_guide_dic):
            # create control
            ctrl, curve, grp, offset, ctrl_joint = create_control(
                shape='circleX',
                name=loc.replace('loc', 'ik'),
                offset=True
            )

            # add object to list
            self.transfrom = extend_list(self.transfrom, [grp, ctrl, offset])
            self.ik_control = append_list(self.ik_control, ctrl)
            self.shapes = append_list(self.shapes, curve)
            self.ik_group = append_list(self.ik_group, [grp, offset])

        # parent control
        for n, grp in enumerate(reversed(self.ik_group)):
            if not grp == self.ik_group[0]:
                cmds.parent(grp, self.ik_control[-(n+2)])

        # place and connect group
        for n, joint in enumerate(self.ik_joint):
            match_transform(ref=joint, target=self.ik_group[n])
            mlm = matrix_constraint(parent=self.ik_control[n], target=joint)

            self.other_nodes = append_list(self.other_nodes, mlm)

        # create attributes
        foot_roll_attr = self.switch.add_attr(
            long_name='foot_roll',
            attribute_type='float',
            default_value=0,
        )
        foot_breack_attr = self.switch.add_attr(
            long_name='foot_breack',
            attribute_type='float',
            default_value=25,
        )
        foot_slide_1_attr = self.switch.add_attr(
            long_name='foot_slide_1',
            attribute_type='float',
            default_value=0,
        )
        foot_slide_2_attr = self.switch.add_attr(
            long_name='foot_slide_2',
            attribute_type='float',
            default_value=0,
        )
        foot_slide_3_attr = self.switch.add_attr(
            long_name='foot_slide_3',
            attribute_type='float',
            default_value=0,
        )
        foot_bank_attr = self.switch.add_attr(
            long_name='foot_bank',
            attribute_type='float',
            default_value=0,
        )

        # create network
        # foot rool network
        # foot 2 network
        foot_2_clp = create_node(
            'clamp',
            n=self.ik_control[1].replace('ctrl', 'clp')
        )
        connect_attr(foot_roll_attr, foot_2_clp+'.inputR', f=True)
        cmds.setattr(foot_2_clp+'.maxR', 90)
        connect_attr(
            foot_2_clp+'.outputR',
            self.ik_offset[1]+'.rotateZ',
            f=True
        )

        # foot 3 network
        foot_3_clp = create_node(
            'clamp',
            n=self.ik_control[2].replace('ctrl', 'clp')
        )
        connect_attr(foot_roll_attr, foot_3_clp+'.inputR', f=True)
        connect_attr(foot_breack_attr, foot_3_clp+'.minR', f=True)
        cmds.setattr(foot_3_clp+'.maxR', 90)

        foot_3_rmp = create_node(
            'rempaValue',
            n=foot_3_clp.replace('clp', 'rmp')
        )
        connect_attr(foot_3_clp+'.outputR', foot_3_rmp+'.inputValue', f=True)
        connect_attr(foot_breack_attr, foot_3_rmp+'.inputMin', f=True)
        cmds.setAttr(foot_3_rmp+'.inputMax', 90)
        cmds.setAttr(foot_3_rmp+'.outputMax', 90)

        connect_attr(
            foot_3_rmp+'.outValue',
            self.ik_offset[2]+'.rotateZ',
            f=True
        )

        # foot 4 network
        foot_4_clp = create_node(
            'clamp',
            n=self.ik_control[3].replace('ctrl', 'clp')
        )
        connect_attr(foot_roll_attr, foot_4_clp+'.inputR', f=True)
        cmds.setAttr(foot_4_clp+'.minR', -90)
        connect_attr(
            foot_4_clp+'.outputR',
            self.ik_offset[3]+'.rotateZ',
            f=True
        )

        # foot bank network
        # foot in
        foot_in_clp = create_node(
            'clamp',
            n=self.ik_control[-2].replace('ctrl', 'clp')
        )
        connect_attr(foot_bank_attr, foot_in_clp+'.inputR', f=True)
        cmds.setAttr(foot_in_clp+'.maxR', 90),
        connect_attr(foot_in_clp+'.outputR', self.ik_offset[-2]+'.rotateZ')

        # foot out
        foot_out_clp = create_node(
            'clamp',
            n=self.ik_control[-1].replace('ctrl', 'clp')
        )
        connect_attr(foot_bank_attr, foot_out_clp+'.inputR', f=True)
        cmds.setAttr(foot_out_clp+'.maxR', 90),
        connect_attr(foot_out_clp+'.outputR', self.ik_offset[-1]+'.rotateZ')

        # foot slide network
        # foot slide 1
        connect_attr(
            foot_slide_1_attr,
            self.ik_control[4]+'.translateY',
            f=True
        )

        # foot slide 2
        connect_attr(
            foot_slide_2_attr,
            self.ik_control[5]+'.translateY',
            f=True
        )

        # foot slide 3
        connect_attr(
            foot_slide_3_attr,
            self.ik_control[6]+'.translateY',
            f=True
        )

        self.other_nodes = extend_list(self.other_nodes, [
            foot_2_clp,
            foot_3_clp,
            foot_3_rmp,
            foot_4_clp,
            foot_in_clp,
            foot_out_clp
        ])

    def create_fk_foot(self):
        # create control
        for n, joint in enumerate(self.fk_joint):
            ctrl, curve, grp, offset, ctrl_joint = create_control(
                shape='circleX',
                name=joint.rpartition('_')[0],
            )

            # set position
            match_transform(ref=joint, target=grp)

            # create constraint
            mlm = matrix_constraint(parent=ctrl, target=joint)

            # add object to list
            self.transfrom = extend_list(self.transfrom, [grp, ctrl])
            self.fk_control = append_list(self.fk_control, ctrl)
            self.shapes = append_list(self.shapes, curve)
            self.fk_group = append_list(self.fk_group, grp)
            self.other_nodes = append_list(self.other_nodes, mlm)

            # parent control
            if not n == 0:
                cmds.parent(grp, self.fk_control[n-1])

    def ik_fk_switch(self):
        self.switch.ik_fk_switch(
            self.main_joint,
            self.ik_joint,
            self.fk_joint,
            self.ik_control,
            self.fk_control
        )
