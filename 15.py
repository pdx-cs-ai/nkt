#!/usr/bin/python3

def choose(s, n):
    if n < 0:
        return
    if len(s) == n:
        yield s
    if len(s) <= n:
        return
    ps = list(s)
    p = ps.pop()
    ps = set(ps)
    for t in choose(ps, n):
        yield t
    for t in choose(ps, n - 1):
        u = set(t)
        u.add(p)
        yield u

class State(object):
    def __init__(self):
        self.onmove = 0
        self.avail = set(range(1, 10))
        self.taken = [set() for _ in range(2)]

    def won(self, side):
        taken = self.taken[side]
        for combo in choose(taken, 3):
            if sum(combo) == 15:
                return True
        return False

    def move(self, p):
        assert p in self.avail
        self.avail.remove(p)
        onmove = self.onmove
        self.taken[onmove].add(p)
        self.onmove = 1 - onmove

    def unmove(self, p):
        onmove = 1 - self.onmove
        assert p in self.taken[onmove]
        self.taken[onmove].remove(p)
        self.avail.add(p)
        self.onmove = onmove

    def negamax(self):
        # Draw if no pieces remain
        if len(self.avail) == 0:
            return 0
        onmove = self.onmove
        result = -1
        for p in self.avail:
            self.move(p)
            if self.won(onmove):
                result = 1
            else:
                result = max(result, -self.negamax())
            self.unmove(p)
        return result

game = State()
print(game.negamax())
