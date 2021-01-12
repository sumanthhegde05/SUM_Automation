import os
from win32com.client import GetObject


def get_pid():
    return os.getpid()

def kill_process():
    os.system('taskkill /IM sum_service_x64.exe /f')
    os.system('taskkill /IM sum_bin_x64.exe /f')
    '''
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')

    for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
        #print ("Killing PID:", p.Properties_('ProcessId').Value)
        print(str(p.Properties_('ProcessId').Value))
        os.system("taskkill /PID "+str(p.Properties_('ProcessId').Value)+" /f")'''

if __name__=='__main__':
    kill_process()
