from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os,sys



global flag
global inc
global obj
obj=[]
flag=True
class new:
    def __init__(self,ip,comp,stat):
        global inc
        global flag
        self.ip=ip
        self.comp=comp
        self.stat=stat
        inc+=1
        if flag==True:
            flag=False
            ip_label = Label(frame,text="IP_Address", font=('Helvetica', 16, 'bold'),bd=1,bg="#fbeec1",fg="Blue")
            ip_label.grid(row=inc,column=0,padx=20,pady=20)
            ip_label.config(highlightbackground="#000000")
            comp_label = Label(frame,text="Component", font=('Helvetica', 16, 'bold'),bd=1,bg="#fbeec1",fg="Blue")
            comp_label.grid(row=inc,column=1,padx=20,pady=20)
            comp_label.config(highlightbackground="#000000")
            stat_label = Label(frame,text="Status", font=('Helvetica', 16, 'bold'),bd=1,bg="#fbeec1",fg="blue")
            stat_label.grid(row=inc,column=2,padx=20,pady=20)
            stat_label.config(highlightbackground="#000000")
            inc+=1
        if self.stat == 'Update returned an error. ':
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat == 'Success,':
            self.stat = 'Success, reboot required to activate new version.'
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="green")
        elif self.stat == 'The':
            self.stat = 'The installation was not attempted because the required hardware is not present, the software is current, or not applicable or there is nothing to install.'
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat == 'Error:':
            self.stat = 'Error: General failure occurred or user cancelled the update.'
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat == 'Failed_to_login_to_the_system(SSH_Failed)':
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat == 'Deployment_Failed ':
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat == 'Log_Failed ':
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat == 'Ping_Failed':
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat=="Inventory_Failed ":
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat=='Node_Addition_Failed ':
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        elif self.stat=='Unable to run component. ':
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="red")
        else:
            self.ip_status = Message(frame,text=self.stat, font=('Helvetica', 14, 'bold'),width=screen_width/5,bd=1,bg="#fbeec1",fg="green")
        self.ip_label = Label(frame,text=self.ip, font=('Helvetica', 14,'bold'),bd=1,bg="#fbeec1")
        self.ip_label.grid(row=inc,column=0,padx=20,sticky=W,pady=3)
        self.ip_label.config(highlightbackground="#000000")
        self.component_label = Message(frame, text=self.comp, font=('Helvetica', 13,) ,width=screen_width/2 ,bd=1,bg="#fbeec1")
        self.component_label.grid(row=inc,column=1,sticky=W,padx=20,pady=3)
        self.component_label.config(highlightbackground="#000000")
        self.ip_status.grid(row=inc,column=2,sticky=W,padx=20,pady=3)
        self.ip_status.config(highlightbackground="#000000")
        print(self.stat)
        if self.stat=="Baseline_addition_failed ":
            self.log_button = Button(frame,text='View Error',command=self.baseline_error, font=('Helvetica', 12, 'bold'),width=10,bd=1,bg="#05386b",fg="#ffffff")
            self.log_button.grid(row=inc,column=3,padx=20,pady=3)
            self.log_button.config(highlightbackground="#000000")   
        elif self.stat=="Failed_to_login_to_the_system(SSH_Failed)":
            pass
        elif self.stat=="Ping_Failed":
            pass
        elif self.stat=="Inventory_Failed ":
            pass
        elif self.stat=='Deployment_Failed ':
            pass
        elif self.stat == 'Log_Failed ':
            pass
        elif self.stat == 'Node_Addition_Failed ':
            pass
        else:
            self.log_button = Button(frame,text='View Log',command=self.view, font=('Helvetica', 12, 'bold'),width=10,bd=1,bg="#05386b",fg="#ffffff")
            self.log_button.grid(row=inc,column=3,padx=20,pady=3)
            self.log_button.config(highlightbackground="#000000")
        #self.err_button = Button(frame,text='View Errors',command=self.view_err,font=('Helvetica', 12, 'bold'),width=10).grid(row=inc,column=4,padx=20)
    #def view_err(self):
        #path= 'D:\\'+sys.argv[1]+'\\output_logs\\'+self.ip+'\\error.txt'
        #os.startfile(path, 'open')
    def baseline_error(self):
        os.startfile(sys.argv[1]+'\\output_logs\\Details\\baseline_error.txt', 'open')

    def view(self):
        path= sys.argv[1]+'\\output_logs\\'+self.ip+"\\"+self.comp+'.txt'
        os.startfile(path, 'open')

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=screen_width,height=screen_height)

main = Tk()
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

main.geometry(str(screen_width)+"x"+str(screen_height))

myframe=Frame(main,relief=GROOVE,width=0,height=100,bd=1)
myframe.place(x=0,y=100)

canvas=Canvas(myframe,bg="#fbeec1")
frame=Frame(canvas,bg="#fbeec1")
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)

inc=-1
header = Label(main,text="Dashboard", font=('Helvetica', 22, 'bold'),bg="#659DBD")
header.place(x=screen_width/2 - screen_width/15,y=30)

file = open(sys.argv[1]+'\\output_logs\\Details\\dash.txt',"r")
data=[]
obj=[]
temp=[]
val=0
for each in file:
    print (each)
    temp = each.split('\n')
    print(temp)
    word = temp[0].split(':') 
    data.append([])
    for every in word:
        data[val].append(every)
    val+=1
file.close()
print(data)

for elem in range (0,len(data)):
    print(data[elem][0],data[elem][1],data[elem][2])
    n=new(data[elem][0],data[elem][1],data[elem][2])
    obj.append(n)
main.configure(background="#659DBD")
main.mainloop()




# --- classes ---



# --- main ---


