def sum_calc(m, n):
    i = 0

    if(n < 0):
        while(i < (-n)):
            m = m - 1
            i = i + 1

    else:
        while (i < n):
            m = m + 1
            i = i + 1


    return m


def divide_calc(m, n):

    i = 0

    if(n == 0):
        raise ValueError("Illegal division by zero")

    if(m < 0):
        if (n < 0):
            while (m < 0):
                m = m - n
                i = i + 1
        else:
            while (m < 0):
                m = m + n
                i = i - 1

    elif(m > 0):
        if(n < 0):
            while (m > 0):
                m = m + n
                i = i - 1
        else:
            while(m > 0):
                m = m - n
                i = i + 1


    return i

#1 entry point, 1 exit point

#print(divide(10, 0))

#print(divide(10, -2))

#print(divide(-10, 2))

#print(divide(-10, -2))

#print(divide(10, 2))

#m = True
#n = False

#result = -result if negativeResult else result

#print(m ^ n)






