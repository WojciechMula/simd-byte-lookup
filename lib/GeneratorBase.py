class GeneratorBase(object):
    def __init__(self, values, name):
        self.values  = values
        self.name    = name
        self.__validate()

        self.lower_nibbles  = [x & 0x0f for x in self.values]
        self.higher_nibbles = [x >> 4 for x in self.values]


    def __validate(self):
        for i, x in enumerate(self.values):
            if x < 0 or x > 255:
                raise ValueError('value #%d = %d outside range [0..255]' % (i, x))

        tmp = set(self.values)
        if len(self.values) != len(tmp):
            raise ValueError('Values must be unique')


    def can_generate(self):
        return False


    def generate(self, builder):
        if not self.can_generate():
            raise ValueError('Generator is not able to generate code for given values')
        
        return self.do_generate(builder)


    def do_generate(self):
        raise NotImplementedError()

