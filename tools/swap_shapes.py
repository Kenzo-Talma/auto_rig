import maya.cmds as cmds
import json
from .create_node import create_node


def swap_shapes(ctrl=None, shape=None, scale=(1, 1, 1), color=0, width=2):
    """
    swap control shape
    :param ctrl: parent transform
    :param shape: shape design
    :param scale: scale of the shape
    :param color: color of the shape
    :param width: width of the shape
    :return: curve
    """
    # get shapes
    control_shape_file = open('ressources/control_shapes.json')

    control_shape_dic = json.load(control_shape_file)

    shape_dic = control_shape_dic[shape]

    # apply scale
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
    ctrl_curve = create_node('nurbsCurve', n=ctrl+'Shape', p=ctrl)

    ctrl_curve = cmds.curve(
        ctrl_curve,
        p=p_list,
        d=shape_dic['d'],
        per=shape_dic['periodic'],
        k=shape_dic['k'],
        r=True
    )

    cmds.setAttr(ctrl_curve+'.overrideEnabled', 1)
    cmds.setAttr(ctrl_curve+'.overrideColor', color)

    cmds.setAttr(ctrl_curve+'.lineWidth', width)

    if plug:
        cmds.connectAttr(plug[0], ctrl_curve+'.v', f=True)

    # return
    return ctrl_curve
