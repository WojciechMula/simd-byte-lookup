from GeneratorBase import *


class LowerNibbleConst(GeneratorBase):
    def __init__(self, values):
        super(LowerNibbleConst, self).__init__(values, "lower nibble constant")


    def can_generate(self):
        n = len(self.values)
        if n > 16:
            return False

        return len(set(self.lower_nibbles)) == 1


    def do_generate(self, builder):

        lookup  = [self.values[0]] * 16
        for i, x in enumerate(self.values):
            hi = x >> 4
            lookup[hi] = x

        lookup = builder.add_lookup(lookup)
        shuffled = builder.add_shuffle(lookup, builder.get_parameter("higher_nibbles"))

        tmp = builder.add_compare_eq(builder.get_parameter("input"), shuffled)
        builder.update_result(tmp)

