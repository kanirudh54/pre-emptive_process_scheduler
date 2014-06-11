
import random
import math
import Gnuplot,Gnuplot.funcutils
import numpy

class task :
    def __init__(self,taskid,deadline,):
        self.taskid=taskid
        self.deadline=deadline
        
#################Heap Class###############

class heap(task):
    heap_list=[]
    
    def __init__(self,deadline_list):                                                        # a constructor for heapifying a given list 
        j=0                                                                              
        for i in deadline_list:                                                              # for a given list of deadline_list we take it into heap 
            test=task(j,i)                                                               # as objects with ids and deadline_list 
            self.heap_list.append(test)
            j=j+1
        self.heapify()
                   
    def heapify(self):                                                                   # general heap datastructure algorithm     
        i=len(self.heap_list)//2 +1
        while(i>=0):
            self.heap_down(i)
            i = i-1

    def swap(self,a,b):                                                                  # swap used in removing the min element   
        c=self.heap_list[a]
        self.heap_list[a]=self.heap_list[b]
        self.heap_list[b]=c

    def heap_down(self,i):                                                               # after swaping we down heap to adjust the heap 
        if(2*i+1 == len(self.heap_list)-1):
            if(self.heap_list[i].deadline>self.heap_list[2*i+1].deadline):
                self.swap(i,2*i+1)
        elif (2*i+1 < len(self.heap_list)-1):
            j=self.minimum(i,2*i+1,2*i+2)
            if(j!=i):
                self.swap(i,j)
                self.heap_down(j)
    
    def heap_up(self,a):
        if(a > 0 and (self.heap_list[(a-1)//2].deadline > self.heap_list[a].deadline)):  # after inserting a new element we heap it up 
            self.swap((a-1)//2,a)
            self.heap_up((a-1)//2)
    
    def insert(self,taskId,taskDeadline,):                                               # insert a new element
        taskobj = task(taskId, taskDeadline)
        self.heap_list.append(taskobj)
        self.heap_up(len(self.heap_list)-1)
     
    def minimum(self,a,b,c):
        if(self.heap_list[a].deadline < self.heap_list[b].deadline):
            mini=a
        else:
            mini=b
            
        if(self.heap_list[c].deadline<self.heap_list[mini].deadline):
            mini=c
        return mini
         
    def extract_min(self):                                                               # extracting min element 
        rem=self.heap_list[0]
        self.swap(0,len(self.heap_list)-1)
        self.heap_list.remove(rem)
        self.heap_down(0)
        return rem
    
    def print_heap(self):                                                                # printing the heap 
        for i in self.heap_list:
            print str(i.taskid) + " , " + str(i.deadline)

################## Round Robin #################
def round_robin(eprime,proc,taskno,T):
    
    miss_no=0                                                                           # calculates the number of miss_no.
    ptr=0                                                                               # This represents the current task which is under consieration. 
    flag=[]                                                                             # This list tracks which tasks are assigned  in a particular time unit.
    round_alloc=[]
    timeslots=[]
    
    TT=T*proc
    for i in range(0,taskno):
        flag.append(0)                                                                  # Initializing the flag list with 0
        timeslots.append(0)                                                             # initialising the timeslots list with 0
        
    
    tempT=1                                                                             # tempT represents current time unit.
    currlag=0                                                                           # represents the current lag for a particular task considered in a particular time unit.
    flag2=0                                                                             # flag2 tracks the number of tasks that has been assigned in a particular time unit.
    
    while (tempT<=T):  
        for i in range(0,proc):
            while(timeslots[ptr]>=eprime[ptr]):  
                if (ptr<taskno-1):
                    ptr+=1
                else:
                    ptr=0
            
            if(flag[ptr]==0):
                timeslots[ptr]+=1
                round_alloc.append(ptr)                                                     # This is for storing the tasks allocated.
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
                        round_alloc.append(ptrtemp)
                        flag2+=1
                        flag[ptrtemp]=1
                        break

            if( ( i != (proc-1)) or ((i==proc-1) and (flag2==proc))):
                if (ptr<taskno-1):
                    ptr+=1
                else:
                    ptr=0
            
                

        for k in range(0,taskno):
            flag[k]=0                                                                    # re-initializing the flag list for the next time unit.
            currlag=((eprime[k]*tempT)/float(T))-timeslots[k]
            if(currlag>=1):
                miss_no += math.floor(currlag)
                                          
        tempT=tempT+1
        flag2=0

    return miss_no



#########Primitive Scheduler###############
def primitive_scheduler(eprime,proc,taskno,T):

    Total_time = T*proc
    round_alloc = []
    timeslots = []
    totalLag = 0
    extracted_tasks = []
    flag=0
    miss_no=0
    
    for i in range(0,taskno):                                                            #initializing timeslots allocated with 0
         timeslots.append(0)

    
    deadline_list = []                                                                       #initialize heap by calculating initial deadline_list
        
    for i in range(0,taskno):                                                            #calculating deadline_list
        deadline_list.append( float(T) / eprime[i] ) 
            
    heap_dead = heap(deadline_list)
    
    for j in heap_dead.heap_list:
        print j.taskid , j.deadline

                                                                                            
    currentTimeSlot = 0                                                                 #currentTimeSlot stores the current value of time slot
    while( currentTimeSlot < T ):                                                       #assigning subtask for every one of T time slots
        i = 0                                                                           #i stores current id of processor for which we are allocating task
        while(i < proc):                                                                #assigning task for every one of "proc" no. of processors
                flag=0
            
                while ( True ):                                                         #extracting a task and checking if it is completed.
                    if(len(heap_dead.heap_list) > 0):
                        currentTask = heap_dead.extract_min()
                      
                        if ( timeslots[currentTask.taskid] < eprime[ currentTask.taskid ] ):
                            flag=1
                            break

                    else:
                        break
                if(flag==1):
                    timeslots[currentTask.taskid] += 1
                    round_alloc.append( currentTask.taskid )                                #storing task allocated in a list
                    currentLag = ( (eprime[ currentTask.taskid ]* currentTimeSlot )/float(T)) - timeslots[ currentTask.taskid ]   #calculating lag and hence number of miss_no
                    if(currentLag >= 1):
                        miss_no += math.floor(currentLag)
                    
                    currentTask.deadline += float(Total_time)/eprime[ currentTask.taskid ]

                    
                    if( timeslots[currentTask.taskid] < eprime[ currentTask.taskid ]):  #storing updated task. This is to be inserted after the end of for loop
                        extracted_tasks.append( currentTask )

                i += 1                                                                  #incrementing value of i so as to assign task for next processor
            
        for j in range(0,len(extracted_tasks)):                                          #inserting updated tasks into the heap
            heap_dead.insert( extracted_tasks[j].taskid , extracted_tasks[j].deadline )

        extracted_tasks = []
        currentTimeSlot += 1                                                            #incrementing currentTimeslot

    for j in range(len(heap_dead.heap_list)):
        heap_dead.extract_min()
     
    del(heap_dead)
    return miss_no



############## Main part #############


processors=[]
no_task=[]
sim_time=[]
miss_prim=[]
miss_round=[]


f=open('taskcon.txt','r')

test = int(f.readline())

for testcase in range(0,test):

    avg_count=0;

    avg_prim=0
    avg_round=0
    
    proc=int(f.readline())                                                        # reading number of processors from file 
    processors.append(proc)
    print proc
    taskno=int(f.readline())                                                      # reading number of tasks from file 
    no_task.append(taskno)
    print taskno
    T=int(f.readline())                                                           # reading total simulation time from file 
    sim_time.append(T)
    print T
  
    count =taskno
    e_natural=[]
    esum=0

    while (count>0):
        rand=random.randrange(1,10)
        e_natural.append(rand)
        esum=esum+rand
        count=count-1

    eprime=[]

    Total_time=T*proc

    eprime_sum = 0
    for i in range(0,taskno-1):
        temp=(e_natural[i]*Total_time)/esum
        if(temp!=0):
            eprime.append(temp)
            eprime_sum += temp
        else:
            eprime.append(1)
            eprime_sum += 1
                
    if(Total_time - eprime_sum <= 0):       
         print 'Incorrect random number generator... not considered for in taking average values of misses !!!!!'
         eprime.append( Total_time - eprime_sum )
         
         print 'processors = '+str(processors)
         print 'tasks = '+str(no_task)
         print 'eprime = '+str(eprime)
         print 'Simulation time of the processor = '+str(T)
                 
    else:     
        avg_count += 1
        eprime.append( Total_time - eprime_sum )
        print 'e = '+str(e_natural)
        print 'esum = ' +str(esum)
        print 'eprime = '+str(eprime)
        print "   "
        avg_prim +=  primitive_scheduler(eprime,proc,taskno,T)
        avg_round +=  round_robin(eprime,proc,taskno,T)
    if(avg_count!=0):            
        avg_prim /= avg_count
        avg_round /= avg_count
        miss_prim.append(math.floor(avg_prim))
        miss_round.append(math.floor(avg_round))
        print ' '
    
print processors
print no_task
print sim_time
print miss_round
print miss_prim


f.close()
########Plotting The Required Graphs###########
if(Total_time - eprime_sum > 0): 
    g= Gnuplot.Gnuplot()
    g('set term wxt enhanced')
    g.title('Scheduler')
    g.xlabel('Number of Processors')
    g.ylabel('No of Misses')
    d= Gnuplot.Data(processors,miss_prim,title='Primitive Scheduler', with_="linespoints lt 1 lw 6 pt 5 linecolor rgb 'red'")
    e=Gnuplot.Data(processors,miss_round,title='Round Robin', with_="linespoints lt 1 lw 6 pt 8 linecolor rgb 'blue'")
   #g('set xrange[:6]')
   #g('set yrange[:25]')
    g.plot(e,d)
    g.hardcopy('gp_test.ps', enhanced=1, color=1)
    raw_input('Please press return to continue...\n')
    g.reset()
    g('set term wxt enhanced')
    g.title('Scheduler')
    g.xlabel('Number of Tasks')
    g.ylabel('No of misses')
    d= Gnuplot.Data(no_task,miss_prim,title='Primitive Scheduler', with_="linespoints lt 1 lw 6 pt 5 linecolor rgb 'red'")
    e=Gnuplot.Data(no_task,miss_round,title='Round Robin', with_="linespoints lt 1 lw 6 pt 8 linecolor rgb 'blue'")
    #g('set xrange[:12]')
    #g('set yrange[:25]')
    g.plot(e,d)
    g.hardcopy('gp_test2.ps', enhanced=1, color=1)
    raw_input('Please press return to exit...\n')



