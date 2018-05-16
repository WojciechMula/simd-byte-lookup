from generator import Generator


class AllNibblesDifferent(Generator):
    def __init__(self, values):
        super(AllNibblesDifferent, self).__init__(values, "all nibbles different")


    def can_generate(self):
        n = len(self.values)
        if n > 16:
            return False

        lower_nibbles = set(x & 0x0f for x in self.values)
        higer_nibbles = set(x & 0xf0 for x in self.values)

        return len(lower_nibbles) == n and len(higer_nibbles) == n


    def do_generate(self):
        # Note: I know there should be additional layer of abstraction here
        #       to gracefully handle different SIMD flavours. Now it's
        #       SSE-centered and ugly.
        listing = []
        
        lookup_lo = self.__generate_lookup_values((x & 0xf for x in self.values), 0x10)
        lookup_hi = self.__generate_lookup_values((x >> 4 for x in self.values),  0x20)

        def format_lookup(name, values):
            assert len(values) == 16
            tmp = ', '.join(str(x) for x in values)
            return 'static const __m128i %s = _mm_setr_epi8(%s)' % (name, tmp)

        listing.append(format_lookup('lookup_lo', lookup_lo))
        listing.append(format_lookup('lookup_hi', lookup_hi))
        listing.append('const __m128i lo     = _mm_and_si128(in, _mm_set1_epi8(0x0f))')
        listing.append('const __m128i hi     = _mm_and_si128(_mm_srli_epi16(in, 4), _mm_set1_epi8(0x0f))')
        listing.append('const __m128i lo_idx = _mm_shuffle_epi8(lookup_lo, lo)')
        listing.append('const __m128i hi_idx = _mm_shuffle_epi8(lookup_hi, hi)')
        listing.append('const __m128i eq     = _mm_cmpeq_epi8(lo_idx, hi_idx)')
        listing.append('return eq');

        return listing


    def __generate_lookup_values(self, values, invalid_value):
        assert invalid_value > len(self.values)

        result = [invalid_value] * 16
        for i, x in enumerate(values):
            assert x < 16
            result[x] = i

        return result

