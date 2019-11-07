import urllib
from bs4 import BeautifulSoup
import  requests
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast
import jsbeautifier
import xlwt 
from datetime import datetime
from xlwt import Workbook 
import  xlsxwriter
import itertools 
import p14 as p #including p14
import sqlite3

def indexer(ttemp):#to convert time to to values of 0-23

    if(ttemp==8):
        index_time=0
    if(ttemp==8.5):
         index_time=1
    if(ttemp==9):
        index_time=2
    if(ttemp==9.5):
        index_time=3
    if(ttemp==10):
        index_time=4
    if(ttemp==10.5):
        index_time=5
    if(ttemp==11):
        index_time=6
    if(ttemp==11.5):
        index_time=7
    if(ttemp==12):
        index_time=8
    if(ttemp==12.5):
        index_time=9
    if(ttemp==1):
        index_time=10
    if(ttemp==1.5):
        index_time=11
    if(ttemp==2):
        index_time=12
    if(ttemp==2.5):
        index_time=13
    if(ttemp==3):
        index_time=14
    if(ttemp==3.5):
        index_time=15
    if(ttemp==4):
        index_time=16
    if(ttemp==4.5):
        index_time=17
    if(ttemp==5):
        index_time=18
    if(ttemp==5.5):
        index_time=19
    if(ttemp==6):
        index_time=20
    if(ttemp==6.5):
        index_time=21
    if(ttemp==7):
        index_time=22
    if(ttemp==7.5):
        index_time=23
    return index_time

#this function checks all sequences and checks the one which have time clash
def timeclash(combo):
    flag=0
    combo_new=list()#to keep the valid combo
    comm=sqlite3.connect('database.db')#importing database

    for temp in combo:
        l=temp.split(',')
        table=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        table[0][0]=99#this table is to store classes

        for a in l:
            curr=comm.cursor()
            atemp=int(a)
            curr.execute("SELECT TIME FROM INFO WHERE (CRN =? )", [a])
            time=curr.fetchall()#stores time
            ltemp=p.realtime(time)
            tstart=ltemp[0]#start time
            tend=ltemp[1]#start time
            curr.execute("SELECT DAY FROM INFO WHERE (CRN =? )", [a])
            day=curr.fetchall()#stores day of classes
            daytemp=p.days(day)

            for d in daytemp:
                ttemp=tstart
                if(d=='MONDAY'):
                    index_day=0
                elif(d=='TUESDAY'):
                    index_day=1
                elif(d=='WEDNESDAY'):
                    index_day=2
                elif(d=='THURSDAY'):
                    index_day=3
                elif(d=='FRIDAY'):
                    index_day=4

                while(ttemp<tend):#fill places in table to mark when class is.  
                    index_time= indexer(ttemp)
                    info=table[index_time][index_day]

                    if(info!=0):#checking if place is already full or not 
                        flag=-1
                        break#break if something already exists
                    else:
                        table[index_time][index_day]=1 #if empty then change to one to indicate this slot if filled

                    ttemp=ttemp+0.5#increament temp by 0.5

                if(flag==-1):#if timeclash detected then break
                    break
         
        if(flag==-1):#if timeclash detected then break
            flag=0
        else:#if no timeclash detected then append
            combo_new.append(temp)   
               
    comm.commit()
    comm.close() 
    return combo_new


#this function returns the starting time in int form
def timedisection(l):
    temp=l.split('-')
    temp1=temp[0].split(':')
    n=int(temp1[0])
    return n

def delete():
    table= sqlite3.connect(table.db)
    cursor=table.cursor()
    cursor.execute('''DELETE FROM ranking WHERE ()''')
    table.commit()
    table.close()


def ranking(list_of_crn):#ranks the combos
    #questions for the user
    q1_type= input("Are you an morning person? (y/n)")
    q2_frequency= input(" Do you like back to back classes? (y/n)")
<<<<<<< HEAD
    day_free= input("Which day do you want to be free?  (Enter full name in caps)")

=======
    q3_holidays= input("Do u want to try a particular day to be free?  (y/n)")
    if(q3_holidays=='y'):
        day_free=input("Enter which day would you like to be free, enter in all caps")
>>>>>>> parent of da95885... Code finished, Minor Changes required
    count=0
    ranks= []
    # table= sqlite3.connect(ranking.db)
    # cursor=table.cursor()
    # cursor.execute('''CREATE TABLE ranking(Subject TEXT, Time Text, CRN TEXT)''')
    # table.commit()
    # table.close()
    time_start_list=[]
    conn= sqlite3.connect('database.db')
    curr= conn.cursor()

    for k in list_of_crn:

        ranks.append(0.0)
        listtemp=k.split(",")

        for j in listtemp:

            curr.execute("SELECT TIME from INFO where CRN= ?",[j])#fetch info of particular crn
            time_start_list=curr.fetchall()#fetch starting 
            time_orignal=time_start_list[0][0]
            tfinal=timedisection(time_orignal)#getting starting life

            #ranking for question 1
            if(tfinal>=8 and q1_type=='y'):
                ranks[count]+=1
            elif(tfinal<=7 and q1_type=='n'):
<<<<<<< HEAD
                ranks[count]+=2.5

=======
                ranks[count]+=1
>>>>>>> parent of da95885... Code finished, Minor Changes required
        count+=1

    combo_new=list()
    comm=sqlite3.connect('database.db')
    count=0

    for temp in list_of_crn:
        l=temp.split(',')
        table=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
        [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        table[0][0]=99
        for a in l:
            curr=comm.cursor()
            atemp=int(a)
            curr.execute("SELECT TIME FROM INFO WHERE (CRN =? )", [a])
            time=curr.fetchall()
            ltemp=p.realtime(time)
            tstart=ltemp[0]
            tend=ltemp[1]
            curr.execute("SELECT DAY FROM INFO WHERE (CRN =? )", [a])
            day=curr.fetchall()
            daytemp=p.days(day)

            for d in daytemp:
                
                ttemp=tstart
                if(d=='MONDAY'):
                    index_day=0
                elif(d=='TUESDAY'):
                    index_day=1
                elif(d=='WEDNESDAY'):
                    index_day=2
                elif(d=='THURSDAY'):
                    index_day=3
                elif(d=='FRIDAY'):
                    index_day=4

                while(ttemp<tend):
                    index_time=indexer(ttemp)
                    try:
                        class_before=table[index_time][index_day]
                    except:
                        class_before=0
<<<<<<< HEAD
                        
                    #ranking for question2
                    if(class_before!=temp and q2_frequency=='y'):
                        ranks[count]+=2.5
                    elif((class_before==temp or class_before==0) and q2_frequency=='n'):
                        ranks[count]+=2.5
=======
                    if(class_before!=temp):
                        ranks[count]+=1
>>>>>>> parent of da95885... Code finished, Minor Changes required
                    table[index_time][index_day]=int(a)      
                    ttemp=ttemp+0.5
        
        ttemp=0
        rt=0.1
        while(ttemp<24):

            if(day_free=='MONDAY'):
                index_day=0
            elif(day_free=='TUESDAY'):
                index_day=1
            elif(day_free=='WEDNESDAY'):
                index_day=2
            elif(day_free=='THURSDAY'):
                index_day=3
            elif(day_free=='FRIDAY'):
                index_day=4
            activ=table[ttemp][index_day]
            if(activ==0):
                ranks[count]+=0.1
            ttemp+=1
<<<<<<< HEAD
        ranks[count]=float(ranks[count])+rt
=======


        #print(table)
>>>>>>> parent of da95885... Code finished, Minor Changes required
        count+=1        
    comm.commit()
    comm.close() 
    print(ranks)
    
        

#This function uses the combo function to make all combinations  Author-vibhu
def seperator(l,combo):
    conn=sqlite3.connect('database.db')
    curr=conn.cursor()
    i=0
    for temp in l:
        combo_temp=[]
        curr.execute("SELECT CRN FROM INFO WHERE (NAME= ? AND TYPE ='Lab') ",[temp])
        lab=curr.fetchall()
        curr.execute("SELECT CRN FROM INFO WHERE (NAME= ? AND TYPE ='Tutorial') ",[temp])
        tutorial=curr.fetchall()
        curr.execute("SELECT CRN FROM INFO WHERE (NAME= ? AND TYPE ='Lecture') ",[temp])
        lecture=curr.fetchall()
        n=0
        l1=[]
        lab2=[]
        tutorial2=[]

        while(True):
            if(n<len(lecture)):                
                l1.append(str(lecture[n][0]))
            if(n<len(lab)):                
                lab2.append(str(lab[n][0]))
            if(n<len(tutorial)):                
                tutorial2.append(str(tutorial[n][0]))
            if(n>=len(lecture) and n>=len(tutorial) and n>len(lab)):
                break
            n=n+1

        lecture=l1
        lab=lab2
        tutorial= tutorial2
     
        if(i==0):

            if(lecture!=None):
                combo=lecture

                if(lab!=None):
                    p.combinations(lab,combo,combo_temp)
                    combo=combo_temp
                if(tutorial!=None):
                    p.combinations(tutorial,combo,combo_temp)
                    combo=combo_temp

            elif(lab!=None):
                combo=lab

                if(lecture!=None):
                    p.combinations(lecture,combo,combo_temp)
                    combo=combo_temp
                if(tutorial!=None):
                    p.combinations(tutorial,combo,combo_temp)
                    combo=combo_temp

            else:
                combo=tutorial

                if(lecture!=None):
                    p.combinations(lecture,combo,combo_temp)
                    combo=combo_temp
                if(lab!=None):
                    p.combinations(lab,combo,combo_temp)
                    combo=combo_temp
            
        else:

            if(lecture!=None):
                p.combinations(lecture,combo,combo_temp)
                combo=combo_temp
            if(lab!=None):
                p.combinations(lab,combo,combo_temp)
                combo=combo_temp
            if(tutorial!=None):
                p.combinations(tutorial,combo,combo_temp)
                combo=combo_temp

        i=i+1
   
    conn.commit()
    conn.close()
    return combo
        
crnl=[]
def assembler():#ask questions from the user and calls all the relevant functions
    ans= 'y'
    n=0
    name=[]
    crn_Combination=[]  

    while(ans=='y'):

        crsname=input("Enter Course Name")
        crsnum=input("Enter Course Number")
        name_temp=crsname+' '+crsnum
        name.append(name_temp)
        #print(name_temp)
        url=p.urlmaker(crsname,crsnum)
        list1=[]
        date=[]
        place=[]
        day=[]
        typec=[]
        time1=[]
        crn1=[]
        crn_temp=[]
        p.crn(url,crn1)
        p.listmaker(list1,url)
        p.lister(list1,date,place,time1,day,typec)  
        #print(time1)  
        p.sql(place,time1,day,typec, crsname,crsnum,crn1 )
        n=n+1
        ans=input("If you want to continue enter 'y'")
        
    crn_Combination= seperator(name,crn_Combination)
    combo_new=[]
    print(crn_Combination)
    combo_new=timeclash(crn_Combination)
    print('after')
    print(len(combo_new)) #use this, it has the correct combination.
    ranking(combo_new)
assembler()