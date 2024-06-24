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


def add_attr(
        node,
        long_name,
        nice_name=None,
        attribute_type='float',
        keyable=True,
        locked=False,
        channel_box=True,
        default_value=None,
        max_value=None,
        min_value=None,
        force=True,
        **kwargs
):
    """
    create new attribute
    param: node(str): node to add the attribute on
    param: attribute_type(str): type of the new attribute
    param: long_name(str): long name of the attribute
    param: nice_name(str): nice name of the attribute
    param: keyable(bool): make the attribute keyable
    param: locked(bool): make the attribite locked
    param: channel_box(bool): make the attribute displayed in the channel box
    param: default_value(float): set default value for the attribute
    param: max_value(float): set max vaule for the attribute
    param: min_value(float): set min attribute value
    param: force(bool): will replace existing attribute
    param: kwargs: regulate maya's addAttr kwargs
    return: attribute name
    """
    # test if attribute exist
    attribute = f'{node}.{long_name}'

    # delete attribute
    if cmds.objectExist(attribute) and force:
        remove_attr(attribute)

    # create attribute
    # witch all parameters
    if not cmds.objExist(attribute)\
            and nice_name\
            and default_value\
            and max_value\
            and min_value:
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            nn=nice_name,
            dv=default_value,
            max=max_value,
            min=min_value,
            **kwargs
        )
    # without min value
    elif not cmds.objExist(attribute)\
            and nice_name\
            and default_value\
            and max_value:
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            nn=nice_name,
            dv=default_value,
            max=max_value,
            **kwargs
        )
    # without max value
    elif not cmds.objExist(attribute)\
            and nice_name\
            and default_value\
            and min_value:
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            nn=nice_name,
            dv=default_value,
            min=min_value,
            **kwargs
        )
    # without min and max value
    elif not cmds.objExist(attribute)\
            and nice_name\
            and default_value:
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            nn=nice_name,
            dv=default_value,
            **kwargs
        )
    # without value seted
    elif not cmds.objExist(attribute)\
            and nice_name:
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            nn=nice_name,
            **kwargs
        )
    # without nice name
    elif not cmds.objExist(attribute)\
            and default_value\
            and max_value\
            and min_value:
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            dv=default_value,
            max=max_value,
            min=min_value,
            **kwargs
        )
    # without nice name and min value
    elif not cmds.objExist(attribute)\
            and default_value\
            and max_value:
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            dv=default_value,
            max=max_value,
            **kwargs
        )
    # without nice name and max value
    elif not cmds.objExist(attribute)\
            and default_value\
            and min_value:
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            dv=default_value,
            min=min_value,
            **kwargs
        )
    # without extra parameters
    elif not cmds.objExist(attribute):
        cmds.addAttr(
            node,
            at=attribute_type,
            ln=long_name,
            **kwargs
        )

    # set attr parameters
    edit_attr(
        attribute,
        keyable=keyable,
        channel_box=channel_box,
        locked=locked
    )

    return f'{node}.{long_name}'


def edit_attr(
        attribute_name=None,
        keyable=True,
        channel_box=False,
        locked=False
):
    """
    edit attribute settings
    param: attribute_name(str): attribute to edit
    param: keyable(bool): make the attribute keyable
    param: locked(bool): make the attribite locked
    param: channel_box(bool): make the attribute displayed in the channel box
    """
    if attribute_name:
        if cmds.objExist(attribute_name):
            cmds.setAttr(
                attribute_name,
                k=keyable,
                cb=channel_box,
                l=locked
            )


def remove_attr(
        attribute_name=None,
        node=None,
        long_name=None,
        short_name=None
):
    """
    remove attribute
    param: attribute_name(str): attribute to delete
    param: node(str): name of the node
    param: long_name(str): long name of the attribute
    param: short_name(str): short name of the attribute
    """
    if node and long_name:
        cmds.deleteAttr(node, at=long_name)
    elif node and short_name:
        cmds.deleteAttr(node, at=long_name)
    elif attribute_name:
        if cmds.objExist(attribute_name):
            cmds.deletaAttr(attribute_name)
