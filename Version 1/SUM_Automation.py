import os,sys

inc=-1
data=[]
print(os.path.dirname(os.path.dirname(__file__)))
#file = open(os.pardir(os.pardir(__file__))+"\\Text_files\\config.txt", "r")

def access():
    for each in file:
        inc+=1
        #print (each)
        word = each.split()
        data.append([])
        for every in word:
            data[inc].append(every)
    print(data)



if len(sys.argv)>1:
    if len(sys.argv)==3:
        if sys.argv[1]=='--help':
            print("Help")
        elif sys.argv[1]=='--input' and sys.argv[2]!="":
            os.system('cmd /c "robot -v input:no -v input_file:"'+sys.argv[2]+'" SUM_Automation.robot"')
        else:
            print("--help for the help")
    else:
        print("--help for the help")
else:
    os.system('cmd /c "robot -v input:yes SUM_Automation.robot"')
