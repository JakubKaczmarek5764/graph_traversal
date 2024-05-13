import copy
import heapq
from collections import deque


# stany przetworzone sa na liscie stanow zamknietych
# odwiedzone to dlugosc listy stanow zamknietych + dlugosc listy stanow otwartych na koniec dzialania programu

def A_star(G, initial, heuristic):
    initial = Board(initial, z=find_zero(initial)) # utworzenie Boarda z poczatkowym satnem
    heuristic_func_dict = {
        "manh": G.manhattan_metric,
        "hamm": G.hamming_metric
    }
    chosen_metric = heuristic_func_dict[heuristic]
    open_states = []
    processed_states = set()
    max_depth = 0
    heapq.heappush(open_states, (0, 0, initial)) # heapq, czyli taka kolejka ze struktura drzewa, gdzie nody sa posortowane rosnaco wg priority i heappop zawsze sciaga node o najnizszym priority
    # w heapq kazdy parent node jest mniejszy lub rowny swoim child nodom, dzieki temu najmniejszy element zawsze jest na samej gorze
    count = 0  # zrobiony na potrzeby heapq, zeby bylo po czym sortowac jezeli priority jest rowne
    while open_states:
        current_node = heapq.heappop(open_states)[2] # w drugim indeksie jest Board
        max_depth = max(max_depth, current_node.depth) # update max_depth
        if current_node not in processed_states:
            if G.isgood(current_node):
                return [track_solution(current_node), len(open_states) + len(processed_states), len(open_states), max_depth]
            processed_states.add(current_node)
            for neighbor in G.neighbors(current_node): # iterowanie po sasiadach
                if neighbor not in processed_states:
                    priority = neighbor.depth + chosen_metric(neighbor)
                    heapq.heappush(open_states, (priority, count, neighbor))
                    count += 1
    return [-1, len(open_states) + len(processed_states), len(open_states), max_depth]


def DFS(G, initial):
    initial = Board(initial, z=find_zero(initial))
    if G.isgood(initial):
        return [track_solution(initial), 0, 0, 0]
    open_states = deque() # kolejka o dwoch koncach
    processed_states = set()
    max_depth = 0
    open_states.append(initial) # wkladamy elementy po prawej
    while open_states:
        current_node = open_states.pop() # sciagamy elementy tez z prawej
        max_depth = max(max_depth, current_node.depth)
        if current_node not in processed_states:
            if G.isgood(current_node):
                return [track_solution(current_node), len(open_states) + len(processed_states), len(processed_states), max_depth]
            processed_states.add(current_node)
            if current_node.depth < 20:
                for neighbor in reversed(G.neighbors(current_node)): # sasiedzi sa dodawani w odwroconej kolejnosci, zeby zachowac porzadek sciagania ich z kolejki
                    if neighbor not in processed_states:
                        open_states.append(neighbor)
    return [-1, len(open_states) + len(processed_states), len(processed_states), max_depth]


def BFS(G, initial):
    initial = Board(initial, z=find_zero(initial))
    if G.isgood(initial):
        return [track_solution(initial), 0, 0, 0]
    max_depth = 0
    open_states = deque()
    processed_states = set()
    open_states.append(initial) # wkladamy elementy po prawej
    processed_states.add(initial)
    while open_states:
        current_node = open_states.popleft() # sciagamy elementy z lewej

        for neighbors in G.neighbors(current_node):
            max_depth = max(max_depth, neighbors.depth)
            if neighbors not in processed_states:
                if G.isgood(neighbors):
                    return [track_solution(neighbors), len(open_states) + len(processed_states), len(processed_states), max_depth]
                open_states.append(neighbors)
                processed_states.add(neighbors)
    return [-1, len(open_states) + len(processed_states), len(processed_states), max_depth]


def track_solution(board):  # przyjmuje obiekt Board
    solution = ""
    while board.prev:
        solution += board.direction
        board = board.prev
    return solution[::-1]


def find_zero(board: list):  # przyjmuje zwyklego boarda
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
        for f in order: # tworzy tablice ze wskaznikami do funkcji
            self.function_order.append(function_order_dict[f])

    def isgood(self, board):
        return self.goal == board

    def neighbors(self, board):
        tmpArr = []
        for f in self.function_order: # stworzenie tablicy z sasiadami noda
            neighbor = f(board)
            if neighbor: tmpArr.append(neighbor) # dodawanie noda jezeli funkcja nie zwroci None
        return tmpArr


    def hamming_metric(self, board): # liczy ile cyfr nie jest jeszcze na swoich miejscach
        val = 0
        for row in range(len(board.b)):
            for col in range(len(board.b[row])):
                if board.b[col][row] != self.goal.b[col][row] and board.b[col][row] != 0:
                    val += 1
        return val

    def manhattan_metric(self, board): # sumuje dystans Manhattan
        val = 0
        for row in range(len(board.b)):
            for col in range(len(board.b[row])):
                if board.b[row][col] != 0:
                    goal_row = (board.b[row][col] - 1) // len(board.b)
                    goal_col = (board.b[row][col] - 1) % len(board.b[row])
                    val += abs(row - goal_row) + abs(col - goal_col)
        return val
    # funkcje przesuwajace zero
    def L(self, board):
        if board.z[1] != 0:
            tmpBoard = copy.deepcopy(board.b) # sklonowanie grida
            new_z = (board.z[0], board.z[1] - 1) # nowe koordynaty zera
            swap(tmpBoard, board.z, new_z) # przesuniecie zera
            return Board(tmpBoard, new_z, prev=board, direction="L", depth=board.depth + 1)

    def R(self, board):
        if board.z[1] != len(board.b[0]) - 1:
            tmpBoard = copy.deepcopy(board.b)
            new_z = (board.z[0], board.z[1] + 1)
            swap(tmpBoard, board.z, new_z)
            return Board(tmpBoard, new_z, prev=board, direction="R", depth=board.depth + 1)

    def U(self, board):
        if board.z[0] != 0:
            tmpBoard = copy.deepcopy(board.b)
            new_z = (board.z[0] - 1, board.z[1])
            swap(tmpBoard, board.z, new_z)
            return Board(tmpBoard, new_z, prev=board, direction="U", depth=board.depth + 1)

    def D(self, board):
        if board.z[0] != len(board.b) - 1:
            tmpBoard = copy.deepcopy(board.b)
            new_z = (board.z[0] + 1, board.z[1])
            swap(tmpBoard, board.z, new_z)
            return Board(tmpBoard, new_z, prev=board, direction="D", depth=board.depth + 1)

class Board:
    def __init__(self, b, z=(), prev=None, direction=None, depth=0):
        self.b = b # Board
        self.z = z # koordynaty zera w tuplu (x, y)
        self.prev = prev # wskaznik do poprzedniego Boarda
        self.direction = direction # kierunek od parenta do tego Boarda
        self.depth = depth

    def __eq__(self, other):
        return self.b == other.b
    def __str__(self):
        tmpStr = ""
        for row in self.b:
            tmpStr += row.__str__()
            tmpStr += "\n"
        return tmpStr

    def __hash__(self):
        return (tuple(x) for x in self.b).__hash__() # przeladowanie metody hash zeby dalo sie dodac obiekt do seta


def swap(board, i1, i2):
    board[i1[0]][i1[1]], board[i2[0]][i2[1]] = board[i2[0]][i2[1]], board[i1[0]][i1[1]]
