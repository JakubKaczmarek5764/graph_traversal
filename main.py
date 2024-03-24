import classes
def readfile(name):
    tmpArr = []
    f = open(name, 'r')
    (rows, cols) = f.readline().split(" ")
    for line in f:
        tmpArr.append([int(x) for x in line[:-1].split(" ")])
    f.close()
    return tmpArr

b1 = readfile(r"puzzle/4x4_14_00001.txt")
b2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

# graph = classes.Graph(b1, None)
# print(graph.board)
# print(graph.neighbors(graph.board))
# for b in graph.neighbors(graph.board):
#     print(b)
solved = classes.BFS(b2,b1, "LRUD")
if solved:
    print("SUCCESS")
    print(solved.path)

