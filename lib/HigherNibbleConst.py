from GeneratorBase import *


class HigherNibbleConst(GeneratorBase):
    def __init__(self, values, builder):
        super(HigherNibbleConst, self).__init__(values, builder, "higher nibble constant")


    def can_generate(self):
        n = len(self.values)
        if n > 16:
            return False

        return len(set(self.higher_nibbles)) == 1


    def do_generate(self):
        lookup  = [self.values[0]] * 16
        for i, x in enumerate(self.values):
            hi = x & 0x0f
            lookup[hi] = x

        bld = self.builder

        lookup = bld.add_lookup(lookup)
        shuffled = bld.add_shuffle(lookup, bld.get_parameter("lower_nibbles"))

        tmp = bld.add_compare_eq(bld.get_parameter("input"), shuffled)
        bld.update_result(tmp)

