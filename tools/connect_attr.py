import maya.cmds as cmds


def connect_attr(output, input, **kwargs):
    """
    connect attributes
    param: output(str): output attribute
    param: input(str): input attribute
    param: kwargs:
        clasic maya 's connectAttr kwargs
    """

    # check if attribute is already connected
    con_list = cmds.listConnections(
        input,
        scn=True,
        c=True,
        p=True
    )

    if not con_list:
        # connect attributes
        cmds.connectAttr(output, input, **kwargs)

    elif output in con_list and input not in con_list:
        # connect attributes
        if 'f' in kwargs:
            if kwargs['f']:
                cmds.connectAttr(output, input, **kwargs)

    elif output not in con_list and input in con_list:
        # connect attributes
        if 'f' in kwargs:
            if kwargs['f']:
                cmds.connectAttr(output, input, **kwargs)
