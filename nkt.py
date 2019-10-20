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
    def __init__(self, n, k, t):
        self.n = n
        self.k = k
        self.t = t
        self.winval = n * k + 1
        self.onmove = 0
        self.avail = set(range(1, n+1))
        self.taken = [set() for _ in range(2)]

    def __str__(self):
        onmove = self.onmove
        opp = 1 - onmove
        return "*" + str(self.taken[onmove]) + "\n" + str(self.taken[opp])

    def won(self, side):
        taken = self.taken[side]
        for combo in choose(taken, self.k):
            if sum(combo) == self.t:
                return True
        return False

    def move(self, p):
        onmove = self.onmove
        self.onmove = 1 - onmove
        assert p in self.avail
        self.avail.remove(p)
        assert p not in self.taken[onmove]
        self.taken[onmove].add(p)

    def unmove(self, p):
        onmove = 1 - self.onmove
        self.onmove = onmove
        assert p in self.taken[onmove]
        self.taken[onmove].remove(p)
        assert p not in self.avail
        self.avail.add(p)

    def eval_side(self, onmove):
        choices = self.taken[onmove]
        wins = 0
        for c in choose(choices, self.k - 1):
            p = self.t - sum(c)
            if p > 0 and p in self.avail:
                wins += 1
        return wins

    def eval(self):
        me = self.eval_side(self.onmove)
        them = self.eval_side(1 - self.onmove)
        return me - them

    def negamax(self, prune=True, depth=None):
        # Draw if no pieces remain
        if len(self.avail) == 0:
            return (0, None)
        if depth == 0:
            return (self.eval(), None)
        onmove = self.onmove
        result = -self.winval
        move = None
        if depth != None:
            depth -= 1
        for m in set(self.avail):
            self.move(m)
            if self.won(onmove):
                r = self.winval
            else:
                r, _ = self.negamax(prune=prune, depth=depth)
                r = -r
            self.unmove(m)
            if r >= result:
                move = m
                result = r
                if prune and result == self.winval:
                    return (result, move)
        assert move != None
        return (result, move)

def play(game, depth=None):
    while True:
        r, m = game.negamax(depth=depth)
        if game.onmove == 0:
            side = "x"
        else:
            side = "o"
        print(side, m, "({})".format(r))
        if m == None:
            break
        game.move(m)

game = State(9, 3, 15)
print(game.negamax(depth=4))
play(game, depth=4)
