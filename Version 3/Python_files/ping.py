from tkinter import messagebox
from tkinter import *
import os,sys

def ping_status(path):
    inc=-1
    file = open(".\\.\\Text_files\\user.txt","r")
    data=[]
    remove=[]
    display=[]
    for each in file:
        inc+=1
        #print (each)
        word = each.split()
        data.append([])
        for every in word:
            data[inc].append(every)
            #print(data)
    file.close()
    file = open(path,"a")
    for elem in range (len(data)):
        hostname =data[elem][0]
        if hostname[0]!='#':      
            response = os.system("ping -c 1 " + hostname)
            # and then check the response...
            #print(response)
            if response == 0:
                pingstatus = " active"
            else:
                pingstatus = " not_active"
                remove.append(hostname+" "+data[elem][1]+" "+data[elem][2]+" "+data[elem][3]+" "+data[elem][4])
                file.write(hostname+":-:Ping_Failed\n")
                display.append(hostname)
        else:
            pingstatus = " not_active"
            remove.append(hostname+" "+data[elem][1]+" "+data[elem][2]+" "+data[elem][3]+" "+data[elem][4])
            
            display.append(hostname)
            
    file.close()
    #print(remove)
    if (len(remove)): 
        #print("Entered")
        file =open(".\\.\\Text_files\\user.txt", "r")
        lines = file.readlines()
        #print("lines:",lines)
        file.close()
        file= open(".\\.\\Text_files\\user.txt", "w")
        file.write("")
        for line in lines:
            if line.strip("\n") not in remove:
                #print(line)
                file.write(line)
        file.close()
    file = open(".\\.\\Text_files\\user.txt", "r")
    lines = file.readlines()
    #print(lines)
    if len(lines)==0:
        res='no'
    else:
        res='yes'
    #print(res)
    return res

