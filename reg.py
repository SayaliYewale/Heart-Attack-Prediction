from tkinter import *
from tkinter import messagebox
import mysql.connector

background = "#06283D"
framebg = "#EDEDED"
framefg = "#06283D"

root = Tk()
root.title("New User Registration")
root.geometry("1250x700+210+100")
root.config(bg=background)
root.resizable(False, False)

def register():
    username=user.get()
    password=code.get()
    admincode=adminaccess.get()

    #print(username,password,admincode)
    if admincode=="9955":
        if (username == "" or username == "UserID") or (password == "" or password == "Password"):
            messagebox.showerror("Entry error", "Type username or password!!")
        else:
            try:
                mydb = mysql.connector.connect(host='localhost', user='username', password="userpassword")
                mycursor = mydb.cursor()
                print("Connected to database!!")
            except:
                messagebox.showerror("Connection", "Database connection not established")
            try:
                command = "use databasename which was created in login page"
                mycursor.execute(command)
                command = "create table login(user int auto_increment key not null,Username varchar(50),Password(100))"
                mycursor.execute(command)
            except:
                mycursor.execute("use databasename which was created in login page")
                mydb=mysql.connector.connect(host="localhost",user="username",password="userpassword",database="databasename which was created in login page")
                mycursor=mydb.cursor()
                command="insert into login(Username,Password) values(%s,%s)"
                mycursor.execute(command,(username,password))
                mydb.commit()
                mydb.close()
                messagebox.showinfo("Register","New User added successfully")
    else:
         messagebox.showerror("Admin code!","Input Correct Admin code to add new user!!")
def login():
    pass
#icon image
image_icon=PhotoImage(file=icon image path)
root.iconphoto(False,image_icon)

#Background image
frame=Frame(root,bg="red")
frame.pack(fill=Y)

backgroundimage=PhotoImage(file=rregister image path)
Label(frame,image=backgroundimage).pack()

adminaccess=Entry(frame,width=15,fg="#000",border=0,bg="#e8ecf7",font=("Arial Bold",20))
adminaccess.focus()
adminaccess.place(x=550,y=280)

#user entry
def user_enter(e):
    user.delete(0,"end")

def user_leave(e):
    name=user.get()
    if name=="":
        user.insert(0,"UserID")

user=Entry(frame,width=18,fg="#fff",bg="#375174",border=0,font=("Arial Bold",20))
user.insert(0,"UserID")
user.bind("<FocusIn>",user_enter)
user.bind("<FocusOut>",user_leave)
user.place(x=500,y=370)

#Password entry
def password_enter(e):
    code.delete(0,"end")

def password_leave(e):
    if code.get()=="":
        code.insert(0,"Password")

code=Entry(frame,width=18,fg="#fff",bg="#375174",border=0,font=("Arial Bold",20))
code.insert(0,"UserID")
code.bind("<FocusIn>",password_enter)
code.bind("<FocusOut>",password_leave)
code.place(x=500,y=470)

button_mode=True
def hide():
    global button_mode

    if button_mode:
        eyebutton.config(image=closeeye,activebackground="white")
        code.config(show="*")
        button_mode=False
    else:
        eyebutton.config(image=openeye,activebackground="white")
        code.config(show="")
        button_mode=True
openeye=PhotoImage(file=Openeye image path)
closeeye=PhotoImage(file=closeeye image path)
eyebutton=Button(frame,image=openeye,bg="#375174",bd=0,command=hide)
eyebutton.place(x=780,y=470)

loginButton=Button(root,text="LOGIN",bg="#1f5675",fg="white",width=10,height=1,font=("arial",16,"bold"),bd=0)
loginButton.place(x=570,y=600)
label=Label(root,text="Don't have an account?",fg="#fff",bg="#00264d",font=("Microsoft Yehei UI Light",9))
label.place(x=500,y=500)

regis_button=Button(root,text="ADD NEW USER",bg="#455c88",fg="white",width=13,height=1,font=("arial",16,"bold"),bd=0)
regis_button.place(x=530,y=600)

backbuttonimage=PhotoImage(file=backbutton image path)
Backbutton=Button(root,image=backbuttonimage,fg="#deeefb")
Backbutton.place(x=20,y=15)
root.mainloop()
