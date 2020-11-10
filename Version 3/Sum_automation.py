import os,sys,time
import sys
sys.path.append("Python_files")
from uninstall_ofed import *
inc=-1
data=[]
print(os.path.dirname(os.path.dirname(__file__)))
try:
    if len(sys.argv)==4:
        file = open(sys.argv[3],"r")
    elif len(sys.argv)==3:
        file = open(sys.argv[2],"r")
    for each in file:
        #print (each)
        word = each.split()
        data.append([])
        for every in word:
            data[-1].append(every)
    #print(data)
    val=str(data[1][1][0])+':'
    spp_name=os.path.basename(data[2][1])
    os.system('cmd /c "c: & '+str(val)+' & cd "'+str(data[1][1])+'" & "'+spp_name)
except:
    print('Failed to mount the spp')
    exit


try:
    if len(sys.argv)>1:
        if len(sys.argv)==2 and sys.argv[1]=='--help':
                print("\nsyntax for parameters:\n py Sum_automation.py --prerequisite_only --input c:/input.txt " + ":  For running only prerequisites".rjust(35)+" \n py Sum_automation.py --prerequisite --input c:/input.txt "+":  For running the script with prerequisites".rjust(51)+" \n py Sum_automation.py --input c:/input.txt "+":  For running the script without prerequisites".rjust(69)+"\n")

        elif len(sys.argv)==4:
            if sys.argv[1]=='--prerequisite_only' and sys.argv[2]=='--input':
                print("Clearing iLO repository...")
                os.system('cmd /c "robot -v input:no -v input_file:"'+sys.argv[3]+'" -l repo_clear_log.html -r repo_clear_report.html iLO_repo.robot > repo_clear_debug_details"')
                time.sleep(300)
                print("Uninstalling OFED...")
                print(uninstall(sys.argv[3]))               
            elif sys.argv[1]=='--prerequisite' and sys.argv[2]=='--input':
                print("Clearing iLO repository...")
                os.system('cmd /c "robot -v input:no -v input_file:"'+sys.argv[3]+'" -l repo_clear_log.html -r repo_clear_report.html iLO_repo.robot > repo_clear_debug_details"')
                time.sleep(300)
                print("Uninstalling OFED...")
                print(uninstall(sys.argv[3]))
                os.system('cmd /c "py Python_files/uninstall_ofed.py"')
                time.sleep(300)
                os.system('cmd /c "robot -v input:no -v input_file:"'+sys.argv[3]+'" -l sum_automation_log.html -r sum_automation_report.html SUM_Automation.robot > sum_automation_debug_details"')
            else:
                print("--help for the help")

        elif len(sys.argv)==3:
            if sys.argv[1]=='--input' and sys.argv[2]!="":
                os.system('cmd /c "robot -v input:no -v input_file:"'+sys.argv[2]+'" -l sum_automation_log.html -r sum_automation_report.html SUM_Automation.robot > sum_automation_debug_details"')
            else:
                print("--help for the help")
        else:
            print("--help for the help")
    else:
        os.system('cmd /c "robot -v input:yes -l sum_automation_log.html -r sum_automation_report.html SUM_Automation.robot > sum_automation_debug_details"')
except:
    print("Check if entered path is correct \n Enter --help for the syntax ")


