from GeneratorBase import *


class SomeNibblesRepeated(GeneratorBase):
    def __init__(self, values):
        super(SomeNibblesRepeated, self).__init__(values, "some nibbles repeated")


    def can_generate(self):
        n = len(self.values)
        if n > 8:
            return False

        return True


    def do_generate(self, builder):
        listing = []

        lookup_lo = [0] * 16
        lookup_hi = [0] * 16

        for i, x in enumerate(self.values):
            lo = x & 0xf
            hi = x >> 4
            
            bitmask = 1 << i

            lookup_lo[lo] |= bitmask
            lookup_hi[hi] |= bitmask
        

        lookup_lo = builder.add_lookup(lookup_lo)
        lookup_hi = builder.add_lookup(lookup_hi)

        lo_mask = builder.add_shuffle(lookup_lo, builder.get_parameter("lower_nibbles"))
        hi_mask = builder.add_shuffle(lookup_hi, builder.get_parameter("higher_nibbles"))

        anded = builder.add_and(lo_mask, hi_mask)
        builder.update_result(anded)

        if not builder.has_epilog():
            builder.target('epilog')

            result = builder.get_parameter("result")
            zeros  = builder.get_parameter("zeros")
            ones   = builder.get_parameter("ones")
            tmp    = builder.add_compare_eq(result, zeros);
            builder.update_result(builder.add_xor(tmp, ones))
            builder.target('main')

