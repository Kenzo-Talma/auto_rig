import maya.cmds as cmds
from tools.create_node import create_node
from tools.attr_lyb import connect_attr
from tools.create_control import create_control
from tools.list_lyb import append_list, extend_list


class Ribbon_Module:
    # init method
    def __init__(
            self,
            switch,
            space_input_list,
            data_input_list,
            name,
            side,
            compound_name=None,
            control_number=3,
            joint_number=5,
            periodic=False,
            strechy=True
    ):
        # inputs
        self.switch = switch
        self.space_input_list = space_input_list
        self.data_input_list = data_input_list

        # outputs
        self.space_output = None
        self.data_output = None

        # def name
        self.name = name
        self.side = side

        if compound_name:
            self.full_name = f'{side}_{compound_name}_{name}'
        else:
            self.full_name = f'{side}_{name}'

        # ribbon parameters
        self.control_number = control_number
        self.joint_number = joint_number
        self.periodic = periodic
        self.strechy = strechy

        # module objects
        self.transfrom = None
        self.joint = None
        self.shapes = None
        self.control = None
        self.other_nodes = None

        # ribbon ojects
        self.surface = None
        self.surface_shape = None
        self.orig_surface = None
        self.ribbon_joint = None
        self.control_joint = None

    def build_surface(self):
        if self.periodic:
            surface = cmds.cylinder(
                ax=[0, 0, 1],
                ch=False,
                d=3,
                n=self.full_name+'_nbs'
            )
        else:
            if self.control_number:
                surface = cmds.nurbsPlane(
                    ch=False,
                    d=3,
                    n=self.full_name+'_nbs',
                    u=1,
                    v=self.control_number-1
                )
            else:
                surface = cmds.nurbsPlane(
                    ch=False,
                    d=3,
                    n=self.full_name+'_nbs',
                    u=1,
                    v=len(self.space_input_list)-1
                )

        # create orig shape
        surface_orig = create_node(
            'nurbsSurface',
            n=surface.name+'orig_nbs',
            p=surface[0]
        )
        connect_attr(
            surface[1]+'.worldSpace[0]',
            surface_orig+'.create',
            f=True
        )
        cmds.disconnectAttr(
            surface[1]+'.worldSpace[0]',
            surface_orig+'.create'
        )
        connect_attr(
            surface_orig+'.worldSpace[0]',
            surface[1]+'.worldSpace'
        )

        # declare objects
        append_list(self.transform, surface[0])

        self.surface = surface[0]
        self.surface_shape = surface[1]
        self.orig_surface = surface_orig

    def attach_joint(self):
        # create and connect uvPin
        surface_uvpin = create_node('uvPin', n=self.full_name+'_uvp')
        connect_attr(
            self.surface+'.worldSpace[0]',
            surface_uvpin+'.deformedGeometry',
            f=True
        )
        connect_attr(
            self.orig_surface+'.local',
            surface_uvpin+'.originalGeometry',
            f=True
        )

        # add uv pint to list
        append_list(self.other_nodes, surface_uvpin)

        # create and connect joint
        for i in range(self.joint_number):
            # create joint
            joint = create_node('joint', n=f'{self.full_name}_{str(1)}_jnt')

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
            append_list(self.joint, joint)
            append_list(self.ribbon_joint, joint)

    def create_control(self):

        # create control
        for i in range(self.control_number):
            # create control
            control, curve, group, offset, joint = create_control(
                'squareX',
                None,
                (1, 1, 1),
                f'{self.full_name}_{str(i)}',
                False,
                True
            )
            append_list(self.control, control)
            append_list(self.shapes, curve)
            extend_list(self.transfrom, [control, group])
            append_list(self.joint, joint)
            append_list(self.control_joint, joint)

        for i in range(self.control_number):
            # parent middle controllers
            if not i == 0 or not i == self.control:
                # create and connect blendmatrix
                blend_matrix = create_node(
                    'blendMatrix',
                    n=f'{self.full_name}_{str(i)}_blm'
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
                    n=f'{self.full_name}_{str(i)}_amm'
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
            elif i == 0:
                # set controller position
                cmds.setAttr(self.control[0]+'.tranlateX', -0.5)
            else:
                # set controller position
                cmds.setAttr(self.control[-1]+'.tranlateX', 0.5)

            # add object to list
            extend_list(self.other_nodes, [blend_matrix, aim_matrix])

    def add_strech_squash(self):
        # create arc length dimension node
        ald_u = create_node(
            'arcLengthDimension',
            n=self.surface.replace('nbs', 'u_adl'),
            p=self.surface
        )

        connect_attr(
            self.surface_shape+'.worldSpace',
            ald_u+'.nurbsGeometry',
            f=True
        )
        cmds.setAttr(ald_u+'.uParamValue', 1)
        cmds.setAttr(ald_u+'.vparamValue', 0.5)

        # create orig arc lenght dimension
        ald_orig_u = create_node(
            'arcLenghtDimension',
            n=self.surface.replace('nbs', 'orig_u_adl'),
            p=self.surface
        )

        connect_attr(
            self.orig_surface+'.worldSpace',
            ald_orig_u+'.nurbsGeometry',
            f=True
        )
        cmds.setAttr(ald_orig_u+'.uParamValue', 1)
        cmds.setAttr(ald_orig_u+'.vparamValue', 0.5)

        # create strech and squash network
        # create ratio multiply divide
        ratio_mld = create_node(
            'multiplyDivide',
            n=self.surface.replace('nbs', 'ratio_adl')
        )
        connect_attr(
            ald_u+'.arcLength',
            ratio_mld+'.input1X',
            f=True
        )
        connect_attr(
            ald_orig_u+'.arcLength',
            ratio_mld+'input2X',
            f=True
        )
        cmds.setAttr(ratio_mld+'.operation', 2)

        # create inverse multoply divide
        inverse_mld = create_control(
            'multiplyDivide',
            n=self.surface.replace('nbs', 'inverse_mld')
        )
        connect_attr(
            ratio_mld+'.outputX',
            inverse_mld+'.input2X',
            f=True
        )
        cmds.setAttr(inverse_mld+'.input1X', 1)
        cmds.setAttr(inverse_mld+'.operation', 2)

        # square root multiply divide
        sqRoot_mld = create_node(
            'multiplyDivide',
            n=self.surface.replace('nbs', 'sqRoot_mld')
        )
        connect_attr(
            inverse_mld+'.outputX',
            sqRoot_mld+'.input1X',
            f=True
        )
        cmds.setAttr(sqRoot_mld+'.input2X', 0.5)
        cmds.setAttr(sqRoot_mld+'.operation', 3)

        # connect to joints
        for joint in self.ribbon_joint:
            connect_attr(ratio_mld+'.outputX', joint+'.scaleX', f=True)
            connect_attr(sqRoot_mld+'.outputX', joint+'.scaleY', f=True)
            connect_attr(sqRoot_mld+'.outputX', joint+'.scaleZ', f=True)

        # add object to list
        extend_list(self.other_nodes, [
                ald_u,
                ald_orig_u,
                ratio_mld,
                inverse_mld,
                sqRoot_mld
            ])

    def skin_surface(self):
        if not self.control_joint:
            # create control joints
            for n, input in enumerate(self.data_input_list):
                # create joint
                joint = create_node('joint', n=input.rpartition('.')[0]+'_jnt')

                # connect joint to input
                connect_attr(input, joint+'.offsetParentMatrix', f=True)

                # add joint to list
                if self.control_joint:
                    self.control_joint.append(joint)
                else:
                    self.control_joint = [joint]

            # create skin cluster
            skin_list = self.control_joint+[self.surface]
            ribbon_skin_cluster = cmds.skinCluster(
                skin_list,
                n=self.full_name+'_skc'
            )

        # create skin cluster
        skin_list = self.control_joint+[self.surface]
        ribbon_skin_cluster = cmds.skinCluster(
            skin_list,
            n=self.full_name+'_skc'
        )

        # set skin values
        for n, joint in enumerate(self.control_joint):
            if joint == self.control_joint[0]:
                cmds.skinPercent(
                    ribbon_skin_cluster,
                    f'{self.surface}.cv[{n}][0:3]',
                    tv=[(joint, 1)],
                    nrm=True
                )
                cmds.skinPercent(
                    ribbon_skin_cluster,
                    f'{self.surface}.cv[{n+1}][0:3]',
                    tv=[
                        (joint, 0.5),
                        (self.control_joint[n+1], 0.5)
                    ],
                    nrm=True
                )
            elif joint == self.control_joint[n-1]:
                cmds.skinPercent(
                    ribbon_skin_cluster,
                    f'{self.surface}.cv[{n+1}][0:3]',
                    tv=[
                        (joint, 0.5),
                        (self.control_joint[n-1], 0.5)
                    ],
                    nrm=True
                )
                cmds.skinPercent(
                    ribbon_skin_cluster,
                    f'{self.surface}.cv[{n+2}][0:3]',
                    tv=[(joint, 1)],
                    nrm=True
                )
            else:
                cmds.skinPercent(
                    ribbon_skin_cluster,
                    f'{self.surface}.cv[{n+1}][0:3]',
                    tv=[(joint, 1)],
                    nrm=True
                )

        # add skincluster to list
        append_list(self.other_nodes, ribbon_skin_cluster)
