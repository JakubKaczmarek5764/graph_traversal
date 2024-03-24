import copy
from collections import deque


def BFS(initial, goal, order):

    G = Graph(initial, goal, order)
    initial = G.board

    if G.isgood(initial):
        return initial
    Q = deque()
    U = set()
    Q.append(initial)
    U.add(initial)
    U.add(None) # bardzo pomocne, poniewaz G.neighbors zwraca None
    while Q:
        v = Q.popleft()
        for n in G.neighbors(v):
            if n not in U:
                if G.isgood(n):
                    return n
                Q.append(n)
                U.add(n)
    return None

class Graph:
    def __init__(self, board, goal, order="LRUD"):

        self.goal = Board(goal, {})

        self.z = self.find_zero(board)
        self.function_order = []
        self.board = Board(board, self.z)
        function_order_dict = {
            "L": self.L,
            "R": self.R,
            "U": self.U,
            "D": self.D
        }
        for f in order:
            self.function_order.append(function_order_dict[f])
    def isgood(self, board):
        return self.goal == board
    def neighbors(self, board):
        return [f(board) for f in self.function_order]

    def find_zero(self, board):
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == 0:
                    return {"row":row, "col":col}
    def L(self, board):
        tmpBoard = Board(copy.deepcopy(board.b), {"row": board.z["row"], "col": board.z["col"]}, copy.deepcopy(board.path))
        return tmpBoard.L()
    def R(self, board):
        tmpBoard = Board(copy.deepcopy(board.b), {"row": board.z["row"], "col": board.z["col"]}, copy.deepcopy(board.path))
        return tmpBoard.R()
    def U(self, board):
        tmpBoard = Board(copy.deepcopy(board.b), {"row": board.z["row"], "col": board.z["col"]}, copy.deepcopy(board.path))
        return tmpBoard.U()
    def D(self, board):
        tmpBoard = Board(copy.deepcopy(board.b), {"row": board.z["row"], "col": board.z["col"]}, copy.deepcopy(board.path))
        return tmpBoard.D()

class Board:
    def __init__(self, b, z={}, path=[]):
        self.b = b
        self.z = z
        self.path = path
    #appendy LR i UD sa na zmiane bo dzieki temu board przechowuje sciezke w druga strone
    def L(self):
        if self.z["col"] != 0:
            self.b[self.z["row"]][self.z["col"]], self.b[self.z["row"]][self.z["col"] - 1] = self.b[self.z["row"]][self.z["col"] - 1], self.b[self.z["row"]][self.z["col"]]
            self.z["col"] -= 1
            self.path.append("R")
            return self
    def R(self):
        if self.z["col"] != len(self.b) - 1:
            self.b[self.z["row"]][self.z["col"]], self.b[self.z["row"]][self.z["col"] + 1] = self.b[self.z["row"]][
                self.z["col"] + 1], self.b[self.z["row"]][self.z["col"]]
            self.z["col"] += 1
            self.path.append("L")
            return self
    def U(self):
        if self.z["row"] != 0:
            self.b[self.z["row"]][self.z["col"]], self.b[self.z["row"] - 1][self.z["col"]] = self.b[self.z["row"] - 1][
                self.z["col"]], self.b[self.z["row"]][self.z["col"]]
            self.z["row"] -= 1
            self.path.append("D")
            return self
    def D(self):
        if self.z["row"] != len(self.b) - 1:
            self.b[self.z["row"]][self.z["col"]], self.b[self.z["row"] + 1][self.z["col"]] = self.b[self.z["row"] + 1][
                self.z["col"]], self.b[self.z["row"]][self.z["col"]]
            self.z["row"] += 1
            self.path.append("U")
            return self
    def __eq__(self, other):
        return self.b == other.b
    def __str__(self):
        tmpStr = ""
        for row in self.b:
            tmpStr += row.__str__()
            tmpStr += "\n"
        return tmpStr
    def __hash__(self):
        return tuple([tuple(x) for x in self.b]).__hash__()
