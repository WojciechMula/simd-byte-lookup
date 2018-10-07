from GeneratorBase import *


class AllNibblesDifferent(GeneratorBase):
    def __init__(self, values):
        super(AllNibblesDifferent, self).__init__(values, "all nibbles different")


    def can_generate(self):
        n = len(self.values)
        if n > 16:
            return False

        lower_nibbles = set(x & 0x0f for x in self.values)
        higer_nibbles = set(x & 0xf0 for x in self.values)

        return len(lower_nibbles) == n and len(higer_nibbles) == n


    def do_generate(self, builder):
        lookup_lo_table = self.__generate_lookup_values((x & 0xf for x in self.values), 0x10)
        lookup_hi_table = self.__generate_lookup_values((x >> 4 for x in self.values),  0x20)

        lookup_lo = builder.add_lookup(lookup_lo_table)
        lookup_hi = builder.add_lookup(lookup_hi_table)

        lo_idx = builder.add_shuffle(lookup_lo, builder.get_parameter("lower_nibbles"))
        hi_idx = builder.add_shuffle(lookup_hi, builder.get_parameter("higher_nibbles"))
        
        tmp = builder.add_compare_eq(lo_idx, hi_idx)
        builder.update_result(tmp)


    def __generate_lookup_values(self, values, invalid_value):
        assert invalid_value > len(self.values)

        result = [invalid_value] * 16
        for i, x in enumerate(values):
            assert x < 16
            result[x] = i

        return result

