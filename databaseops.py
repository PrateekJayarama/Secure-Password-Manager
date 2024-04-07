import cryptography.fernet
import mysql.connector
import random
import string
from tkinter import *

# Database connection
db_config = {
    "user": "root",
    "password": "Your_password",
    "host": "localhost",
    "database": "password_manager"
}
conn = mysql.connector.connect(**db_config)
key = cryptography.fernet.Fernet.generate_key()
fernet = cryptography.fernet.Fernet(key)

# Global variables
name_var = StringVar()
leng_var = IntVar()
webs_var = StringVar()
usern_var = StringVar()
passw_var = StringVar()
details = []

def create():
    mycur = conn.cursor()
    query = ("select COUNT(*) FROM information_schema.tables WHERE table_schema= %s  AND table_name=%s")
    mycur.execute(query, ("password_manager", name_var.get()))
    if mycur.fetchone()[0] == 0:
        lb2.config(text="Your Name Already Exists! Please Enter a Different One.")
    else:
        mycur.execute("CREATE TABLE %s(website varchar(30),username varchar(30),password varchar(12))" % name_var.get())
        lb2.config(text="Sucessfully created!")

def pass_generate():
    passg = ""
    for i in range(0, leng_var.get()):
        passg = passg + random.choice("abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*-=_+")
    passw_var.set(passg)
    lb5.config(text="Successfully Generated. Would you like to add it to your password holder?")

def add_db():
    encpass = fernet.encrypt(passw_var.get().encode())
    mycur = conn.cursor()
    mycur.execute("INSERT INTO %s values(%s,%s,%s)" % (name_var.get(), webs_var.get(), encpass, usern_var.get()))
    mycur.commit()
    lb5.config(text="Added Sucessfully!")

def view_db():
    mycur = conn.cursor()
    mycur.execute("select password from %s" % name_var.get())
    encrypted_passwords = mycur.fetchall()
    mycur.execute("select * from %s" % name_var.get())
    details = mycur.fetchall()
    decrypted_passwords = [fernet.decrypt(password[0]).decode() for password in encrypted_passwords]
    for i, detail in enumerate(details):
        lb.insert(END, (detail[0], detail[1], decrypted_passwords[i]))

win3 = Tk()
win3.minsize(width=400, height=720)

lb1 = Label(win3, text="Create Your Password Holder", font=14)
lb1.grid(row=0, column=2)
lb1 = Label(win3, text="Enter Your Name:")
lb1.grid(row=1, column=1)
en1 = Entry(win3, textvariable=name_var)
en1.grid(row=1, column=2)
b1 = Button(win3, text="Create", bg="blue", fg="white", command=create)
b1.grid(row=1, column=3)
lb2 = Label(win3, text="")
lb2.grid(row=2, column=1)

lb3 = Label(win3, text="Password Generator", font=14)
lb3.grid(row=3, column=2)
lb4 = Label(win3, text="What is the length of the password If you want to generate:")
lb4.grid(row=4, column=1)
en2 = Entry(win3, textvariable=leng_var)
en2.grid(row=4, column=2)
lb4 = Label(win3, text="Website:")
lb4.grid(row=5, column=1)
en2 = Entry(win3, textvariable=webs_var)
en2.grid(row=5, column=2)
lb4 = Label(win3, text="UserName:")
lb4.grid(row=6, column=1)
en2 = Entry(win3, textvariable=usern_var)
en2.grid(row=6, column=2)
b2 = Button(win3, text="Generate", bg="blue", fg="white", command=pass_generate)
b2.grid(row=5, column=3)
b3 = Button(win3, text="Add", bg="blue", fg="white", command=add_db)
b3.grid(row=6, column=3)
lb5 = Label(win3, text="")
lb5.grid(row=7, column=1)
lb = Listbox(win3, width=50, height=10)
lb.grid(row=8, column=1)
b4 = Button(win3, text="View", bg="blue", fg="white", command=view_db)
b4.grid(row=8, column=2)
win3.mainloop()