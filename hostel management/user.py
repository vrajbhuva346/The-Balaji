import sqlite3
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
from PIL import Image, ImageTk
import os

# Database Setup
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

    conn.commit()
    conn.close()

create_database()

# Frontend Setup
base = Tk()
base.title("HOSTEL MANAGEMENT SYSTEM - STUDENT PORTAL")
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

# ----------------- Student Registration Form -----------------
def registration_form():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="STUDENT REGISTRATION", font=("Helvetica 30 bold"), bg="#34495e", fg="white", padx=490, pady=20).pack()

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
            messagebox.showinfo("Success", "Student registered successfully!")
            user_login_screen()  # Redirect to login screen after registration
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Register", command=save_student).place(x=1000, y=500)
    ttk.Button(base, text="Back to Login", command=user_login_screen).place(x=1200, y=500)

# ----------------- User Login Screen -----------------
def user_login_screen():
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="STUDENT LOGIN", font=("Helvetica 30 bold"), bg="#34495e", fg="white", padx=490, pady=20).pack()

    Label(base, text="Student ID", font=("Helvetica 20"), bg="#2c3e50", fg="white").place(x=400, y=200)
    global user_student_id_entry
    user_student_id_entry = ttk.Entry(base, font=("Helvetica 20"))
    user_student_id_entry.place(x=600, y=200)

    Label(base, text="Contact Number", font=("Helvetica 20"), bg="#2c3e50", fg="white").place(x=400, y=300)
    global user_contact_entry
    user_contact_entry = ttk.Entry(base, font=("Helvetica 20"))
    user_contact_entry.place(x=600, y=300)

    ttk.Button(base, text="Login", command=user_login).place(x=650, y=400)
    ttk.Button(base, text="New Student? Register Here", command=registration_form).place(x=550, y=500)

def user_login():
    student_id = user_student_id_entry.get()
    contact = user_contact_entry.get()

    if not student_id or not contact:
        messagebox.showerror("Error", "Please enter Student ID and Contact Number")
        return

    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ? AND contact = ?", (student_id, contact))
    student = cursor.fetchone()
    conn.close()

    if student:
        user_dashboard(student_id)
    else:
        messagebox.showerror("Error", "Invalid Student ID or Contact Number")

# ----------------- User Dashboard -----------------
def user_dashboard(student_id):
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="STUDENT DASHBOARD", font=("Helvetica 30 bold"), bg="#34495e", fg="white", padx=490, pady=20).pack()

    # Fetch student details
    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    # Display student details
    details_frame = Frame(base, bg="#34495e", bd=2, relief="solid")
    details_frame.place(x=400, y=100, width=800, height=210)

    Label(details_frame, text="Student Details", font=("Helvetica 20 bold"), bg="#34495e", fg="white").place(x=10, y=10)
    Label(details_frame, text=f"ID: {student[0]}", font=("Helvetica 15"), bg="#34495e", fg="white").place(x=10, y=50)
    Label(details_frame, text=f"Name: {student[1]} {student[2]}", font=("Helvetica 15"), bg="#34495e", fg="white").place(x=10, y=80)
    Label(details_frame, text=f"Contact: {student[6]}", font=("Helvetica 15"), bg="#34495e", fg="white").place(x=10, y=110)
    Label(details_frame, text=f"Room No: {student[12]}", font=("Helvetica 15"), bg="#34495e", fg="white").place(x=10, y=140)
    Label(details_frame, text=f"Bed No: {student[13]}", font=("Helvetica 15"), bg="#34495e", fg="white").place(x=10, y=170)

    # Fetch leave applications
    cursor.execute("SELECT * FROM leave_applications WHERE student_id = ?", (student_id,))
    leave_applications = cursor.fetchall()

    # Display leave applications
    leave_frame = Frame(base, bg="#34495e", bd=2, relief="solid")
    leave_frame.place(x=400, y=330, width=800, height=170)

    Label(leave_frame, text="Leave Applications", font=("Helvetica 20 bold"), bg="#34495e", fg="white").place(x=10, y=10)
    y_pos = 50
    for leave in leave_applications:
        Label(leave_frame, text=f"Start Date: {leave[2]} | End Date: {leave[3]} | Status: {leave[5]}", font=("Helvetica 15"), bg="#34495e", fg="white").place(x=10, y=y_pos)
        y_pos += 30

    # Fetch in/out timings
    cursor.execute("SELECT * FROM timing WHERE student_id = ?", (student_id,))
    timings = cursor.fetchall()

    # Display in/out timings
    timing_frame = Frame(base, bg="#34495e", bd=2, relief="solid")
    timing_frame.place(x=400, y=520, width=800, height=150)

    Label(timing_frame, text="In/Out Timings", font=("Helvetica 20 bold"), bg="#34495e", fg="white").place(x=10, y=10)
    y_pos = 50
    for timing in timings:
        Label(timing_frame, text=f"In Time: {timing[2]} | Out Time: {timing[3]}", font=("Helvetica 15"), bg="#34495e", fg="white").place(x=10, y=y_pos)
        y_pos += 30

    # Fetch notifications
    cursor.execute("SELECT * FROM notifications WHERE student_id = ?", (student_id,))
    notifications = cursor.fetchall()

    # Display notifications
    notification_frame = Frame(base, bg="#34495e", bd=2, relief="solid")
    notification_frame.place(x=400, y=690, width=800, height=130)

    Label(notification_frame, text="Notifications", font=("Helvetica 20 bold"), bg="#34495e", fg="white").place(x=10, y=10)
    y_pos = 50
    for notification in notifications:
        Label(notification_frame, text=f"Message: {notification[2]}", font=("Helvetica 15"), bg="#34495e", fg="white").place(x=10, y=y_pos)
        y_pos += 30

    conn.close()

    # Profile Management Button
    ttk.Button(base, text="Profile Management", command=lambda: profile_management(student_id)).place(x=60, y=200)

    # Attendance History Button
    ttk.Button(base, text="Attendance History", command=lambda: attendance_history(student_id)).place(x=60, y=300)

    # Hostel Rules and Guidelines Button
    ttk.Button(base, text="Hostel Rules", command=lambda: hostel_rules(student_id)).place(x=60, y=400)

    # Feedback and Suggestions Button
    ttk.Button(base, text="Feedback", command=lambda: feedback_and_suggestions(student_id)).place(x=60, y=500)

    # Emergency Contacts Button
    ttk.Button(base, text="Emergency Contacts", command=lambda: emergency_contacts(student_id)).place(x=60, y=600)

    # Logout Button
    ttk.Button(base, text="Logout", command=user_login_screen).place(x=50, y=750)

# ----------------- Profile Management -----------------
def profile_management(student_id):
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="PROFILE MANAGEMENT", font=("Helvetica 30 bold"), bg="#34495e", fg="white", padx=490, pady=20).pack()

    # Fetch student details
    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()

    entries = {}
    fields = [
        ("Contact", 100), ("Email", 150), ("Profile Picture", 200)
    ]

    for field, y_pos in fields:
        Label(base, text=field, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=y_pos)
        entries[field] = ttk.Entry(base, font=("Helvetica 15"))
        entries[field].place(x=600, y=y_pos)

    # Pre-fill the contact and email fields
    entries["Contact"].insert(0, student[6])
    entries["Email"].insert(0, student[7])

    # Image Upload
    def upload_image():
        global student_image_path
        student_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if student_image_path:
            Label(base, text="Image Uploaded", font=("Helvetica 12"), bg="#2c3e50", fg="white").place(x=600, y=250)

    ttk.Button(base, text="Upload Image", command=upload_image).place(x=400, y=250)

    def save_profile():
        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students SET contact = ?, email = ?, image_path = ? WHERE id = ?
            ''', (
                entries["Contact"].get(),
                entries["Email"].get(),
                student_image_path,
                student_id
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Profile updated successfully!")
            user_dashboard(student_id)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Save", command=save_profile).place(x=600, y=300)
    ttk.Button(base, text="Back", command=lambda: user_dashboard(student_id)).place(x=800, y=300)

# ----------------- Attendance History -----------------
def attendance_history(student_id):
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="ATTENDANCE HISTORY", font=("Helvetica 30 bold"), bg="#34495e", fg="white", padx=490, pady=20).pack()

    conn = sqlite3.connect('hostel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timing WHERE student_id = ?", (student_id,))
    timings = cursor.fetchall()
    conn.close()

    canvas = Canvas(base, bg="#2c3e50")
    scrollbar = Scrollbar(base, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#2c3e50")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for timing in timings:
        timing_frame = Frame(scrollable_frame, bg="#34495e")
        timing_frame.pack(anchor='w')
        Label(timing_frame, 
              text=f"In Time: {timing[2]} | Out Time: {timing[3]}",
              font=("Helvetica 15"), bg="#34495e", fg="white").pack(side='left')

    ttk.Button(base, text="Back", command=lambda: user_dashboard(student_id)).place(x=50, y=750)

# ----------------- Hostel Rules and Guidelines -----------------
def hostel_rules(student_id):
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="HOSTEL RULES AND GUIDELINES", font=("Helvetica 30 bold"), bg="#34495e", fg="white", padx=490, pady=20).pack()

    rules = """
    1. No loud music after 10 PM.
    2. Keep your room clean and tidy.
    3. No smoking or alcohol in the hostel premises.
    4. Visitors are allowed only during visiting hours.
    5. Follow the mess timings strictly.
    """

    Label(base, text=rules, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=150)

    # Back Button
    ttk.Button(base, text="Back", command=lambda: user_dashboard(student_id)).place(x=50, y=750)

# ----------------- Feedback and Suggestions -----------------
def feedback_and_suggestions(student_id):
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="FEEDBACK AND SUGGESTIONS", font=("Helvetica 30 bold"), bg="#34495e", fg="white", padx=490, pady=20).pack()

    Label(base, text="Message", font=("Helvetica 20"), bg="#2c3e50", fg="white").place(x=400, y=150)
    global feedback_message_entry
    feedback_message_entry = ttk.Entry(base, font=("Helvetica 20"))
    feedback_message_entry.place(x=600, y=150)

    def submit_feedback():
        message = feedback_message_entry.get()

        if not message:
            messagebox.showerror("Error", "Please enter your feedback or suggestion")
            return

        try:
            conn = sqlite3.connect('hostel_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO feedback (student_id, message) VALUES (?, ?)
            ''', (student_id, message))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Feedback submitted successfully!")
            user_dashboard(student_id)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    ttk.Button(base, text="Submit", command=submit_feedback).place(x=600, y=200)
    ttk.Button(base, text="Back", command=lambda: user_dashboard(student_id)).place(x=800, y=200)

# ----------------- Emergency Contacts -----------------
def emergency_contacts(student_id):
    for widget in base.winfo_children():
        widget.destroy()

    Label(base, text="EMERGENCY CONTACTS", font=("Helvetica 30 bold"), bg="#34495e", fg="white", padx=490, pady=20).pack()

    contacts = """
    Warden: +91 
    Security: +91 
    Ambulance: 108
    Police: 100
    """

    Label(base, text=contacts, font=("Helvetica 15"), bg="#2c3e50", fg="white").place(x=400, y=150)

    # Back Button
    ttk.Button(base, text="Back", command=lambda: user_dashboard(student_id)).place(x=50, y=750)

# Start with the user login screen
user_login_screen()

base.mainloop()