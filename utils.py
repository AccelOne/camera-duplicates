class Roman:
    """
        Credit to Paul M. Winkler from The Python Cookbook.
        https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html
    """
    def int_to_roman(input):
        """ Convert an integer to a Roman numeral. """
        NUMS = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
        INTS = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        if not isinstance(input, int):
            raise(TypeError, "expected integer, got %s" % type(input))
        if not 0 < input < 4000:
            raise(ValueError, "Argument must be between 1 and 3999")
        result = []
        for i in range(len(INTS)):
            count = int(input / INTS[i])
            result.append(NUMS[i] * count)
            input -= INTS[i] * count
        return ''.join(result)


class Levenshtein:
    def distance(self, s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        if len(s0) == 0:
            return len(s1)
        if len(s1) == 0:
            return len(s1)

        v0 = [0] * (len(s1) + 1)
        v1 = [0] * (len(s1) + 1)

        for i in range(len(v0)):
            v0[i] = i

        for i in range(len(s0)):
            v1[0] = i + 1
            for j in range(len(s1)):
                cost = 1
                if s0[i] == s1[j]:
                    cost = 0
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            v0, v1 = v1, v0
        return v0[len(s1)]

