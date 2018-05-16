from generator import Generator


class SomeNibblesRepeated(Generator):
    def __init__(self, values):
        super(SomeNibblesRepeated, self).__init__(values, "some nibbles repeated")


    def can_generate(self):
        n = len(self.values)
        if n > 8:
            return False

        return True


    def do_generate(self):
        listing = []

        lookup_lo = {}
        lookup_hi = {}
        for i in xrange(16):
            lookup_lo[i] = 0
            lookup_hi[i] = 0

        for i, x in enumerate(self.values):
            lo = x & 0xf
            hi = x >> 4
            
            bitmask = 1 << i

            lookup_lo[lo] |= bitmask
            lookup_hi[hi] |= bitmask
        

        def format_lookup(name, lookup):
            assert len(lookup) == 16
            tmp = ', '.join('0x%02x' % lookup[i] for i in xrange(16))
            return 'static const __m128i %s = _mm_setr_epi8(%s)' % (name, tmp)

        listing.append(format_lookup('lookup_lo', lookup_lo))
        listing.append(format_lookup('lookup_hi', lookup_hi))
        listing.append('const __m128i lo      = _mm_and_si128(in, _mm_set1_epi8(0x0f))')
        listing.append('const __m128i hi      = _mm_and_si128(_mm_srli_epi16(in, 4), _mm_set1_epi8(0x0f))')
        listing.append('const __m128i lo_mask = _mm_shuffle_epi8(lookup_lo, lo)')
        listing.append('const __m128i hi_mask = _mm_shuffle_epi8(lookup_hi, hi)')
        listing.append('const __m128i t0      = _mm_and_si128(lo_mask, hi_mask)')
        listing.append('const __m128i t1      = _mm_cmpeq_epi8(t0, _mm_setzero_si128())')
        listing.append('const __m128i eq      = _mm_xor_si128(t1, _mm_set1_epi32(-1))')
        listing.append('return eq');

        return listing


