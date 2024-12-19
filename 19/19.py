class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input19.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]

        separator = lines.index('')
        self.towels = [ line.strip() for line in lines[:separator][0].split(",") ]
        self.towels = list(reversed(sorted(self.towels, key=lambda x: len(x))))

        self.patterns = [ line.strip() for line in lines[separator+1:] ]
        self.patterns = self.patterns

    def trymatch(self, towels, pattern):
        towelstry = [ towel for towel in towels if towel in pattern ]
        found_matches = 0
        if pattern in self.nmatches_by_pattern:
            return self.nmatches_by_pattern[pattern]
        for t in towelstry:
            if t == pattern:
                found_matches+=1
                if not self.part2:
                    break
            elif t == pattern[:len(t)]:
                _pattern = pattern[len(t):]
                nexttowels = [ t for t in towelstry if len(t) <= len(_pattern) ]
                extramatches = self.trymatch(nexttowels, _pattern)
                if extramatches:
                    found_matches+=extramatches
                    if not self.part2:
                        break
        self.nmatches_by_pattern[pattern] = found_matches
        return found_matches

    def solve(self, part2=False):
        self.part2=part2
        self.readinput()
        res = 0
        self.nmatches_by_pattern = {}
        for pattern in self.patterns:
            towelstry = [ towel for towel in self.towels if towel in pattern ]
            found_matches = 0
            for t in towelstry:
                if t == pattern:
                    print(t, pattern)
                    found_matches+=1
                    if not self.part2:
                        break
                elif t == pattern[:len(t)]:
                    _pattern = pattern[len(t):]
                    nexttowels = [ t for t in towelstry if len(t) <= len(_pattern) ]
                    extramatches = self.trymatch(nexttowels, _pattern)
                    if extramatches:
                        found_matches+=extramatches
                        if not self.part2:
                            break
            if pattern not in self.nmatches_by_pattern:
                self.nmatches_by_pattern[pattern] = found_matches
            res+=found_matches
        if not part2:
            print("Solved1:", res)
        else:
            print("Solved2:", res)

                

        



if __name__ == "__main__":
    s = PSolver()
    s.solve()
    s.solve(part2=True)
