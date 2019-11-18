#!/usr/bin/python3.7

class Some_class:
    def __init__(self):
        self.f1 = 'a'
        self.fun(10)

    def fun(self, b):
        self.b = b


a = Some_class()
print(a.__dict__)
