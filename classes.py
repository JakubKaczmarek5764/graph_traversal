import copy
import heapq
from collections import deque

# stany przetworzone sa na liscie stanow zamknietych
# odwiedzone to jest dlugosc listy stanow zamknietych + dlugosc listy stanow otwartych na koniec dzialania programu
# w przypadku dfsa algorytm moze nie znalezc rozwiazania, ignorujemy tylko rozwiazanie i dlugosc rozwiazania w wykresach, reszte informacji uwzgledniamy

def A_star(G, initial, heuristic):
    initial = Board(initial, z=find_zero(initial))
    heuristic_func_dict = {
        "manh": G.manhattan_metric,
        "hamm": G.hamming_metric
    }
    chosen_metric = heuristic_func_dict[heuristic]
    P = []
    T = set()
    max_depth = 0
    heapq.heappush(P, (0, 0, initial))
    count = 0 # zrobiony na potrzeby heapq, zeby bylo po czym sortowac jezeli priority jest rowne
    while P:
        v = heapq.heappop(P)[2]
        max_depth = max(max_depth, v.depth)
        if v not in T:
            if G.isgood(v):
                return (track_solution(v), len(P) + len(T), len(P), max_depth)
            T.add(v)
            for n in G.neighbors(v):
                if n not in T:
                    f = n.depth + chosen_metric(n)
                    heapq.heappush(P, (f, count, n))
                    count += 1
    return None
def DFS(G, initial):
    initial = Board(initial, z=find_zero(initial))
    if G.isgood(initial):
        return track_solution(initial)
    S = deque()
    T = set()
    S.append(initial)
    while S:
        v = S.pop()
        if v not in T:
            if G.isgood(v):
                return track_solution(v)
            T.add(v)
            if v.depth < 20:
                for n in reversed(G.neighbors(v)):
                    if n not in T:
                        S.append(n)
    return None




def BFS(G, initial):
    initial = Board(initial, z=find_zero(initial))
    if G.isgood(initial):
        return track_solution(initial)
    Q = deque()
    U = set()
    Q.append(initial)
    U.add(initial)
    while Q:
        v = Q.popleft()
        for n in G.neighbors(v):
            if n not in U:
                if G.isgood(n):
                    return track_solution(n)
                Q.append(n)
                U.add(n)
    return None

def track_solution(board): #przyjmuje obiekt Board
    solution = ""
    while board.prev:
        solution += board.direction
        board = board.prev
    return solution[::-1]
def find_zero(board: list): # przyjmuje zwyklego boarda
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                return (row, col)

class Graph:
    def __init__(self, goal, order="LRUD"):
        self.goal = Board(goal)
        self.function_order = []

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
        tmpArr = []
        for f in self.function_order:
            neighbor = f(board)
            if neighbor: tmpArr.append(neighbor)
        return tmpArr
       # return [f(board) for f in self.function_order] # nie bylo mi dane tak ladnie napisac smuti

    def hamming_metric(self, board):
        val = 0
        for row in range(len(board.b)):
            for col in range(len(board.b[row])):
                if board.b[col][row] == self.goal.b[col][row] and board.b[col][row] != 0:
                    val += 1
        return val
    def manhattan_metric(self, board):
        val = 0
        for row in range(len(board.b)):
            for col in range(len(board.b[row])):
                if board.b[row][col] != 0:
                    goal_row = (board.b[row][col] - 1) // len(board.b)
                    goal_col = (board.b[row][col] - 1) // len(board.b[row])
                    val += abs(row - goal_row) + abs(col - goal_col)
        return val
    def L(self, board):
        if board.z[1] != 0:
            tmpBoard = copy.deepcopy(board.b)
            new_z = (board.z[0], board.z[1] - 1)
            swap(tmpBoard, board.z, new_z)
            return Board(tmpBoard, new_z, prev=board, direction="L", depth=board.depth+1)

    def R(self, board):
        if board.z[1] != len(board.b[0]) - 1:
            tmpBoard = copy.deepcopy(board.b)
            new_z = (board.z[0], board.z[1] + 1)
            swap(tmpBoard, board.z, new_z)
            return Board(tmpBoard, new_z, prev=board, direction="R", depth=board.depth+1)
    def U(self, board):
        if board.z[0] != 0:
            tmpBoard = copy.deepcopy(board.b)
            new_z = (board.z[0] - 1, board.z[1])
            swap(tmpBoard, board.z, new_z)
            return Board(tmpBoard, new_z, prev=board, direction="U", depth=board.depth+1)
    def D(self, board):
        if board.z[0] != len(board.b) - 1:
            tmpBoard = copy.deepcopy(board.b)
            new_z = (board.z[0] + 1, board.z[1])
            swap(tmpBoard, board.z, new_z)
            return Board(tmpBoard, new_z, prev=board, direction="D", depth=board.depth+1)

class Board:
    def __init__(self, b, z=(), prev=None, direction=None, depth=0):
        self.b = b
        self.z = z
        self.prev = prev
        self.direction = direction
        self.depth=depth
    def __eq__(self, other):
        return self.b == other.b
    # def __lt__(self, other): # zrobiony na potrzeby heapq
    #     return False
    def __str__(self):
        tmpStr = ""
        for row in self.b:
            tmpStr += row.__str__()
            tmpStr += "\n"
        return tmpStr
    def __hash__(self):
        return tuple([tuple(x) for x in self.b]).__hash__() # dlaczego zrobienie listy i castowanie na tupla jest szybsze niż zrobienie tupla od razu?



def swap(board, i1, i2):
    board[i1[0]][i1[1]], board[i2[0]][i2[1]] = board[i2[0]][i2[1]], board[i1[0]][i1[1]]


