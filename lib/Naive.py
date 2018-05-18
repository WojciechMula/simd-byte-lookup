from generator import Generator


class Naive(Generator):
    def __init__(self, values, builder):
        super(Naive, self).__init__(values, builder, "naive")


    def can_generate(self):
        return True


    def do_generate(self):
        bld = self.builder

        input = bld.get_parameter("input")
        for x in self.values:
            eq = bld.add_compare_eq_byte(input, x)
            bld.update_result(eq)

