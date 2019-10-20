# NKT
Bart Massey

This is a negamax solver in Python 3 for generalizations of
a two-player game known as "15" or "Pick 15" [pick15]. This
game is apparently due to George Pólya, but I found it in a
Martin Gardner book as a kid.

In Pick 15, players in turn pick tiles from a set of tiles
numbered 1..9. If any player manages to assemble a set of
3 tiles that add up to 15, that player wins. If all tiles
are exhausted without a win, the game is a draw.

In the NKT generalization there are N tiles (default 9), K
tiles in a win (default 3), and the total must be T (default
15). The game is otherwise identical.

This solver uses depth-first negamax search in the normal
way to select an optimal move and determine game value in an
arbitrary legal state of NKT. Options include early win
pruning and depth-limited search with a heuristic evaluator.
The solver will optionally play out a game.

Say `python3 nkt.py -h` for program arguments.

-----

[pick15]: [15: Combining Magic Squares and Tic-Tac-Toe](https://www.jstor.org/stable/pdf/10.5951/mathteacher.106.1.0034).
Joseph B. W. Yeo, *The Mathematics Teacher,* Vol. 106, No. 1 (August 2012), pp. 34-39
