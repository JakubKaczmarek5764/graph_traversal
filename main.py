import classes
import sys
from timeit import default_timer as timer


def readfile(name):
    tmpArr = []
    f = open(name, 'r')
    (rows, cols) = f.readline().split(" ")  # liczba wierszy i kolumn
    for line in f:
        tmpArr.append([int(x) for x in line[:-1].split(" ")])
    f.close()
    return ((rows, cols), tmpArr)


def savefile(solution, solution_file, stats, stats_file):
    f = open(solution_file, 'w')
    for line in solution:
        f.write(str(line) + "\n")
    f.close()
    f2 = open(stats_file, 'w')
    for line in stats:
        f2.write(str(line) + "\n")
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

    (size, board) = readfile(puzzle_file)

    # generowanie docelowego stanu ukladanki
    goal = [
        [i * int(size[1]) + j + 1 for j in range(int(size[1]))] for i in range(int(size[0]))
    ]
    goal[-1][-1] = 0

    if algorithm == classes.A_star:
        G = classes.Graph(goal)
        start = timer()
        output = algorithm(G, board, order_heuristic)
        end = timer()
    else:  # algorytmy slepe
        G = classes.Graph(goal, order_heuristic)
        start = timer()
        output = algorithm(G, board)
        end = timer()
    output.append("{:.3f}".format(end - start))
    solution = (len(output[0]), output[0]) if output[0] != -1 else (-1,)
    savefile(solution, solution_file, [len(output[0]) if output[0] != -1 else -1] + output[1:], stats_file)


main()
