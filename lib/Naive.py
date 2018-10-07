from GeneratorBase import *


class Naive(GeneratorBase):
    def __init__(self, values):
        super(Naive, self).__init__(values, "naive")


    def can_generate(self):
        return True


    def do_generate(self, builder):

        input = builder.get_parameter("input")
        for x in self.values:
            eq = builder.add_compare_eq_byte(input, x)
            builder.update_result(eq)

