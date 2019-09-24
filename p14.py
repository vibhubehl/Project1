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
import sqlite3

try:
    conn=sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE INFO 
                (NAME CHAR(50) NOT NULL,
                PLACE CHAR(50) NOT NULL,
                TIME CHAR(50) NOT NULL,
                DAY CHAR(50) NOT NULL,
                TYPE CHAR(50) NOT NULL,
                CRN INT PRIMARY KEY NOT NULL);''')
    conn.close()
except:
    conn=sqlite3.connect('database.db')
    conn.execute('''DROP TABLE INFO''')
    conn.execute('''CREATE TABLE INFO 
                (NAME CHAR(50) NOT NULL,
                PLACE CHAR(50) NOT NULL,
                TIME CHAR(50) NOT NULL,
                DAY CHAR(50) NOT NULL,
                TYPE CHAR(50) NOT NULL,
                CRN INT PRIMARY KEY NOT NULL);''')

wb= Workbook()

workbook = xlsxwriter.Workbook('TB.xlsx') 
worksheet = workbook.add_worksheet() 
worksheet.write(0,0,'NAME')
worksheet.write(0,2,'Place')
worksheet.write(0,3,'TIME')
worksheet.write(0,1,'Days')
worksheet.write(0,4,'Type')
worksheet.write(0,5,'CRN')

#this is aclasss, to keep different combinations
class combo:
    c1=''
    c2=''
    c3=''
    c4=''
    c5=''
    c6=''
    c7=''
    c8=''
    c9=''
    c10=''
    #add function is used to add new sections to this combination
    def add(c):
        if(c1==''):
            c1=c
        elif(c2==''):
            c2=c
        elif(c3==''):
            c3=c
        elif(c4==''):
            c4=c
        elif(c5==''):
            c5=c
        elif(c6==''):
            c6=c
        elif(c7==''):
            c7=c
        elif(c8==''):
            c8=c
        elif(c9==''):
            c9=c
        else:
            c10=c


#makes shortform for the building names
def shortform(j):
    if(j.rfind("Comp")):
        return("ECS")
    if(j.rfind("Bob")):
        return("BWC")
    if(j.rfind("David")):
        return("DTB")
    if(j.rfind("Elliot")):
        return("Ell")
    if(j.rfind("Contin")):
        return("CST")
    if(j.rfind("Lab")):
        return("ELW")
    if(j.rfind("Fine Arts")):
        return("FIA")
    if(j.rfind("Hickman")):
        return("HH")
    if(j.rfind("uman")):
        return("HSD")
    if(j.rfind("McLauri")):
        return("MAC")
    if(j.rfind("McKi")):
        return("MCK")
    if(j.rfind("Petch")):
        return("PCh")
    if(j.rfind("Strong")):
        return("DSB")
    if(j.rfind("Social Sciences")):
        return("SSM")
    if(j.rfind("Visua")):
        return("VIA")
    if(j.rfind("Clearihu")):
        return("CLE")

def daysign(now):
    name=now.weekday()
    if(name==0):
        return("M")
    elif(name==1):
        return("T")
    elif(name==2):
        return("W")
    elif(name==3):
        return("R")
    elif(name==4):
        return("F")
    elif(name==5):
        return("S")

def days(day):
    ans=[]
    d=day[0][0]
    for temp in d:
        if(temp=='M'):
            ans.append('MONDAY')
        if(temp=='T'):
            ans.append('TUESDAY')
        if(temp=='W'):
            ans.append('WEDNESDAY')
        if(temp=='R'):
            ans.append('THURSDAY')
        if(temp=='F'):
            ans.append('FRIDAY')
    return ans


# this function will create xl file. NOT COMPLETED. Author- Saumya & Vibhu
def sql(place,time,day,typ,crsname,crsnum,crn1 ):
    url=urlmaker(crsname,crsnum)
    n=1
    name=crsname+' '+crsnum
    conn=sqlite3.connect('database.db')
    while(n<=len(place)):
        d=day[n-1]
        t=time[n-1]
        p=place[n-1]
        ty=typ[n-1]
        c=crn1[n-1]
        temp=shortform(p)
        #print(name)
        #conn.execute("INSERT INTO INFO (NAME, PLACE, TIME, DAY, TYPE, CRN) \ VALUES name, temp,t,d,ty,c )");
        conn.execute("INSERT INTO INFO VALUES (?, ?,?,?,?,?)", (name, temp,t,d,ty,c))      
        n+=1
    conn.commit()
    conn.close()


def combinations(crn1,crn2,crn_Combination):
    #c=0
    crn_comb=(itertools.product(list(crn1),list(crn2)))
    i=0
    for x,y in crn_comb:
        crn_Combination+=[x+","+y]
        i+=1

    
#this function creates initital list that lister needs. Author- Saumya
def crn(url,crn):
    tlist=[]
    crn_string=""
    text=[]
    headings=[]
    count=0
    crn_start=0
    crn_count=5
    page= requests.get(url)
    soup1= BeautifulSoup(page.text,'html.parser')
    class_list= soup1.find_all(class_='ddtitle')
    for heading in class_list:
        headings+=heading.find_all('a')
    # print(headings,"\n")    

    for i in headings:
        text += [i.contents[0]]
    # print(text)

    for j in text:
        for k in j:
            if (k.isdigit() and count<=4):
                tlist+=[k]
                count+=1
        count=0
    # print(tlist)
    count1= len(tlist)/5
    while(count1>0):
        for number in range(crn_start,crn_count):
            crn_string+=tlist[number]
        crn+=[crn_string]
        crn_start+=5
        crn_count+=5
        crn_string=""
        count1-=1



def listmaker(list1,url):

    soup = BeautifulSoup(urllib.request.urlopen(url).read())
    l=""
    
    lis1=[]
    lis2=[]
    text=""
    lis=soup.find_all("td",{"class":"dddefault"})
    for i in range(len(lis)):
        lis1+=lis[i].find_all("td")
    lis2+=lis1
    for j in lis2:
        text=""
        for k in j:
            
            for char in '<>tdclass="dddefaultEveryWeek/<=abbr titlr>TBA':
                if(k==char):
                    k=(k.replace(char," "))
                    k=k.strip(" ")
        

        list1+=[k]
      

#this function will create the final list - Author- Vibhu
def lister(l,date1,place,time1,day,typec):
    i=0
    l1=[]
    date=[]
    for a in l:
        i+=1
        if(a!= None):
            try:
                alpha=a.split()
                temp=''
                #print("here")
                for b in alpha:
                    temp+=b  
                #print(temp)
                if ((temp.rfind("am")) or (temp.rfind("pm"))):
                    l1.append(temp)
                
                
            except:
                alpha=None
                #print("none")
        else:
            i=1
    #print(l1)
    for a in l1:
        temp=a.splitlines()
        try:
            here=temp[0]
            #print(here)
            if ((here.rfind("am")>0) or (here.rfind("pm")>0)):
                time1.append(here)
            elif((here.rfind("ab")>0) or (here.rfind("utorial")>0) or (here.rfind("ecture")>0)):
                typec.append(here)
            elif(here=="TWF" or here=="R" or here=="M" or here == "T" or here=="W" or here=="F" or here== "MWF" or here=="MWR" or here=="TRF" or here=="MW" or here=="MR"):
                day.append(here)
            elif((here.rfind("ichael")>0) or (here.rfind("avid")>0) or (here.rfind("lliot")>0) or (here.rfind("ngineering")>0) or (here.rfind("ob")>0) or (here.rfind("uisness")>0) or (here.rfind("arquhar")>0)  or (here.rfind("raser")>0) or (here.rfind("ickman")>0) or (here.rfind("uman")>0) or (here.rfind("acLaurin")>0) or (here.rfind("cean")>0) or (here.rfind("trong")>0) or (here.rfind("isual")>0) or (here.rfind("learihue")>0)):
                place.append(here)
            elif((here.rfind("201")>0)):
                date.append(here)
                    
        except:
            continue
    i=0
    a=''
    while(i<len(date)):
        if((i+1)>len(day)):
            day.append(a)
        elif((i+1)==len(day)):
            a=day[i]
        i+=1

        
    

#makes url, from where net crawling is done. Author- Vibhu
def urlmaker(crsname,crsnum):
    base='https://www.uvic.ca/BAN1P/bwckctlg.p_disp_listcrse?term_in=201909&subj_in='
    end='&schd_in=%'
    url=base+crsname+'&crse_in='+crsnum+end
    return url

#this functions finds the starting and ending time 
def realtime(time):
    t=time[0][0]
    temp=t.split('-')
    tstart=0
    tend=0
    if(temp[0].rfind("8:00")!=-1):
        tstart=8
    if(temp[0].rfind("8:30")!=-1):
        tstart=8.5
    if(temp[0].rfind("9:00")!=-1):
        tstart=9
    if(temp[0].rfind("9:30")!=-1):
        tstart=9.5
    if(temp[0].rfind("10:00")!=-1):
        tstart=10
    if(temp[0].rfind("10:30")!=-1):
        tstart=10.5
    if(temp[0].rfind("11:00")!=-1):
        tstart=11
    if(temp[0].rfind("11:30")!=-1):
        tstart=11.5
    if(temp[0].rfind("12:00")!=-1):
        tstart=12
    if(temp[0].rfind("12:30")!=-1):
        tstart=12.5
    if(temp[0].rfind("1:00")!=-1):
        tstart=1
    if(temp[0].rfind("1:30")!=-1):
        tstart=1.5
    if(temp[0].rfind("2:00")!=-1):
        tstart=2
    if(temp[0].rfind("2:30")!=-1):
        tstart=2.5
    if(temp[0].rfind("3:00")!=-1):
        tstart=3
    if(temp[0].rfind("3:30")!=-1):
        tstart=3.5
    if(temp[0].rfind("4:00")!=-1):
        tstart=4
    if(temp[0].rfind("4:30")!=-1):
        tstart=4.5
    if(temp[0].rfind("5:00")!=-1):
        tstart=5
    if(temp[0].rfind("5:30")!=-1):
        tstart=5.5
    if(temp[0].rfind("6:00")!=-1):
        tstart=6
    if(temp[0].rfind("6:30")!=-1):
        tstart=6.5
    if(temp[0].rfind("7:00")!=-1):
        tstart=7
    if(temp[0].rfind("7:30")!=-1):
        tstart=7.5
    if(temp[1].rfind("8:50")!=-1):
        tend=9
    if(temp[1].rfind("9:20")!=-1):
        tend=9.5
    if(temp[1].rfind("9:50")!=-1):
        tend=10
    if(temp[1].rfind("10:20")!=-1):
        tend=10.5
    if(temp[1].rfind("10:50")!=-1):
        tend=11
    if(temp[1].rfind("11:20")!=-1):
        tend=11.5
    if(temp[1].rfind("11:50")!=-1):
        tend=12
    if(temp[1].rfind("12:20")!=-1):
        tend=12.5
    if(temp[1].rfind("12:50")!=-1):
        tend=1
    if(temp[1].rfind("1:20")!=-1):
        tend=1.5
    if(temp[1].rfind("1:50")!=-1):
        tend=2
    if(temp[1].rfind("2:20")!=-1):
        tend=2.5
    if(temp[1].rfind("2:50")!=-1):
        tend=3
    if(temp[1].rfind("3:20")!=-1):
        tend=3.5
    if(temp[1].rfind("3:50")!=-1):
        tend=4
    if(temp[1].rfind("4:20")!=-1):
        tend=4.5
    if(temp[1].rfind("4:50")!=-1):
        tend=5
    if(temp[1].rfind("5:20")!=-1):
        tend=5.5
    if(temp[1].rfind("5:50")!=-1):
        tend=6
    if(temp[1].rfind("6:20")!=-1):
        tend=6.5
    if(temp[1].rfind("6:50")!=-1):
        tend=7
    if(temp[1].rfind("7:20")!=-1):
        tend=7.5
    ltemp=list()
    ltemp.append(tstart)
    ltemp.append(tend)
    return ltemp




