import classes
def readfile(name):
    tmpArr = []
    f = open(name, 'r')
    (rows, cols) = f.readline().split(" ")
    for line in f:
        tmpArr.append([int(x) for x in line[:-1].split(" ")])
    f.close()
    return tmpArr

b1 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [0, 13, 14, 15]]
b2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

# graph = classes.Graph(b1, None)
# print(graph.board)
# print(graph.neighbors(graph.board))
# for b in graph.neighbors(graph.board):
#     print(b)
G = classes.Graph(b2, "LRUD")
solved = classes.BFS(G, b1)
if solved:
    print("SUCCESS")
    print(solved.path)
solved = classes.DFS(G, b1)
if solved:
    print("SUCCESS")
    print(solved.path)

