class Cover(object):
    def __init__(self):
        self.__matrix = []
        for i in xrange(16):
            self.__matrix.append(['.'] * 16)

    def set(self, value, symbol):

        assert 0 <= value <= 255
        assert len(symbol) == 1

        lo = value & 0xf
        hi = value >> 4

        self.__matrix[hi][lo] = symbol

    def dump(self):
        rows = []

        # header
        line = ' '
        for i in xrange(16):
            line += ' %x' % i

        rows.append(line)

        # rows
        for i, row in enumerate(self.__matrix):
            line = '%x ' % i
            line += ' '.join(row)
            rows.append(line)


        return '\n'.join(rows)

