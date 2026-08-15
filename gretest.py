def greatest(a,b,c):
    if (a>b & a>c):
        return a
    elif (b>a & b>c):
        return b
    else:
        return c
a = int(input("enter the number"))
b = int(input("enter the number"))
c = int(input("enter the number"))
print(f" greatest number is : {greatest(a,b,c)}")


