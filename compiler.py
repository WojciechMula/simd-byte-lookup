from lib.AllNibblesDifferent import *
from lib.SomeNibblesRepeated import *
from lib.LowerNibbleConst import *
from lib.HigherNibbleConst import *
from lib.Naive import *
from lib.generate import FunctionListing
from lib.builder import make_builder
from lib.sse_writer import SSEWriter

import sys
import itertools

class Candidate(object):
    __slots__ = ["values", "cls", "instruction_count", "cost"]

    def __init__(self, values, cls):
        self.values = values
        self.cls    = cls

        self.instruction_count  = self.__calculate_instruction_count()
        self.cost               = self.__calculate_cost()


    def __str__(self):
        return '%s [%d/%0.2f=%0.3f] %s' % (self.values, len(self.values), self.instruction_count, self.cost, self.cls)


    def __calculate_instruction_count(self):
        builder   = make_builder()
        generator = self.cls(self.values)
        generator.generate(builder)

        return len(builder.instructions) + 0.5 * len(builder.lookups)


    def __calculate_cost(self):

        items_covered = len(self.values)
        instr_per_item = float(items_covered) / self.instruction_count

        return instr_per_item


class Compiler(object):
    def __init__(self, values):
        self.values = values


    def compile(self):
        values = self.values[:]
        result = []

        while len(values) > 0:

            tmp = []
            tmp.append(Candidate(
                find_const_nibble(values, lambda byte: byte & 0x0f),
                LowerNibbleConst
            ))

            tmp.append(Candidate(
                find_const_nibble(values, lambda byte: byte >> 4),
                HigherNibbleConst
            ))

            tmp.append(Candidate(
                findbest_unique(values),
                AllNibblesDifferent
            ))

            tmp.append(Candidate(
                values[:8],
                SomeNibblesRepeated
            ))

            for i in xrange(1, len(values)):
                tmp.append(Candidate(
                    values[:i],
                    Naive
                ))

            if len(values) == 1:
                tmp.append(Candidate(
                    [values[0]],
                    Naive
                ))

            best = max(tmp, key=lambda item: item.cost)
            result.append(best)
            for x in best.values:
                values.remove(x)

            self.dump(tmp)

        self.dump(result)

        return result


    def dump(self, data):
        dump(self.values)
        for item in data:
            print item
            #dump(subset)





def find_const_nibble(values, keyfun):
    nibbles = {}
    for x in values:
        nibble = keyfun(x)
        assert nibble < 16
        nibbles[nibble] = nibbles.get(nibble, 0) + 1

    result = None
    for nibble, count in nibbles.iteritems():
        if result is None or count > result[1]:
            result = (nibble, count)

    if result is not None:
        nibble = result[0]
        return [x for x in values if keyfun(x) == nibble]


class Stack(object):
    def __init__(self, index):
        self.index   = index
        self.used_lo = set()
        self.used_hi = set()
        self.values  = []


    def __str__(self):
        return '<%d, %s, %s, %s>' % (self.index, self.used_hi, self.used_hi, self.values)


def iter_unique_subset(values):
    stack = [Stack(-1)]

    n = len(values)

    while len(stack) > 0:
        top = stack[-1]

        top.index += 1
        if top.index == n:
            yield top.values
            stack.pop()
            continue

        x = values[top.index]

        lo = x & 0x0f
        if lo in top.used_lo:
            continue

        hi = x >> 4
        if hi in top.used_hi:
            continue

        s = Stack(-1)

        s.values = top.values[:]
        s.values.append(x)

        s.used_lo = top.used_lo.copy()
        s.used_hi = top.used_hi.copy()

        s.used_lo.add(lo)
        s.used_hi.add(hi)

        stack.append(s)


def findbest_unique(values):

    best = None
    for subset in iter_unique_subset(values):
        if best is None or len(subset) > len(best):
            best = subset

    return best


def dump(values):
    matrix = []
    for i in xrange(16):
        matrix.append([0] * 16)

    for x in values:
        lo = x & 0xf
        hi = x >> 4

        matrix[hi][lo] = 1

    for row in matrix:
        for x in row:
            if x:
                print 'x',
            else:
                print '.',
        print


def parse_args():
    v = set()
    for arg in sys.argv[1:]:
        prefix = '--string='
        if arg.startswith(prefix):
            for c in arg[len(prefix):]:
                v.add(ord(c))
        else:
            try:
                v.add(int(arg))
            except ValueError:
                v.add(int(arg, 16))

    return list(v)

def main():
    #v = [ord(c) for c in "0123456789()+-*=<>[]{}/%!"]
    #v = [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66]
    v = parse_args()

    compiler = Compiler(v)
    data = compiler.compile()
    builder = make_builder()
    for item in data:
        generator = item.cls(item.values)
        generator.generate(builder)

    writer = SSEWriter(builder)
    print '\n'.join(writer.write())

if __name__ == '__main__':
    main()
