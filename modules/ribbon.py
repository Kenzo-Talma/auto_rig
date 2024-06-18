import maya.cmds as cmds
from tools.create_node import create_node
from tools.connect_attr import connect_attr
from tools.create_control import create_control


class Ribbon_Module:
    # init method
    def __init__(
            self,
            switch,
            space_input_list,
            name,
            side,
            compound_name=None,
            control_number=3,
            joint_number=5,
            periodic=False,
            degree=3
    ):
        # inputs
        self.switch = switch
        self.space_input_list = space_input_list

        # def name
        if compound_name:
            self.name = f'{side}_{compound_name}_{name}'
        else:
            self.name = f'{side}_{name}'

        # ribbon parameters
        self.control_number = control_number
        self.joint_number = joint_number
        self.periodic = periodic
        self.degree = degree

        # ribbon objects
        self.transfrom = None
        self.joint = None
        self.shapes = None
        self.control = None
        self.other_nodes = None

        self.surface = None
        self.surface_shape = None
        self.build_surface = None
        self.ribbon_joint = None

    def built_surface(self):
        if self.periodic:
            surface = cmds.cylinder(
                ax=[0, 0, 1],
                ch=False,
                d=self.degree,
                n=self.name+'_nbs'
            )
        else:
            surface = cmds.nurbsPlane(
                ch=False,
                d=self.degree,
                n=self.name+'_nbs',
                u=1,
                v=self.control_number-1
            )

        # create built shape
        surface_built = create_node(
            'nurbsSurface',
            n=surface.name+'built_nbs',
            p=surface[0]
        )
        connect_attr(
            surface[1]+'.worldSpace[0]',
            surface_built+'.create',
            f=True
        )
        cmds.disconnectAttr(
            surface[1]+'.worldSpace[0]',
            surface_built+'.create'
        )
        connect_attr(
            surface_built+'.worldSpace[0]',
            surface[1]+'.worldSpace'
        )

        # declare objects
        if not self.transfrom:
            self.transfrom = [surface[0]]
        else:
            self.transfrom.append(surface[0])

        if not self.surface:
            self.surface = [surface[1], surface_built]

        self.surface = surface[0]
        self.surface_shape = surface[1]
        self.build_surface = surface_built

    def attach_joint(self):
        # create and connect uvPin
        surface_uvpin = create_node('uvPin', n=self.name+'_uvp')
        connect_attr(
            self.surface+'.worldSpace[0]',
            surface_uvpin+'.deformedGeometry',
            f=True
        )
        connect_attr(
            self.build_surface+'.local',
            surface_uvpin+'.originalGeometry',
            f=True
        )

        # create and connect joint
        if not self.joint:
            self.joint = []
        if not self.ribbon_joint:
            self.ribbon_joint = []

        for i in range(self.joint_number):
            # create joint
            joint = create_node('joint', n=f'{self.name}_{str(1)}_jnt')

            # connect joint
            connect_attr(
                f'{surface_uvpin}.outputMatrix[{str(i)}]',
                joint+'.offsetParentMatrix',
                f=True
            )

            # set uv pin attributes
            cmds.setAttr(
                f'{surface_uvpin}.coordinate[{str(i)}].coordinateU',
                i/(self.joint_number-1)
            )

            # add joint to joint list
            self.joint.append(joint)
            self.ribbon_joint.append(joint)

    def create_control(self):
        if not self.control:
            self.control = []

        # create control
        for i in range(self.control_number):
            # create control
            control, curve, group, offset, joint = create_control(
                'squareX',
                None,
                (1, 1, 1),
                f'{self.name}_{str(i)}',
                False,
                True
            )
            self.control.append(control)

        for i in range(self.control_number):
            # parent middle controllers
            if not i == 0 or not i == self.control:
                # create and connect blendmatrix
                blend_matrix = create_node(
                    'blendMatrix',
                    n=f'{self.name}_{str(i)}_blm'
                )
                connect_attr(
                    self.control[0]+'.worldMatrix',
                    blend_matrix+'.inputMatrix',
                    f=True
                )
                connect_attr(
                    self.control[-1]+'.worldMatrix',
                    blend_matrix+'.target[0].targetMatrix',
                    f=True
                )
                cmds.setAttr(
                    blend_matrix+'target[0].weight',
                    i/self.control_number
                )

                # create and connect aim matrix
                aim_matrix = create_node(
                    'aimMatrix',
                    n=f'{self.name}_{str(i)}_amm'
                )
                connect_attr(
                    blend_matrix+'.outputMatrix',
                    aim_matrix+'.inputMatrix',
                    f=True
                )
                connect_attr(
                    blend_matrix+'.outputMatrix',
                    aim_matrix+'.secondary.secondaryTargetMatrix',
                    f=True
                )
                connect_attr(
                    self.control[-1]+'worldMatrix',
                    aim_matrix+'.primary.primaryTargetMatrix',
                    f=True
                )
                cmds.setAttr(aim_matrix+'secondary.secondaryInputAxisY', 0)
                cmds.setAttr(aim_matrix+'secondary.secondaryInputAxisZ', 1)
                cmds.setAttr(aim_matrix+'secondary.secondaryInputVectorZ', 1)

                # connect control
                connect_attr(
                    aim_matrix+'.outputMatrix',
                    group+'.offsetParentMatrix',
                    f=True
                )
