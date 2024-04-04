import classes
import sys
import timeit

def readfile(name):
    tmpArr = []
    f = open(name, 'r')
    _ = f.readline().split(" ") # liczba wierszy i kolumn
    for line in f:
        tmpArr.append([int(x) for x in line[:-1].split(" ")])
    f.close()
    return tmpArr
def savefile(solution, solution_file, stats, stats_file):
    f = open(solution_file, 'w')
    for line in solution:
        f.write(line)
    f.close()
    f2 = open(stats_file, 'w')
    for line in stats:
        f2.write(line)
    f2.close()

algo_dict = {
    "bfs": classes.BFS,
    "dfs": classes.DFS,
    "astr": classes.A_star
}


def main():
    algorithm = algo_dict[sys.argv[1]]
    order_heuristic = sys.argv[2]
    puzzle_file = sys.argv[3]
    solution_file = sys.argv[4]
    stats_file = sys.argv[5]

    output = []
    if algorithm == classes.A_star:
        G = classes.Graph(b2)
        output = algorithm(G, readfile(puzzle_file), order_heuristic)
    else:
        G = classes.Graph(b2, order_heuristic)
        output = algorithm(G, readfile(puzzle_file))


# b1 = [[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]]
b1 = readfile(name)
b2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

# graph = classes.Graph(b1, None)
# print(graph.board)
# print(graph.neighbors(graph.board))
# for b in graph.neighbors(graph.board):
#     print(b)

G = classes.Graph(b2, "LRUD")
solved = classes.A_star(G, b1, "hamm")
if solved:
    print("SUCCESS")
    print(solved)
solved = classes.DFS(G, b1)
if solved:
    print("SUCCESS")
    print(solved)
solved = classes.BFS(G, b1)
if solved:
    print("SUCCESS")
    print(solved)


print(timeit.timeit('''
import classes

b1 = [[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]]
b2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
G = classes.Graph(b2, "LRUD")
solved = classes.DFS(G, b1)
solved = classes.BFS(G, b1)
''',number=1))

