class Generator(object):
    def __init__(self, values, name):
        self.values = values
        self.name   = name
        self.__validate()


    def __validate(self):
        for i, x in enumerate(self.values):
            if x < 0 or x > 255:
                raise ValueError('value #%d = %d outside range [0..255]' % (i, x))

        tmp = set(self.values)
        if len(self.values) != len(tmp):
            raise ValueError('Values must be unique')


    def can_generate(self):
        raise False


    def generate(self):
        if not self.can_generate():
            raise ValueError('Generator is not able to generate code for given values')
        
        return self.do_generate()


    def do_generate(self):
        raise NotImplementedError()

