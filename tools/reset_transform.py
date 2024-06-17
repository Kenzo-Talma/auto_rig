import maya.cmds as cmds


def reset_transform(node, **kwargs):
    """
    reset transform attributes
    param: node(str): node to reset, must be a transform or a joint
    param: kwargs:
        skip(lst): list of skiped atrributes
    """

    # skip list
    if 'skip' in kwargs:
        # translate
        if 'translate' in kwargs['skip']:
            translate = False
        else:
            translate = True

        # rotate
        if 'rotate' in kwargs['skip']:
            rotate = False
        else:
            rotate = True

        # scale
        if 'scale' in kwargs['skip']:
            scale = False
        else:
            scale = True

        # shear
        if 'shear' in kwargs['skip']:
            shear = False
        else:
            shear = True

        # offset parent matrix
        if 'offsetParentMatrix' in kwargs['skip']:
            offsetParentMatrix = False
        else:
            offsetParentMatrix = True

    # reset node
    # translate
    if not cmds.listConnections(
        node+'.translate',
        s=True,
        d=False
    ) and translate:
        cmds.setAttr(node+'.translate', 0, 0, 0)

    # rotate
    if not cmds.listConnections(node + '.rotate', s=True, d=False) and rotate:
        cmds.setAttr(node+'.rotate', 0, 0, 0)

    # scale
    if not cmds.listConnections(node + '.scale', s=True, d=False) and scale:
        cmds.setAttr(node+'.scale', 1, 1, 1)

    # shear
    if not cmds.listConnections(node + '.shear', s=True, d=False) and shear:
        cmds.setAttr(node+'.shear', 0, 0, 0)

    # offset parent matrix
    if not cmds.listConnections(
        node+'.offsetParentMatrix',
        s=True,
        d=False
    ) and offsetParentMatrix:
        cmds.setAttr(
            node+'.offsetParentMatrix',
            (
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0
            ),
            type='matrix'
        )
