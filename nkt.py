#!/usr/bin/python3

import argparse

# Generator for all subsets of exactly n items from a collection s.
def choose(s, n):
    # Base case: sets cannot have negative cardinality.
    if n < 0:
        return
    ns = len(s)
    # Base case: exactly enough elements to form a subset.
    if ns == n:
        yield set(s)
    # Base case: no extra elements to form subsets.
    if ns <= n:
        return
    # Extract an arbitrary element from the collection.
    ps = list(s)
    p = ps.pop()
    # Yield each full set not containing t.
    for t in choose(ps, n):
        yield t
    # Yield each full set containing t.
    for t in choose(ps, n - 1):
        t.add(p)
        yield t

# NKT game state.
class State(object):
    def __init__(self, n, k, t):
        # Number of tiles.
        self.n = n
        # Number of tiles in a win.
        self.k = k
        # Sum of tile values for a win.
        self.t = t
        # Value greater than any possible eval.
        self.winval = n * k + 1
        # Side on move.
        self.onmove = 0
        # Available tiles.
        self.avail = set(range(1, n+1))
        # Taken tiles for each side.
        self.taken = [set() for _ in range(2)]

    # Representation of game state for debugging.
    def __str__(self):
        onmove = self.onmove
        opp = 1 - onmove
        return "*" + str(self.taken[onmove]) + "\n" + str(self.taken[opp])

    # True iff the game is won by the given side.
    def won(self, side):
        taken = self.taken[side]
        for combo in choose(taken, self.k):
            if sum(combo) == self.t:
                return True
        return False

    # Make the side on move take tile p and switch sides.
    def move(self, p):
        onmove = self.onmove
        self.onmove = 1 - onmove
        assert p in self.avail
        self.avail.remove(p)
        assert p not in self.taken[onmove]
        self.taken[onmove].add(p)

    # Undo a move that took tile p.
    def unmove(self, p):
        onmove = 1 - self.onmove
        self.onmove = onmove
        assert p in self.taken[onmove]
        self.taken[onmove].remove(p)
        assert p not in self.avail
        self.avail.add(p)

    # Heuristic score: number of single tiles the
    # given side could take to win.
    def eval_side(self, onmove):
        choices = self.taken[onmove]
        wins = set()
        for c in choose(choices, self.k - 1):
            p = self.t - sum(c)
            if p in self.avail:
                wins.add(p)
        return len(wins)

    # Zero-sum heuristic score for side on move.
    def eval(self):
        me = self.eval_side(self.onmove)
        them = self.eval_side(1 - self.onmove)
        return me - them

    # Negamax search. If prune is true, search will stop
    # early when an immediate win is found. If the depth is
    # set to some non-negative integer, it will be used as a
    # search depth limit.
    def negamax(self, prune=True, depth=None):
        # Draw if no pieces remain
        if len(self.avail) == 0:
            return (0, None)
        # Use a heuristic evaluation if at depth limit.
        if depth == 0:
            return (self.eval(), None)

        # Search the space of possible moves.
        onmove = self.onmove
        result = -self.winval
        move = None
        if depth != None:
            depth -= 1
        for m in set(self.avail):
            # Do-undo.
            self.move(m)
            if self.won(onmove):
                # Do not search further on win position.
                r = self.winval
            else:
                # Recursively search for opponent value.
                r, _ = self.negamax(prune=prune, depth=depth)
                r = -r
            self.unmove(m)
            # Update best result found.
            if r >= result:
                move = m
                result = r
                if prune and result == self.winval:
                    return (result, move)
        # Return winning score and move.
        assert move != None
        return (result, move)

# Play out a game and show a trace.
def play(game, result, **args):
    while not game.won(1 - game.onmove):
        r, m = result
        if m == None:
            return

        if game.onmove == 0:
            side = "x"
        else:
            side = "o"

        if r == -game.winval:
            ev = "L"
        elif r == game.winval:
            ev = "W"
        else:
            ev = str(r)

        print(side, m, "({})".format(ev))
        game.move(m)
        result = game.negamax(**args)

# Process arguments.
parser = argparse.ArgumentParser(description='Play NKT.')
parser.add_argument('-n', type=int,
                    default=9, help='number of tiles')
parser.add_argument('-k', type=int,
                    default=3, help='number of tiles in win')
parser.add_argument('-t', type=int,
                    default=15, help='target sum')
parser.add_argument('--depth', '-d', type=int,
                    default=None, help='maximum search depth')
parser.add_argument('--unpruned', '-u',
                    action="store_false", help='prune on wins')
parser.add_argument('--game', '-g',
                    action="store_true", help='play out a game')
args = parser.parse_args()

# Run the search(es).
def go(game, **argv):
    r = game.negamax(**argv)
    print(r)
    if args.game:
        play(game, r, **argv)

game = State(args.n, args.k, args.t)
go(game, prune=args.unpruned, depth=args.depth)
