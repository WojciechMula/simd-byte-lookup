from writer import Writer

class SSEWriter(Writer):
    def __init__(self, builder):
        super(SSEWriter, self).__init__(builder)
        self.type = '__m128i'

        self.result_action = 'set'


    def get_type_name(self):
        return self.type


    def handle__get_lower_nibbles(self, target, attr):
        input = attr[0]
        return 'const %s %s = _mm_and_si128(%s, _mm_set1_epi8(0x0f))' % (self.type, target, input)


    def handle__get_higher_nibbles(self, target, attr):
        input = attr[0]
        return 'const %s %s = _mm_and_si128(_mm_srli_epi16(%s, 4), _mm_set1_epi8(0x0f))' % (self.type, target, input)


    def handle__declare_zeros(self, target, attr):
        return 'const %s %s = _mm_setzero_si128()' % (self.type, target)


    def handle__declare_ones(self, target, attr):
        return 'const %s %s = _mm_set1_epi32(-1)' % (self.type, target)


    def handle__declare_lookup(self, target, attr):
        values = attr[0]
        tmp = ', '.join(self.format_byte_const(x) for x in values)

        return 'static const %s %s = _mm_setr_epi8(%s)' % (self.type, target, tmp)


    def handle__byte_const(self, target, attr):
        value = attr[0]

        return 'const %s %s = _mm_set1_epi8(%s)' % (self.type, target, self.format_byte_const(value))
    

    def handle__shuffle(self, target, attr):
        lookup = attr[0]
        vector = attr[1]

        return 'const %s %s = _mm_shuffle_epi8(%s, %s)' % (self.type, target, lookup, vector)

    
    def __binary_fun(self, target, function, arg1, arg2):
        return 'const %s %s = %s(%s, %s)' % (self.type, target, function, arg1, arg2)

    
    def __ternary_fun(self, target, function, arg1, arg2, arg3):
        return 'const %s %s = %s(%s, %s, %s)' % (self.type, target, function, arg1, arg2, arg3)


    def handle__cmpeq(self, target, attr):
        a = attr[0]
        b = attr[1]

        return self.__binary_fun(target, '_mm_cmpeq_epi8', a, b)


    def handle__cmpeq_byte(self, target, attr):
        vector = attr[0]
        byte   = attr[1]

        const_vector = '_mm_set1_epi8(%s)' % self.format_byte_const(byte)

        return self.__binary_fun(target, '_mm_cmpeq_epi8', vector, const_vector)


    def handle__cmplt_byte(self, target, attr):
        vector = attr[0]
        byte   = attr[1]

        const_vector = '_mm_set1_epi8(%s)' % self.format_byte_const(byte)

        return self.__binary_fun(target, '_mm_cmplt_epi8', vector, const_vector)


    def handle__and(self, target, attr):
        a = attr[0]
        b = attr[1]

        return self.__binary_fun(target, '_mm_and_si128', a, b)


    def handle__or(self, target, attr):
        a = attr[0]
        b = attr[1]

        return self.__binary_fun(target, '_mm_or_si128', a, b)


    def handle__andnot(self, target, attr):
        a = attr[0]
        b = attr[1]

        return self.__binary_fun(target, '_mm_andnot_si128', a, b)


    def handle__xor(self, target, attr):
        a = attr[0]
        b = attr[1]

        return self.__binary_fun(target, '_mm_xor_si128', a, b)


    def handle__select(self, target, attr):
        cond  = attr[0]
        true  = attr[1]
        false = attr[2]

        return self.__ternary_fun(target, '_mm_blendv_epi8', false, true, cond)


    def handle__update_result(self, target, attr):
        
        if self.result_action == 'set':
            self.result_action = 'update'

            return '%s %s = %s' % (self.type, target, attr[0])

        elif self.result_action == 'update':
            return '%s = _mm_or_si128(%s, %s)' % (target, target, attr[0])


    def handle__return(self, result, unused):
        
        return 'return %s' % result
