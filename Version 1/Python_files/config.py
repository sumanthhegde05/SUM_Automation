import os
import sys
global spp_dir
global cd_drive
global custom

data=[]
inc=-1
file = open(sys.argv[1])
remove=[]
display=[]
for each in file:
    inc+=1
    word = each.split()
    data.append([])
    for every in word:
        data[inc].append(every)

flag=False
file= open(".\\.\\Text_files\\user.txt", "w")
file.write("")
for each in data:
    if len(each)==0:
        continue
    elif flag==True:
        line=each[0]+' '+each[1]+' '+each[2]+' '+each[3]+' '+each[4]+"\n"
        file.write(line)
    elif each[0]=='#<iLO/Network':
        flag=True

file.close()
    
