import maya.cmds as cmds


def match_transform(ref, target, **kwargs):
    """
    reset transform attributes
    param: ref: reference to match
    param: target(str): target to move, must be a transform or a joint
    param: kwargs:
        translate or t(bool): reset tranlate (true by default)
        rotate or ro(bool): reset rotate (true by default)
        scale or s(bool): reset scale (true by default)
        shear or sh(bool): reset shear (true by default)
        relative or r(bool): match transform in relative space
                            (false by default)
    """

    # skip list
    # translate
    if 'translate' in kwargs:
        if kwargs['translate']:
            translate = True
        else:
            translate = False
    elif 't' in kwargs:
        if kwargs['t']:
            translate = True
        else:
            translate = False
    else:
        translate = True

    # rotate
    if 'rotate' in kwargs:
        if kwargs['rotate']:
            rotate = True
        else:
            rotate = False
    elif 'ro' in kwargs:
        if kwargs['ro']:
            rotate = True
        else:
            rotate = False
    else:
        rotate = True

    # scale
    if 'scale' in kwargs:
        if kwargs['scale']:
            scale = True
        else:
            scale = False
    elif 's' in kwargs:
        if kwargs['s']:
            scale = True
        else:
            scale = False
    else:
        scale = True

    # shear
    if 'shear' in kwargs:
        if kwargs['shear']:
            shear = True
        else:
            shear = False
    elif 'sh' in kwargs:
        if kwargs['sh']:
            shear = True
        else:
            shear = False
    else:
        shear = True

    # relative
    if 'relative' in kwargs:
        if kwargs['relative']:
            relative = True
        else:
            relative = False
    elif 'r' in kwargs:
        if kwargs['r']:
            relative = True
        else:
            relative = False
    else:
        relative = False

    # match transform
    if not relative:
        # translate
        if not cmds.listConnections(
            target+'.translate',
            s=True,
            d=False
        ) and translate:
            cmds.xform(
                target,
                t=cmds.xform(ref, q=True, t=True, ws=True),
                ws=True
            )

        # rotate
        if not cmds.listConnections(
            target+'.rotate',
            s=True,
            d=False
        ) and rotate:
            cmds.xform(
                target,
                ro=cmds.xform(ref, q=True, ro=True, ws=True),
                ws=True
            )

        # scale
        if not cmds.listConnections(
            target+'.scale',
            s=True,
            d=False
        ) and scale:
            cmds.xform(
                target,
                s=cmds.xform(ref, q=True, s=True, ws=True),
                ws=True
            )

        # shear
        if not cmds.listConnections(
            target+'.shear',
            s=True,
            d=False
        ) and shear:
            cmds.xform(
                target,
                sh=cmds.xform(ref, q=True, sh=True, ws=True),
                ws=True
            )

    else:
        # tranlate
        if not cmds.listConnections(
            target+'.translate',
            s=True,
            d=False
        ) and translate:
            cmds.setAttr(
                target+'.translate',
                cmds.getAttr(ref+'.tranlate')
            )

        # rotate
        if not cmds.listConnections(
            target+'.rotate',
            s=True,
            d=False
        ) and rotate:
            cmds.setAttr(
                target+'.rotate',
                cmds.getAttr(ref+'.rotate')
            )

        # scale
        if not cmds.listConnections(
            target+'.scale',
            s=True,
            d=False
        ) and scale:
            cmds.setAttr(
                target+'.scale',
                cmds.getAttr(ref+'.scale')
            )

        # tranlate
        if not cmds.listConnections(
            target+'.shear',
            s=True,
            d=False
        ) and shear:
            cmds.setAttr(
                target+'.shear',
                cmds.getAttr(ref+'.shear')
            )


def reset_transform(node, **kwargs):
    """
    reset transform attributes
    param: node(str): node to reset, must be a transform or a joint
    param: kwargs:
        translate or t(bool): reset tranlate
        rotate or ro(bool): reset rotate
        scale or s(bool): reset scale
        shear or sh(bool): reset shear
        offsetParentMatrix or opm(bool): reset offsetParentMatrix
    """

    # skip list
    # translate
    if 'translate' in kwargs:
        if kwargs['translate']:
            translate = True
        else:
            translate = False
    elif 't' in kwargs:
        if kwargs['t']:
            translate = True
        else:
            translate = False
    else:
        translate = True

    # rotate
    if 'rotate' in kwargs:
        if kwargs['rotate']:
            rotate = True
        else:
            rotate = False
    elif 'ro' in kwargs:
        if kwargs['ro']:
            rotate = True
        else:
            rotate = False
    else:
        rotate = True

    # scale
    if 'scale' in kwargs:
        if kwargs['scale']:
            scale = True
        else:
            scale = False
    elif 's' in kwargs:
        if kwargs['s']:
            scale = True
        else:
            scale = False
    else:
        scale = True

    # shear
    if 'shear' in kwargs:
        if kwargs['shear']:
            shear = True
        else:
            shear = False
    elif 'sh' in kwargs:
        if kwargs['sh']:
            shear = True
        else:
            shear = False
    else:
        shear = True

    # offset parent matrix
    if 'offsetParentMatrix' in kwargs:
        if kwargs['offsetParentMatrix']:
            offsetParentMatrix = True
        else:
            offsetParentMatrix = False
    elif 'opm' in kwargs:
        if kwargs['opm']:
            offsetParentMatrix = True
        else:
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
