from GeneratorBase import *


class SomeNibblesRepeated(GeneratorBase):
    def __init__(self, values, builder):
        super(SomeNibblesRepeated, self).__init__(values, builder, "some nibbles repeated")


    def can_generate(self):
        n = len(self.values)
        if n > 8:
            return False

        return True


    def do_generate(self):
        listing = []

        lookup_lo = [0] * 16
        lookup_hi = [0] * 16

        for i, x in enumerate(self.values):
            lo = x & 0xf
            hi = x >> 4
            
            bitmask = 1 << i

            lookup_lo[lo] |= bitmask
            lookup_hi[hi] |= bitmask
        

        lookup_lo = self.builder.add_lookup(lookup_lo)
        lookup_hi = self.builder.add_lookup(lookup_hi)

        lo_mask = self.builder.add_shuffle(lookup_lo, self.builder.get_parameter("lower_nibbles"))
        hi_mask = self.builder.add_shuffle(lookup_hi, self.builder.get_parameter("higher_nibbles"))

        anded = self.builder.add_and(lo_mask, hi_mask)
        self.builder.update_result(anded)

        if not self.builder.has_epilog():
            self.builder.target('epilog')

            result = self.builder.get_parameter("result")
            zeros  = self.builder.get_parameter("zeros")
            ones   = self.builder.get_parameter("ones")
            tmp    = self.builder.add_compare_eq(result, zeros);
            self.builder.update_result(self.builder.add_xor(tmp, ones))
            self.builder.target('main')

