from generator import Generator


class Naive(Generator):
    def __init__(self, values):
        super(Naive, self).__init__(values, "naive")


    def can_generate(self):
        return True


    def do_generate(self):
        listing = []

        def format_compare(const):
            return '_mm_cmpeq_epi8(in, _mm_set1_epi8(%d))' % const

        listing.append('__m128i eq = %s' % format_compare(self.values[0]))
        for x in self.values[1:]:
            listing.append('eq = _mm_or_si128(eq, %s)' % format_compare(x))

        listing.append('return eq');

        return listing

