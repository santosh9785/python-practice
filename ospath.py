import os

path = "/"   # current directory

contents = os.listdir(path)

for item in contents:
    print(item)