import maya.cmds as cmds
from tools.matrix_constraint import matrix_constraint
from tools.create_node import create_node
from tools.create_control import create_control
from tools.transform_lyb import match_transform
from tools.list_lyb import append_list, extend_list


class Limb_Module:
    # init method
    def __init__(
            self,
            switch,
            space_input_list,
            data_input_list,
            name,
            side,
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

        # limb obects
        self.guide_list = None
        self.group_list = None

        self.ik_control = None
        self.fk_control = None

        self.ik_joint = None
        self.fk_joint = None

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

    def create_ik_limb(self):
        for n, guide in enumerate(self.guide_list):
            # create joint
            joint = create_node('joint', n=guide.replace('loc', 'ik')+'_jnt')

            # set position
            match_transform(guide, joint)

            # add joint to list
            self.joint = append_list(self.joint, joint)
            self.ik_joint = append_list(self.ik_joint, joint)

            # parent joint
            if not n == 0:
                cmds.parent(joint, self.ik_joint[n-1])

        # orient joint
        for joint in self.ik_joint:
            if cmds.listRelatives(joint, c=True, type='joint'):
                cmds.joint(joint, e=True, oj='xzy', sao='zup', zso=True)
            else:
                cmds.joint(joint, e=True, oj='none', zso=True)

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

        # add obect to list
        self.transfrom = extend_list(self.transfrom, [
                ik_ctrl,
                ik_grp,
                pv_ctrl,
                pv_grp
            ])
        self.ik_control = extend_list(self.ik_control, [ik_ctrl, pv_ctrl])
        self.shapes = extend_list(self.shapes, [ik_curve, pv_curve])
        self.transfrom = extend_list(self.transfrom, [
            ik_grp,
            pv_grp,
            ik_ctrl,
            pv_ctrl
        ])
        self.other_nodes = extend_list(self.other_nodes, [ik_handle, effector])

    def create_fk_limb(self):
        for n, guide in enumerate(self.guide_list):
            # create joint
            joint = create_node('joint', n=guide.replace('loc', 'jnt'))

            # add joint to list
            self.joint = append_list(self.joint, joint)
            self.fk_joint = append_list(self.fk_joint, joint)

            # parent joint
            if not n == 0:
                cmds.parent(joint, self.joint[n-1])

        for n, joint in enumerate(self.fk_joint):
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
            match_transform(joint, grp)

            # connect joint
            joint_mlm = matrix_constraint(ctrl, joint)
            self.other_nodes = append_list(self.other_nodes, joint_mlm)

            # parent group
            if not n == 0:
                cmds.parent(grp, self.fk_control[n-1])
