from tkinter import *
import string
import mysql.connector


win1=Tk()
win1.title("Secure Password Manager")
win1.minsize(width=400,height=720)
emailid=StringVar()
newpass=StringVar()
conpass=StringVar()
#Registeration Page
def logonto():
    win1.destroy()
    import login 
def register():
    conn=mysql.connector.connect(user="root",password="Your_Password",host="localhost",database="password_manager")
    mycur=conn.cursor()
    em=emailid.get()
    np=newpass.get()
    cp=conpass.get()
    mycur.execute("select *from user where emailid='%s'" ,(em))
    if mycur.fetchone():
        lb2.config(text="The User ALready exists ! Please Login Instead.")
    else:
        if np==" ":
            lb2.config(text="Please fill in the register details correctly")
        else:
            if np==cp:
                mycur.execute("insert into user values(%s,%s)",(em,np))
                conn.commit()
                lb2.config(text="Sucessfully Registered")
            else:
                lb2.config(text="Both passwords does'nt Match")
lb1=Label(win1,text="Registeration of New User",font=20)
lb1.grid(row=0,column=3)
lb1=Label(win1,text="E-Mail",font=12)
lb1.grid(row=1,column=2)
en1=Entry(win1,width=20,font=("calabri",10),textvariable=emailid)
en1.grid(row=1,column=3)
lb1=Label(win1,text="New Password",font=10)
lb1.grid(row=2,column=2)
en1=Entry(win1,width=20,font=("calabri",10),textvariable=newpass)
en1.grid(row=2,column=3)
lb1=Label(win1,text="Confirm New Password",font=10)
lb1.grid(row=3,column=2)
en1=Entry(win1,width=20,font=("calabri",10),textvariable=conpass)
en1.grid(row=3,column=3)
b1=Button(win1,text="Register",bg="blue",fg="white",command=register)
b1.grid(row=4,column=3)
lb2=Label(win1,text=" ",font=10)
lb2.grid(row=5,column=3)
b1=Button(win1,text="Log In",bg="blue",fg="white",command=logonto)
b1.grid(row=4,column=2)

win1.mainloop()