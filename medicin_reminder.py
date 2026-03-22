"""
Medicine Reminder Application
--------------------------------
A Tkinter-based desktop application that allows users to create an account, 
log in, add medicines with reminder times, view the list of medicines, and 
receive pop-up alerts when it's time to take the medicine.

Features:
    • User Login and Account Creation (MySQL authentication)
    • Add Medicine Name and Reminder Time
    • Auto-refreshing table view of medicines
    • Double-click on any row to delete that medicine
    • Real-time reminder notifications every minute
    • Personalized greeting for logged-in user
    • Footer branding with developer name
    • Fully graphical UI built using Tkinter and ttk

Modules Used:
    tkinter        -> GUI creation and message boxes
    mysql.connector -> Database connectivity to MySQL
    datetime        -> Time checking for reminders
    ttk             -> Table (Treeview) widget for displaying medicines

Database -> login_db

Database Tables:
    users(username, password)
    data(username, medicin, frequence, ids)

Developed By:
    Eagle Head | Daksh Sharma (2025)
"""


import tkinter
from tkinter import messagebox, ttk
import mysql.connector
from datetime import timedelta
from datetime import datetime


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="login_db")

cur = conn.cursor()


root = tkinter.Tk()
root.title("Medicin Reminder - Login")
root.geometry("400x500")
root.configure(bg="#f7f7f7")
root.resizable(False, False)


def main_window():
    win = tkinter.Tk()
    win.title("Medicine Reminder - Main")
    win.geometry("700x600")
    win.configure(bg="#f7f7f7")
    win.resizable(False, False)

    main_heading = tkinter.Label(win, text="MEDICINE REMINDER", bg="white", fg="black", font=("Arial", 30, "bold"))
    main_heading.pack(pady=(30, 5))

    sub_heading = tkinter.Label(win, text="Main Page", bg="white", fg="black", font=("Arial", 20, "bold"))
    sub_heading.pack(pady=(0, 20))

    hello_label = tkinter.Label(win, text=f"Hello, {username}",bg="white",fg="black",font=("Arial", 14, "bold"))
    hello_label.pack(pady=(0, 10))


    frame1 = tkinter.Frame(win, bg="#e6e6e6", bd=2, relief="groove")
    frame1.pack(pady=20, padx=20, fill="both")
    frame1.config(width=600, height=310)

    frame2 = tkinter.Frame(win, bg="#d9d9d9", bd=2,relief="groove", height=120)
    frame2.pack(pady=10, padx=20, fill="x")
    frame2.config(height=120)

    medci_label = tkinter.Label(frame2, text="Medicine Name", bg="#d9d9d9", fg="black", font=("Arial", 11, "bold"))
    medci_label.grid(row=0, column=0, padx=10, pady=20)

    medci_entry = tkinter.Entry(frame2, bg="#f2f2f2", fg="black", width=20, bd=0, font=("Arial", 9))
    medci_entry.grid(row=0, column=1, padx=10)

    time_label = tkinter.Label(frame2, text="frequence", bg="#d9d9d9", fg="black", font=("Arial", 11, "bold"))
    time_label.grid(row=0, column=2, padx=10)

    time_entry = tkinter.Entry(frame2, bg="#f2f2f2", fg="black", width=20, bd=0, font=("Arial", 9))
    time_entry.grid(row=0, column=3, padx=10)

    def delete_selected(event):
        item = tree.focus()
        if item:
            data = tree.item(item)["values"]
            med = data[1]
            freq = data[2]
            cur.execute("DELETE FROM data WHERE username=%s AND medicin=%s AND frequence=%s",(username, med, freq))
            conn.commit()
            tree.delete(item)


    columns = ("SNO.", "Medicine", "Frequence")
    tree = ttk.Treeview(frame1, columns=columns, show="headings")
    tree.heading("Medicine", text="Medicine")
    tree.heading("Frequence", text="Frequence")
    tree.heading("SNO.", text="SNO.")

    tree.column("SNO.", width=80, anchor="center")
    tree.column("Medicine", width=420, anchor="center")
    tree.column("Frequence", width=100, anchor="center")

    tree.bind("<Double-1>", delete_selected)

    vsb = ttk.Scrollbar(frame1, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    from datetime import datetime

    def check_medicine_time():
        cur.execute("select medicin, frequence from data where username=%s", (username,))
        rows = cur.fetchall()
        now = datetime.now().strftime("%H:%M")
        print(now)
        for med, t in rows:
            if isinstance(t, timedelta):
                h = str(t).split(":")[0]
                m = str(t).split(":")[1]
                t_str = f"{h}:{m}"
            else:
                t_str = str(t)[:5]
            if t_str == now:
                messagebox.showinfo("Reminder", f"Time to take Medicine: {med}")

        win.after(60000, check_medicine_time)


    def load_data():
        tree.delete(*tree.get_children())
        cur.execute("select medicin, frequence from data where username=%s", (username,))
        rows = cur.fetchall()
        sno = 1
        for med, freq in rows:
            tree.insert("", "end", values=(sno, med, freq, "Delete"))
            sno+=1

    def insert_data():
        medci_name = medci_entry.get().strip()
        frequence = time_entry.get().strip()

        if medci_name == "" or frequence == "":
            messagebox.showerror("Empty", "Enter both Medicine Name and Frequence")
            return

        try:
            cur.execute("insert into data (username, medicin, frequence) values (%s, %s, %s)",(username, medci_name, frequence))
            conn.commit()
            load_data()
            messagebox.showinfo("Success", "Medicine Added Successfully")

        except:
            messagebox.showerror("Error", "Medicine already exists or DB error")

    add_button = tkinter.Button(frame2, text="Add", bg="#0078FF", fg="white",width=10, font=("Arial", 9, "bold"),cursor="hand2", bd=0, command=insert_data)
    add_button.grid(row=0, column=4, padx=10)

    footer = tkinter.Label(win,text="Daksh Sharma | Vansh Sharma",bg="white",fg="black",font=("Arial", 9))
    footer.pack(pady=15)

    load_data()
    check_medicine_time()
    win.mainloop()

frame = tkinter.Frame(root, bg="white", bd=2, relief="groove")
frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=420)

heading = tkinter.Label(frame, text="MEDICINE REMINDER",bg="white", fg="black", font=("Arial", 14, "bold"))
heading.pack(pady=(30, 5))

subheading = tkinter.Label(frame, text="Login Page",bg="white", fg="black", font=("Arial", 11, "bold"))
subheading.pack(pady=(0, 20))

user_label = tkinter.Label(frame, text="Username",bg="white", fg="black", font=("Arial", 10))
user_label.pack(pady=(10, 5))

user_entry = tkinter.Entry(frame, bg="#f2f2f2", fg="black", width=30, bd=0, font=("Arial", 10))
user_entry.pack(pady=(0, 10), ipady=5)

pass_label = tkinter.Label(frame, text="Password",bg="white", fg="black", font=("Arial", 10))
pass_label.pack(pady=(10, 5))

pass_entry = tkinter.Entry(frame, show="*", bg="#f2f2f2", fg="black", width=30, bd=0, font=("Arial", 10))
pass_entry.pack(pady=(0, 20), ipady=5)


def check_login():
    global username
    username = user_entry.get().strip()
    password = pass_entry.get().strip()
    cur.execute("select * from users where username=%s AND password=%s", (username, password))
    data = cur.fetchone()
    if data:
        messagebox.showinfo("Login Success", "Welcome to Medicine Reminder System!")
        root.destroy()
        main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


def create_account():
    username = user_entry.get().strip()
    password = pass_entry.get().strip()
    if username == "" or password == "":
        return
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    try:
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully")
    except:
        messagebox.showerror("Error", "Username already exists")


login_button = tkinter.Button(frame, text="Log in →", bg="#0078FF", fg="white",width=15, font=("Arial", 10, "bold"), bd=0,cursor="hand2", command=check_login)
login_button.pack(pady=(10, 10))

create_account_btn = tkinter.Button(frame, text="Create account", bg="silver",fg="black", font=("Arial", 9, "underline"),cursor="hand2", command=create_account)
create_account_btn.pack(pady=(10, 20))

footer = tkinter.Label(frame, text="Daksh Sharma | Vansh Sharma",bg="white", fg="black", font=("Arial", 8))
footer.pack(side="bottom", pady=10)

root.mainloop()
