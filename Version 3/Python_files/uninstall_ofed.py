import paramiko
from tkinter import messagebox
from tkinter import *
import os

def sshCommand(hostname, port, username, password, command):
    sshClient = paramiko.SSHClient()                                   # create SSHClient instance
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())    # AutoAddPolicy automatically adding the hostname and new host key
    #host = sshClient.get_host_keys()
    #host.clear()
    #print(sshClient.load_system_host_keys())  
    sshClient.connect(hostname, port, username, password)
    stdin, stdout, stderr = sshClient.exec_command(command)
    result = stdout.readlines()
    #result = ''.join(stdout.readlines())
    return  result[-1]

def uninstall(input_file):
    file = open(input_file,"r")
    data=[]
    for each in file:
        word = each.split()
        data.append([])
        for every in word:
            data[-1].append(every)
    file.close()
    test=[]
    #print(data)
    for elem in data:
        flag=False
        try:
            if elem[3]=='Linux':
                flag=True
                value = sshCommand(elem[0],22,elem[1],elem[2],'ofed_uninstall.sh --force')
                compare = value.rstrip("\n")
                if compare=='Uninstall finished successfully':
                    print("asad")
                    return  elem[0]+' : ofed uninstallation was successful'
                else:
                    print("asad")
                    return  elem[0]+' : ofed uninstallation was unsuccessful'
        except:
            if flag==True and elem[0][0]!='#':
                return  elem[0]+' : ofed already been uninstalled'


