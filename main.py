import classes
import timeit
def readfile(name):
    tmpArr = []
    f = open(name, 'r')
    (rows, cols) = f.readline().split(" ")
    for line in f:
        tmpArr.append([int(x) for x in line[:-1].split(" ")])
    f.close()
    return tmpArr

b1 = [[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]]
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

