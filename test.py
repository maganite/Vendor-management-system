class A:
    def get_my_list(self):
        return self.my_list
    
    def add_data(self):
        self.my_list.append(8)

    @staticmethod
    def get_my_list2():
        return A.my_list



A.my_list = [9]

obj1 = A()
obj1.add_data()

A.get_my_list(obj1)

obj2 = A()
obj2.add_data()

print(A.my_list)
