from GeneratorBase import *


class HigherNibbleConst(GeneratorBase):
    def __init__(self, values):
        super(HigherNibbleConst, self).__init__(values, "higher nibble constant")


    def can_generate(self):
        n = len(self.values)
        if n > 16:
            return False

        return len(set(self.higher_nibbles)) == 1


    def do_generate(self, builder):
        lookup  = [self.values[0]] * 16
        for i, x in enumerate(self.values):
            hi = x & 0x0f
            lookup[hi] = x

        lookup = builder.add_lookup(lookup)
        shuffled = builder.add_shuffle(lookup, builder.get_parameter("lower_nibbles"))

        tmp = builder.add_compare_eq(builder.get_parameter("input"), shuffled)
        builder.update_result(tmp)

