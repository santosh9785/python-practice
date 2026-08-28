# class student():
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age
# s1 = student("santu", 19)
# s2 = student("rahul", 22)

# print(s1.name)
# print(s2.age)


class car():
    def __init__(self,carname,car_no,price_per_day,car_status='available',rented=0):
        self.carname = carname
        self.car_no = car_no
        self.price_per_day = price_per_day
        self.car_status = car_status
        self.rented = rented
      

    def car_details(self):
        print(f" The details of the  {self.carname}  is :- name: {self.carname},car_no:{self.car_no},car_status:{self.car_status},rented;{self.rented})")

    def car_update_status(self,new_status):
        self.car_status = new_status
        print(f"car {self.car_no} is updated to {self.car_status}")
    def car_rented_price(self):
        total_price = self.price_per_day * self.rented
        print(f"total price for{self.carname} is : {total_price}")

car1 = car("bmw",8055,999999,"rented",3)
car2 = car("mercedes",777,88888,"available",2)
car3 = car("lamborginii",6789,7777,"rented",1)

car1.car_update_status(new_status="not available")
car2.car_details()
car3.car_rented_price()



    



