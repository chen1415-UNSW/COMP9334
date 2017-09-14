
# coding: utf-8


## k repersents for the job coming  from 1 - 10 
## m repersents for the queue slots from 1 - 20

import numpy as np
import matplotlib.pyplot as plt
import math

L_k = []
L_m = []
L_res = []

##general job lists and slots lists.
for i in range(1,21):
    L_k.append(i)
for i in range(1,21):
    L_m.append(i)

##The r is 20/6
r = 20/6

for k in L_k:
    ##if the k is less than 4 then we caculate only the first part.
    if k <= 4:
        p_0 = 0
        k_top = k
        L_temp = []
        ##while loop to caculate the sum
        while True:
            if k_top == -1:
                #caculate p_0 when all processe finished
                p_0 = (sum(L_temp))**-1
                break
            k_top_factory = math.factorial(k_top)
            p_temp = (1/k_top_factory) * r**k_top
            L_temp.append(p_temp)
            k_top = k_top - 1
        #caculate p_k 
        k_factory = math.factorial(k)
        p_k = p_0 * (1/k_factory) * r**k
        L_res.append((k,p_0,p_k))
        
    ##if the k is more than 4 then we caculate both part.
    if k > 4:
        for m in L_m:
            p_0 = 0
            k_top = 4
            L_temp = []
            ##first loop is to the caculate the first part under 4
            while True:
                if k_top == -1:
                    break
                k_top_factory = math.factorial(k_top)
                p_temp = (1/k_top_factory) * r**k_top
                L_temp.append(p_temp)
                k_top = k_top - 1
            k_top_2 = m + 4
            ##second loop is to the caculate the second part with k >= 5
            while True:
                if k_top_2 == 4:
                    #caculate p_0 when all processe finished
                    p_0 = (sum(L_temp))**-1
                    break
                p_temp_2 = 1/(24 * 4**(k_top_2-4)) * r**k_top_2
                L_temp.append(p_temp_2)
                k_top_2 = k_top_2 - 1
            #caculate p_k     
            p_k = p_0 * (1/(24 * 4**(k-4)) ) * r**k
            L_res.append((k,m,p_0,p_k))




## find the p_0
for i in L_res:
    if len(i) == 3:
        if i[0] == 4:
            P_0 = i[2]

##find all k = m+4
L_final = []
for i in L_res:
    if len(i) == 4:
        if i[0] == i[1] + 4:
            L_final.append((i[1],i[3]))
            
##Show the final result
Temp = []
for i in L_final:
    temp = P_0*0.5 - i[1]
    Temp.append((i[0],temp))

find_L = []
for i in Temp:
    if i[1] > 0:
        find_L.append(i[1])
num_min = min(find_L)
for i in Temp:
    if i[1] == num_min:
        M_num = i[0]
for i in L_final:
    if i[0] == M_num:
        print("Below is the result: ")
        print("m is:",i[0])
        print("p_k is:",i[1])

print('-------------------------------------------')
print()

## draw the plot chart
L_draw_x = []
L_draw_y = []
for i in L_res:
    if len(i) == 4:
        if i[0] == i[1] + 4:
            L_draw_x.append(i[1])
            L_draw_y.append(i[3])
plt.figure(figsize = {8,4})
plt.plot(L_draw_x,L_draw_y,"b--",linewidth=1)
plt.xlabel("Slots")
plt.ylabel("Probability of reject")
plt.title("Line plot")

print("Draw the chart")
plt.show()


## print the details
print('-------------------------------------------')
print('Print the details as followings: ')
print('k from 1 - 20 and m from 1 - 16')
print('-------------------------------------------')
for i in L_res:
    if len(i) == 3:
        print("k is:",i[0], end =', ')
        print("P(0) is:",i[1], end =', ')
        print("P(k) is:",i[2], end =' ')
        if i[0] == 4:
            P_0 = i[2]
        print()
        print('-------------------------------------------')
        
    if len(i) == 4:
        if i[0] == i[1] + 4:
            print("k is:",i[0], end =', ')
            print("m is:",i[1], end =', ')
            print("P(0) is:",i[2], end =', ')
            print("P(k) is:",i[3], end =' ')
            print()
            print('-------------------------------------------')

