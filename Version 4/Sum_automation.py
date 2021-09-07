import os,sys,time
import sys

from Python_files.uninstall_ofed import *
from optparse import OptionParser,OptionGroup

data=[]

help_message = "syntax for parameters:\n\
                -o,--prerequisite_only <path to input file>     :     For running only prerequisites \n\
                -p,--prerequisite <path to input file>          :     For running the script with prerequisites\n\
                -i,--input <path to input file>                 :     For running the script without prerequisites\n"


def add_options (parser):
    """
    Method that defines the options(prameters) for the script.
    """
    parser.add_option("-h","--help",  help=help_message , action="store_true",default = False)
    parser.add_option("-o","--prerequisite_only", help = "Executes only the prerequisites", action="store_true", default = False)
    parser.add_option("-p","--prerequisite", help = "Executes the prerequisites along with the main automation process", action="store_true", default = False)
    parser.add_option("-i","--input", help = "Executes only automation process (no prerequisites)", action="store_true", default = False)



def initialize(args):
    file = open(args[0],"r")
    for each in file:
        word = each.split()
        data.append([])
        for every in word:
            data[-1].append(every)
    try:
        val=str(data[1][1][0])+':'
        spp_name=os.path.basename(data[2][1])
        print('cmd /c "c: & '+str(val)+' & cd '+str(data[1][1])+' & '+spp_name+'"')
        os.system('cmd /c "c: & '+str(val)+' & cd '+str(data[1][1])+' & '+spp_name+'"')
    except:
        print('Failed to mount the spp')
        sys.exit()


if __name__=='__main__':
    parser = OptionParser(add_help_option=False)
    add_options(parser)                                                                 
    (options, args) = parser.parse_args()
    #print(options)
    #print(args)
    
    if options.help:
        print(help_message)
        sys.exit()
        
    initialize(args)
    
    if options.prerequisite_only:
        print("Uninstalling OFED...")
        print(uninstall(args[0]))
        print("Clearing iLO repository...")
        os.system('cmd /c "robot -v input:no -v input_file:"'+args[0]+'" -l repo_clear_log.html -r repo_clear_report.html iLO_repo.robot > repo_clear_debug_details"')
    
          
    elif options.prerequisite:
        print("Uninstalling OFED...")
        print(uninstall(args[0]))
        print("Clearing iLO repository...")
        os.system('cmd /c "robot -v input:no -v input_file:"'+args[0]+'" -l repo_clear_log.html -r repo_clear_report.html iLO_repo.robot > repo_clear_debug_details"')
        time.sleep(300)
        print("SUM Automation in progres...")
        os.system('cmd /c "robot -v input:no -v input_file:"'+args[0]+'" -l sum_automation_log.html -r sum_automation_report.html SUM_Automation.robot > sum_automation_debug_details"')
    elif options.input:
        print("SUM Automation in progres...")
        os.system('cmd /c "robot -v input:no -v input_file:"'+args[0]+'" -l sum_automation_log.html -r sum_automation_report.html SUM_Automation.robot > sum_automation_debug_details"')
    else:
        os.system('cmd /c "robot -v input:yes -l sum_automation_log.html -r sum_automation_report.html SUM_Automation.robot > sum_automation_debug_details"')
        