import sys
from math import ceil, log, pow


def int_bytes(i, radix):
    """
    Retrieves the minimum number of bytes required to identify an integer.

    :param radix: Number base
    :param i: Input integer
    :return: Number of bytes used to identify integer
    """
    l = 1
    while (absolute(i) >> l) > 0:
        l += 1
    return (((l) - (l % radix)) / radix) + 1


def absolute(num):
    """
    Custom implementation of abs(Num)
    :param num: Number to find absolute value of
    :return: absolute value of num
    """
    if num == (-sys.maxint) - 1:
        return sys.maxint
    return -num if num < 0 else num


def make_radixsort_class(
    setitem=None,
    setslice=None,
):
    if setitem is None:

        def setitem(list, item, value):
            list[item] = value

    if setslice is None:

        def setslice(list, slice, index):
            list[index : index + len(slice)] = slice

    class Radixsort(object):
        def __init__(self, list, listlength=None):
            self.list = list
            self.base = 6
            self.listlength = len(self.list)
            self.radix = int(pow(2, self.base))
            self.threshold = self.list[0]

        def list_abs_max(self, checkorder=False):
            """
            Returns the list item that will require the most bits to express. (the smallest or the largest value)
            Also optinoally returns booleans stating whether the list is ordered or reverse ordered
            :param checkorder: Flag that determines whether to check whether the list is ordered
            :return: the maximum absolute value in the list
            """

            assert len(self.list) != 0
            m = self.list[0]
            n = self.list[0]
            prev = self.list[0]
            (ordered, reverseordered) = (True, True)
            for i in xrange(1, len(self.list)):
                if self.list[i] > m:
                    m = self.list[i]
                if self.list[i] < n:
                    n = self.list[i]
                if checkorder:
                    ordered &= self.list[i] >= prev
                    reverseordered &= self.list[i] <= prev
                    prev = self.list[i]
            if checkorder:
                self.ordered = ordered
                self.reverseOrdered = reverseordered
            return m if absolute(m) > absolute(n) else n

        def setitem(self, item, value):
            setitem(self.list, item, value)

        def setslice(self, slice, index):
            setslice(self.list, slice, index)

        def insertion_sort(self, start, end):
            for step in xrange(start, end):
                key = self.list[step]
                j = step - 1
                while j >= 0 and key < self.list[j]:
                    self.setitem(j + 1, self.list[j])
                    j = j - 1
                self.setitem(j + 1, key)

        def reverseSlice(self, start=0, stop=0):
            if stop == 0:
                stop = self.listlength - 1
            while start < stop:
                i = self.list[start]
                j = self.list[stop]
                self.setitem(start, j)
                self.setitem(stop, i)
                start += 1
                stop -= 1

        def is_sorted(self, start=0, end=-1):
            end = end if end > -1 else self.listlength
            assert start >= 0
            assert end >= 0
            sortd, rsortd = True, True
            for i, el in enumerate(self.list[start + 1 : end]):
                # if i+start==end:break
                if el < self.list[start + i]:
                    sortd = False
                    if rsortd == False:
                        return sortd, rsortd
                if el > self.list[start + i]:
                    rsortd = False
                    if sortd == False:
                        return sortd, rsortd
            return sortd, rsortd

        def sort(self):
            if self.listlength < 2:
                return
            listmax = self.list_abs_max(checkorder=True)
            min_bytes = int_bytes(listmax, self.radix)
            if self.ordered:
                return
            if self.reverseOrdered:
                self.list.reverse()
                return
            bitno = int(int_bytes(listmax, 1))
            if min_bytes == int_bytes((-sys.maxint) - 1, self.base):
                uint_63 = ~((1 << bitno - 1) - 1)
            else:
                uint_63 = ~((1 << bitno) - 1)

            if bitno % self.base == 0 and bitno != int_bytes((-sys.maxint) - 1, 1):
                min_bytes += 1

            bucket_indexes = [(0, self.listlength)]
            buckets = [[] for _ in xrange(self.radix)]
            for k in xrange(min_bytes, -1, -1):
                shift = k * self.base
                temp_indexes = []
                for start, end in bucket_indexes:
                    if start + 1 == end:
                        continue
                    sortd, rsortd =  self.is_sorted(start, end)
                    if sortd:continue
                    if rsortd:
                        self.reverseSlice(start, end-1)
                        continue
                    if (end - start) < 212:
                        self.insertion_sort(start, end)
                        continue
                    for i in xrange(start, end):
                        sortkey = (self.list[i]) ^ uint_63
                        val = ((sortkey >> shift)) & self.radix - 1
                        buckets[val].append(self.list[i])
                    if len([len(b) for b in buckets if b != []]) == 1:
                        temp_indexes.append((start, end))
                        buckets = [[] for _ in buckets]
                        continue
                    index = 0
                    for bdx, b in enumerate(buckets):
                        if len(b) >= 1:
                            temp_indexes.append((start + index, start + index + len(b)))
                            self.setslice(b, start + index)
                        index += len(b)
                        buckets[bdx] = []
                bucket_indexes = temp_indexes
                if not bucket_indexes:
                    return

    return Radixsort
