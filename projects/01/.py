print('''
Not (in=sel[0], out=Notsel0);
Not (in=sel[1], out=Notsel1);
And (a=Notsel0, b=Notsel1, out=if0);
And (a=Notsel0, b=sel[1], out=if1);
And (a=sel[0], b=Notsel1, out=if2);
And (a=sel[0], b=sel[1], out=if3);''')
for i in range(16):
    print(f"And (a=a[{i}], b=if0, out=a{i});")
    print(f"And (a=b[{i}], b=if1, out=b{i});")
    print(f"And (a=c[{i}], b=if2, out=c{i});")
    print(f"And (a=d[{i}], b=if3, out=d{i});")
    print(f"Or  (a=a{i}, b=b{i}, out=aOrb{i});")
    print(f"Or  (a=c{i}, b=d{i}, out=cOrd{i});")
    print(f"Or  (a=aOrb{i}, b=cOrd{i}, out=out[{i}]);")
