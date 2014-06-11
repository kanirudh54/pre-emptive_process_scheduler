
import random
import math
import Gnuplot,Gnuplot.funcutils
import numpy
from heapq import heapify, heappush, heappop

class task:
    def __init__(self,taskid,deadline):
        self.deadline=deadline
        self.taskid=taskid


#######Heap Class########
        
class heap(task):

    
    #def down_heapify(self,i):
     #   if(2*i+1 == len(self.heap_list)-1):
      #      if(self.heap_list[i].deadline>self.heap_list[2*i+1].deadline):
       #         self.swap(i,2*i+1)
        #elif (2*i+1 < len(self.heap_list)-1):
         #   j=self.minimum(i,2*i+1,2*i+2)
          #  if(j!=i):
           #     self.swap(i,j)
            #    self.down_heapify(j)
            
   # def heapify(self):
    #    i=len(self.heap_list)//2 +1
     #   while (i>=0):
      #      self.down_heapify(i)
       #     i=i-1
    heap_list=[]
    def __init__(self,deadlines):
        j=0
        for i in deadlines:
            test=task(j,i)
            self.heap_list.append(test)
            j=j+1
        heapify(self.heap_list)
            
        
    def insert(self,taskDeadline,taskId):
        taskobj = task(taskId,taskDeadline)
        heappush(self.heap_list,taskobj)
        #self.heap_list.append(taskobj)
        #self.up_heapify(len(self.heap_list)-1)

    #def up_heapify(self,a):
     #   if(a > 0 and (self.heap_list[(a-1)//2].deadline > self.heap_list[a].deadline)):
      #      self.swap((a-1)//2,a)
       #     self.up_heapify((a-1)//2)
    
    def minimum(self,a,b,c):
        if(self.heap_list[a].deadline < self.heap_list[b].deadline):
            mini=a
        else:
            mini=b
            
        if(self.heap_list[c].deadline<self.heap_list[mini].deadline):
            mini=c
        return mini
    def swap(self,a,b):
        c=self.heap_list[a]
        self.heap_list[a]=self.heap_list[b]
        self.heap_list[b]=c
    def extract_min(self):
        rem=self.heap_list[0]
        self.swap(0,len(self.heap_list)-1)
        self.heap_list.remove(rem)
        heapify(self.heap_list)
        return rem
    
    
    def print_heap(self):
        for i in self.heap_list:
            print str(i.taskid) + " , " + str(i.deadline)
########################################################################################################################
###################################################### Round Robin #####################################################
########################################################################################################################
########################################################################################################################



def round_robin(eprime,proc,taskno,T):
    
    misses=0  # calculates the number of misses.
    ptr=0     # This represents the current task which is under consieration. 
    flag=[]   # This list tracks which tasks are assigned  in a particular time unit.
    rralloc=[]
    timeslots=[]
    
    TT=T*proc
    for i in range(0,taskno):
        flag.append(0)         # Initializing the flag list with 0
        timeslots.append(0)    # initialising the timeslots list with 0
        
    
    tempT=1   # tempT represents current time unit.
    currlag=0 # represents the current lag for a particular task considered in a particular time unit.
    flag2=0   # flag2 tracks the number of tasks that has been assigned in a particular time unit.
    
    while (tempT<=T):  
        for i in range(0,proc):
            while(timeslots[ptr]>=eprime[ptr]):  
               # print 'Hai'
                if (ptr<taskno-1):
                    ptr+=1
                else:
                    ptr=0
            
            if(flag[ptr]==0):
                timeslots[ptr]+=1
                rralloc.append(ptr)  # This is for storing the tasks allocated.
                flag2+=1
                flag[ptr]=1
            else:
                ptrtemp=ptr
                for j in range(0,taskno):
                    
                    if (ptrtemp<taskno-1):
                        ptrtemp+=1
                    else:
                        ptrtemp=0
                    if(flag[ptrtemp]==0 and timeslots[ptrtemp]<eprime[ptrtemp]):                      
                        timeslots[ptrtemp]+=1
                        rralloc.append(ptrtemp)
                        flag2+=1
                        flag[ptrtemp]=1
                        break

            if( ( i != (proc-1)) or ((i==proc-1) and (flag2==proc))):
                if (ptr<taskno-1):
                    ptr+=1
                else:
                    ptr=0
            
                

        for k in range(0,taskno):
            flag[k]=0  # re-initializing the flag list for the next time unit.
            currlag=((eprime[k]*tempT)/float(T))-timeslots[k]
            if(currlag>=1):
                misses += math.floor(currlag)
                                          
            
                
        tempT=tempT+1
        flag2=0
    
##    print 'rralloc = '+str(rralloc)
##    print 'timeslots = '+str(timeslots)
##    print "misses = " + str(misses)

    return misses


########################################################################################################################
######################################################Primitive Scheduler###############################################
########################################################################################################################
########################################################################################################################


def primitive_scheduler(eprime,proc,taskno,T):

    TT = T*proc
    rralloc = []
    timeslots = []
    totalLag = 0
    extractedTasks = []
    flag=0
    misses=0
    
    #initializing timeslots allocated with 0
    for i in range(0,taskno):
        timeslots.append(0)

    #initialize heap by calculating initial deadlines
        #calculating deadlines
    deadlines = []
    for i in range(0,taskno):
        deadlines.append( float(T) / eprime[i] )
            
    deadlinesHeap = heap(deadlines)
    
    for j in deadlinesHeap.heap_list:
        print j.taskid , j.deadline

    #assigning subtask for every one of T time slots
    currentTimeSlot = 0    #currentTimeSlot stores the current value of time slot
    while( currentTimeSlot < T ):

        i = 0        #i stores current id of processor for which we are allocating task
        while(i < proc):   #assigning task for every one of "proc" no. of processors
                flag=0
            #extracting a task and checking if it is completed.
                while ( True ):
                    if(len(deadlinesHeap.heap_list) > 0):
                        currentTask = deadlinesHeap.extract_min()
                        print 'currentTask.taskid = '+str(currentTask.taskid)
                        if ( timeslots[currentTask.taskid] < eprime[ currentTask.taskid ] ):
                            flag=1
                            break

                    else:
                        break
                if(flag==1):
                        
##                    print 'currentTask.taskid = ' + str(currentTask.taskid)
##                    #incrementing number of allocated time slots of extracted task
##                    print 'timeslots['+str(currentTask.taskid)+'] = '+str(timeslots[currentTask.taskid])
                    timeslots[currentTask.taskid] += 1
                

                    #storing task allocated in a list
                    rralloc.append( currentTask.taskid )

                    #calculating lag and hence number of misses
                    currentLag = ( (eprime[ currentTask.taskid ]* currentTimeSlot )/float(T)) - timeslots[ currentTask.taskid ]
##                    print 'currentLag = '+str(currentLag)

                    if(currentLag >= 1):
                        misses += math.floor(currentLag)
                    
                    #updating deadline of the task. This will be inserted after the for loop
                
                    currentTask.deadline += float(TT)/eprime[ currentTask.taskid ]

                    #storing updated task. This is to be inserted after the end of for loop
                    if( timeslots[currentTask.taskid] < eprime[ currentTask.taskid ]):
                        extractedTasks.append( currentTask )
##                    print 'Extracted Tasks are :'
##                    for j in range(0,len(extractedTasks)):
##                        print extractedTasks[j].taskid , extractedTasks[j].deadline

##                    print 'DealinesHeap is : '
##                    for j in deadlinesHeap.heap_list:
##                        print j.taskid , j.deadline

                    #incrementing value of i so as to assign task for next processor
                i += 1
            
                        #inserting updated tasks into the heap
        for j in range(0,len(extractedTasks)):
            deadlinesHeap.insert( extractedTasks[j].taskid , extractedTasks[j].deadline )

##            for i in range(0,len(extractedTasks)):
##                print extractedTasks[i].taskid , extractedTasks[i].deadline 
                #print extractedTasks

            #deleting elements from extractedTasks list so, that it will be useful for next iteration
        extractedTasks = []
        
        #incrementing currentTimeslot
        currentTimeSlot += 1

    for j in range(len(deadlinesHeap.heap_list)):
        deadlinesHeap.extract_min()
     
##    print rralloc
##    print " "
##    print 'timeslots = '+str(timeslots)
##    print " "
##    print 'totallag = '+str(totalLag)
    
    del(deadlinesHeap)
    return misses


########################################################################################################################
###################################################### Main part #######################################################
########################################################################################################################
########################################################################################################################

average_test= 10 # This variable tells how many cases we are considering to take an average for each and every test case.
processors=[]
tasks=[]
time=[]
misseslist=[]
misseslist_round=[]


readfile=open('generate.txt','r')

test = int(readfile.readline())

for testcase in range(0,test):

    cnt_for_average_test=0;

    avg1=0
    avgr=0
    
    proc=int(readfile.readline())
    processors.append(proc)
    print proc
    taskno=int(readfile.readline())
    tasks.append(taskno)
    print taskno
    T=int(readfile.readline())
    time.append(T)
    print T

    
    dumytask=taskno
    e=[]
    esum=0

    while (dumytask>0):
        rand=random.randrange(1,10)
        e.append(rand)
        esum=esum+rand
        dumytask=dumytask-1

    eprime=[]

    TT=T*proc

    eprimesum = 0
    for i in range(0,taskno-1):
        temp=(e[i]*TT)/esum
        if(temp!=0):
            eprime.append(temp)
            eprimesum += temp
        else:
            eprime.append(1)
            eprimesum += 1
                
    if(TT - eprimesum <= 0):       
         print 'The random values generated in this program could not satisfy the constraints of the problem.......'
         print 'So , this case is not considered in taking average values of misses. '
         eprime.append( TT - eprimesum )
         print 'eprime = '+str(eprime)
         print 'processors = '+str(processors)
         print 'tasks = '+str(tasks)
         print 'Simulation time of the processor = '+str(T)
                 
    else:     
        cnt_for_average_test += 1
        eprime.append( TT - eprimesum )
        print 'e = '+str(e)
        print 'esum = ' +str(esum)
##        eprime = [4, 2, 13, 11, 5, 8, 7, 11, 1, 11, 5, 12]
        print 'eprime = '+str(eprime)
        print "   "
        avg1 +=  primitive_scheduler(eprime,proc,taskno,T)
        avgr +=  round_robin(eprime,proc,taskno,T)
    if(cnt_for_average_test!=0):            
        avg1 /= cnt_for_average_test
        avgr /= cnt_for_average_test
        misseslist.append(math.floor(avg1))
        misseslist_round.append(math.floor(avgr))
        print cnt_for_average_test
        
    
##  
##    print " primitive scheduler results for " + `testcase` + "iteration"
##
##    print 'e = '+str(e)
##    print 'esum = ' +str(esum)
##    	
##    print 'eprime = '+str(eprime)
##    print "   "

print processors
print tasks
print time
print misseslist
print misseslist_round

readfile.close()
g= Gnuplot.Gnuplot(debug=1)
g.title('Scheduler')
d= Gnuplot.Data(processors,misseslist)
g.plot(d)
g.hardcopy('gp_test.ps', enhanced=1, color=1)
