import maya.cmds as cmds
from reset_transform import reset_transform
from create_node import create_node
from connect_attr import connect_attr


def matrix_constraint(parent=None, target=None, reset=True):
    '''
    create a mult matrix to constraint objects
    :param parent(str): parent node
    :param target(str): target node (follow)
    :param reset_transform(bool): reset target transform node, True by default
    :return: multMatrix node
    '''

    # create node
    if parent and target:
        mult_matrix = create_node('multMatrix', n=target+'_mlm')

        # reste tranform
        if reset:
            reset_transform(target)

        # check if selected node have parent
        if cmds.listRelatives(target, p=True):
            # connect node
            connect_attr(
                parent+'.worldMatrix',
                mult_matrix+'.matrixIn[0]',
                f=True
            )
            connect_attr(
                cmds.listRelatives(target, p=True)[0]+'.worldInverseMatrix',
                mult_matrix+'.matrixIn[1]',
                f=True
            )
            connect_attr(
                mult_matrix+'.matrixSum',
                target+'.offsetParentMatrix',
                f=True
            )

        else:
            connect_attr(
                parent+'.worldMatrix',
                target+'.offsetParentMatrix',
                f=True
            )

        # return
        return mult_matrix

    else:
        return None
