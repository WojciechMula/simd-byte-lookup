from lib.AllNibblesDifferent import *
from lib.SomeNibblesRepeated import *
from lib.LowerNibbleConst import *
from lib.HigherNibbleConst import *
from lib.Naive import *
from lib.generate import generate, FunctionListing

import sys
import itertools


class Compiler(object):
    def __init__(self, values):
        self.values = values


    def compile(self):
        values = self.values[:]
        result = []

        while len(values) > 0:

            tmp = []
            tmp.append((
                find_const_nibble(values, lambda byte: byte & 0x0f),
                LowerNibbleConst
            ))

            tmp.append((
                find_const_nibble(values, lambda byte: byte >> 4),
                HigherNibbleConst
            ))

            tmp.append((
                findbest_unique(values),
                AllNibblesDifferent
            ))

            tmp.append((
                values[:8],
                SomeNibblesRepeated
            ))

            best = max(tmp, key=lambda item: self.cost(item[0]))
            result.append(best)
            for x in best[0]:
                values.remove(x)


        self.dump(result)

        return result


    def dump(self, data):
        dump(self.values)
        for subset, cls in data:
            print subset, cls, self.cost(subset)
            dump(subset)


    def cost(self, values):
        return len(values)


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
        #print len(stack), top

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
    compiler.compile()


if __name__ == '__main__':
    main()
