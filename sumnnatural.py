def sum(n):
    if (n==1):
        return 1
    return n+sum(n-1)

n = int(input("enter the number :"))
print(f"sum of 1st {n} natural numbers is :{sum(n)}")

