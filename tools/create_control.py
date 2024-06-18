import maya.cmds as cmds
import json
from create_node import create_node


def createcontrol(
        shape=None,
        parent=None,
        scale=(1, 1, 1),
        color=0, width=2,
        name=None,
        offset=False,
        joint=False,
):
    """
    swap control shape
    :param shape(str): shape design
    :param scale(tuple): scale of the shape (int, int, int)
    :param color(int): color of the shape
    :param width(int): width of the shape
    :param name(str): name off the controller
    :param offset(bool): create an extra offset group over the control
    :return:
        control
        curve
        group
        offset
        joint
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

    # create controls
    # apply parent
    if parent:
        ctrl_grp = create_node('transform', n=name+'_grp', p=parent)
    else:
        ctrl_grp = create_node('transform', n=name+'_grp')

    # apply offset
    if offset:
        ctrl_offset = create_node('transform', n=name+'_offset', p=ctrl_grp)
        ctrl = create_node('transform', n=name+'_ctrl', p=ctrl_offset)
    else:
        ctrl = create_node('transform', n=name+'_ctrl', p=ctrl_grp)
        ctrl_offset = None

    # add curve
    ctrl_curve = create_node('nurbsCurve', n=ctrl+'Shape', p=ctrl)

    ctrl_curve = cmds.curve(
        ctrl_curve,
        p=p_list,
        d=shape_dic['d'],
        per=shape_dic['periodic'],
        k=shape_dic['k'],
        r=True
    )

    # set curve width
    cmds.setAttr(ctrl_curve+'.lineWidth', width)

    # set curve color
    cmds.setAttr(ctrl_curve+'.overrideEnabled', 1)
    cmds.setAttr(ctrl_curve+'.overrideColor', color)

    # apply joint
    if joint:
        ctrl_jnt = create_node('joint', n=ctrl+'_jnt', p=ctrl)
    else:
        ctrl_jnt = None

    # return
    return ctrl, ctrl_curve, ctrl_grp, ctrl_offset, ctrl_jnt
