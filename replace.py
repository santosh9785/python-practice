word = "santu"

with open("santu.txt", "r") as f:
    c = f.read()

cnew = c.replace(word, "charan")

with open("santu.txt", "w") as f:
    f.write(cnew) 