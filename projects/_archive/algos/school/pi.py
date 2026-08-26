import math 
maximum_iterations = 20



def ATTEMPT1():
    def pi(co:int , iteration:int, val=1):
        if iteration == maximum_iterations:
            return val
        iteration += 1

        val = co+(1/pi((co*2)+1 , iteration , val))
        return val
    print(pi(3,0))



def ATTEMPT2():
    val = 0
    def pi(co , iterations):
        global val
        if iterations == maximum_iterations: return val
        iterations += 1

        val = co + (1/((co*2)+1))
        return pi((co*2)+1, iterations)
    print(pi(3,0))



def ATTEMPT3():
    co_effs = [3]
    val = 0
    i = 0
    while i != maximum_iterations:
        co_effs.append((co_effs[i]*2)+1)
        i+=1
        val += co_effs[i]
    print(val)






def ATTEMPT4():
    vals = [3] 
    i = 0
    positive = False
    while i != maximum_iterations:
        if positive: abv_z = 1 ; positive = False
        else: abv_z = -1 ; positive = True
        vals.append(  abv_z *  abs((vals[i]*2)+1)    )
        i+=1
    # print(vals)
    print("unfinished")



def ATTEMPT5():
    vals = []

    for num in range(2,maximum_iterations):
        prime = True
        for i in range(2,num):
            if (num%i==0):
                prime = False
        if prime:
           vals.append(num)
    vals = vals[1:]
    # print( "PRIME NUMBERS"  , vals)

    for i in range(0,len(vals), 1):
        # if vals[i] % 4 == 1:
        #     vals[i] = 1 + 1/vals[i] 
        # else:
        #     vals[i] = 1 - 1/vals[i] 
        
        vals[i] =  1/vals[i] 
        # print(vals[i])
    print(sum(vals))




def ATTEMPT6():
    # chudnovsky's formula
    factorial = lambda x : x * factorial(x-1) if x-1 > 0 else 1
    part1 = math.sqrt(10005) / 4270934400
    weird_e = 0
    positive = False
    k = 1
    while k != maximum_iterations:
        if positive:
            abs_z = 1
            positive = False
        else:
            abs_z = -1
            positive = True
        value = abs_z * (  (factorial(6*k)) / ((factorial(k)**3) * factorial(3*k) )  ) * ((13591409 + (545140134 * k)) / (640320**(3*k)) )
        weird_e += value
        k+=1
    print( part1 * weird_e   )





def ATTEMPT7():
    val = 3+(1/(7+(1/(15+(1/31)))))
    def idk(co, iteration):
        if iteration == maximum_iterations: return 0.0000000000000001
        iteration += 1
        return 1/idk((co*2)+1, iteration)

    print( 3 + idk(3, 0)   )




def ATTEMPT8():
    # val = 3+(1/(7+(1/15+(...))))
    def pi(co=3 , iteration=0):
        if iteration == maximum_iterations: return 0.00000000000000001
        iteration += 1

        return co + (1/pi((co*2)+1,iteration))

    out = pi()
    print(out)





if __name__ == "__main__":
    print("ATTEMPT: 1", end="\t") ;  ATTEMPT1()
    print("ATTEMPT: 2", end="\t") ;  ATTEMPT2()
    print("ATTEMPT: 3", end="\t") ;  ATTEMPT3()
    print("ATTEMPT: 4", end="\t") ;  ATTEMPT4()
    print("ATTEMPT: 5", end="\t") ;  ATTEMPT5()
    print("ATTEMPT: 6", end="\t") ;  ATTEMPT6()
    print("ATTEMPT: 7", end="\t") ;  ATTEMPT7()
    print("ATTEMPT: 8", end="\t") ;  ATTEMPT8()