path = input("path:")

if path[-6] == "_":
    path1 = path[:-6] + ".xml"
    path2 = path
else:
    path1 = path
    path2 = path[:-4] + "_M" + ".xml"

f = open(path1, "r")
text1 = f.readlines()
f.close()
f = open(path2, "r")
text2 = f.readlines()
f.close()

t = 0
for i in range(len(text1)):
    if text1[i] != text2[i]:
        t += 1
        print(i + 1, text1[i], text2[i])
    if t >= 10:
        input("按enter鍵繼續:")
        t = 0
