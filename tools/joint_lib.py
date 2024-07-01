import maya.cmds as cmds
from .transform_lib import match_transform
from .create_node import create_node
from .list_lib import append_list


def orient_joint(joint_list, axis_order='xzy', secondary_axis='zup'):
    for joint in joint_list:
        if cmds.listRelatives(joint, c=True, type='joint'):
            cmds.joint(
                joint,
                e=True,
                oj=axis_order,
                sao=secondary_axis,
                zso=True
            )
        else:
            cmds.joint(joint, e=True, oj='none', zso=True)


def simple_joint_chain(
        guide_list,
        is_joint_orient=True,
        axis_order='xzy',
        secondary_axis='zup'
):
    joint_list = None
    for n, guide in enumerate(guide_list):
        # create joint
        joint = create_node('joint', n=guide.replace('loc', 'main_jnt'))

        # set joint position
        match_transform(ref=guide, target=joint)

        # add joint to list
        joint_list = append_list(joint_list, joint)

        # parent joint
        if not n == 0:
            cmds.parent(joint, joint_list[n-1])

    # orient joints
    if orient_joint:
        is_joint_orient(
            joint_list,
            axis_order,
            secondary_axis
        )

    # return
    return joint_list
