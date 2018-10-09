class Range(object):
    __slots__ = ["lo", "hi"]

    def __init__(self, lo, hi):
        assert lo <= hi

        self.lo = lo
        self.hi = hi


    def __len__(self):
        return self.hi - self.lo + 1


    def __contains__(self, x):
        return self.lo <= x <= self.hi


    def __str__(self):
        if self.lo == self.hi:
            return "[%d]" % self.lo
        else:
            return "[%d,%d]" % (self.lo, self.hi)


class Ranges(object):
    def __init__(self):
        self.ranges = []
        self.last_added = None

    def add_point(self, x):
        if self.last_added is not None and x <= self.last_added:
            raise ValueError("Add points in ascending order")
        
        self.last_added = x

        if len(self.ranges) == 0:
            # no ranges, add the first one
            self.ranges.append(Range(x, x))
            return

        if self.ranges[-1].hi + 1 == x:
            # new points extends the last range
            self.ranges[-1].hi += 1
            return

        # a new range
        self.ranges.append(Range(x, x))


    def add_range(self, lo, hi):
        for x in range(lo, hi + 1):
            self.add_point(x)


    def remove_point(self, x):
        def get_range():
            for i, r in enumerate(self.ranges):
                if x in r:
                    return i, r

        res = get_range()
        if res is None:
            return

        index, range = res

        if range.lo == x:
            range.lo += 1
            if len(range) == 0:
                del self.ranges[index]

        elif range.hi == x:
            range.hi -= 1
            if len(range) == 0:
                del self.ranges[i]

        else:
            r1 = Range(range.lo, x - 1)
            r2 = Range(x + 1, range.hi)

            self.ranges[index] = r2
            self.ranges.insert(index, r1)

    def filter(self, predicate):
        self.ranges = [r for r in self.ranges if predicate(r)]


    def __str__(self):
        return "{%s}" % ', '.join(map(str, self.ranges))

