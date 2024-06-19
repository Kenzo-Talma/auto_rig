import maya.cmds as cmds
from create_node import create_node
from attr_lyb import connect_attr
from transform_lyb import reset_transform


def space_switch(
        follow_parent='world',
        parent_list=None,
        target_list=None,
        control=None,
        attribute_name=None,
        attribute_list=None,
        skip_list=None
):
    """
    create space switch
    :param follow_parent(str): parent that follow the given nodes
    :param parent_list(lst): list of parents that will be followed
    :param target_list(lst): list of targets obects that will follow
    :param control(str): controller that get the switch attributes
    :param attribute_name(str): name off the switch attribute
    :param attribute_list(lst): list off the names displayed in the attribute
                (the length of the list must be equal to the parent list + 1)
    :param skip_list(lst): list of attributes that will be skipped by script
    :return: follow list
    """
    # check list
    if parent_list and target_list:
        if not isinstance(parent_list, list):
            parent_list = [parent_list]
        if not isinstance(target_list, list):
            target_list = [target_list]

    # def lists
    target_ref_list = []
    blm_list = []
    follow_list = []

    # parent attr list
    if attribute_list:
        parent_attr_list = attribute_list
    else:
        parent_attr_list = [follow_parent]+parent_list

    # target loop
    for target in target_list:
        # create nodes
        target_ref = create_node('transform', n=target+'_ref')
        blm = create_node('blendMatrix', n=target+'_blm')
        follow = create_node('transform', n=target+'_follow')

        # appen node to lists
        target_ref_list.append(target_ref)
        blm_list.append(blm)
        follow_list.append(follow)

        cmds.xform(
            target_ref,
            m=cmds.xform(target, q=True, m=True, ws=True),
            ws=True
        )

        if cmds.listRelatives(target, p=True):
            cmds.parent(follow, cmds.listRelatives(target, p=True)[0])
        cmds.parent(target, follow)

        # reset node
        reset_transform(target)

        # connect blendMatrix
        if not follow_parent == 'world':
            parent_ref = create_node('transform', n=follow_parent + '_ref')
            parent_mlm = create_node(
                'multMatrix',
                n=f'{follow_parent}_{target}_mlm'
            )
            cmds.xform(
                parent_ref,
                m=cmds.xform(follow_parent, q=True, m=True, ws=True),
                ws=True
            )
            connect_attr(
                target_ref+'.worldMatrix',
                parent_mlm+'.matrixIn[0]',
                f=True
            )
            connect_attr(
                parent_ref+'.worldInverseMatrix',
                parent_mlm+'.matrixIn[1]',
                f=True
            )
            connect_attr(
                follow_parent+'.worldMatrix',
                parent_mlm+'.matrixIn[2]',
                f=True
            )
            connect_attr(
                parent_mlm+'.matrixSum',
                blm+'.inputMatrix',
                f=True
            )

        connect_attr(
            blm+'.outputMatrix',
            follow+'.offsetParentMatrix',
            f=True
        )

        # create attribute
        if not control:
            control = target

        # custom attribute name
        if not attribute_name:
            attr = attribute_name
        else:
            attr = target+'_space'

        if not cmds.objExists(f'{control}.{attr}'):
            cmds.addAttr(
                control,
                ln=attr,
                at='enum',
                en=':'.join(parent_attr_list),
                k=True
            )
            attr = f'{control}.{attr}'
            cmds.setAttr(attr, cb=True, k=True)

        # parent loop
        for n, parent in enumerate(parent_list):
            # create node
            mlm = create_node('multMatrix', n=f'{parent}_{target}_mlm')
            ref = create_node('transform', n=parent+'_ref')
            con = create_node('condition', n=f'{parent}_{target}_con')

            cmds.xform(
                ref,
                m=cmds.xform(parent, q=True, m=True, ws=True),
                ws=True
            )

            connect_attr(
                target_ref+'.worldMatrix',
                mlm+'.matrixIn[0]',
                f=True
            )
            connect_attr(
                ref+'.worldInverseMatrix',
                mlm+'.matrixIn[1]',
                f=True
            )
            connect_attr(
                parent+'.worldMatrix',
                mlm+'.matrixIn[2]',
                f=True
            )
            connect_attr(
                mlm+'.matrixSum',
                f'{blm}.target[{n}].targetMatrix',
                f=True
            )

            connect_attr(attr, con+'.firstTerm', f=True)
            cmds.setAttr(con+'.secondTerm', n+1)
            cmds.setAttr(con+'.colorIfTrueR', 1)
            cmds.setAttr(con+'.colorIfFalseR', 0)
            connect_attr(
                con+'.outColorR',
                f'{blm}.target[{n}].weight',
                f=True
            )

            if skip_list:
                for at in skip_list:
                    cmds.setAttr(f'{blm}.target[{n}].{at}Weight', 0)

    # return
    return target_ref_list, blm_list, follow_list
