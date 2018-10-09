from GeneratorBase import *


class Range(GeneratorBase):
    def __init__(self, values):
        super(Range, self).__init__(values, "range")


    def can_generate(self):
        if len(self.values) < 2:
            return False

        diffs = [b - a for a, b in zip(self.values, self.values[1:])]
        if diffs.count(1) != len(self.values) - 1:
            return False

        return True


    def do_generate(self, builder):

        input = builder.get_parameter("input")

        lo = self.values[0]
        above_hi = self.values[-1] + 1

        lt_lo       = builder.add_compare_lt_byte(input, lo)
        lt_above_hi = builder.add_compare_lt_byte(input, above_hi)

        in_range    = builder.add_andnot(lt_lo, lt_above_hi)

        builder.update_result(in_range)

