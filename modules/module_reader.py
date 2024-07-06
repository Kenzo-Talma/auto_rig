class Reader_Module:
    # init method
    def __init__(self, module):
        # mmodules
        self.modules = module

        # inputs
        self.space_input_type = None
        self.space_input = None
        self.data_input = None

        # outputs
        self.space_output_type = None
        self.space_output = None
        self.data_output = None

    def get_space_input(self):
        self.space_input_type = type(self.modules.space_input)
        self.space_input = self.modules.space_input

    def get_space_output(self):
        self.space_output_type = type(self.modules.space_input)
        self.space_output = self.modules.space_input
