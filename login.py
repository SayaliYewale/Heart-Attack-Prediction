from tkinter import *
from tkinter import messagebox
import mysql.connector

background = "#06283D"
framebg = "#EDEDED"
framefg = "#06283D"

global trial_no
trial_no=0
def trial():
    global trial_no

    trial_no +=1
    print("Trial no is:",trial_no)
    if trial_no==3:
        messagebox.showwarning("Warning","You havr tried more then linit!!")
        root.destroy()
def loginuser():
    username = user.get()
    password = code.get()

    if (username == "" or username == "UserID") or (password == "" or password == "Password"):
        messagebox.showerror("Entry error", "Type username or password!!")
    else:
        mycursor = None  # Initialize mycursor here
        try:
            mydb = mysql.connector.connect(host='localhost', user=username, password=userpassword, database=databasename)
            mycursor = mydb.cursor()
            print("Connected to database!!")

            command = "use databasename"
            mycursor.execute(command)

            command = "select * from login where Username=%s and Password=%s"
            mycursor.execute(command, (username, password))
            myresult = mycursor.fetchone()
            print(myresult)

            if myresult is None:
                messagebox.showinfo("invalid", "Invalid userid and password!!")
                trial()
            else:
                messagebox.showinfo("Login", "Successfully Login!!")
                root.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Connection", f"Database connection not established: {err}")
        finally:
            if mycursor:
                mycursor.close()

root = Tk()
root.title("Login System")
root.geometry("1250x700+210+100")
root.config(bg=background)
root.resizable(False, False)

# Icon image
image_icon = PhotoImage(file=icon image path)
root.iconphoto(False, image_icon)

# Background image
frame = Frame(root, bg="red")  # Fix typo here, should be `frame`, not `Frame`
frame.pack(fill=Y)

backgroundimage = PhotoImage(file=login image path)
Label(frame, image=backgroundimage).pack()  # Fix typo here, should be `frame`, not `Frame`

####user entry
def user_enter(e):
    user.delete(0,'end')
def user_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'UserID')


user =Entry(frame,width=18,fg="#fff",borde=0,bg="#375174",font=('Arial Bold',24))
user.insert(0,"UserID")
user.bind("<FocusIn>",user_enter)
user.bind("<FocusOut>",user_leave)
user.place(x=500,y=315)

####Password entry
def password_enter(e):
    code.delete(0,'end')
def password_leave(e):
    if code.get()=='':
        code.insert(0,'Password')


code =Entry(frame,width=18,fg="#fff",borde=0,bg="#375174",font=('Arial Bold',24))
code.insert(0,"Password")
code.bind("<FocusIn>",password_enter)
code.bind("<FocusOut>",password_leave)
code.place(x=500,y=410)

###hide and show button
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
openeye=PhotoImage(file=openeye image path)
closeeye=PhotoImage(file=closeeye image path)
eyebutton=Button(frame,image=openeye,bg="#375174",bd=0,command=hide)
eyebutton.place(x=780,y=410)

loginButton=Button(root,text="LOGIN",bg="#1f5675",fg="white",width=10,height=1,font=("arial",16,"bold"),bd=0,command=loginuser)
loginButton.place(x=570,y=600)
label=Label(root,text="Don't have an account?",fg="#fff",bg="#00264d",font=("Microsoft Yehei UI Light",9))
label.place(x=500,y=500)

registerButton=Button(root,width=10,text="add new user",border=0,bg="#00264d",cursor='hand2',fg="#57a1f8")
registerButton.place(x=650,y=500)

root.mainloop()
