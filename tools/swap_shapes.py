import maya.cmds as cmds
import json


def swap_shapes(ctrl=None, shape=None, scale=(1, 1, 1), color=0, width=2):
    """
    swap control shape
    :param ctrl: parent transform
    :param shape: shape design
    :param scale: scale of the shape
    :param color: color of the shape
    :param width: width of the shape
    :return: None
    """
    # get shapes
    control_shape_file = open('ressources/control_shapes.json')

    control_shape_dic = json.load(control_shape_file)

    shape_dic = control_shape_dic[shape]

    # scale
    point_list = shape_dic['p']
    p_list = []
    for point in point_list:
        p = (point[0] * scale[0], point[1] * scale[1], point[2] * scale[2])
        p_list.append(p)

    # delete shapes
    plug = cmds.listConnections(
        cmds.listRelatives(ctrl, s=True)[0]+'.v',
        s=True,
        d=False,
        p=True
    )
    cmds.delete(cmds.listRelatives(ctrl, s=True))

    # create curve
    cur = cmds.curve(
        p=p_list,
        d=shape_dic['d'],
        per=shape_dic['periodic'],
        k=shape_dic['k']
    )
    sh = cmds.rename(cmds.listRelatives(cur, s=True)[0], ctrl+'Shape')
    cmds.parent(sh, ctrl, r=True, s=True)

    cmds.setAttr(sh+'.overrideEnabled', 1)
    cmds.setAttr(sh+'.overrideColor', color)

    cmds.setAttr(sh+'.lineWidth', width)

    if plug:
        cmds.connectAttr(plug[0], sh+'.v', f=True)

    cmds.delete(cur)
