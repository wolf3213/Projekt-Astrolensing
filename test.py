#!/usr/bin/python3.7

def fun(n):
    return [ i**2 for i in range(n) ]


def fun1(n):
    a = []
    for i in range(n):
        #a.append(i**2)
        try:
            a.append(i**2)
        except:
            pass

    return a


inp = 1000000

#try:
#    fun(inp)
#except:
#    print(inp)


fun1(inp)

