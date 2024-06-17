import maya.cmds as cmds


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
