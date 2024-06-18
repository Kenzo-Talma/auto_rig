# import maya.cmds as cmds


class Ribbon_Module:
    # init method
    def __init__(
            self,
            switch,
            space_input_list,
            name,
            side,
            compound_name=None,
            controls=3,
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
        self.controls = controls
        self.joint_number = joint_number
        self.periodic = periodic
        self.degree = degree
