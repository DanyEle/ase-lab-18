from bdb import foo

import calculator as c



class FooCalculator:

    def __init__(self):
        pass

    def sum(self,m, n):
        return c.sum(m, n)

    def divide(self, m, n):
        return c.divide(m, n)


fooCalc = FooCalculator()

print(fooCalc.divide(10, 4));