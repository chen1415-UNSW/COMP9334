import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as pl
import scipy as sp
import scipy.stats


# the class of creating the request object
class req:
    def __init__(self, arvTime, serTime, index):
        self.arvTime = arvTime
        self.serTime = serTime
        self.index = index
        self.L = []
        self.L.append([self.index, self.arvTime, self.serTime])
        
    def setSerTime(self,time):
        if time>= 0:
            self.serTime = time

    def record(self, currentTime, leftTime):
        self.currentTime = currentTime
        self.L.append([self.index, currentTime, leftTime])
        
        

#create the arrival list and allocate the coming requests to the single sever
def getArrival(requestes_number, seed, running_sever_num):
    #create the inter-arrival list
    random.seed(seed)
    Lambda = 7.2
    arrival_list = []
    inter_arrival_list = []
    for i in range(requestes_number):
        a1 = random.expovariate(Lambda)
        a2 = random.uniform(0.75, 1.17)
        inter_arrival_list.append(a1*a2)
        
    for j in range(len(inter_arrival_list)+1):
        if(j <= len(inter_arrival_list) and j > 0):
            arrival_list.append(sum(inter_arrival_list[:j]))
            
    # based on the running sever number, allocate the requests
    set_arrival = []
    if( len(arrival_list) <= running_sever_num):
        set_arrival.append(arrival_list[0])
    else:
        num_k = 0
        while(True):
            set_arrival.append(arrival_list[num_k])
            num_k = num_k + running_sever_num
            if(num_k > len(arrival_list)-1):
                break

    return set_arrival


#create the serviceTime list 
def getSeriveTime(requestes_number, frequency,seed):
    random.seed(seed)
    alpha1 = 0.43
    alpha2 = 0.98
    beta = 0.86
    gama = (1-beta) /( (alpha2**(1-beta)) - (alpha1**(1-beta)) ) # calculate the gama
    service_time_list = []
    for i in range(0,requestes_number):
        prob = random.uniform(0,1)
        # service time can be caculated by the euqation provided in PDF
        service_time = (prob*(1-beta)/gama + alpha1**(1-beta)) ** (1/(1-beta)) /frequency
        service_time_list.append(service_time)
    return service_time_list

def return_index(arrival, reqList):
    for i in reqList:
        if (i.arvTime == arrival):
            return i.index
    
# the function of simulating the processorSharing
def processorSharing(set_arriavl, service_time_list, record_List, re_L):
    reqList = []
    record_List = []
    responseTime = []    
    currentTime = 0
    lastTime = 0
    for i in range(len(set_arriavl)):
        # time equals the arrival time of the coming request
        currentTime = set_arriavl[i]
        #update the service Time of each request when one request arrival
        updateServiceTime(currentTime,lastTime,reqList, record_List)
        #record the last time of update
        lastTime = currentTime
        req_Object = req(currentTime, service_time_list[i], i+1)
        
        reqList.append(req_Object)
        
        req_Object_2 = req(currentTime, service_time_list[i], i+1)
        record_List.append(req_Object_2)
        
        length = len(reqList)
        #get the closest departure time of the current reqList
        arrival, depatureTime = getDepature(currentTime, reqList)
        while (len(reqList) >= 1 and i <= len(set_arriavl) - 2 and depatureTime < set_arriavl[i+1]):
            #deal with depature first if depature first
            currentTime = depatureTime
            updateServiceTime(currentTime,lastTime,reqList, record_List)
            single_response_time = depatureTime - arrival
            responseTime.append(single_response_time)
            
            index = return_index(arrival, reqList)
            re_L.append(index)
        
            lastTime = currentTime      
            del_object(arrival, reqList)
            length = len(reqList)
            if(length>0):
                arrival, depatureTime = getDepature(currentTime,reqList)
    #deal with the arrival, caculate the response time
    while(length>0):
        currentTime = depatureTime
        updateServiceTime(currentTime, lastTime, reqList, record_List)
        single_response_time = depatureTime - arrival
        responseTime.append(single_response_time)
        
        index = return_index(arrival, reqList)
        re_L.append(index)        
        
        lastTime = currentTime
        del_object(arrival, reqList)
        length = len(reqList)
        if(length>0):
            arrival, depatureTime = getDepature(currentTime, reqList)
    # caculate the average response time
    average_response_time = sum(responseTime)/len(responseTime)
    return responseTime, record_List  


# update the service time of each task when depature/arrival happens
def updateServiceTime(currentTime,lastTime, reqList, record_List):
    usedTime = currentTime - lastTime
    length = len(reqList)
    for i in range(length):
        if(reqList[i].arvTime != currentTime):
            a_time = reqList[i].serTime
            reqList[i].setSerTime( reqList[i].serTime - usedTime/length )
            
            for j in range(len(record_List)):
                if (record_List[j].index == reqList[i].index):
                    record_List[j].record(currentTime, a_time - usedTime/length)
            

# the function to del the certin req from the reqList
def del_object(arrival, reqList):
    length = len(reqList)
    for i in range(length):
        if(reqList[i].arvTime == arrival):
            del reqList[i]
            break

# caculate the depature time from the current reqList and return this task's arrival and departure time
def getDepature(currentTime, reqList):
    current_serive_time_list = []
    current_arrival_time_list = []
    length = len(reqList)
    for i in range(length):
        current_serive_time_list.append(reqList[i].serTime)
        current_arrival_time_list.append(reqList[i].arvTime)

    minSerTime = min(current_serive_time_list)
    depatureTime = minSerTime*length + currentTime
    
    index = current_serive_time_list.index(minSerTime)
    arrival = current_arrival_time_list[index]
    
    return arrival, depatureTime


#main function to run
def main(seed, requestes_number, Res):
    
    record_List = []
    Power = 2000
    for running_sever_num in range(6, 8): # simulate how one sever runs when severs change from 1-10
        re_L = []
                                  
        ave_Power = Power/running_sever_num  # calculate the average Power
        frequency = 1.25 + 0.31*(ave_Power/200-1) # calculate the clock frequency

        arrival_list = getArrival(requestes_number, seed, running_sever_num)  # create the arrival requests list
        print("len(arrival_list): ",len(arrival_list))
        print("Seed: ", seed)
        if( len(arrival_list) ==  5000 ):
            service_time_list = getSeriveTime(len(arrival_list), frequency, seed)  # create the service_time_list
            
    #code for test the case from the given PDF
    #        arrival_list = [1,2,3,5,15]
    #        service_time_list = [2.1, 3.3, 1.1, 0.5, 1.7]
            
            response_time, record_List = processorSharing(arrival_list, service_time_list, record_List, re_L)
            # calcuate the mean response time
            Res.append([running_sever_num, seed, sum(response_time[1000:])/4000])
            print("Res: ",Res)
            print("-----------------------")
    
    
           # code for Part III's figures.
            '''
            final_L = []
            for x in range(len(response_time)):
                temp = [re_L[x], response_time[x]]
                final_L.append(temp)
                
            sorted_final = sorted(final_L)
            L_x = []
            L_y = []
            for i in sorted_final:
                L_x.append(i[0])
                L_y.append(i[1])
                
    
            window = int(len(L_x)/10)
            L_y_smooth = []
            for i in range(len(L_y)):
                if(i == 0):
                    L_y_smooth.append(L_y[0])
                if(i>=1 and i <= window):
                    L_y_smooth.append(sum(L_y[:2*i-1])/len(L_y[:2*i-1]))
                if(i > window and i < len(L_y) - window):
                    if(len(L_y[i-window:i+window])!=0):
                        L_y_smooth.append(sum(L_y[i-window:i+window])/len(L_y[i-window:i+window]))
                        
            for j in range(len(L_y) - window, len(L_y)):
                L_y_smooth.append( sum(L_y[j-window:])/len(L_y[j-window:]) )
                
            
            print("response_time: ", L_y)
            print("L_x: ",L_x)
            print("Total requests: ", len(L_x))
            print("running_sever_num: ", running_sever_num)
            print("---------------------------------------")
     
           
            pl.plot(L_x, L_y_smooth)# use pylab to plot x and y
            pl.xlabel("Sever = 10, window = 500")# make axis labels
    
            pl.show()# show the plot on the screen
            return
            '''
                
                
'''
Code for drawing the Part II of the report
'''
#        x1 = []
#        y1 = []     
#        x2 = []
#        y2 = []
#        x3 = []
#        y3 = []
#        x4 = []
#        y4 = []
#        x5 = []
#        y5 = []
#        
#        for i in record_List:
#            for j in i.L:
#                if (j[0] == 1):
#                    x1.append(j[1])
#                    y1.append(j[2])
#                if (j[0] == 2):
#                    x2.append(j[1])
#                    y2.append(j[2])              
#                if (j[0] == 3):
#                    x3.append(j[1])
#                    y3.append(j[2])
#                if (j[0] == 4):
#                    x4.append(j[1])
#                    y4.append(j[2])
#                if (j[0] == 5):
#                    x5.append(j[1])
#                    y5.append(j[2])
#
#        pl.plot(x1, y1)# use pylab to plot x and y
#        pl.plot(x2, y2)
#        pl.plot(x3, y3)
#        pl.plot(x4, y4)
#        pl.plot(x5, y5)
# 
#        pl.title(’Plot of y vs. x’)# give plot a title
#        pl.xlabel("Sever = 1")# make axis labels
#        pl.ylabel("Response Time")
#
#        pl.show()# show the plot on the screen


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h 


#program start here
if __name__ == '__main__':
    # The total power budget is 2000 Watts
    seed = [] # set the seed as 1 
    # We assume that 5000 requests arrive in total as an example
    for num in range(1, 6):
        seed.append(num)
    
    
    Res = []
    L = [30000, 35000]
    for i in L:
        for j in seed:
            main(j, i, Res)
    
    print("-------------FINAL---------------")
    
    
#    Res = [[7, 1, 0.5116321231010089], [7, 2, 0.5107743698340516], [7, 3, 0.510227568195017], [7, 4, 0.5159230736141066], [7, 5, 0.5173359383526055], [8, 1, 0.5213357484235728], [8, 2, 0.5217415040644496], [8, 3, 0.521185149314534], [8, 4, 0.5232730605105432], [8, 5, 0.5228559150032616]]
   # Res = [[6, 1, 0.5151407559829395], [6, 2, 0.511333329754647], [6, 3, 0.5131594545931618], [6, 4, 0.5149850093538996], [6, 5, 0.5199387993237776], [7, 1, 0.5116321231010089], [7, 2, 0.5107743698340516], [7, 3, 0.510227568195017], [7, 4, 0.5159230736141066], [7, 5, 0.5173359383526055]]


'''
code for drawing the confidence interval
'''
##    print("Res ", Res)
##    print()
##    L_final = []
##    for i in Res:
##        for j in Res:
##            temp = []
##            if(i!=j and i[1]==j[1] and i[0]<j[0]):
##                temp.append( [ (i[0],j[0]), i[1], i[2]-j[2]] )
##            if temp!= []:
##                L_final.append(temp)
##    print("L_final: ",L_final)
##    L_sample_numbers = []    
##    for i in L_final:
##        for j in i:
##            L_sample_numbers.append(j)
##    print("L_sample_numbers: ",L_sample_numbers)
##    L_con = [L_sample_numbers[0][0]]
##    for i in L_sample_numbers:
##        L_con.append(i[2])
##
##    print("L_con: ",L_con)
##    L_c = L_con[1:]
##    mean,lower,upper = mean_confidence_interval(L_c)
##    print("mean: ", mean)
##    print("lower: ",lower)
##    print("upper: ",upper)
    
    

# code for darwing the table of ten severs.    
#    L_sum_10 = [[3, 0.9431998741692614], [4, 0.6214193964195144], [5, 0.5361260669998087], [6, 0.5151407559829395], [7, 0.5116321231010089], [8, 0.5213357484235728], [9, 0.531650211151551], [10, 0.5419250518302015]]
#    L_sum_10 = [[3, 0.9431998741692614], [3, 0.9555514255332669], [3, 0.9636733804885541], [3, 0.9563749488727658], [3, 0.9499981471639476], [3, 1.2701130695231557], [3, 1.13861623761934], [3, 1.1794604419986958], [3, 0.9617592486749754], [3, 1.0496061777636314], [4, 0.6214193964195144], [4, 0.6261741202475014], [4, 0.6126950142179729], [4, 0.6337637923954339], [4, 0.6152162389311573], [4, 0.6417182086999988], [4, 0.6285158515355861], [4, 0.6461404111633413], [4, 0.6397422920679833], [4, 0.6322219379018647], [5, 0.5361260669998087], [5, 0.5372019463875736], [5, 0.5387158075967878], [5, 0.5373881978620136], [5, 0.5438630552802676], [5, 0.5466285531226308], [5, 0.5541691512666013], [5, 0.5481140308476474], [5, 0.5547727089838759], [5, 0.5456612294065332], [6, 0.5151407559829395], [6, 0.511333329754647], [6, 0.5131594545931618], [6, 0.5149850093538996], [6, 0.5199387993237776], [6, 0.5205397259676579], [6, 0.5207000220960641], [6, 0.5201601288295161], [6, 0.5188495715037121], [6, 0.5174605856719611], [7, 0.5116321231010089], [7, 0.5107743698340516], [7, 0.510227568195017], [7, 0.5159230736141066], [7, 0.5173359383526055], [7, 0.5183102982247938], [7, 0.516646025560054], [7, 0.5169591273324498], [7, 0.5161736728018509], [7, 0.5148147303576566], [8, 0.5213357484235728], [8, 0.5217415040644496], [8, 0.521185149314534], [8, 0.5232730605105432], [8, 0.5228559150032616], [8, 0.5256582232810021], [8, 0.5233236312916536], [8, 0.5220316373074745], [8, 0.5235138953817005], [8, 0.5219142669403156], [9, 0.531650211151551], [9, 0.5312871794091575], [9, 0.53179678991586], [9, 0.5294811966783034], [9, 0.5328620264886158], [9, 0.5327920391565568], [9, 0.5313484991646956], [9, 0.5295176565971501], [9, 0.531772492448315], [9, 0.5303423845478041], [10, 0.5419250518302015], [10, 0.5420231833945358], [10, 0.5413700306453854], [10, 0.5419446379871177], [10, 0.5426403295452314], [10, 0.5442057417421029], [10, 0.5414132384250376], [10, 0.541697256317292], [10, 0.5435351788130347], [10, 0.5427153586708507]]
#    L3 = []
#    L4 = []
#    L5 = []
#    L6 = []
#    L7 = []
#    L8 = []
#    L9 = []
#    L10 = []
#    
#    for i in L_sum_10:
#        if i[0] == 3:
#            L3.append(i[1])
#        if i[0] == 4:
#            L4.append(i[1])    
#        if i[0] == 5:
#            L5.append(i[1])    
#        if i[0] == 6:
#            L6.append(i[1])    
#        if i[0] == 7:
#            L7.append(i[1])   
#        if i[0] == 8:
#            L8.append(i[1])
#        if i[0] == 9:
#            L9.append(i[1])            
#        if i[0] == 10:
#            L10.append(i[1])            
#    L_final = []
#    for i in range(3,11):
#        if i==3:
#            L_final.append([i,sum(L3)/10])
#        if i==4:
#            L_final.append([i,sum(L4)/10])            
#        if i==5:
#            L_final.append([i,sum(L5)/10]) 
#        if i==6:
#            L_final.append([i,sum(L6)/10])
#        if i==7:
#            L_final.append([i,sum(L7)/10])
#        if i==8:
#            L_final.append([i,sum(L8)/10])
#        if i==9:
#            L_final.append([i,sum(L9)/10])
#        if i==10:
#            L_final.append([i,sum(L10)/10])
#         
#    x = []
#    y = []
#
#    for i in L_final:
#        x.append(i[0])
#        y.append(i[1])
#    print("x: ",x)
#    print("y: ",y)
#
#    pl.plot(x,y,'o')
#    pl.xlabel("Sever Number")
#    pl.ylabel("Mean Response Time")
#    pl.show()
    
  


