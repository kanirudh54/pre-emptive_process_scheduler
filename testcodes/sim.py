def allocate(q,k,processor,diff):
    main = [['a' for i in xrange(int(sum(q)/processor))] for i in xrange(processor+diff)]
    check=['a' for i in xrange(processor)]

    #print check
    heap=[1]
    flag=0
    for i in range(len(k)-1):
        heap+=[1]
    for b in range(int(sum(q)/processor)):
        if flag==0:
            for j in range(len(k)):
                heap[j]=(s[0]*s[1])*k[j]/q[j]
        if flag==1:
            for j in range(processor):
                k[check[j]]+=1
                heap[check[j]]=(s[0]*s[1])*k[check[j]]/q[check[j]]
        #print heap,k#,q,check
        for a in range(processor):
            main[a][b]=heap.index(min(heap))
            #print heap.index(min(heap))
            check[a]=heap.index(min(heap))
            heap[heap.index(min(heap))]=1000
            #print check, heap
            flag=1
    return main
f=open("generate.txt","r")
T=int(f.readline())
for i in range (T):
    s=f.readline() 
    s=s.split() 
    for j in range (4):
        s[j]=int(s[j])
    p=f.readline()
    p=p.split()
    for j in range(s[2]):
        p[j]=int(p[j])
    q=p
    total1=sum(p)
    for j in range(s[2]):
        p[j]=float(p[j]*s[0]*s[1])/total1
        q[j]=int(p[j])
    total2=sum(q)-q[s[2]-1]
    q[s[2]-1]=s[0]*s[1]-total2
    if q[0]==0:
        k=[0]
    else:
        k=[1]
    for j in range(s[2]-1):
        if q[j]==0:
            k=k+[0]
        else:
            k=k+[1]
    if max(q)>s[1]:
        print "Oops I cant find it !!!!"
    else:
        if s[2]>=s[0]:
            main=allocate(q,k,s[0],0)
        else:
            main=allocate(q,k,s[2],s[0]-s[2])
        miss=[0]
        #print main
        for j in range(s[2]):
            actual=0
            miss+=[0]
            for h in range(s[1]):
                for a in range(s[0]):
                    if main[a][h]==j:
                        actual+=1
                lag=(float(q[j]*(h+1))/s[1])-actual
                if lag>=1:
                    miss[j]+=int(lag)
    del miss[-1]
    print main,miss
    if s[0]<=s[2]:
        main2 = [['a' for i in xrange(s[1])] for i in xrange(s[0])]
        l=0
        for j in range(s[0]*s[1]):
            if q[l%s[2]]!=0:
                #print "loop", j/s[0],j%s[0],l%s[2]
                main2[j%s[0]][j/s[0]]=l%s[2]
                #print main2
                q[l%s[2]]-=1
                l=(l+1)%s[2]
            else:
                #l=(l+1)%s[2]
                while q[l%s[2]]==0:
                    l=(l+1)%s[2]
                #print "equal",j/s[0],j%s[0],l%s[2]
                main2[j%s[0]][j/s[0]]=l%s[2]
                q[l%s[2]]-=1
                l=(l+1)%s[2]
        miss2=[0]
        #print main
        for j in range(s[2]):
            actual2=0
            miss2+=[0]
            for h in range(s[1]):
                for a in range(s[0]):
                    if main2[a][h]==j:
                        actual2+=1
                lag2=(float(q[j]*(h+1))/s[1])-actual2
                if lag2>=1:
                    miss2[j]+=int(lag2)
    del miss2[-1]
    print main2,miss2
f.close()














