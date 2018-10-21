from collections import OrderedDict

Referenced = True

class Instruction(object):
    def __init__(self, target, name, arguments):
        self.target     = target
        self.name       = name
        self.arguments  = arguments


class Builder(object):
    def __init__(self):
        self.lookups        = OrderedDict()
        self.temporaries    = OrderedDict()
        self.parameters     = {}
        self.instructions   = []
        self.epilog         = []
        self.current_list   = self.instructions

        self.__create_parameter("input")
        self.__create_parameter("result")
        self.__create_parameter("zeros")
        self.__create_parameter("ones")
        self.__create_parameter("lower_nibbles")
        self.__create_parameter("higher_nibbles")

    
    def capture(self):
        result = []

        assert self.parameters["result"] == Referenced
        assert self.parameters["lower_nibbles"] == Referenced or \
               self.parameters["higher_nibbles"] == Referenced or \
               self.parameters["input"] == Referenced

        if self.parameters["zeros"]:
            result.append(Instruction("zeros", "declare_zeros", None))

        if self.parameters["ones"]:
            result.append(Instruction("ones", "declare_ones", None))
        
        if self.parameters["lower_nibbles"]:
            result.append(Instruction("lower_nibbles", "get_lower_nibbles", ("input",)))

        if self.parameters["higher_nibbles"]:
            result.append(Instruction("higher_nibbles", "get_higher_nibbles", ("input",)))


        for values, name in self.lookups.iteritems():
            result.append(Instruction(name, "declare_lookup", (values,)))

        result.extend(self.instructions)
        result.extend(self.epilog)
        result.append(Instruction(self.get_parameter("result"), "return", None))

        return result
 

    def __create_parameter(self, name):
        assert name not in self.parameters
        self.parameters[name] = False


    def has_epilog(self):
        return len(self.epilog) > 0


    def target(self, name):
        if name == 'main':
            self.current_list = self.instructions
        elif name == 'epilog':
            self.current_list = self.epilog
        else:
            raise ValueError("'%s' is not a valid list name" % name)


    def get_parameter(self, name):
        assert name in self.parameters
        self.parameters[name] = Referenced
        return name


    def add_lookup(self, values):
        values = tuple(values)
        assert len(values) == 16
        try:
            return self.lookups[values]
        except KeyError:
            name = "lookup%d" % len(self.lookups)
            self.lookups[values] = name
            return name

    
    def get_tmp(self):
        name = 't%d' % len(self.temporaries)
        self.temporaries[name] = True
        return name


    def byte_const(self, value):
        assert 0 <= value <= 255

        return self.add_raw('byte_const', (value,))


    def add_shuffle(self, lookup_name, vector):
        return self.add_raw('shuffle', (lookup_name, vector))


    def add_compare_eq(self, a, b):
        return self.add_raw('cmpeq', (a, b))


    def add_compare_eq_byte(self, a, value):
        assert value >= 0
        assert value < 256
        return self.add_raw('cmpeq_byte', (a, value))


    def add_compare_lt_byte(self, a, value):
        assert value >= 0
        assert value < 256
        return self.add_raw('cmplt_byte', (a, value))


    def add_and(self, a, b):
        return self.add_raw('and', (a, b))


    def add_or(self, a, b):
        return self.add_raw('or', (a, b))


    def add_andnot(self, a, b):
        return self.add_raw('andnot', (a, b))


    def add_xor(self, a, b):
        return self.add_raw('xor', (a, b))


    def add_select(self, x, t, f):
        return self.add_raw('select', (x, t, f))


    def update_result(self, value):
        target = self.get_parameter('result')
        self.current_list.append(Instruction(target, 'update_result', (value,)))
        return target


    def add_raw(self, name, args):
        target = self.get_tmp()
        self.current_list.append(Instruction(target, name, args))
        return target


def make_builder():
    builder = Builder()

    return builder
