import maya.cmds as cmds
# import maya.api.OpenMaya as om
# import maya.api.OpenMayaAnim as omanim
# import maya.api.OpenMayaRender as omrender

import json
import pathlib


class module:
    def __init__(self):
        # open file containing the dictionnary template
        path = str((pathlib.Path(__file__).parent)).replace('\\', '/')
        path = path.replace('d:', 'D:')
        path = f"{path.rpartition('/')[0]}/ressources/module_dic_template.json"
        file = open(path, 'r')
        self.module_dic = json.load(file)

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
            f'{node}.translate',
            s=True,
            d=False
        ) and translate:
            cmds.setAttr(f'{node}.translate', 0, 0, 0)

        # rotate
        if not cmds.listConnections(f'{node}.rotate', s=True, d=False)\
                and rotate:
            cmds.setAttr(f'{node}.rotate', 0, 0, 0)

        # scale
        if not cmds.listConnections(f'{node}.scale', s=True, d=False)\
                and scale:
            cmds.setAttr(f'{node}.scale', 1, 1, 1)

        # shear
        if not cmds.listConnections(f'{node}.shear', s=True, d=False)\
                and shear:
            cmds.setAttr(f'{node}.shear', 0, 0, 0)

        # offset parent matrix
        if not cmds.listConnections(
            f'{node}.offsetParentMatrix',
            s=True,
            d=False
        ) and offsetParentMatrix:
            cmds.setAttr(
                f'{node}.offsetParentMatrix',
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

    def create_node(typ='transform', **kwargs):
        """
        create a new node
        param: typ(str): type of the object, tranform by default
        param: kwargs:
            clasic maya 's createNode kwargs
        """

        if 'n' in kwargs:
            if not cmds.objExists(kwargs['n']):
                if typ == 'spaceLocator':
                    return cmds.spaceLocator(**kwargs)[0]
                else:
                    return cmds.createNode(typ, **kwargs)
            else:
                return kwargs['n']

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
            mult_matrix = create_node('multMatrix', n=f'{target}_mlm')

            # reste tranform
            if reset:
                reset_transform(target)

            # check if selected node have parent
            if cmds.listRelatives(target, p=True):
                # connect node
                connect_attr(
                    f'{parent}.worldMatrix',
                    f'{mult_matrix}.matrixIn[0]',
                    f=True
                )
                connect_attr(
                    f'{cmds.listRelatives(target, p=True)[0]}.worldInverseMatrix',
                    f'{mult_matrix}.matrixIn[1]',
                    f=True
                )
                connect_attr(
                    f'{mult_matrix}.matrixSum',
                    f'{target}.offsetParentMatrix',
                    f=True
                )

            else:
                connect_attr(
                    f'{parent}.worldMatrix',
                    f'{target}.offsetParentMatrix',
                    f=True
                )

            # return
            return mult_matrix

        else:
            return None



"""
module_dic = {
            'module_name': None,  # string
            'module_type': None,  # string
            'space': {
                'space_input': {
                    'input_type': None,  # string
                    'input_dic': None,  # dictionnary
                },
                'space_output': {
                    'output_type': None,  # string
                    'output_dic': None,  # dictionnary
                }
            },
            'data': {
                'data_input': {
                    'input_type': None,  # string
                    'input_plugs': None,  # list
                },
                'data_output': {
                    'output_type': None,  # string
                    'output_plugs': None,  # list
                }
            },
            'nodes': None,  # dictionnary of nodes by types
            'attributes': None,  # dictionnary of extra attributes by nodes
            'module_input': None,  # dictionnary of modules input
            #                       (used for rebuilt connections)
            'module_output': None,  # dictionnary of module output
            'param': None,  # dictionnary of module parameters
        }
"""
