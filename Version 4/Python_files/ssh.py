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
    #print(stdout.readlines())
#sshCommand('192.168.2.133',22,'root','Hptc_ib123','sut /status')


def ssh_reply(path):
    inc=-1
    file = open(".\\.\\Text_files\\user.txt","r")
    data=[]
    remove=[]
    display=[]
    for each in file:
        inc+=1
        print (each)
        word = each.split()
        data.append([])
        for every in word:
            data[inc].append(every)
            print(data)
    file.close()
    if len(data)==0:
        root=Tk()
        messagebox.showerror("Alert!","No ip addresses found")
        root.withdraw()
        flag='no'

    else:
        file = open(path, "a")
        for elem in range (len(data)):
            hostname = data[elem][0]
            username = data[elem][1]
            password = data[elem][2]
            if data[elem][3]=='Windows':
                try:
                    sshCommand(hostname, 22, username, password, 'rmdir /s /q c:\\cpqsystem')
                    sshCommand(hostname, 22, username, password, 'rmdir /s /q c:\\Users\\Administrator\\AppData\\Local\\localsum')
                    sshCommand(hostname, 22, username, password, 'rmdir /f /q c:\\Users\\Administrator\\AppData\\Local\\sum')
                    sshCommand(hostname, 22, username, password, 'rmdir /s /q c:\\Users\\Administrator\\AppData\\Local\\hpsut')
                    sshCommand(hostname, 22, username, password, 'rmdir /f /q c:\\Users\\Administrator\\AppData\\Local\\sut')
                except Exception:
                    remove.append(hostname+" "+username+" "+password+" "+data[elem][3]+" "+data[elem][4])
                    file.write(hostname+":-:Failed_to_login_to_the_system(SSH_Failed)\n")
                    display.append(hostname)
            elif data[elem][3]=='Linux':
                try:
                    sshCommand(hostname, 22, username, password, 'rm -rf /root/sum')
                    sshCommand(hostname, 22, username, password, 'rm -rf /var/tmp/sum')
                    sshCommand(hostname, 22, username, password, 'rm -rf /var/log/sum')
                    sshCommand(hostname, 22, username, password, 'rm -rf /usr/bin/sum')
                    sshCommand(hostname, 22, username, password, 'rm -rf /var/cpq')
                except Exception:
                    file.write(hostname+":-:Failed_to_login_to_the_system(SSH_Failed)\n")
                    remove.append(hostname+" "+username+" "+password+" "+data[elem][3]+" "+data[elem][4])
                    display.append(hostname)
            else:
                pass
        file.close()
        if(len(remove)):
            file = open(".\\.\\Text_files\\user.txt", "r")
            lines = file.readlines()
            file.close()
            file= open(".\\.\\Text_files\\user.txt", "w")
            for line in lines:
                if line.strip("\n") not in remove:
                    file.write(line)
            file.close()
        file =open(".\\.\\Text_files\\user.txt", "r")
        lines = file.readlines()
        if len(lines)==0:
            flag='no'
        else:
            flag='yes'
    print(flag)
    return flag

