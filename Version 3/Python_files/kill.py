import os
from win32com.client import GetObject
def kill_cmd():
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')

    for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
        #print ("Killing PID:", p.Properties_('ProcessId').Value)
        print(str(p.Properties_('ProcessId').Value))
        os.system("taskkill  "+str(p.Properties_('ProcessId').Value)+" /f")

