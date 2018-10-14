class Writer(object):
    def __init__(self, builder):
        self.instructions = builder.capture()


    def write(self):
        result = []
        for instr in self.instructions:
            target    = instr.target
            name      = instr.name
            arguments = instr.arguments

            try:
                handler = getattr(self, "handle__" + name)
            except AttributeError:
                raise ValueError("Can't handle opcode '%s'" % name)

            ret = handler(target, arguments)
            if type(ret) is str:
                result.append(ret)
            else:
                assert type(ret) is list
                result.extend(ret)

        return result


    def get_type_name(self):
        raise NotImplementedError()


    def format_byte_const(self, x):
        if x & 0x80:
            x = (~x + 1) & 0xff
            x = -x

        return str(x)
