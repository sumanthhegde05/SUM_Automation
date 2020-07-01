from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
global val
global inc
global obj
global spp_name
global custom_baseline_name
global cd_drive_name
obj=[]
class add:
    def __init__(self):
        self.username = StringVar()
        self.password = StringVar()
        self.net_id = StringVar()
        self.net_ip = StringVar()
        self.os = StringVar()
        self.comp = StringVar()
        global val
        global inc
        inc+=1
        val+=1
        value = Label(frame,text="Server"+str(val),font=('cd DHelvetica', 12, 'bold'),bg="#fbeec1").grid(row=inc,column=0,sticky=W,padx=10,pady=5)
        Entry(frame,textvariable=self.net_id).grid(row=inc,column=1,sticky=W,padx=20,pady=10)
        Entry(frame,textvariable=self.username).grid(row=inc,column=2,sticky=W,padx=20,pady=10)
        Entry(frame,textvariable=self.password).grid(row=inc,column=3,sticky=W,padx=20,pady=10)
        #choices = { 'network_ip','ilo_ip'}
        # self.net_ip.set('network_ip') # set the default option
        #popupMenu = OptionMenu(main, self.net_ip, *choices)
        #popupMenu.place(x=950,y=inc-10)
        multiple_os = {'Windows','Linux','iLO-ESXi'}
        self.os.set('Windows')
        popupMenu = OptionMenu(frame, self.os , *multiple_os )
        popupMenu.grid(row=inc,column=4,padx=20,pady=10)
        popupMenu.configure(bg="#05386b",fg="#ffffff",font=('Helvetica', 9, 'bold'),activebackground="#0538bb",activeforeground="#ffffff")
        components = {'Firmware','Driver','Both','All'}
        self.comp.set('Firmware')   
        popupMenu = OptionMenu(frame, self.comp , *components)
        popupMenu.grid(row=inc,column=5,padx=20,pady=10)
        popupMenu.configure(bg="#05386b",fg="#ffffff",font=('Helvetica', 9, 'bold'),activebackground="#0538bb",activeforeground="#ffffff")


def save_info():
    #print(fill.get())   
    global obj
    global spp_name
    global custom_baseline_name
    global cd_drive_name
    spp_dir = fill.get()
    spp_name = os.path.basename(spp_dir)
    custom_baseline_name = custom_fill.get()
    if custom_baseline_name == "":
        custom_baseline_name='None'
    else:
        pass
    cd_drive_name = cd_drive.get()
    cd_drive_name = cd_drive_name+":\\\\"
   
    file = open(".\\.\\Text_files\\input.txt", "w")
    file.write("")
    file.close()
    flag=True
    file = open(".\\.\\Text_files\\input.txt", "a")
    file.write("#INPUT FILE\nSPP_ISO= "+spp_name+"\nCUSTOM_BASELINE_DIR= "+custom_baseline_name+"\nCD_DRIVE= "+cd_drive_name+"\n\n")
    file.write("#SERVER DETAILS\n#<iLO/Network IP> <username> <password> <Linux/Windows/iLO-ESXi> <Firmware/Driver/Both/All>\n")
    for elem in obj:
        #print(elem)
        username_info = elem.username.get()
        password_info = elem.password.get()
        net_id_info = elem.net_id.get()
        #net_id_type = elem.net_ip.get()
        os_type = elem.os.get()
        comp_type = elem.comp.get()
        print(spp_name)
        if fill.get()=="" or cd_drive.get()=="":
            messagebox.showerror("Alert!!","Select spp")
            flag=False
        else:
            if elem.net_id.get() == "" :
                if elem.password.get() != "" or  elem.username.get()!="":
                    messagebox.showerror("Alert!!","Enter all the fileds")
                    flag=False
            elif elem.password.get() == "":
                if elem.net_id.get() != ""  or  elem.username.get()!="":
                    messagebox.showerror("Alert!!","Enter all the fileds")
                    flag=False
            elif elem.username.get()=="":
                if elem.password.get() != ""  or  elem.net_id.get() != "" :
                    messagebox.showerror("Alert!!","Enter all the fileds")
                    flag=False
            else:
                print(username_info,password_info,net_id_info,os_type,comp_type)
                file.write(net_id_info+" "+username_info+" "+password_info+" "+os_type+" "+comp_type+"\n")
                flag=True
                val=str(spp_dir[0])+":"
                os.system('cmd /c "c: & '+str(val)+' & cd "'+str(spp_dir.split('\\'+spp_name)[0]).replace('\\','\\\\')+'" & "'+spp_name)
                #os.system('cmd /c '+strng)
            print(" User ", username_info, " has been registered successfully",password_info,net_id_info)
    file.close()
    if flag==True:
        main.destroy()

def heading():
    global obj
    network_label = Label(frame,text="IP Adress", font=('Helvetica', 12, 'bold'),bg="#fbeec1",width=10 ).grid(row=inc,column=1,padx=20,pady=10)
    username_label = Label(frame,text="Username", font=('Helvetica', 12, 'bold'),bg="#fbeec1",width=10).grid(row=inc,column=2,padx=20,pady=10)
    password_label = Label(frame,text="Password", font=('Helvetica', 12, 'bold'),bg="#fbeec1",width=10).grid(row=inc,column=3,padx=20,pady=10)
    #value = Label(frame,text="Network"+str(val), font=('Helvetica', 12, 'bold'),width=10).grid(row=inc,column=0,padx=10,pady=5)
    #network_type_label = Label(text="ILO/NET IP", font=('Helvetica', 16, 'bold'))
    #network_type_label.place(x=950,y=200)
    os_type_label = Label(frame,text="OS Type", font=('Helvetica', 12, 'bold'),bg="#fbeec1",width=10).grid(row=inc,column=4,padx=20,pady=10)
    comp_type_label = Label(frame,text="Component", font=('Helvetica', 12, 'bold'),bg="#fbeec1",width=10 ).grid(row=inc,column=5,padx=20,pady=10)
    n=add()
    obj.append(n)

def add_button():
    global obj
    n = add()
    print(n)
    obj.append(n)

def delete_button():
    global obj
    del obj[-1]

def select():
    spp=path()
    fill.set(spp)

def custom_baseline():
    directory=filedialog.askdirectory()
    custom_fill.set(directory.replace('/','\\\\'))

def path():
    directory=filedialog.askopenfilename(initialdir="D:\\spp", title="Select a SPP")
    return directory.replace('/','\\')

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=1800,height=750)
    
main = Tk()
main.geometry("1920x1080")

myframe=Frame(main,relief=GROOVE,width=50,height=100,bd=1,bg="black")
myframe.place(x=10,y=200)

canvas=Canvas(myframe,bg="#fbeec1")
frame=Frame(canvas,bg="#fbeec1")
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
username = StringVar()
password = StringVar()
net_id = StringVar()
fill = StringVar()
custom_fill = StringVar()
cd_drive = StringVar()
select_label=Entry(textvariable=fill,width=30,state=DISABLED).place(x=200,y=110)
Label(text="*", font=('Helvetica', 16, 'bold'),fg="#000000",bg="#659DBD").place(x=370,y=110)
select_custombaseline_label= Entry(textvariable=custom_fill,width=30,state=DISABLED).place(x=770,y=110)
main.geometry("1920x1080")
header = Label(text="ENTER THE REQUIRED INFORMATION", font=('Helvetica', 26, 'bold'),fg="#000000",bg="#659DBD")
header.pack(pady=20)
submit = Button(main,text='Submit',command=save_info, font=('Helvetica', 16, 'bold')).place(x=900,y=960)
inc=-1
val=0

select_spp_button = Button(main,text='Select SPP iso',command=select, font=('Helvetica', 16, 'bold'),fg="#ffffff",bg="#05386b",activebackground="#0538bb",activeforeground="#ffffff").place(x=25,y=100)
select_custombaseline_button = Button(main,text='Select custom baseline',command=custom_baseline, font=('Helvetica', 16, 'bold'),fg="#ffffff",bg="#05386b",activebackground="#0538bb",activeforeground="#ffffff").place(x=500,y=100)
select_cd=Entry(textvariable=cd_drive,width=30).place(x=1270,y=105)
Label(text="*", font=('Helvetica', 16, 'bold'),fg="#000000",bg="#659DBD").place(x=1450,y=105)
cd_label = Label(text="CD drive name:", font=('Helvetica', 16, 'bold'),fg="#000000",bg="#659DBD").place(x=1100,y=100)
flag=True
if flag==True:
    flag=False
    inc+=1
    main_button = Button(frame,text='Add Server',command=add_button, font=('Helvetica', 12, 'bold'),fg="#ffffff",bg="#05386b",activebackground="#0538bb",activeforeground="#ffffff").grid(row=inc,column=0)
    heading()
    
main.configure(background="#659DBD")
main.mainloop()