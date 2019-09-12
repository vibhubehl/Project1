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
import p14 as p
import sqlite3

#this function checks all sequences and checks the one which have time clash
def timeclash(combo):
    flag=0
    combo_new=list()
    comm=sqlite3.connect('database.db')
    for temp in combo:
        l=temp.split(',')
        try:
            conn=sqlite3.connect('time.db')
            conn.execute('''CREATE TABLE T 
                        (TIME INT,
                        MONDAY CHAR(50),
                        TUESDAY CHAR(50),
                        WEDNESDAY CHAR(50),
                        THURSDAY CHAR(50),
                        FRIDAY CHAR(50));''')
        except:
            conn=sqlite3.connect('time.db')
            conn.execute('''DROP TABLE T''')
            conn.execute('''CREATE TABLE T 
                        (TIME INT,
                        MONDAY CHAR(50),
                        TUESDAY CHAR(50),
                        WEDNESDAY CHAR(50),
                        THURSDAY CHAR(50),
                        FRIDAY CHAR(50)); ''')
        conn.execute('''INSERT INTO T (TIME) VALUES (8)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (8.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (9)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (9.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (10)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (10.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (11)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (11.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (12)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (12.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (1)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (1.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (2)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (2.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (3)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (3.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (4)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (4.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (5.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (6)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (6.5)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (7)''')
        conn.execute('''INSERT INTO T (TIME) VALUES (7.5)''')
        conn.commit()
        for a in l:
            curr=comm.cursor()
            atemp=int(a)
            curr.execute("SELECT TIME FROM INFO WHERE (CRN =? )", [a])
            time=curr.fetchall()
            ltemp=p.realtime(time)
            tstart=ltemp[0]
            tend=ltemp[1]
            #print(time[0][0])
            curr.execute("SELECT DAY FROM INFO WHERE (CRN =? )", [a])
            day=curr.fetchall()
            daytemp=p.days(day)
            #print(ltemp)
            curr1=conn.cursor()
            #print(daytemp)
            for d in daytemp:
                ttemp=tstart
                while(ttemp<tend):
                    #print("hello")
                    stemp=int(tstart)
                    p1='SELECT '+d+' FROM T WHERE TIME='+ str(stemp)
                    #curr1.execute("SELECT ? FROM T WHERE (TIME= '9:00')",[d])
                    curr1.execute(p1)
                    info=curr1.fetchall()
                    if(info[0][0]!=None):
                        flag=-1
                        #print(info[0])
                        break
                    #p2='INSERT INTO T ('+d+') VALUES ('+a+') WHERE (TIME='+str(ttemp)+')'
                    p2='UPDATE T SET '+d+' = '+ a +' WHERE TIME= '+ str(ttemp) 
                    #print(p2)
                    curr1.execute(p2)       
                    ttemp=ttemp+0.5

                if(flag==-1):
                    break
        if(flag==-1):
            flag=0
            continue
        else:
            combo_new.append(temp)           
        conn.commit()
        conn.close()
    print(combo_new)
    comm.commit()
    comm.close() 
    return combo_new

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
        #print(type(lecture[0]))
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
def assembler():
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
    combo_new=timeclash(crn_Combination)
    print('after')
    print(combo_new)
assembler()