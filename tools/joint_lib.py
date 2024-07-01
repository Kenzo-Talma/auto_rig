import maya.cmds as cmds


def orient_joint(joint_list):
    for joint in joint_list:
        if cmds.listRelatives(joint, c=True, type='joint'):
            cmds.joint(joint, e=True, oj='xzy', sao='zup', zso=True)
        else:
            cmds.joint(joint, e=True, oj='none', zso=True)
