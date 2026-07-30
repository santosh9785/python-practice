def order(*items, **customer):
    print("items")
    for i in items:
       print(i)
       print()
    

    print("customor details")
    for key,value in customer.items():
        print(key,value)
        print()

order("laptop","mouse","mobile",name = "santu", age = 19,sgpa = 8.43)