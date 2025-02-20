import sqlite3
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
from PIL import Image, ImageTk
import os

# Database Setup (unchanged)
def create_database():
    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()

    # Students Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        father_name TEXT NOT NULL,
        mother_name TEXT NOT NULL,
        dob TEXT NOT NULL,
        contact TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        vehicle_no TEXT,
        workplace TEXT NOT NULL,
        gender TEXT NOT NULL,
        room_no TEXT NOT NULL,
        bed_no TEXT NOT NULL,
        image_path TEXT
    )
    ''')

    # Employees Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        contact TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        role TEXT NOT NULL,
        salary TEXT NOT NULL
    )
    ''')

    # Visitors Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT NOT NULL,
        purpose TEXT NOT NULL,
        student_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')

    # Guardians Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS guardians (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        name TEXT NOT NULL,
        contact TEXT NOT NULL,
        relation TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')

    # Timing Table (Student In/Out)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS timing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        in_time TEXT,
        out_time TEXT,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')

    # Leave Applications Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        reason TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')
    
    # Fees Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        amount REAL NOT NULL,
        due_date TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')

    # Complaints Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        description TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')

    # Mess Menu Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mess_menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT NOT NULL,
        breakfast TEXT NOT NULL,
        lunch TEXT NOT NULL,
        dinner TEXT NOT NULL
    )
    ''')

    # Feedback Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        message TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')

    # Notifications Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        message TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')
     # Add a table for background images
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS background_image (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

create_database()

# Frontend Setup
base = Tk()
base.title("HOSTEL MANAGEMENT SYSTEM")
base.geometry('1800x1100+0+0')
base.configure(bg='#2c3e50')  # Dark background

# Global variable to store the image path
student_image_path = None

# Custom Styles
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10, background='#3498db', foreground='black')
style.map('TButton', background=[('active', '#2980b9')])

style.configure('TLabel', font=('Helvetica', 14), background='#2c3e50', foreground='white')
style.configure('TEntry', font=('Helvetica', 12), padding=5)

# ----------------- Login Screen -----------------
def login():
    if user_entry.get() == "Vraj" and pass_entry.get() == "vraj346":
        dashboard_screen()  # Redirect to dashboard after login
    else:
        messagebox.showerror("Error", "Invalid Credentials")

def login_screen():
    for widget in base.winfo_children():
        widget.destroy()

    login_frame = Frame(base, bg='#34495e')
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(login_frame, text="HOSTEL MANAGEMENT SYSTEM", font=("Helvetica 30 bold"), bg="#34495e", fg="white").pack(pady=20)

    Label(login_frame, text="Username", font=("Helvetica 20"), bg="#34495e", fg="white").pack()
    global user_entry
    user_entry = ttk.Entry(login_frame, font=("Helvetica 20"))
    user_entry.pack(pady=10)

    Label(login_frame, text="Password", font=("Helvetica 20"), bg="#34495e", fg="white").pack()
    global pass_entry
    pass_entry = ttk.Entry(login_frame, show="*", font=("Helvetica 20"))
    pass_entry.pack(pady=10)

    ttk.Button(login_frame, text="Login", command=login).pack(pady=20)

# ----------------- Dashboard Screen -----------------
def dashboard_screen():
    for widget in base.winfo_children():
        widget.destroy()

    # Fetch the background image path from the database
    try:
        conn = sqlite3.connect('hostel_management.db')
        cursor = conn.cursor()
        cursor.execute("SELECT image_path FROM background_image LIMIT 1")
        result = cursor.fetchone()
        conn.close()

        if result:
            image_path = result[0]
            # Load the image using PIL
            img = Image.open(image_path)
            img = img.resize((1800, 1100), Image.Resampling.LANCZOS)  # Resize the image to fit the window
            bg_image = ImageTk.PhotoImage(img)

            # Create a label with the image and place it at the back
            background_label = Label(base, image=bg_image)
            background_label.image = bg_image  # Keep a reference to avoid garbage collection
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading background image: {e}")


    # Dashboard Title
    Label(base, text="ADMIN DASHBOARD", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    # Quick Access Buttons
    ttk.Button(base, text="Add Student", command=add_student).place(x=50, y=150)
    ttk.Button(base, text="Add Employee",  command=add_employee).place(x=250, y=150)
    ttk.Button(base, text="Add Visitor",  command=add_visitor).place(x=450, y=150)
    ttk.Button(base, text="Add Guardian",  command=add_guardian).place(x=50, y=250)
    ttk.Button(base, text="Student Timing",  command=student_timing).place(x=250, y=250)
    ttk.Button(base, text="Student Details",  command=student_personal_detail).place(x=450, y=250)
    ttk.Button(base, text="Leave Application",  command=leave_application).place(x=50, y=350)
    ttk.Button(base, text="Information",  command=show_information).place(x=250, y=350)
    ttk.Button(base, text="Manage Students",  command=manage_students).place(x=450, y=350)
    ttk.Button(base, text="Manage Fees",  command=manage_fees).place(x=50, y=450)
    ttk.Button(base, text="Manage Complaints", command=manage_complaints).place(x=250, y=450)
    ttk.Button(base, text="Manage Mess Menu",  command=manage_mess_menu).place(x=450, y=450)
    ttk.Button(base, text="Generate Reports",  command=generate_reports).place(x=50, y=550)
    ttk.Button(base, text="Send Notifications", command=send_notifications).place(x=250, y=550)
    ttk.Button(base, text="change background", command=change_background).place(x=450, y=550)
    # Logout Button
    ttk.Button(base, text="Logout", command=logout).place(x=50, y=650)
    

def change_background():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    
    if file_path:
        try:
            # Save the image path to the database
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()

            # Clear any existing background image entry
            cursor.execute("DELETE FROM background_image")
            
            # Insert the new image path
            cursor.execute("INSERT INTO background_image (image_path) VALUES (?)", (file_path,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Background image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image path: {e}")
# ----------------- Send Notifications -----------------
def send_notifications():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="SEND NOTIFICATIONS", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    Label(base, text="Student ID", font=("Helvetica 20"), bg="#2c3e50", fg="white").place(x=400, y=150)
    global notification_student_id_entry
    notification_student_id_entry = ttk.Entry(base, font=("Helvetica 20"))
    notification_student_id_entry.place(x=600, y=150)

    Label(base, text="Message", font=("Helvetica 20"), bg="#2c3e50", fg="white").place(x=400, y=200)
    global notification_message_entry
    notification_message_entry = ttk.Entry(base, font=("Helvetica 20"))
    notification_message_entry.place(x=600, y=200)

    def send_notification():
        student_id = notification_student_id_entry.get()
        message = notification_message_entry.get()

        if not student_id or not message:
            messagebox.showerror("Error", "Please enter Student ID and Message")
            return

        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notifications (student_id, message) VALUES (?, ?)
            ''', (student_id, message))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Notification sent successfully!")
            dashboard_screen()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Send", command=send_notification).place(x=600, y=250)
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=800, y=250)

def logout():
    for widget in base.winfo_children():
        widget.destroy()
    login_screen()  # Redirect to the login screen

# ----------------- Manage Students -----------------
def manage_students():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="MANAGE STUDENTS", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    # Add Student Button
    ttk.Button(base, text="Add Student", command=add_student).place(x=50, y=150)

    # View Students Button
    ttk.Button(base, text="View Students", command=view_students).place(x=400, y=150)

    # Back Button
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=750, y=150)

# ----------------- View Students -----------------    
def view_students():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="VIEW STUDENTS", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    canvas = Canvas(base, bg="#2c3e50")
    scrollbar = Scrollbar(base, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#2c3e50")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for student in students:
        student_frame = Frame(scrollable_frame, bg="#34495e")
        student_frame.pack(anchor='w', pady=5, padx=10)
        Label(student_frame, 
              text=f"ID: {student[0]} | Name: {student[1]} {student[2]} | Contact: {student[6]}",
              font=("Helvetica 15"), bg="#34495e", fg="white").pack(side='left')
        ttk.Button(student_frame, text="Delete", 
              command=lambda s=student[0]: delete_student(s)).pack(side='right')

    ttk.Button(base, text="Back", command=manage_students).place(x=50, y=750)

def delete_student(student_id):
    try:
        conn = sqlite3.connect('hostel_management.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student deleted successfully!")
        view_students()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

# ----------------- Manage Fees -----------------
def manage_fees():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="MANAGE FEES", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    # Add Fee Button
    ttk.Button(base, text="Add Fee", command=add_fee).place(x=50, y=150)

    # View Fees Button
    ttk.Button(base, text="View Fees", command=view_fees).place(x=400, y=150)

    # Back Button
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=750, y=150)

# ----------------- Add Fee -----------------
def add_fee():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="ADD FEE", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    entries = {}
    fields = [
        ("Student ID", 100), ("Amount", 150), ("Due Date (YYYY-MM-DD)", 200)
    ]

    for field, y_pos in fields:
        Label(base, text=field, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=y_pos)
        entries[field] = ttk.Entry(base, font=("Helvetica 15"))
        entries[field].place(x=600, y=y_pos)

    def save_fee():
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO fees (student_id, amount, due_date) VALUES (?, ?, ?)
            ''', (
                entries["Student ID"].get(),
                entries["Amount"].get(),
                entries["Due Date (YYYY-MM-DD)"].get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Fee added successfully!")
            manage_fees()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Save", command=save_fee).place(x=600, y=300)
    ttk.Button(base, text="Back", command=manage_fees).place(x=800, y=300)

# ----------------- View Fees -----------------
def view_fees():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="VIEW FEES", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fees")
    fees = cursor.fetchall()
    conn.close()

    canvas = Canvas(base, bg="#2c3e50")
    scrollbar = Scrollbar(base, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#2c3e50")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for fee in fees:
        fee_frame = Frame(scrollable_frame, bg="#34495e")
        fee_frame.pack(anchor='w', pady=5, padx=10)
        Label(fee_frame, 
              text=f"ID: {fee[0]} | Student ID: {fee[1]} | Amount: {fee[2]} | Due Date: {fee[3]} | Status: {fee[4]}",
              font=("Helvetica 15"), bg="#34495e", fg="white").pack(side='left')
        ttk.Button(fee_frame, text="Delete", 
              command=lambda f=fee[0]: delete_fee(f)).pack(side='right')

    ttk.Button(base, text="Back", command=manage_fees).place(x=50, y=750)

def delete_fee(fee_id):
    try:
        conn = sqlite3.connect('hostel_management.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fees WHERE id = ?", (fee_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Fee deleted successfully!")
        view_fees()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

# ----------------- Manage Complaints -----------------
def manage_complaints():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="MANAGE COMPLAINTS", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    # View Complaints Button
    ttk.Button(base, text="View Complaints", command=view_complaints).place(x=50, y=150)

    # Back Button
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=750, y=150)

# ----------------- View Complaints -----------------
def view_complaints():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="VIEW COMPLAINTS", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()
    conn.close()

    canvas = Canvas(base, bg="#2c3e50")
    scrollbar = Scrollbar(base, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#2c3e50")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for complaint in complaints:
        complaint_frame = Frame(scrollable_frame, bg="#34495e")
        complaint_frame.pack(anchor='w', pady=5, padx=10)
        Label(complaint_frame, 
              text=f"ID: {complaint[0]} | Student ID: {complaint[1]} | Description: {complaint[2]} | Status: {complaint[3]}",
              font=("Helvetica 15"), bg="#34495e", fg="white").pack(side='left')
        ttk.Button(complaint_frame, text="Resolve", 
              command=lambda c=complaint[0]: resolve_complaint(c)).pack(side='right')

    ttk.Button(base, text="Back", command=manage_complaints).place(x=50, y=750)

def resolve_complaint(complaint_id):
    try:
        conn = sqlite3.connect('hostel_management.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE complaints SET status = 'Resolved' WHERE id = ?", (complaint_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Complaint resolved successfully!")
        view_complaints()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

# ----------------- Manage Mess Menu -----------------
def manage_mess_menu():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="MANAGE MESS MENU", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    # Add Mess Menu Button
    ttk.Button(base, text="Add Mess Menu", command=add_mess_menu).place(x=50, y=150)

    # View Mess Menu Button
    ttk.Button(base, text="View Mess Menu", command=view_mess_menu).place(x=400, y=150)

    # Back Button
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=750, y=150)

# ----------------- Add Mess Menu -----------------
def add_mess_menu():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="ADD MESS MENU", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    entries = {}
    fields = [
        ("Day", 100), ("Breakfast", 150), ("Lunch", 200), ("Dinner", 250)
    ]

    for field, y_pos in fields:
        Label(base, text=field, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=y_pos)
        entries[field] = ttk.Entry(base, font=("Helvetica 15"))
        entries[field].place(x=600, y=y_pos)

    def save_mess_menu():
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO mess_menu (day, breakfast, lunch, dinner) VALUES (?, ?, ?, ?)
            ''', (
                entries["Day"].get(),
                entries["Breakfast"].get(),
                entries["Lunch"].get(),
                entries["Dinner"].get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Mess menu added successfully!")
            manage_mess_menu()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Save", command=save_mess_menu).place(x=600, y=300)
    ttk.Button(base, text="Back", command=manage_mess_menu).place(x=800, y=300)

# ----------------- View Mess Menu -----------------
def view_mess_menu():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="VIEW MESS MENU", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mess_menu")
    mess_menu = cursor.fetchall()
    conn.close()

    canvas = Canvas(base, bg="#2c3e50")
    scrollbar = Scrollbar(base, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#2c3e50")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for menu in mess_menu:
        menu_frame = Frame(scrollable_frame, bg="#34495e")
        menu_frame.pack(anchor='w', pady=5, padx=10)
        Label(menu_frame, 
              text=f"Day: {menu[1]} | Breakfast: {menu[2]} | Lunch: {menu[3]} | Dinner: {menu[4]}",
              font=("Helvetica 15"), bg="#34495e", fg="white").pack(side='left')
        ttk.Button(menu_frame, text="Delete", 
              command=lambda m=menu[0]: delete_mess_menu(m)).pack(side='right')

    ttk.Button(base, text="Back", command=manage_mess_menu).place(x=50, y=750)

def delete_mess_menu(menu_id):
    try:
        conn = sqlite3.connect('hostel_management.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mess_menu WHERE id = ?", (menu_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Mess menu deleted successfully!")
        view_mess_menu()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

# ----------------- Generate Reports -----------------
def generate_reports():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="GENERATE REPORTS", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    # Generate Student Report Button
    ttk.Button(base, text="Student Report", command=generate_student_report).place(x=50, y=150)

    # Generate Fee Report Button
    ttk.Button(base, text="Fee Report", command=generate_fee_report).place(x=400, y=150)

    # Generate Complaint Report Button
    ttk.Button(base, text="Complaint Report", command=generate_complaint_report).place(x=750, y=150)

    # Back Button
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=50, y=250)

# ----------------- Generate Student Report -----------------
def generate_student_report():
    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    report = "Student Report\n\n"
    for student in students:
        report += f"ID: {student[0]} | Name: {student[1]} {student[2]} | Contact: {student[6]}\n"

    messagebox.showinfo("Student Report", report)

# ----------------- Generate Fee Report -----------------
def generate_fee_report():
    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fees")
    fees = cursor.fetchall()
    conn.close()

    report = "Fee Report\n\n"
    for fee in fees:
        report += f"ID: {fee[0]} | Student ID: {fee[1]} | Amount: {fee[2]} | Due Date: {fee[3]} | Status: {fee[4]}\n"

    messagebox.showinfo("Fee Report", report)

# ----------------- Generate Complaint Report -----------------
def generate_complaint_report():
    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()
    conn.close()

    report = "Complaint Report\n\n"
    for complaint in complaints:
        report += f"ID: {complaint[0]} | Student ID: {complaint[1]} | Description: {complaint[2]} | Status: {complaint[3]}\n"

    messagebox.showinfo("Complaint Report", report)

# ----------------- Leave Application -----------------
def leave_application():
    base.geometry('1800x1100+0+0')

    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="LEAVE APPLICATION", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    entries = {}
    fields = [
        ("Student ID", 100), ("Start Date (YYYY-MM-DD)", 150), ("End Date (YYYY-MM-DD)", 200), ("Reason", 250)
    ]

    for field, y_pos in fields:
        Label(base, text=field, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=y_pos)
        entries[field] = ttk.Entry(base, font=("Helvetica 15"))
        entries[field].place(x=600, y=y_pos)

    def submit_leave():
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO leave_applications (student_id, start_date, end_date, reason) VALUES (?, ?, ?, ?)
            ''', (
                entries["Student ID"].get(),
                entries["Start Date (YYYY-MM-DD)"].get(),
                entries["End Date (YYYY-MM-DD)"].get(),
                entries["Reason"].get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Leave application submitted successfully!")
            dashboard_screen()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Submit", command=submit_leave).place(x=600, y=300)
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=800, y=300)

# ----------------- Student Personal Detail -----------------
def student_personal_detail():
    base.geometry('1800x1100+0+0')

    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="STUDENT PERSONAL DETAIL", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    Label(base, text="Enter Student ID:", font=("Helvetica 20"), bg="#2c3e50", fg="white").place(x=400, y=150)
    student_id_entry = ttk.Entry(base, font=("Helvetica 20"))
    student_id_entry.place(x=600, y=150)

    def fetch_student_details():
        student_id = student_id_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID")
            return

        conn = sqlite3.connect('hostel_management.db')
        cursor = conn.cursor()

        # Fetch student details
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()

        if not student:
            messagebox.showerror("Error", "Student not found!")
            conn.close()
            return

        # Fetch guardian details
        cursor.execute("SELECT * FROM guardians WHERE student_id = ?", (student_id,))
        guardian = cursor.fetchone()

        # Fetch timing logs
        cursor.execute("SELECT * FROM timing WHERE student_id = ?", (student_id,))
        timing_logs = cursor.fetchall()

        conn.close()

        # Display student details
        details_frame = Frame(base, bg="white", bd=2, relief="solid")
        details_frame.place(x=400, y=200, width=800, height=500)

        Label(details_frame, text="Student Details", font=("Helvetica 20 bold"), bg="white").place(x=10, y=10)
        Label(details_frame, text=f"ID: {student[0]}", font=("Helvetica 15"), bg="white").place(x=10, y=50)
        Label(details_frame, text=f"Name: {student[1]} {student[2]}", font=("Helvetica 15"), bg="white").place(x=10, y=80)
        Label(details_frame, text=f"Father Name: {student[3]}", font=("Helvetica 15"), bg="white").place(x=10, y=110)
        Label(details_frame, text=f"Mother Name: {student[4]}", font=("Helvetica 15"), bg="white").place(x=10, y=140)
        Label(details_frame, text=f"DOB: {student[5]}", font=("Helvetica 15"), bg="white").place(x=10, y=170)
        Label(details_frame, text=f"Contact: {student[6]}", font=("Helvetica 15"), bg="white").place(x=10, y=200)
        Label(details_frame, text=f"Email: {student[7]}", font=("Helvetica 15"), bg="white").place(x=10, y=230)
        Label(details_frame, text=f"Address: {student[8]}", font=("Helvetica 15"), bg="white").place(x=10, y=260)
        Label(details_frame, text=f"Vehicle No: {student[9]}", font=("Helvetica 15"), bg="white").place(x=10, y=290)
        Label(details_frame, text=f"Workplace: {student[10]}", font=("Helvetica 15"), bg="white").place(x=10, y=320)
        Label(details_frame, text=f"Gender: {student[11]}", font=("Helvetica 15"), bg="white").place(x=10, y=350)
        Label(details_frame, text=f"Room No: {student[12]}", font=("Helvetica 15"), bg="white").place(x=10, y=380)
        Label(details_frame, text=f"Bed No: {student[13]}", font=("Helvetica 15"), bg="white").place(x=10, y=410)

        # Display guardian details
        if guardian:
            Label(details_frame, text="Guardian Details", font=("Helvetica 20 bold"), bg="white").place(x=10, y=450)
            Label(details_frame, text=f"Name: {guardian[2]}", font=("Helvetica 15"), bg="white").place(x=10, y=490)
            Label(details_frame, text=f"Contact: {guardian[3]}", font=("Helvetica 15"), bg="white").place(x=10, y=520)
            Label(details_frame, text=f"Relation: {guardian[4]}", font=("Helvetica 15"), bg="white").place(x=10, y=550)

        # Display timing logs
        if timing_logs:
            Label(details_frame, text="Timing Logs", font=("Helvetica 20 bold"), bg="white").place(x=10, y=580)
            y_pos = 620
            for log in timing_logs:
                Label(details_frame, text=f"In Time: {log[2]} | Out Time: {log[3]}", font=("Helvetica 15"), bg="white").place(x=10, y=y_pos)
                y_pos += 30

    ttk.Button(base, text="Fetch Details", command=fetch_student_details).place(x=600, y=200)
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=800, y=200)

# ----------------- Add Student -----------------
def add_student():
    global student_image_path
    base.geometry('1800x1100+0+0')

    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="ADD STUDENT", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    entries = {}
    fields = [
        ("First Name", 100), ("Last Name", 150), ("Father Name", 200), 
        ("Mother Name", 250), ("DOB (YYYY-MM-DD)", 300), ("Contact", 350),
        ("Email", 400), ("Address", 450), ("Vehicle No", 500), 
        ("Workplace", 550), ("Gender (M/F/O)", 600), ("Room No", 650), ("Bed No", 700)
    ]

    for field, y_pos in fields:
        Label(base, text=field, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=y_pos)
        entries[field] = ttk.Entry(base, font=("Helvetica 15"))
        entries[field].place(x=600, y=y_pos)

    # Image Upload
    def upload_image():
        global student_image_path
        student_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if student_image_path:
            Label(base, text="Image Uploaded", font=("Helvetica 12"), bg="#2c3e50", fg="white").place(x=600, y=750)

    ttk.Button(base, text="Upload Image", command=upload_image).place(x=1000, y=600)

    def save_student():
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students VALUES (
                    NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', (
                entries["First Name"].get(),
                entries["Last Name"].get(),
                entries["Father Name"].get(),
                entries["Mother Name"].get(),
                entries["DOB (YYYY-MM-DD)"].get(),
                entries["Contact"].get(),
                entries["Email"].get(),
                entries["Address"].get(),
                entries["Vehicle No"].get(),
                entries["Workplace"].get(),
                entries["Gender (M/F/O)"].get().upper(),
                entries["Room No"].get(),
                entries["Bed No"].get(),
                student_image_path
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")
            dashboard_screen()  # Return to dashboard after saving
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Save", command=save_student).place(x=1000, y=500)
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=1200, y=500)

# ----------------- Add Employee -----------------
def add_employee():
    base.geometry('1800x1100+0+0')

    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="ADD EMPLOYEE", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    entries = {}
    fields = [
        ("First Name", 100), ("Last Name", 150), ("Contact", 200),
        ("Email", 250), ("Address", 300), ("Role", 350), ("Salary", 400)
    ]

    for field, y_pos in fields:
        Label(base, text=field, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=y_pos)
        entries[field] = ttk.Entry(base, font=("Helvetica 15"))
        entries[field].place(x=600, y=y_pos)

    def save_employee():
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees VALUES (
                    NULL, ?, ?, ?, ?, ?, ?, ?
                )
            ''', (
                entries["First Name"].get(),
                entries["Last Name"].get(),
                entries["Contact"].get(),
                entries["Email"].get(),
                entries["Address"].get(),
                entries["Role"].get(),
                entries["Salary"].get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Employee added successfully!")
            dashboard_screen()  # Return to dashboard after saving
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Save", command=save_employee).place(x=600, y=450)
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=800, y=450)

# ----------------- Add Visitor -----------------
def add_visitor():
    base.geometry('1800x1100+0+0')

    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="ADD VISITOR", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    entries = {}
    fields = [
        ("Name", 100), ("Contact", 150), ("Purpose", 200), ("Student ID", 250)
    ]

    for field, y_pos in fields:
        Label(base, text=field, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=y_pos)
        entries[field] = ttk.Entry(base, font=("Helvetica 15"))
        entries[field].place(x=600, y=y_pos)

    def save_visitor():
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO visitors VALUES (
                    NULL, ?, ?, ?, ?
                )
            ''', (
                entries["Name"].get(),
                entries["Contact"].get(),
                entries["Purpose"].get(),
                entries["Student ID"].get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Visitor added successfully!")
            dashboard_screen()  # Return to dashboard after saving
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Save", command=save_visitor).place(x=600, y=300)
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=800, y=300)

# ----------------- Add Guardian -----------------
def add_guardian():
    base.geometry('1800x1100+0+0')

    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="ADD GUARDIAN", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    entries = {}
    fields = [
        ("Student ID", 100), ("Name", 150), ("Contact", 200), ("Relation", 250)
    ]

    for field, y_pos in fields:
        Label(base, text=field, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=y_pos)
        entries[field] = ttk.Entry(base, font=("Helvetica 15"))
        entries[field].place(x=600, y=y_pos)

    def save_guardian():
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO guardians VALUES (
                    NULL, ?, ?, ?, ?
                )
            ''', (
                entries["Student ID"].get(),
                entries["Name"].get(),
                entries["Contact"].get(),
                entries["Relation"].get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Guardian added successfully!")
            dashboard_screen()  # Return to dashboard after saving
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Save", command=save_guardian).place(x=600, y=300)
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=800, y=300)

# ----------------- Student Timing -----------------
def student_timing():
    base.geometry('1800x1100+0+0')

    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="STUDENT TIMING", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    Label(base, text="Student ID:", font=("Helvetica 20"), bg="#2c3e50", fg="white").place(x=400, y=150)
    student_id_entry = ttk.Entry(base, font=("Helvetica 20"))
    student_id_entry.place(x=600, y=150)

    def mark_in_time():
        student_id = student_id_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID")
            return
        in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO timing (student_id, in_time) VALUES (?, ?)
            ''', (student_id, in_time))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"In time marked for Student ID: {student_id} at {in_time}")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def mark_out_time():
        student_id = student_id_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID")
            return
        out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE timing SET out_time = ? WHERE student_id = ? AND out_time IS NULL
            ''', (out_time, student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Out time marked for Student ID: {student_id} at {out_time}")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Mark In Time", command=mark_in_time).place(x=400, y=250)
    ttk.Button(base, text="Mark Out Time", command=mark_out_time).place(x=600, y=250)
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=800, y=250)

# ----------------- Information Screen -----------------
def show_information():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="HOSTEL INFORMATION", font=("Helvetica 30 bold"), bg="#2c3e50", fg="white").pack(pady=20)

    canvas = Canvas(base, bg="#2c3e50")
    scrollbar = Scrollbar(base, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#2c3e50")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def fetch_data():
        conn = sqlite3.connect('hostel_management.db')
        cursor = conn.cursor()
        
        # Students
        cursor.execute("SELECT * FROM students")
        Label(scrollable_frame, text="\nSTUDENTS", font=("Helvetica 25 bold"), bg="#2c3e50", fg="white").pack()
        for student in cursor.fetchall():
            student_frame = Frame(scrollable_frame, bg="#34495e")
            student_frame.pack(anchor='w', pady=5, padx=10)
            Label(student_frame, 
                  text=f"ID: {student[0]} | Name: {student[1]} {student[2]} | Contact: {student[6]}",
                  font=("Helvetica 15"), bg="#34495e", fg="white").pack(side='left')
            ttk.Button(student_frame, text="Delete", 
                  command=lambda s=student[0]: delete_student(s)).pack(side='right')
        
        # Employees
        cursor.execute("SELECT * FROM employees")
        Label(scrollable_frame, text="\nEMPLOYEES", font=("Helvetica 25 bold"), bg="#2c3e50", fg="white").pack()
        for employee in cursor.fetchall():
            Label(scrollable_frame, 
                  text=f"ID: {employee[0]} | Name: {employee[1]} {employee[2]} | Role: {employee[5]}",
                  font=("Helvetica 15"), bg="#34495e", fg="white").pack(anchor='w', pady=5, padx=10)
        
        # Visitors
        cursor.execute("SELECT * FROM visitors")
        Label(scrollable_frame, text="\nVISITORS", font=("Helvetica 25 bold"), bg="#2c3e50", fg="white").pack()
        for visitor in cursor.fetchall():
            Label(scrollable_frame, 
                  text=f"ID: {visitor[0]} | Name: {visitor[1]} | Purpose: {visitor[3]}",
                  font=("Helvetica 15"), bg="#34495e", fg="white").pack(anchor='w', pady=5, padx=10)
        
        # Guardians
        cursor.execute("SELECT * FROM guardians")
        Label(scrollable_frame, text="\nGUARDIANS", font=("Helvetica 25 bold"), bg="#2c3e50", fg="white").pack()
        for guardian in cursor.fetchall():
            Label(scrollable_frame, 
                  text=f"ID: {guardian[0]} | Name: {guardian[2]} | Relation: {guardian[4]}",
                  font=("Helvetica 15"), bg="#34495e", fg="white").pack(anchor='w', pady=5, padx=10)
        
        # Timing
        cursor.execute("SELECT * FROM timing")
        Label(scrollable_frame, text="\nTIMING", font=("Helvetica 25 bold"), bg="#2c3e50", fg="white").pack()
        for timing in cursor.fetchall():
            Label(scrollable_frame, 
                  text=f"Student ID: {timing[1]} | In Time: {timing[2]} | Out Time: {timing[3]}",
                  font=("Helvetica 15"), bg="#34495e", fg="white").pack(anchor='w', pady=5, padx=10)
        
        # Leave Applications
        cursor.execute("SELECT * FROM leave_applications")
        Label(scrollable_frame, text="\nLEAVE APPLICATIONS", font=("Helvetica 25 bold"), bg="#2c3e50", fg="white").pack()
        for leave in cursor.fetchall():
            leave_frame = Frame(scrollable_frame, bg="#34495e")
            leave_frame.pack(anchor='w', pady=5, padx=10)
            Label(leave_frame, 
                  text=f"ID: {leave[0]} | Student ID: {leave[1]} | Status: {leave[5]}",
                  font=("Helvetica 15"), bg="#34495e", fg="white").pack(side='left')
            if leave[5] == 'Pending':
                ttk.Button(leave_frame, text="Approve", 
                      command=lambda l=leave[0]: approve_leave(l)).pack(side='right')
                ttk.Button(leave_frame, text="Reject", 
                      command=lambda l=leave[0]: reject_leave(l)).pack(side='right')
        
        conn.close()

    def delete_student(student_id):
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()

            # Delete related records from other tables
            cursor.execute("DELETE FROM guardians WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM visitors WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM timing WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM leave_applications WHERE student_id = ?", (student_id,))

            # Delete the student from the students table
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student and all related records deleted successfully!")
            show_information()  # Refresh the information screen
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def approve_leave(leave_id):
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE leave_applications SET status = 'Approved' WHERE id = ?", (leave_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Leave application approved!")
            show_information()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def reject_leave(leave_id):
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE leave_applications SET status = 'Rejected' WHERE id = ?", (leave_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Leave application rejected!")
            show_information()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    fetch_data()
    ttk.Button(base, text="Back", command=dashboard_screen).place(x=50, y=750)

login_screen()
base.mainloop()