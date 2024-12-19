import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime
import datetime
import re 
from PIL import Image, ImageTk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

class DrivingSchoolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pass IT Driving School Management System")
        self.root.geometry("1200x700")

          # Show loading screen first
        self.loading = show_loading_screen(root)
        self.root.after(1600, self.initialize_app)

        self.pay_rate_map = {
            'Introductory': 30,  # £30 per hour
            'Standard': 45,      # £45 per hour
            'Pass Plus': 60,     # £60 per hour
            'Driving Test': 75   # £75 per hour
        }


    def initialize_app(self):
        # Database Setup
        self.create_database()

        # Create Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create Tabs
        self.create_student_tab()
        self.create_instructor_tab()
        self.create_lesson_tab()

      
    def create_database(self):
        # Create SQLite database and tables
        self.conn = sqlite3.connect('driving_school.db')
        self.cursor = self.conn.cursor()

        # Students Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone TEXT
            )
        ''')

        # Instructors Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone TEXT,
                license TEXT
            )
        ''')

 
        # Lessons Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER, 
                instructor_id INTEGER,  
                lesson_type TEXT,
                lesson_date TEXT,
                duration INTEGER,
                status TEXT,
                fee REAL,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (instructor_id) REFERENCES instructors (id)
            )
        ''')
        self.conn.commit()


# student section---------

    def create_student_tab(self):
            # Student Management Tab
            student_tab = ttk.Frame(self.notebook, style='Student.TFrame')
            self.notebook.add(student_tab, text="Students")

            # Initialize entry widgets
            self.student_first_name = tk.Entry(None)
            self.student_last_name = tk.Entry(None)
            self.student_email = tk.Entry(None)
            self.student_phone = tk.Entry(None)
            self.student_search_entry = tk.Entry(None)

            # Colors
            colors = {
                'background': '#f4f6f9',
                'primary': '#3498db',
                'secondary': '#2ecc71',
                'accent': '#e74c3c',
                'text_dark': '#2c3e50',
                'text_light': '#34495e',
                'input_bg': '#ffffff',
                'border': '#bdc3c7'
            }
            
            # Configure styles
            style = ttk.Style()
            style.configure('Student.TFrame', background=colors['background'])
            style.configure('TLabel', 
                background=colors['background'], 
                foreground=colors['text_dark'], 
                font=('Segoe UI', 10))
            style.configure('Custom.TButton', 
                font=('Segoe UI', 10, 'bold'),
                padding=10)
            
            # Button styles
            style.map('Search.TButton',
                background=[('active', colors['primary']), ('pressed', '#2980b9')],
                foreground=[('active', 'black'), ('pressed', 'black')]
            )
            style.map('Reset.TButton',
                background=[('active', colors['accent']), ('pressed', '#c0392b')],
                foreground=[('active', 'black'), ('pressed', 'black')]
            )
            style.map('Add.TButton',
                background=[('active', colors['secondary']), ('pressed', '#27ae60')],
                foreground=[('active', 'black'), ('pressed', 'black')]
            )

            # Main Frame
            main_frame = tk.Frame(student_tab, bg=colors['background'], bd=0)
            main_frame.pack(expand=True, fill="both", padx=20, pady=20)

            # Title
            title_label = tk.Label(
                main_frame, 
                text="Student Management", 
                font=('Segoe UI', 18, 'bold'), 
                bg=colors['background'], 
                fg=colors['text_dark']
            )
            title_label.pack(pady=(0, 20), anchor='center')

            # Search Section
            search_frame = tk.Frame(main_frame, bg=colors['background'])
            search_frame.pack(pady=10, fill='x')

            search_label = ttk.Label(search_frame, text="Search:", style='TLabel')
            search_label.pack(side="left", padx=(0, 10))

            self.student_search_entry = tk.Entry(
                search_frame, 
                font=('Segoe UI', 12), 
                width=30, 
                bg=colors['input_bg'], 
                fg=colors['text_light'],
                relief='solid',
                borderwidth=1
            )
            self.student_search_entry.pack(side="left", padx=10, fill='x', expand=True)
            self.student_search_entry.bind("<Return>", lambda event: self.search_students())

            search_btn = ttk.Button(
                search_frame, 
                text="Search", 
                command=self.search_students, 
                style='Search.TButton'
            )
            search_btn.pack(side="left", padx=5)

            reset_btn = ttk.Button(
                search_frame, 
                text="Reset", 
                command=self.view_students, 
                style='Reset.TButton'
            )
            reset_btn.pack(side="left", padx=5)

            # Input Section
            input_frame = tk.Frame(
                main_frame, 
                bg='white', 
                bd=1, 
                relief='solid', 
                highlightbackground=colors['border'], 
                highlightthickness=1
            )
            input_frame.pack(pady=(10,5), ipadx=10, ipady=10, fill='x')

            # Updated input fields
            input_fields = [
                ("First Name:", "first_name"),
                ("Last Name:", "last_name"),
                ("Email:", "email"),
                ("Phone:", "phone")
            ]

            for i, (label_text, field_name) in enumerate(input_fields):
                label = ttk.Label(input_frame, text=label_text, style='TLabel')
                label.grid(row=i, column=0, padx=(5,10), pady=3, sticky="e")
                
                entry = tk.Entry(       
                    input_frame, 
                    font=('Segoe UI', 12), 
                    width=25, 
                    bg=colors['input_bg'], 
                    fg=colors['text_light'],
                    relief='solid',
                    borderwidth=1
                )
                entry.grid(row=i, column=1, padx=(0,5), pady=3, sticky="w")
                
                # Assign to specific variables
                if i == 0:
                    self.student_first_name = entry
                elif i == 1:
                    self.student_last_name = entry
                elif i == 2:
                    self.student_email = entry
                else:
                    self.student_phone = entry

            # Add button
            add_btn = ttk.Button(
                input_frame, 
                text="Add Student", 
                command=self.add_student, 
                style='Add.TButton'
            )
            add_btn.grid(row=len(input_fields), column=1, pady=(3,5), padx=(0,5), sticky='w')

            input_frame.grid_columnconfigure(1, weight=1)
            
            # Delete frame
            delete_frame = tk.Frame(main_frame, bg=colors['background'])
            delete_frame.pack(pady=0, fill='x', anchor='e')
        
            delete_btn = ttk.Button(
                delete_frame, 
                text="Delete Student", 
                command=self.delete_student,
                style='Reset.TButton'
            )
            delete_btn.pack(side='right', padx=10, pady=2)

            self.student_count_label = tk.Label(
                delete_frame,
                text="Total Students: 0",
                font=('Segoe UI', 10, 'bold'),
                bg=colors['background'],
                fg=colors['text_dark']
            )
            self.student_count_label.pack(side='right', padx=10, pady=2)

            # TreeView Section
            tree_frame = tk.Frame(main_frame, bg='white', bd=1, relief='solid')
            tree_frame.pack(pady=10, fill="both", expand=True)

            vertical_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
            vertical_scrollbar.pack(side="right", fill="y")

            horizontal_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
            horizontal_scrollbar.pack(side="bottom", fill="x")

            # Updated TreeView columns
            self.student_tree = ttk.Treeview(
                tree_frame,
                columns=("ID", "First Name", "Last Name", "Email", "Phone"),
                show="headings",
                yscrollcommand=vertical_scrollbar.set,
                xscrollcommand=horizontal_scrollbar.set
            )
            self.student_tree.pack(fill="both", expand=True)

            # Configure columns with updated widths
            column_widths = {
                "ID": 50, 
                "First Name": 150, 
                "Last Name": 150, 
                "Email": 200, 
                "Phone": 150
            }
            for col, width in column_widths.items():
                self.student_tree.heading(col, text=col)
                self.student_tree.column(col, width=width, anchor="center")

            vertical_scrollbar.config(command=self.student_tree.yview)
            horizontal_scrollbar.config(command=self.student_tree.xview)

            # Populate initial data
            self.view_students()

 
    def search_students(self):
        search_term = self.student_search_entry.get().strip().lower()
        
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        try:
            conn = sqlite3.connect('driving_school.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM students 
                WHERE LOWER(first_name) LIKE ? OR 
                    LOWER(last_name) LIKE ? OR 
                    LOWER(email) LIKE ? OR
                    LOWER(phone) LIKE ?
            """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            students = cursor.fetchall()
            for student in students:
                self.student_tree.insert("", "end", values=student)
                
            self.student_count_label.config(text=f"Total Students: {len(students)}")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def add_student(self):
        first_name = self.student_first_name.get().strip()
        last_name = self.student_last_name.get().strip()
        email = self.student_email.get().strip()
        phone = self.student_phone.get().strip()
        
        # Check if all fields are filled
        if not all([first_name, last_name, email, phone]):
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return
        
        # Validate phone number
        if not phone.isdigit():
            messagebox.showwarning("Invalid Input", "Phone number must contain only digits")
            return
            
        if len(phone) != 11:
            messagebox.showwarning("Invalid Input", "Phone number must be exactly 11 digits")
            return
        
        try:
            conn = sqlite3.connect('driving_school.db')
            cursor = conn.cursor()
            
            # Check for duplicate email
            cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
            if cursor.fetchone():
                messagebox.showwarning("Duplicate Entry", "A student with this email already exists")
                return
            
            # Check for duplicate phone
            cursor.execute("SELECT * FROM students WHERE phone = ?", (phone,))
            if cursor.fetchone():
                messagebox.showwarning("Duplicate Entry", "A student with this phone number already exists")
                return
            
            cursor.execute("""
                INSERT INTO students (first_name, last_name, email, phone)
                VALUES (?, ?, ?, ?)
            """, (first_name, last_name, email, phone))
            
            conn.commit()
            
            # Clear entries
            self.student_first_name.delete(0, tk.END)
            self.student_last_name.delete(0, tk.END)
            self.student_email.delete(0, tk.END)
            self.student_phone.delete(0, tk.END)
            
            self.view_students()
            messagebox.showinfo("Success", "Student added successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

    # Add this method to validate phone number input in real-time
    def validate_phone_input(self, P):
        # P is the proposed value for the entry
        # Return True to allow the change, False to reject it
        
        # Allow empty value (for backspace/delete)
        if P == "":
            return True
            
        # Check if input is digit and not longer than 11
        if P.isdigit() and len(P) <= 11:
            return True
            
        return False

    def initialize_student_database(self):
        try:
            conn = sqlite3.connect('driving_school.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT NOT NULL
                )
            """)
            
            conn.commit()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()


    def view_students(self):
        # Clear the tree
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        try:
            # Connect to database
            conn = sqlite3.connect('driving_school.db')
            cursor = conn.cursor()
            
            # Fetch all students
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            
            # Display in tree
            for student in students:
                self.student_tree.insert("", "end", values=student)
                
            # Update count
            self.student_count_label.config(text=f"Total Students: {len(students)}")
            
            # Clear search entry
            self.student_search_entry.delete(0, tk.END)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

  
    def delete_student(self):
        # Get selected item
        selected_item = self.student_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a student to delete")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            return
        
        try:
            # Connect to database
            conn = sqlite3.connect('driving_school.db')
            cursor = conn.cursor()
            
            # Get student ID from selected item
            student_values = self.student_tree.item(selected_item)['values']
            student_id = student_values[0]  # Assuming ID is the first column
            
            # Delete student
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            
            # Refresh view
            self.view_students()
            
            messagebox.showinfo("Success", "Student deleted successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()


    def populate_student_dropdown(self):
        # Populate student dropdown
        self.cursor.execute('SELECT id, CONCAT(first_name, " ", last_name) as full_name FROM students')
        students = self.cursor.fetchall()
        self.student_select['values'] = [f"{s[1]}" for s in students]  # Display only full names for selection


# Instructor section--------

    def create_instructor_tab(self):
        # Instructor Management Tab
        instructor_tab = ttk.Frame(self.notebook, style='Instructor.TFrame')
        self.notebook.add(instructor_tab, text="Instructors")

        # Initialize entry widgets BEFORE using them
        self.instructor_first_name = tk.Entry(None)  # Temporary placeholder
        self.instructor_last_name = tk.Entry(None)   # Temporary placeholder
        self.instructor_license = tk.Entry(None)     # Temporary placeholder
        self.search_entry = tk.Entry(None)           # Temporary placeholder

        # Configure custom styles
        style = ttk.Style()
        
        # Color Palette (Modern, Professional)
        colors = {
            'background': '#f4f6f9',      # Soft light blue-gray
            'primary': '#3498db',          # Bright blue
            'secondary': '#2ecc71',        # Green for positive actions
            'accent': '#e74c3c',           # Red for destructive actions
            'text_dark': '#2c3e50',        # Dark slate blue for text
            'text_light': '#34495e',       # Slightly lighter dark blue
            'input_bg': '#ffffff',         # Clean white for inputs
            'border': '#bdc3c7'            # Light gray border
        }
        
        # Custom Styles
        style.configure('Instructor.TFrame', background=colors['background'])
        style.configure('TLabel', 
            background=colors['background'], 
            foreground=colors['text_dark'], 
            font=('Segoe UI', 10))
        
        style.configure('Custom.TButton', 
            font=('Segoe UI', 10, 'bold'),
            padding=10)
        
# Add these style map configurations
        style.map('Search.TButton',
            background=[('active', colors['primary']), ('pressed', '#2980b9')],
            foreground=[('active', 'black'), ('pressed', 'black')]
        )

        style.map('Reset.TButton',
            background=[('active', colors['accent']), ('pressed', '#c0392b')],
            foreground=[('active', 'black'), ('pressed', 'black')]
        )

        style.map('Add.TButton',
            background=[('active', colors['secondary']), ('pressed', '#27ae60')],
            foreground=[('active', 'black'), ('pressed', 'black')]
        )
                # Main Frame with soft background
        main_frame = tk.Frame(instructor_tab, bg=colors['background'], bd=0)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title with modern typography
        title_label = tk.Label(
            main_frame, 
            text="Instructor Management", 
            font=('Segoe UI', 18, 'bold'), 
            bg=colors['background'], 
            fg=colors['text_dark']
        )
        title_label.pack(pady=(0, 20), anchor='center')

        # Search Section with improved layout
        search_frame = tk.Frame(main_frame, bg=colors['background'])
        search_frame.pack(pady=10, fill='x')

        search_label = ttk.Label(search_frame, text="Search:", style='TLabel')
        search_label.pack(side="left", padx=(0, 10))

        self.search_entry = tk.Entry(
            search_frame, 
            font=('Segoe UI', 12), 
            width=30, 
            bg=colors['input_bg'], 
            fg=colors['text_light'],
            relief='solid',
            borderwidth=1
        )
        self.search_entry.pack(side="left", padx=10, fill='x', expand=True)

        # Bind the Enter key to search_instructors method
        self.search_entry.bind("<Return>", lambda event: self.search_instructors())

        search_btn = ttk.Button(
            search_frame, 
            text="Search", 
            command=self.search_instructors, 
            style='Search.TButton'
        )
        search_btn.pack(side="left", padx=5)

        reset_btn = ttk.Button( 
            search_frame, 
            text="Reset", 
            command=self.view_instructors, 
            style='Reset.TButton'
        )
        reset_btn.pack(side="left", padx=5)

        # Input Section with card-like design
    # Input Section with optimized spacing
        input_frame = tk.Frame(
            main_frame, 
            bg='white', 
            bd=1, 
            relief='solid', 
            highlightbackground=colors['border'], 
            highlightthickness=1
        )
        input_frame.pack(pady=(10,5), ipadx=10, ipady=10, fill='x')  # Reduced padding

        input_fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("License Number:", "license")
        ]

        for i, (label_text, field_name) in enumerate(input_fields):
            label = ttk.Label(input_frame, text=label_text, style='TLabel')
            label.grid(row=i, column=0, padx=(5,10), pady=3, sticky="e")  # Reduced padding
            
            entry = tk.Entry(
                input_frame, 
                font=('Segoe UI', 12), 
                width=25, 
                bg=colors['input_bg'], 
                fg=colors['text_light'],
                relief='solid',
                borderwidth=1
            )
            entry.grid(row=i, column=1, padx=(0,5), pady=3, sticky="w")  # Reduced padding
            
            # Assign to specific variables
            if i == 0:
                entry_first_name = entry
                self.instructor_first_name = entry
            elif i == 1:
                entry_last_name = entry
                self.instructor_last_name = entry
            else:
                entry_license = entry
                self.instructor_license = entry

        # Add button with minimal spacing
        add_btn = ttk.Button(
            input_frame, 
            text="Add Instructor", 
            command=self.add_instructor, 
            style='Add.TButton'
        )
        add_btn.grid(row=3, column=1, pady=(3,5), padx=(0,5), sticky='w')  # Reduced padding

        # Configure grid columns to minimize space
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Separate frame for delete button and instructor count
        delete_frame = tk.Frame(main_frame, bg=colors['background'])
        delete_frame.pack(pady=0, fill='x', anchor='e')  # Removed vertical padding
    
        # Delete button
        delete_btn = ttk.Button(
            delete_frame, 
            text="Delete Instructor", 
            command=self.delete_instructor,
            style='Reset.TButton'
        )
        delete_btn.pack(side='right', padx=10, pady=2)  # Reduced padding

        # Total instructor count label
        self.instructor_count_label = tk.Label(
            delete_frame,
            text="Total Instructors: 0",  # Initial placeholder
            font=('Segoe UI', 10, 'bold'),
            bg=colors['background'],
            fg=colors['text_dark']
        )
        self.instructor_count_label.pack(side='right', padx=10, pady=2)

        # TreeView Section
        tree_frame = tk.Frame(main_frame, bg='white', bd=1, relief='solid')
        tree_frame.pack(pady=10, fill="both", expand=True)

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        vertical_scrollbar.pack(side="right", fill="y")

        horizontal_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        horizontal_scrollbar.pack(side="bottom", fill="x")

        # TreeView with improved styling
        self.instructor_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "First Name", "Last Name", "License Number"),
            show="headings",
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )
        self.instructor_tree.pack(fill="both", expand=True)

        # Configure columns
        column_widths = {"ID": 50, "First Name": 150, "Last Name": 150, "License Number": 150}
        for col, width in column_widths.items():
            self.instructor_tree.heading(col, text=col)
            self.instructor_tree.column(col, width=width, anchor="center")

        # Configure scrollbars
        vertical_scrollbar.config(command=self.instructor_tree.yview)
        horizontal_scrollbar.config(command=self.instructor_tree.xview)

        # Populate initial data
        self.view_instructors()

    def add_instructor(self):
        # Retrieve input values
        first_name = self.instructor_first_name.get().strip()
        last_name = self.instructor_last_name.get().strip()
        license_number = self.instructor_license.get().strip()

        # Validation checks
        if not first_name or not last_name:
            messagebox.showerror("Input Error", "First Name and Last Name cannot be empty.")
            return

        if not license_number:
            messagebox.showerror("Input Error", "License Number cannot be empty.")
            return

        # License Number Validation: Alphanumeric mix
        license_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$'
        if not re.match(license_regex, license_number):
            messagebox.showerror("Input Error", "License Number must contain both letters and numbers.")
            return

        # Check for duplicate license number (case-insensitive)
        try:
            # Convert to uppercase for case-insensitive comparison
            # Using UPPER() function in SQLite for case-insensitive comparison
            self.cursor.execute('''
                SELECT COUNT(*) FROM instructors 
                WHERE UPPER(license_number) = UPPER(?)
            ''', (license_number,))
            
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", 
                    "This License Number is already registered.")
                return

            # If no duplicate found, proceed with insertion
            # Store the license number in its original case
            self.cursor.execute('''
                INSERT INTO instructors 
                (first_name, last_name, license_number) 
                VALUES (?, ?, ?)
            ''', (first_name, last_name, license_number))
            
            self.conn.commit()
            
            # Clear input fields after successful addition
            self.instructor_first_name.delete(0, tk.END)
            self.instructor_last_name.delete(0, tk.END)
            self.instructor_license.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Instructor Added Successfully")
            
            # Refresh views
            self.populate_instructor_dropdown()
            self.view_instructors()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Database error occurred while adding instructor.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def delete_instructor(self):
        selected_item = self.instructor_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No instructor selected.")
            return
        
        # Retrieve the ID from the selected row
        values = self.instructor_tree.item(selected_item, "values")
        if not values:
            messagebox.showerror("Error", "Please select a valid row.")
            return
        
        instructor_id = values[0]  # Assuming the first column is the ID
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete instructor ID {instructor_id}?")
        if confirm:
            try:
                # First, check if the instructor has any existing lessons
                self.cursor.execute("SELECT COUNT(*) FROM lessons WHERE instructor_id = ?", (instructor_id,))
                lesson_count = self.cursor.fetchone()[0]
                
                if lesson_count > 0:
                    messagebox.showerror("Error", "Cannot delete instructor with existing lessons.")
                    return
                
                # Delete from the database
                delete_query = "DELETE FROM instructors WHERE id=?"
                self.cursor.execute(delete_query, (instructor_id,))
                self.conn.commit()  # Commit the change to the database
                
                # Refresh the TreeView
                self.view_instructors()
                messagebox.showinfo("Success", "Instructor deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def view_instructors(self):
        # Clear the TreeView
        for row in self.instructor_tree.get_children():
            self.instructor_tree.delete(row)

        # Fetch data from the database
        select_query = 'SELECT id, first_name, last_name, license_number FROM instructors'
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()

        # Populate the TreeView
        for row in rows:
            self.instructor_tree.insert("", "end", values=row)

        # Update the total count label
        total_instructors = len(rows)
        self.instructor_count_label.config(text=f"Total Instructors: {total_instructors}")

    def search_instructors(self):
        # Clear the TreeView
        for item in self.instructor_tree.get_children():
            self.instructor_tree.delete(item)

        # Get the search query
        search_query = self.search_entry.get().strip()

        # Perform a case-insensitive search in the database
        query = """
            SELECT id, first_name, last_name, license_number 
            FROM instructors 
            WHERE UPPER(first_name) LIKE UPPER(?) OR 
                UPPER(last_name) LIKE UPPER(?) OR 
                UPPER(license_number) LIKE UPPER(?)
        """
        self.cursor.execute(query, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        results = self.cursor.fetchall()

        if results:
            # Populate TreeView with results
            for instructor in results:
                self.instructor_tree.insert("", "end", values=instructor)
        else:
            # Add a dummy row for "No results found"
            self.instructor_tree.insert("", "end", values=("", "No results found", "", ""), tags=("placeholder",))

        # Style for the placeholder row
        self.instructor_tree.tag_configure("placeholder", foreground="red", font=("Arial", 12, "italic"))

    def populate_instructor_dropdown(self):
    # Populate instructor dropdown
        self.cursor.execute('SELECT id, CONCAT(first_name, " ", last_name) as full_name FROM instructors')
        instructors = self.cursor.fetchall()
        self.instructor_select['values'] = [f"{i[1]}" for i in instructors]  # Display only full names for selection


# lesson  section------------


    def create_lesson_tab(self):
        # Lesson Management Tab
        lesson_tab = ttk.Frame(self.notebook, style='Lesson.TFrame')
        self.notebook.add(lesson_tab, text="Lessons")

        # Configure custom styles
        style = ttk.Style()
        
        # Color Palette (Modern, Professional)
        colors = {
            'background': '#f4f6f9',      # Soft light blue-gray
            'primary': '#3498db',         # Bright blue
            'secondary': '#2ecc71',       # Green for positive actions
            'accent': '#e74c3c',          # Red for destructive actions
            'text_dark': '#2c3e50',       # Dark slate blue for text
            'text_light': '#34495e',      # Slightly lighter dark blue
            'input_bg': '#ffffff',        # Clean white for inputs
            'border': '#bdc3c7'           # Light gray border
        }
        
        # Custom Styles
        style.configure('Lesson.TFrame', background=colors['background'])
        style.configure('TLabel', 
            background=colors['background'], 
            foreground=colors['text_dark'], 
            font=('Segoe UI', 10))
        
        # Main Frame with soft background
        main_frame = tk.Frame(lesson_tab, bg=colors['background'], bd=0)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title with modern typography
        title_label = tk.Label(
            main_frame, 
            text="Lesson Management", 
            font=('Segoe UI', 18, 'bold'), 
            bg=colors['background'], 
            fg=colors['text_dark']
        )
        title_label.pack(pady=(0, 20), anchor='center')

        # Input Section with card-like design
        input_frame = tk.Frame(
            main_frame, 
            bg='white', 
            bd=1, 
            relief='solid', 
            highlightbackground=colors['border'], 
            highlightthickness=1
        )
        input_frame.pack(pady=(10,5), ipadx=10, ipady=10, fill='x')

        # Initialize widgets first
        self.student_select = ttk.Combobox(input_frame, font=('Segoe UI', 12), width=25)
        self.instructor_select = ttk.Combobox(input_frame, font=('Segoe UI', 12), width=25)
        self.lesson_type = ttk.Combobox(input_frame, font=('Segoe UI', 12), width=25,
                                    values=['Introductory', 'Standard', 'Pass Plus', 'Driving Test'])
        self.pay_rate_label = tk.Label(input_frame, text="0", font=('Segoe UI', 12),
                                    bg=colors['input_bg'], fg=colors['text_dark'])
        self.lesson_date = DateEntry(input_frame, font=('Segoe UI', 12), width=25,
                                    date_pattern='yyyy-mm-dd')
        self.lesson_duration = tk.Entry(input_frame, font=('Segoe UI', 12), width=25)
        self.total_fee_label = tk.Label(input_frame, text="0", font=('Segoe UI', 12),
                                    bg=colors['input_bg'], fg=colors['text_dark'])

        # Bind events
        self.lesson_type.bind("<<ComboboxSelected>>", self.update_pay_rate)
        self.lesson_duration.bind("<KeyRelease>", self.calculate_total_fee)

        # Input fields configuration
        input_fields = [
            ("Select Student:", self.student_select),
            ("Select Instructor:", self.instructor_select),
            ("Lesson Type:", self.lesson_type),
            ("Pay Rate (£/hr):", self.pay_rate_label),
            ("Lesson Date:", self.lesson_date),
            ("Duration (hours):", self.lesson_duration),
            ("Total Fee (£):", self.total_fee_label)
        ]

        for i, (label_text, widget) in enumerate(input_fields):
            label = ttk.Label(input_frame, text=label_text, style='TLabel')
            label.grid(row=i, column=0, padx=(5,10), pady=3, sticky="e")
            widget.grid(row=i, column=1, padx=(0,5), pady=3, sticky="w")

        # Button frame
        button_frame = tk.Frame(main_frame, bg=colors['background'])
        button_frame.pack(pady=10, fill='x')

        # Styled buttons
        view_btn = ttk.Button(
            button_frame,
            text="View Lessons",
            command=self.view_lessons,
            style='Search.TButton'
        )
        view_btn.pack(side='left', padx=5)

        book_btn = ttk.Button(
            button_frame,
            text="Book Lesson",
            command=self.book_lesson,
            style='Add.TButton'
        )
        book_btn.pack(side='left', padx=5)

        # TreeView Section with improved styling
        tree_frame = tk.Frame(main_frame, bg='white', bd=1, relief='solid')
        tree_frame.pack(pady=10, fill="both", expand=True)

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        vertical_scrollbar.pack(side="right", fill="y")

        # TreeView Configuration
        self.lesson_tree = ttk.Treeview(
            tree_frame,
            columns=('Student', 'Instructor', 'Type', 'Date', 'Duration', 'Fee', 'Status'),
            show="headings",
            yscrollcommand=vertical_scrollbar.set
        )
        self.lesson_tree.pack(fill="both", expand=True)

        # Configure columns
        column_configs = {
            'Student': {'width': 120, 'anchor': 'center'},
            'Instructor': {'width': 120, 'anchor': 'center'},
            'Type': {'width': 100, 'anchor': 'center'},
            'Date': {'width': 100, 'anchor': 'center'},
            'Duration': {'width': 70, 'anchor': 'center'},
            'Fee': {'width': 70, 'anchor': 'center'},
            'Status': {'width': 80, 'anchor': 'center'}
        }

        for col, config in column_configs.items():
            self.lesson_tree.heading(col, text=col)
            self.lesson_tree.column(col, **config)

        # Configure scrollbar
        vertical_scrollbar.config(command=self.lesson_tree.yview)

        # Initial data load
        self.populate_student_dropdown()
        self.populate_instructor_dropdown()
 
        self.view_lessons()


    def reset_lesson_form(self):
        """Clears all input fields in the lesson form."""
        self.student_select.set("")
        self.instructor_select.set("")
        self.lesson_type.set("")
        self.pay_rate_label.config(text="0")
        self.lesson_date.set_date(datetime.date.today())  # Reset to today's date
        self.lesson_duration.delete(0, tk.END)
        self.total_fee_label.config(text="0")

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def book_lesson(self):
        # Get values from the form
        student_name = self.student_select.get()
        instructor_name = self.instructor_select.get()
        lesson_type = self.lesson_type.get()
        lesson_date = self.lesson_date.get_date()  # Assuming DateEntry returns a datetime object
        duration = int(self.lesson_duration.get())
        status = 'Booked'
        
        # Get the pay rate as a float
        pay_rate_text = self.pay_rate_label.cget("text")
        
        # Remove currency symbol if present
        if '£' in pay_rate_text:
            pay_rate_text = pay_rate_text.replace('£', '')
        
        # Convert to float
        try:
            fee = float(pay_rate_text)
        except ValueError:
            self.show_error("Invalid fee format")  # Display error if conversion fails
            return

        # Fetch IDs for student and instructor based on names
        self.cursor.execute("SELECT id FROM students WHERE CONCAT(first_name, ' ', last_name) = ?", (student_name,))
        student_record = self.cursor.fetchone()
        
        if student_record is None:
            self.show_error(f"Student '{student_name}' not found.")  # Show error if student is not found
            return
        student_id = student_record[0]

        self.cursor.execute("SELECT id FROM instructors WHERE CONCAT(first_name, ' ', last_name) = ?", (instructor_name,))
        instructor_record = self.cursor.fetchone()
        
        if instructor_record is None:
            self.show_error(f"Instructor '{instructor_name}' not found.")  # Show error if instructor is not found
            return
        instructor_id = instructor_record[0]

        # Insert into the lessons table
        self.cursor.execute('''
            INSERT INTO lessons (student_id, instructor_id, lesson_type, lesson_date, duration, status, fee)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, instructor_id, lesson_type, lesson_date, duration, status, fee))

        # Commit the changes
        self.conn.commit()
        self.reset_lesson_form()
        messagebox.showinfo("Success", "Lesson Booked ")
        self.view_lessons()       # Refresh the lessons view
        # self.clear_lesson_form()  # Clear form fields
        
        # Update UI: Clear form fields and refresh the lessons view

    def clear_lesson_form(self):
        # Clear the student selection
        self.student_select.set('')

        # Clear the instructor selection
        self.instructor_select.set('')

        # Clear the lesson type selection
        self.lesson_type.set('')

        # Clear the date picker
        self.lesson_date.set_date('')  # Reset to empty or current date

        # Clear the lesson duration entry
        self.lesson_duration.delete(0, tk.END)

        # Clear the total fee display
        self.pay_rate_label.config(text="0")  # Reset to default

    def update_pay_rate(self, event):
        lesson_type = self.lesson_type.get()
        pay_rate = self.pay_rate_map.get(lesson_type, 0)  # Fetch pay rate for the lesson type
        self.pay_rate_label.config(text=f"£{pay_rate}")  # Update pay rate display
        self.calculate_total_fee()  # Recalculate fee in case duration is already entered

    def calculate_total_fee(self, event=None):
        lesson_type = self.lesson_type.get()
        duration = self.lesson_duration.get()

        if lesson_type and duration.isdigit():
            pay_rate = self.pay_rate_map.get(lesson_type, 0)
            total_fee = pay_rate * int(duration)
            self.total_fee_label.config(text=f"£{total_fee}")
        else:
            self.total_fee_label.config(text="0")  # Reset if input is invalid

    def view_lessons(self):
        # Clear existing items
        for i in self.lesson_tree.get_children():
            self.lesson_tree.delete(i)
        
        # Fetch lessons with student and instructor names
        self.cursor.execute('''
            SELECT s.first_name || ' ' || s.last_name as student_name,
                i.first_name || ' ' || i.last_name as instructor_name,
                l.lesson_type, 
                l.lesson_date, 
                l.duration,
                l.fee,
                l.status
            FROM lessons l
            JOIN students s ON l.student_id = s.id
            JOIN instructors i ON l.instructor_id = i.id
        ''')
        rows = self.cursor.fetchall()
        
        # Debug print
        print("Fetched rows:", rows)
        
        # Insert the fetched rows into the treeview
        for row in rows:
            print("Inserting row:", row)  # Debug print
            self.lesson_tree.insert('', 'end', values=row)


class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide the main window initially
        
        # Create loading window
        self.loading_window = tk.Toplevel()
        self.loading_window.title("Loading")
        self.loading_window.attributes('-topmost', True)
        
        # Get screen width and height
        screen_width = self.loading_window.winfo_screenwidth()
        screen_height = self.loading_window.winfo_screenheight()
        
        # Set loading window size and position
        window_width = 400
        window_height = 300
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.loading_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.loading_window.overrideredirect(True)  # Remove window borders
        
        # Set background color
        self.loading_window.configure(bg='#ffffff')
        
        # Create and pack frames
        self.image_frame = tk.Frame(self.loading_window, bg='#ffffff')
        self.image_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        self.progress_frame = tk.Frame(self.loading_window, bg='#ffffff')
        self.progress_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Load and display animated GIF
        try:
            # Load GIF using PIL
            self.image_frames = []
            gif = Image.open("loading.gif")  # Make sure the GIF exists
            for frame in range(gif.n_frames):
                gif.seek(frame)
                frame_image = ImageTk.PhotoImage(gif.copy())
                self.image_frames.append(frame_image)
            self.current_frame = 0
        except Exception as e:
            print(f"Error loading GIF: {e}")
            # Fallback to a static image
            self.image_frames = [tk.PhotoImage(width=200, height=200)]
            self.current_frame = 0
            
        self.image_label = tk.Label(self.image_frame, image=self.image_frames[self.current_frame], bg='#ffffff')
        self.image_label.pack(pady=10)
        self.animate_gif()  # Start animation
        
        # Add title
        self.title_label = tk.Label(
            self.image_frame,
            text="Pass IT Driving School",
            font=('Segoe UI', 16, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        )
        self.title_label.pack(pady=5)
        
        # Add loading text
        self.loading_label = tk.Label(
            self.image_frame,
            text="Loading...",
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#7f8c8d'
        )
        self.loading_label.pack(pady=5)
        
        # Create progress bar
        self.progress = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=300
        )
        self.progress.pack(fill='x', pady=10)
        
        # Start progress
        self.progress_value = 0
        self.update_progress()

    def animate_gif(self):
        """Animate the GIF by looping through frames."""
        if self.image_frames:
            self.current_frame = (self.current_frame + 1) % len(self.image_frames)
            self.image_label.config(image=self.image_frames[self.current_frame])
            self.loading_window.after(20, self.animate_gif)  # Change frame every 100ms

    def update_progress(self):
        if self.progress_value < 100:
            self.progress_value += 2
            self.progress['value'] = self.progress_value
            self.loading_window.after(40, self.update_progress)  # Update every 40ms
        else:
            self.loading_window.after(500, self.show_main_window)  # Wait 0.5s before showing main window
    
    def show_main_window(self):
        self.loading_window.destroy()  # Close loading window
        self.root.deiconify()  # Show main window

def show_loading_screen(root):
        loading = LoadingScreen(root)
        return loading



def main():
    root = tk.Tk()
    app = DrivingSchoolApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    