from tkinter import *
import mysql.connector
from mysql.connector import Error
import os
import sys
from datetime import date
from tkinter.ttk import Combobox
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, StringVar
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

from backend import *
from mysql import *
import warnings
warnings.filterwarnings("ignore",message="X does not have a valid feature names")
background = "#f0ddd5"
framebg = "#62a7ff"
framefg = "#fefbfb"

root = Tk()
root.title("Heart Attack Prediction System")
root.geometry('1450x730+60+80')
root.resizable(False, False)
root.config(bg=background)


########Analysis####

def analysis():
    try:
        name = Name.get()
        D1 = Date.get()
        today = datetime.date.today()
        A = today.year - int(DOB.get())

        # Get and convert categorical values to numeric
        B = gen.get()  # Gender: 1 for male, 2 for female
        F = fbs.get()  # Fasting blood sugar: 1 for true, 2 for false
        I = exang.get()  # Exercise-induced angina: 1 for yes, 2 for no
        C = int(selection4())  # Chest pain type
        G = int(restecg_combobox.get())  # Resting ECG results
        K = int(selection5())  # Slope of the peak exercise ST segment
        L = int(ca_combobox.get())  # Number of major vessels colored by fluoroscopy
        M = int(thal_combobox.get())  # Thalassemia: 0, 1, 2, 3

        # Convert the rest of the input data to integers
        D = int(trestbps.get())
        E = int(chol.get())
        H = int(thalach.get())
        J = float(oldpeak.get())

        # Check inputs
        print(f"Age: {A}, Gender: {B}, Chest Pain: {C}, Resting BP: {D}, Cholesterol: {E}, Fasting Blood Sugar: {F}")
        print(f"Resting ECG: {G}, Max Heart Rate: {H}, Exercise Induced Angina: {I}, Oldpeak: {J}")
        print(f"Slope: {K}, Major Vessels: {L}, Thalassemia: {M}")

        # Graphs
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot(["sex", "fbs", "exang"], [B, F, I])
        canvas = FigureCanvasTkAgg(f)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.place(width=250, height=250, x=600, y=240)

        f2 = Figure(figsize=(5, 5), dpi=100)
        a2 = f2.add_subplot(111)
        a2.plot(["age", "trestbps", "chol", "thalach"], [A, D, E, H])
        canvas2 = FigureCanvasTkAgg(f2)
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas2._tkcanvas.place(width=250, height=250, x=860, y=240)

        f3 = Figure(figsize=(5, 5), dpi=100)
        a3 = f3.add_subplot(111)
        a3.plot(["oldpeak", "restecg", "cp"], [J, G, C])
        canvas3 = FigureCanvasTkAgg(f3)
        canvas3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas3._tkcanvas.place(width=250, height=250, x=600, y=470)

        f4 = Figure(figsize=(5, 5), dpi=100)
        a4 = f4.add_subplot(111)
        a4.plot(["slope", "ca", "thal"], [K, L, M])
        canvas4 = FigureCanvasTkAgg(f4)
        canvas4.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas4._tkcanvas.place(width=250, height=250, x=860, y=470)

        # Prepare input data for prediction
        input_data = [A, B, C, D, E, F, G, H, I, J, K, L, M]

        heart_data = pd.read_csv(Dataset path)
        feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        heart_data.columns = feature_names + ['target']

        X = heart_data.drop('target', axis=1)
        y = heart_data['target']

        X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state=23)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, Y_train)

        X_train_prediction = model.predict(X_train)
        training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
        print(f'Accuracy on Training data: {training_data_accuracy * 100:.2f}%')

        X_test_prediction = model.predict(X_test)
        test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
        print(f'Accuracy on Test data: {test_data_accuracy * 100:.2f}%')

        input_data_as_numpy_array = np.asarray(input_data).reshape(1, -1)
        prediction = model.predict(input_data_as_numpy_array)

        if prediction[0] == 0:
            print("The person does not have a heart disease")
            report.config(text=f"Report: 0\nYou do not have heart disease", fg="#8dc63f")
            report1.config(text=f"{name}, you do not have heart disease")
        else:
            print("The person has a heart disease")
            report.config(text=f"Report: 1\nYou have heart disease", fg="#ed1c24")
            report1.config(text=f"{name}, you have heart disease")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

###Info window(operated by info button)###
def Info():
    Icon_window = Toplevel(root)
    Icon_window.title("Info")
    Icon_window.geometry("700x600+400+100")
    # icon image
    image_icon = PhotoImage(file=Icon image path)
    Icon_window.iconphoto(False, image_icon)

    # Heading
    Label(Icon_window, text="Infromation related to dataset", font="robot 19 bold").pack(padx=20, pady=20)

    # info
    Label(Icon_window, text="age - age in years", font="arial 11").place(x=20, y=100)
    Label(Icon_window, text="sex - sex (1 = male; 0 = female)", font="arial 11").place(x=20, y=130)
    Label(Icon_window, text="cp - chest pain type (0 = typical angina; 1 = atypical angina; 2 = non-anginal pain; 3 = asymptomatic)", font="arial 11").place(x=20, y=160)
    Label(Icon_window, text="trestbps - resting blood pressure (in mm Hg on admission to the hospital)", font="arial 11").place(x=20, y=190)
    Label(Icon_window, text="chol - serum cholestoral in mg/dl", font="arial 11").place(x=20, y=220)
    Label(Icon_window, text="fbs - fasting blood sugar > 120 mg/dl (1 = true; 0 = false)", font="arial 11").place(x=20, y=250)
    Label(Icon_window, text="restecg - resting electrocardiographic results (0 = normal; 1 = having ST-T; 2 = hypertrophy)", font="arial 11").place(x=20, y=280)
    Label(Icon_window, text="thalach - maximum heart rate achieved", font="arial 11").place(x=20, y=310)
    Label(Icon_window, text="exang - exercise induced angina (1 = yes; 0 = no)", font="arial 11").place(x=20, y=340)
    Label(Icon_window, text="oldpeak - ST depression induced by exercise relative to rest", font="arial 11").place(x=20, y=370)
    Label(Icon_window, text="slope - the slope of the peak exercise ST segment (0 = upsloping; 1 = flat; 2 = downsloping)", font="arial 11").place(x=20, y=400)
    Label(Icon_window, text="ca - number of major vessels (0-3) colored by flourosopy", font="arial 11").place(x=20, y=430)
    Label(Icon_window, text="thal - 0 = normal; 1 = fixed defect; 2 = reversable defect", font="arial 11").place(x=20, y=460)

    Icon_window.mainloop()


def logout():
    root.destroy()


def Clear():
    Name.set('')
    DOB.set('')
    trestbps.set('')
    chol.set('')
    thalach.set('')
    oldpeak.set('')


##header section 2
logo = PhotoImage(file=Header image path)
myimage = Label(image=logo, bg=background)
myimage.place(x=0, y=0)

# frame 3
Heading_entry = Frame(root, width=800, height=190, bg="#df2d4b")
Heading_entry.place(x=600, y=20)

Label(Heading_entry, text="Registration No.", font="arial 13", bg="#df2d4d", fg=framefg).place(x=30, y=0)
Label(Heading_entry, text="Date", font="arial 13", bg="#df2d4d", fg=framefg).place(x=430, y=0)

Label(Heading_entry, text="Patient Name", font="arial 13", bg="#df2d4d", fg=framefg).place(x=30, y=90)
Label(Heading_entry, text="Birth Year", font="arial 13", bg="#df2d4d", fg=framefg).place(x=430, y=90)

Entry_image = PhotoImage(file=Rounded Rectangle 1 image path)
Entry_image2 = PhotoImage(file=Rounded Rectangle 2 image path)
Label(Heading_entry, image=Entry_image, bg="#df2d4b").place(x=20, y=30)
Label(Heading_entry, image=Entry_image, bg="#df2d4b").place(x=430, y=30)

Label(Heading_entry, image=Entry_image2, bg="#df2d4b").place(x=20, y=120)
Label(Heading_entry, image=Entry_image, bg="#df2d4b").place(x=430, y=120)

Registration = IntVar()
reg_entry = Entry(Heading_entry, textvariable=Registration, width=30, font="arial 15", bg="#0e5363", fg="white",
                  bd=0)
reg_entry.place(x=30, y=45)

Date = StringVar()
today = date.today()
d1 = today.strftime("%d/%m/%Y")
data_entry = Entry(Heading_entry, textvariable=Date, width=15, font="arial 15", bg="#0e5363", fg="white", bd=0)
data_entry.place(x=500, y=45)
Date.set(d1)

Name = StringVar()
name_entry = Entry(Heading_entry, textvariable=Name, width=20, font="arial 20", bg="#ededed", fg="#222222", bd=0)
name_entry.place(x=30, y=130)

DOB = StringVar()
dob_entry = Entry(Heading_entry, textvariable=DOB, width=20, font="arial 20", bg="#ededed", fg="#222222", bd=0)
dob_entry.place(x=450, y=130)

########BODY
Detail_entry = Frame(root, width=490, height=260, bg="#dbe0e3")
Detail_entry.place(x=30, y=450)

######Radio Button
Label(Detail_entry, text="sex:", font="arial 13", bg=framebg, fg=framefg).place(x=10, y=10)
Label(Detail_entry, text="fbs:", font="arial 13", bg=framebg, fg=framefg).place(x=180, y=10)
Label(Detail_entry, text="exang:", font="arial 13", bg=framebg, fg=framefg).place(x=335, y=10)

gen = IntVar()
R1 = Radiobutton(Detail_entry, text='Male', variable=gen, value=1)
R2 = Radiobutton(Detail_entry, text="Female", variable=gen, value=2)
R1.place(x=43, y=10)
R2.place(x=93, y=10)

fbs = IntVar()
R3 = Radiobutton(Detail_entry, text='True', variable=fbs, value=1)
R4 = Radiobutton(Detail_entry, text="False", variable=fbs, value=2)
R3.place(x=213, y=10)
R4.place(x=263, y=10)

exang = IntVar()
R5 = Radiobutton(Detail_entry, text='Yes', variable=exang, value=1)
R6 = Radiobutton(Detail_entry, text="No", variable=exang, value=2)
R5.place(x=387, y=10)
R6.place(x=430, y=10)

#######Coboboxx
Label(Detail_entry, text="cp:", font="arial 13", bg=framebg, fg=framefg).place(x=10, y=50)
Label(Detail_entry, text="restecg:", font="arial 13", bg=framebg, fg=framefg).place(x=10, y=90)
Label(Detail_entry, text="slope:", font="arial 13", bg=framebg, fg=framefg).place(x=10, y=130)
Label(Detail_entry, text="ca:", font="arial 13", bg=framebg, fg=framefg).place(x=10, y=170)
Label(Detail_entry, text="thal:", font="arial 13", bg=framebg, fg=framefg).place(x=10, y=210)


def selection4():
    input = cp_combobox.get()
    if input == "0=typical angina":
        return 0
    elif input == "1=atypical angina":
        return 1
    elif input == "2=non-anginal pain":
        return 2
    elif input == "3=asymptomatic":
        return 3
    else:
        return 0  # Default value


def selection5():
    input = slope_combobox.get()
    if input == "0=upsloping":
        return 0
    elif input == "1=flat":
        return 1
    elif input == "2=downsloping":
        return 2
    else:
        return 0  # Default value


cp_combobox = Combobox(Detail_entry,values=['0=typical angina', '1=atypical angian', '2=non-anginal pain', '3=asymptomatic'],font="arial 12", state="r", width=11)
restecg_combobox = Combobox(Detail_entry, values=['0', '1', '2'], font="arial 12", state="r", width=11)
slope_combobox = Combobox(Detail_entry, values=['0=upsloping', '1=flat', '2=downsloping'], font="arial 12", state="r", width=12)
ca_combobox = Combobox(Detail_entry, values=['0', '1', '2', '3', '4'], font="arial 12", state="r", width=14)
thal_combobox = Combobox(Detail_entry, values=['0', '1', '2', '3'], font="arial 12", state="r", width=14)

cp_combobox.place(x=50, y=50)
restecg_combobox.place(x=80, y=90)
slope_combobox.place(x=70, y=130)
ca_combobox.place(x=50, y=170)
thal_combobox.place(x=50, y=210)

#########Data entry box############ 7
Label(Detail_entry, text="Smoking:", font="arial 13", width=7, bg="#dbe0e3", fg="black").place(x=240, y=50)
Label(Detail_entry, text="trestbpc:", font="arial 13", width=7, bg=framebg, fg=framefg).place(x=240, y=90)
Label(Detail_entry, text="chol:", font="arial 13", width=7, bg=framebg, fg=framefg).place(x=240, y=130)
Label(Detail_entry, text="thalach:", font="arial 13", width=7, bg=framebg, fg=framefg).place(x=240, y=170)
Label(Detail_entry, text="oldpeak:", font="arial 13", width=7, bg=framebg, fg=framefg).place(x=240, y=210)

trestbps = StringVar()
chol = StringVar()
thalach = StringVar()
oldpeak = StringVar()

trestbps_entry = Entry(Detail_entry, textvariable=trestbps, width=10, font="arial 15", bg="#ededed", fg="#222222", bd=0)
chol_entry = Entry(Detail_entry, textvariable=chol, width=10, font="arial 15", bg="#ededed", fg="#222222", bd=0)
thalach_entry = Entry(Detail_entry, textvariable=thalach, width=10, font="arial 15", bg="#ededed", fg="#222222", bd=0)
oldpeak_entry = Entry(Detail_entry, textvariable=oldpeak, width=10, font="arial 15", bg="#ededed", fg="#222222", bd=0)
trestbps_entry.place(x=320, y=90)
chol_entry.place(x=320, y=130)
thalach_entry.place(x=320, y=170)
oldpeak_entry.place(x=320, y=210)

###########Report############ 8

square_report_image = PhotoImage(file=Report image path)
report_background = Label(image=square_report_image, bg=background)
report_background.place(x=1120, y=340)

report = Label(root, font="arial 12 bold", bg="white", fg="#8dc63f")
report.place(x=1180, y=550)

report1 = Label(root, font="arial 10 ", bg="white")
report.place(x=1130, y=610)

###########Graph####### 9

graph_image = PhotoImage(file=graph image path)
Label(image=graph_image).place(x=600, y=270)
Label(image=graph_image).place(x=860, y=270)
Label(image=graph_image).place(x=600, y=500)
Label(image=graph_image).place(x=860, y=500)

#############Button##########10

analysis_button = PhotoImage(file=Analysis image path)
Button(root, image=analysis_button, bd=0, bg=background, cursor='hand2', command=analysis).place(x=1130, y=240)

##########info button###
info_button = PhotoImage(file=info image path)
Button(root, image=info_button, bd=0, bg=background, cursor='hand2', command=Info).place(x=10, y=240)

##########save button###
save_button = PhotoImage(file=save image path)
Button(root, image=save_button, bd=0, bg=background, cursor='hand2').place(x=1370, y=250)

##########smoking and non-smoking button#########11

button_mode = True
choice = "smoking"


def changemode():
    global button_mode
    global choice
    if button_mode:
        choice = "non_smoking"
        mode.config(image=non_smoking_icon, activebackground="white")
        button_mode = False

    else:
        choice = "smoking"
        mode.config(image=smoking_icon, activebackground="white")
        button_mode = True
    print(choice)


smoking_icon = PhotoImage(file=smoker image path)
non_smoking_icon = PhotoImage(file=non-smoker image path)
mode = Button(root, image=smoking_icon, bg="#dbe0e3", bd=0, cursor="hand2", command=changemode)
mode.place(x=350, y=495)

################logout############12
logout_icon = PhotoImage(file=logout image path)
logout_button = Button(root, image=logout_icon, bg="#df2d4b", cursor='hand2', bd=0, command=logout)
logout_button.place(x=1390, y=60)

root.mainloop()
