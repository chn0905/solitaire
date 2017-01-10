SUB = lambda a, b: (a[0]-b[0], a[1]-b[1])
GET = lambda axis, a: a[0] if axis == "x" else a[1]

CHECKMOVES = {
        "K": lambda vec: vec in tuple( (x,y) for y in (-1, 0, 1) for x in (-1, 0, 1) ),
        "Q": lambda vec: (GET("x", vec) == 0 or GET("y", vec) == 0) or abs(GET("x", vec)) == abs(GET("y", vec)),
        "R": lambda vec: GET("x", vec) == 0 or GET("y", vec) == 0,
        "B": lambda vec: abs(GET("x", vec)) == abs(GET("y", vec)),
        "H": lambda vec: not (GET("x", vec) == 0 or GET("y", vec) == 0) and abs(GET("y", vec)) + abs(GET("x", vec)) == 3,
        "P": lambda vec: vec in ((-1, 1), (1, 1))
        }


class ChessPiece(object):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def isAllowed(self, pos):
        return pos != self.pos and CHECKMOVES[self.name](SUB(pos, self.pos))


class Board(object):
    def __init__(self, pieces):
        self.pieces = [ ChessPiece(name, pos) for (name, pos) in pieces ]
        self.killed = []

    def getPiece(self, pos):
        for piece in self.pieces:
            if piece.pos == pos:
                return piece

    def getPositions(self):
        return tuple( piece.pos for piece in self.pieces )

    def kill(self, piece):
        self.pieces.remove(piece)
        self.killed.append(piece)

    def revive(self, dead):
        self.killed.remove(dead)
        self.pieces.append(dead)


class Solver(object):
    def __init__(self, pieces):
        self.board = Board(pieces)
        self.solution = []

    def isSolved(self):
        return "K" not in [piece.name for piece in self.board.killed] and len(self.board.pieces) == 1

    def getMoves(self):
        return [ (piece, pos) for pos in self.board.getPositions() for piece in self.board.pieces if piece.isAllowed(pos) ]

    def findSolution(self):
        if self.isSolved():
            return True
        moves = self.getMoves()
        if not moves:
            return False
        for piece, pos in moves:
            self.solution.append("{} {} to {}".format(piece.name, piece.pos, pos))
            dead = self.board.getPiece(pos)
            self.board.kill(dead)
            orig = piece.pos
            piece.pos = pos

            if self.findSolution():
                return True
            else:
                piece.pos = orig
                self.board.revive(dead)
                self.solution.pop()
        return False

