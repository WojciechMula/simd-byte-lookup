from generator import Generator


class HigherNibbleConst(Generator):
    def __init__(self, values):
        super(HigherNibbleConst, self).__init__(values, "higher nibble constant")


    def can_generate(self):
        n = len(self.values)
        if n > 16:
            return False

        return len(set(self.higher_nibbles)) == 1


    def do_generate(self):
        listing = []
        
        lookup  = [self.values[0]] * 16
        for i, x in enumerate(self.values):
            hi = x & 0x0f
            lookup[hi] = x

        def format_lookup(name, values):
            assert len(values) == 16
            tmp = ', '.join(str(x) for x in values)
            return 'static const __m128i %s = _mm_setr_epi8(%s)' % (name, tmp)

        listing.append(format_lookup('lookup', lookup))
        listing.append('const __m128i lo  = _mm_and_si128(in, _mm_set1_epi8(0x0f))')
        listing.append('const __m128i val = _mm_shuffle_epi8(lookup, lo)')
        listing.append('const __m128i eq  = _mm_cmpeq_epi8(in, val)')
        listing.append('return eq');

        return listing

