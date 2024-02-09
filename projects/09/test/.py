from random import randint as ri

def generatemaze0(lx, ly):
    maze = []
    for x in range(lx):
        a = []
        for y in range(ly):
            if x % 2 == 0 or y % 2 == 0:
                a.append(1)
            else:
                a.append(0)
        maze.append(a)
    a = [[1, 1]]
    b = [[2, 1, 1, 0],[1, 2, 0, 1]]
    c = [0, 1, 0, -1]
    d = [1, 0, -1, 0]
    while True:
        i = b[ri(0, len(b) - 1)]
        if [i[0] + i[2], i[1] + i[3]] in a:
            b.remove(i)
        else:
            a.append([i[0] + i[2], i[1] + i[3]])
            b.remove(i)
            maze[i[0]][i[1]] = 0
            for e in range(4):
                f = [i[0] + i[2] + c[e], i[1] + i[3] + d[e]]
                if f[0] <= lx - 2 and f[0] >= 1 and f[1] <= ly - 2 and f[1] >= 1:
                    if maze[i[0] + i[2] + c[e]][i[1] + i[3] + d[e]] == 1:
                        b.append([i[0] + i[2] + c[e], i[1] + i[3] + d[e], c[e], d[e]])
        for x in range(lx):
            for y in range(ly):
                if a.count([x, y]) > 1:
                    a.remove([x, y])
        if len(a) == ((lx - 1) / 2) * ((ly - 1) / 2):
            maze[1][1] = 2
            maze[lx - 2][ly - 2] = 3
            return maze

def generate_maze1(lx, ly):
    maze = []
    for x in range(lx):
        row = []
        for y in range(ly):
            if x % 2 == 0 or y % 2 == 0:
                row.append(1)
            else:
                row.append(0)
        maze.append(row)

    a = [[1, 1]]
    b = [[2, 1, 1, 0],[1, 2, 0, 1]]
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    c = []

def draw(maze):
    for i in maze:
        for j in i:
            if j == 0:
                print("  ",end="")
            else:
                print("11",end="")
        print()

maze = generatemaze0(31,63)
draw(maze)
maze = generate_maze1(31,63)
draw(maze)