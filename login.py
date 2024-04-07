from tkinter import *
import string
import mysql.connector
import random
from email.message import EmailMessage
import smtplib
import Register

win2 = Tk()
win2.title("Secure Password Manager")
win2.minsize(width=400, height=720)
emailid = StringVar()
passw = StringVar()
rotp = StringVar()
gotp = ""

def send_otp():
    global gotp
    gotp = ""
    for i in range(6):
        gotp += str(random.randint(0, 9))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("yourmailid@gmail.com", "your_password")
        Content = ("otp is:" + gotp)
        server.sendmail("yourmailid@gmail.com", emailid.get(), Content)
        server.close()
    except Exception as e:
        print(f"Error sending OTP: {e}")
        gotp = ""
    return gotp

def registerto():
    win2.destroy()
    Register.register(emailid.get(), passw.get())

def loger():
    conn = mysql.connector.connect(user="root", password="Your_Password", host="localhost", database="password_manager")
    mycur = conn.cursor()
    mycur.execute("select * from user where id= %s", (emailid.get(),))
    if mycur.rowcount > 0:
        if gotp == rotp.get():
            import databaseops
            databaseops.function_name()
            conn.close()
            win2.destroy()
        else:
            lb2.config(text="Incorrect OTP")
    else:
        lb2.config(text="User doesn't exist please register")
    conn.close()

lb1 = Label(win2, text="Log In Window", font=20)
lb1.grid(row=0, column=3)
lb1 = Label(win2, text="E-Mail", font=12)
lb1.grid(row=1, column=2)
en1 = Entry(win2, width=20, font=("calabri", 10), textvariable=emailid)
en1.grid(row=1, column=3)
lb1 = Label(win2, text="Password", font=10)
lb1.grid(row=2, column=2)
en1 = Entry(win2, width=20, font=("calabri", 10), textvariable=passw)
en1.grid(row=2, column=3)
lb1 = Label(win2, text="OTP", font=10)
lb1.grid(row=3, column=2)
en1 = Entry(win2, width=20, font=("calabri", 10), textvariable=rotp)
en1.grid(row=3, column=3)
bt1 = Button(win2, text="Send OTP", font=10, command=send_otp)
bt1.grid(row=4, column=2)
bt1 = Button(win2, text="Register", font=10, command=registerto)
bt1.grid(row=4, column=3)
bt1 = Button(win2, text="Log In", font=10, command=loger)
bt1.grid(row=5, column=3)
lb2 = Label(win2, text="", font=10)
lb2.grid(row=6, column=3)

