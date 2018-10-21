from GeneratorBase import *


class Universal(GeneratorBase):
    def __init__(self, values):
        super(Universal, self).__init__(values, "universal")


    def can_generate(self):
        return True


    def _prepare_lookups(self):
        self.lookup_0_7  = [0x00] * 16
        self.lookup_8_15 = [0x00] * 16

        for value in self.values:
            lo_nibble = value & 0x0f
            hi_nibble = value >> 4

            if hi_nibble < 8:
                bit = 1 << hi_nibble
                assert (bit < 256)
                self.lookup_0_7[lo_nibble] |= bit
            else:
                bit = 1 << (hi_nibble - 8)
                assert (bit < 256)
                self.lookup_8_15[lo_nibble] |= bit


        self.lookup_bitpos = [None] * 16
        for i in xrange(0, 8):
            self.lookup_bitpos[i] = 1 << i

        for i in xrange(8, 16):
            self.lookup_bitpos[i] = 1 << (i - 8)
    

    def do_generate(self, builder):

        self._prepare_lookups()

        lookup_0_7    = builder.add_lookup(self.lookup_0_7)
        lookup_8_15   = builder.add_lookup(self.lookup_8_15)
        lookup_bitpos = builder.add_lookup(self.lookup_bitpos)

        lo_nibble   = builder.get_parameter("lower_nibbles")
        
        bitset_0_8  = builder.add_shuffle(lookup_0_7, lo_nibble)
        bitset_8_15 = builder.add_shuffle(lookup_8_15, lo_nibble)

        less_than_8 = builder.add_compare_lt_byte(builder.get_parameter("higher_nibbles"), 8)

        bitset      = builder.add_select(less_than_8, bitset_0_8, bitset_8_15)
        bitpos      = builder.add_shuffle(lookup_bitpos, builder.get_parameter("higher_nibbles"))

        t0          = builder.add_and(bitset, bitpos)
        t1          = builder.add_compare_eq(t0, bitpos);

        builder.update_result(t1)



class Universal2(Universal):
    def __init__(self, values):
        super(Universal2, self).__init__(values)
        self.name = "universal2"


    def do_generate(self, builder):

        self._prepare_lookups()

        lookup_0_7    = builder.add_lookup(self.lookup_0_7)
        lookup_8_15   = builder.add_lookup(self.lookup_8_15)
        lookup_bitpos = builder.add_lookup(self.lookup_bitpos)

        input       = builder.get_parameter("input")
        msb_mask    = builder.byte_const(0x80)

        lo_nibble1  = builder.add_and(input, builder.byte_const(0x8f))
        lo_nibble2  = builder.add_xor(lo_nibble1, msb_mask)
        
        bitset_0_8  = builder.add_shuffle(lookup_0_7, lo_nibble1)
        bitset_8_15 = builder.add_shuffle(lookup_8_15, lo_nibble2)

        bitset      = builder.add_or(bitset_0_8, bitset_8_15)
        bitpos      = builder.add_shuffle(lookup_bitpos, builder.get_parameter("higher_nibbles"))

        t0          = builder.add_and(bitset, bitpos)
        t1          = builder.add_compare_eq(t0, bitpos);

        builder.update_result(t1)
