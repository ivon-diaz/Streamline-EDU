import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class TemplateDialog:
    """Dialog for creating or editing a lesson template"""
    def __init__(self, parent, callback, template_data=None):
        self.callback = callback
        self.template_data = template_data
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Template" if template_data else "Create New Template")
        self.dialog.geometry("500x600")
        self.dialog.configure(bg="white")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
        # Header
        header = tk.Label(
            self.dialog,
            text="Edit Template" if template_data else "Create New Template",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        )
        header.pack(pady=20)
        
        # Form container
        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # Template Name
        tk.Label(
            form_frame,
            text="Template Name *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.name_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.name_entry.pack(fill="x", ipady=8, pady=(0, 15))
        if template_data:
            self.name_entry.insert(0, template_data.get("name", ""))
        
        # Subject
        tk.Label(
            form_frame,
            text="Subject *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(
            form_frame,
            textvariable=self.subject_var,
            font=("Arial", 11),
            state="readonly",
            values=["Reading", "Math", "Science", "Social Studies", "Art", "Physical Education", "Other"]
        )
        subject_combo.pack(fill="x", ipady=8, pady=(0, 15))
        if template_data:
            subject_combo.set(template_data.get("subject", "Select a subject"))
        else:
            subject_combo.set("Select a subject")
        
        # Duration
        tk.Label(
            form_frame,
            text="Duration (minutes) *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.duration_var = tk.StringVar()
        duration_combo = ttk.Combobox(
            form_frame,
            textvariable=self.duration_var,
            font=("Arial", 11),
            state="readonly",
            values=["15", "30", "45", "60", "90"]
        )
        duration_combo.pack(fill="x", ipady=8, pady=(0, 15))
        if template_data:
            duration_combo.set(template_data.get("duration", "45"))
        else:
            duration_combo.set("45")
        
        # Standards
        tk.Label(
            form_frame,
            text="Standards/Objectives",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.standards_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            height=3,
            wrap="word"
        )
        self.standards_text.pack(fill="x", pady=(0, 15))
        if template_data:
            self.standards_text.insert("1.0", template_data.get("standards", ""))
        
        # Activities/Materials
        tk.Label(
            form_frame,
            text="Activities/Materials",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.activities_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            height=4,
            wrap="word"
        )
        self.activities_text.pack(fill="x", pady=(0, 20))
        if template_data:
            self.activities_text.insert("1.0", template_data.get("activities", ""))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#E0E0E0",
            fg="#212121",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = tk.Button(
            button_frame,
            text="Save Template",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.save_template
        )
        save_btn.pack(side="right")
        
    def save_template(self):
        name = self.name_entry.get().strip()
        subject = self.subject_var.get()
        duration = self.duration_var.get()
        
        if not name:
            messagebox.showwarning("Validation Error", "Please enter a template name.")
            return
        
        if subject == "Select a subject":
            messagebox.showwarning("Validation Error", "Please select a subject.")
            return
        
        template_data = {
            "name": name,
            "subject": subject,
            "duration": duration,
            "standards": self.standards_text.get("1.0", "end-1c").strip(),
            "activities": self.activities_text.get("1.0", "end-1c").strip()
        }
        
        # If editing, preserve the original ID
        if self.template_data and "id" in self.template_data:
            template_data["id"] = self.template_data["id"]
        
        self.callback(template_data)
        self.dialog.destroy()


class LessonDialog:
    """Dialog for adding a new lesson"""
    def __init__(self, parent, callback):
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Lesson")
        self.dialog.geometry("500x550")
        self.dialog.configure(bg="white")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (550 // 2)
        self.dialog.geometry(f"500x550+{x}+{y}")
        
        # Header
        header = tk.Label(
            self.dialog,
            text="Create New Lesson",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        )
        header.pack(pady=20)
        
        # Form container
        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # Lesson Title
        tk.Label(
            form_frame,
            text="Lesson Title *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.title_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.title_entry.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Subject
        tk.Label(
            form_frame,
            text="Subject *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(
            form_frame,
            textvariable=self.subject_var,
            font=("Arial", 11),
            state="readonly",
            values=["Reading", "Math", "Science", "Social Studies", "Art", "Physical Education", "Other"]
        )
        subject_combo.pack(fill="x", ipady=8, pady=(0, 15))
        subject_combo.set("Select a subject")
        
        # Standards
        tk.Label(
            form_frame,
            text="Standards/Objectives",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.standards_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            height=3,
            wrap="word"
        )
        self.standards_text.pack(fill="x", pady=(0, 15))
        
        # Duration
        tk.Label(
            form_frame,
            text="Duration (minutes)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.duration_var = tk.StringVar()
        duration_combo = ttk.Combobox(
            form_frame,
            textvariable=self.duration_var,
            font=("Arial", 11),
            state="readonly",
            values=["15", "30", "45", "60", "90"]
        )
        duration_combo.pack(fill="x", ipady=8, pady=(0, 15))
        duration_combo.set("45")
        
        # Notes
        tk.Label(
            form_frame,
            text="Notes",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.notes_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            height=4,
            wrap="word"
        )
        self.notes_text.pack(fill="x", pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#E0E0E0",
            fg="#212121",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = tk.Button(
            button_frame,
            text="Create Lesson",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.save_lesson
        )
        save_btn.pack(side="right")
        
    def save_lesson(self):
        title = self.title_entry.get().strip()
        subject = self.subject_var.get()
        
        if not title:
            messagebox.showwarning("Validation Error", "Please enter a lesson title.")
            return
        
        if subject == "Select a subject":
            messagebox.showwarning("Validation Error", "Please select a subject.")
            return
        
        lesson_data = {
            "title": title,
            "subject": subject,
            "standards": self.standards_text.get("1.0", "end-1c").strip(),
            "duration": self.duration_var.get(),
            "notes": self.notes_text.get("1.0", "end-1c").strip(),
            "progress": 0
        }
        
        self.callback(lesson_data)
        self.dialog.destroy()


class DashboardScreen:
    """Main dashboard screen"""
    def __init__(self, root, switch_to_lessons_callback):
        self.root = root
        self.switch_to_lessons = switch_to_lessons_callback
        
        self.frame = tk.Frame(root, bg="#f5f5f5")
        
        # Header
        header = tk.Frame(self.frame, bg="#2196F3", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="StreamlineEDU",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white",
            anchor="w"
        )
        header_label.pack(side="left", padx=30, pady=15)
        
        # User info
        user_frame = tk.Frame(header, bg="#2196F3")
        user_frame.pack(side="right", padx=30)
        
        user_circle = tk.Canvas(user_frame, width=40, height=40, bg="#2196F3", highlightthickness=0)
        user_circle.pack()
        user_circle.create_oval(2, 2, 38, 38, fill="#1976D2", outline="")
        user_circle.create_text(20, 20, text="IG", fill="white", font=("Arial", 12, "bold"))
        
        # Main content
        content = tk.Frame(self.frame, bg="#f5f5f5")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        welcome_label = tk.Label(
            content,
            text="Welcome back!",
            font=("Arial", 24, "bold"),
            bg="#f5f5f5",
            fg="#212121"
        )
        welcome_label.pack(anchor="w", pady=(0, 5))
        
        tagline_label = tk.Label(
            content,
            text="Reclaim your time with intelligent classroom management",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#757575"
        )
        tagline_label.pack(anchor="w", pady=(0, 25))
        
        # Dashboard cards
        cards_container = tk.Frame(content, bg="#f5f5f5")
        cards_container.pack(fill="both", expand=True)
        
        # Create dashboard cards
        self.create_card(
            cards_container, 
            "1. Attendance", 
            "Track student attendance",
            "#4CAF50",
            0, 0
        )
        
        self.create_card(
            cards_container,
            "2. Assessments",
            "Manage student assessments",
            "#FF9800",
            0, 1
        )
        
        self.create_card(
            cards_container,
            "3. Parent Communication",
            "Messages and updates",
            "#9C27B0",
            1, 0
        )
        
        # Lesson Planning card (clickable)
        lesson_card = self.create_card(
            cards_container,
            "4. Lesson Planning",
            "Plan and organize lessons",
            "#2196F3",
            1, 1,
            clickable=True
        )
        
        self.create_card(
            cards_container,
            "5. IEP Documentation",
            "Individual education plans",
            "#F44336",
            2, 0
        )
        
        self.create_card(
            cards_container,
            "6. Class Resources",
            "Materials and resources",
            "#00BCD4",
            2, 1
        )
        
    def create_card(self, parent, title, description, color, row, col, clickable=False):
        card = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1,
            cursor="hand2" if clickable else ""
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        if clickable:
            card.bind("<Button-1>", lambda e: self.switch_to_lessons())
            
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Color bar
        color_bar = tk.Frame(card, bg=color, height=8)
        color_bar.pack(fill="x")
        
        # Content
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            content_frame,
            text=title,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 10))
        
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=("Arial", 11),
            bg="white",
            fg="#757575",
            anchor="w"
        )
        desc_label.pack(fill="x")
        
        if clickable:
            for widget in [card, content_frame, title_label, desc_label]:
                widget.bind("<Button-1>", lambda e: self.switch_to_lessons())
        
        return card
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()


class LessonPlanningScreen:
    """Lesson planning screen with tabs"""
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.current_tab = "this_week"
        self.template_id_counter = 3  # For generating unique IDs
        
        # Sample data for different weeks
        self.lessons_data = {
            "this_week": [
                {
                    "day": "Monday, November 10",
                    "lessons": [
                        {"title": "Reading Comprehension", "progress": 75},
                        {"title": "Math - Multiplication Tables", "progress": 100}
                    ]
                },
                {
                    "day": "Tuesday, November 11",
                    "lessons": [
                        {"title": "Science - Plant Life Cycle", "progress": 50}
                    ]
                }
            ],
            "next_week": [
                {
                    "day": "Monday, November 17",
                    "lessons": [
                        {"title": "Writing Workshop", "progress": 0}
                    ]
                }
            ],
            "templates": [
                {
                    "id": 0,
                    "name": "Standard Math Lesson",
                    "subject": "Math",
                    "duration": "45",
                    "standards": "Common Core Math Standards",
                    "activities": "Warm-up exercises, direct instruction, guided practice, independent work"
                },
                {
                    "id": 1,
                    "name": "Reading Comprehension",
                    "subject": "Reading",
                    "duration": "60",
                    "standards": "Reading comprehension and analysis",
                    "activities": "Read aloud, group discussion, comprehension questions, writing response"
                },
                {
                    "id": 2,
                    "name": "Science Experiment",
                    "subject": "Science",
                    "duration": "90",
                    "standards": "Scientific method and inquiry",
                    "activities": "Hypothesis, materials setup, experiment, observation, conclusion"
                }
            ]
        }
        
        self.frame = tk.Frame(root, bg="#f5f5f5")
        
        # Header
        header = tk.Frame(self.frame, bg="#2196F3", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # StreamlineEDU branding
        branding_frame = tk.Frame(header, bg="#2196F3")
        branding_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(
            branding_frame,
            text="StreamlineEDU",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white"
        ).pack(anchor="w")
        
        header_label = tk.Label(
            branding_frame,
            text="Lesson Planning",
            font=("Arial", 11),
            bg="#2196F3",
            fg="#E3F2FD",
            anchor="w"
        )
        header_label.pack(anchor="w")
        
        # Navigation bar
        nav_frame = tk.Frame(self.frame, bg="#37474F", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)
        
        back_btn = tk.Label(
            nav_frame,
            text="← Back to Dashboard",
            font=("Arial", 11),
            bg="#37474F",
            fg="white",
            cursor="hand2"
        )
        back_btn.pack(side="left", padx=20, pady=10)
        back_btn.bind("<Button-1>", lambda e: self.back_callback())
        
        # User initials
        user_circle = tk.Canvas(nav_frame, width=35, height=35, bg="#37474F", highlightthickness=0)
        user_circle.pack(side="right", padx=20)
        user_circle.create_oval(2, 2, 33, 33, fill="#78909C", outline="")
        user_circle.create_text(17.5, 17.5, text="IG", fill="white", font=("Arial", 10, "bold"))
        
        # Tab bar
        self.tab_frame = tk.Frame(self.frame, bg="white")
        self.tab_frame.pack(fill="x", pady=(0, 10))
        
        tab_container = tk.Frame(self.tab_frame, bg="white")
        tab_container.pack(anchor="w", padx=20, pady=10)
        
        # Tab buttons
        self.this_week_tab = tk.Label(
            tab_container,
            text="This Week",
            font=("Arial", 11),
            bg="white",
            fg="#2196F3",
            cursor="hand2",
            padx=10,
            pady=5
        )
        self.this_week_tab.pack(side="left", padx=(0, 20))
        self.this_week_tab.bind("<Button-1>", lambda e: self.switch_tab("this_week"))
        
        self.next_week_tab = tk.Label(
            tab_container,
            text="Next Week",
            font=("Arial", 11),
            bg="white",
            fg="#757575",
            cursor="hand2",
            padx=10,
            pady=5
        )
        self.next_week_tab.pack(side="left", padx=(0, 20))
        self.next_week_tab.bind("<Button-1>", lambda e: self.switch_tab("next_week"))
        
        self.templates_tab = tk.Label(
            tab_container,
            text="Templates",
            font=("Arial", 11),
            bg="white",
            fg="#757575",
            cursor="hand2",
            padx=10,
            pady=5
        )
        self.templates_tab.pack(side="left")
        self.templates_tab.bind("<Button-1>", lambda e: self.switch_tab("templates"))
        
        # Underline for active tab
        self.underline = tk.Frame(tab_container, bg="#2196F3", height=3, width=80)
        self.underline.place(x=10, y=30)
        
        # Scrollable content area
        self.content_canvas = tk.Canvas(self.frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.content_canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.content_canvas, bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))
        )
        
        self.content_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.content_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.content_canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        self.content_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Render initial content
        self.render_content()
        
    def _on_mousewheel(self, event):
        self.content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        
        # Update tab colors
        self.this_week_tab.config(fg="#2196F3" if tab_name == "this_week" else "#757575")
        self.next_week_tab.config(fg="#2196F3" if tab_name == "next_week" else "#757575")
        self.templates_tab.config(fg="#2196F3" if tab_name == "templates" else "#757575")
        
        # Update underline position
        positions = {
            "this_week": 10,
            "next_week": 110,
            "templates": 230
        }
        self.underline.place(x=positions[tab_name], y=30)
        
        # Re-render content
        self.render_content()
        
    def render_content(self):
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if self.current_tab == "templates":
            self.render_templates()
        else:
            days_data = self.lessons_data[self.current_tab]
            for day_data in days_data:
                self.create_day_card(self.scrollable_frame, day_data)
            
            # Info banner
            self.create_info_banner(self.scrollable_frame)
    
    def render_templates(self):
        # Templates view header with create button
        header_frame = tk.Frame(self.scrollable_frame, bg="white")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header = tk.Label(
            header_frame,
            text="Lesson Templates",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        header.pack(side="left")
        
        create_btn = tk.Button(
            header_frame,
            text="+ Create Template",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            command=self.create_template
        )
        create_btn.pack(side="right")
        
        # Display templates
        templates = self.lessons_data["templates"]
        
        if not templates:
            empty_label = tk.Label(
                self.scrollable_frame,
                text="No templates yet. Click 'Create Template' to add one.",
                font=("Arial", 11),
                bg="white",
                fg="#757575",
                anchor="w"
            )
            empty_label.pack(fill="x", padx=20, pady=20)
        else:
            for template in templates:
                self.create_template_card(self.scrollable_frame, template)
    
    def create_template_card(self, parent, template):
        template_card = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        template_card.pack(fill="x", padx=20, pady=5)
        
        # Main content area
        content_frame = tk.Frame(template_card, bg="white")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Left side - Template info
        info_frame = tk.Frame(content_frame, bg="white")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Template name and subject
        name_label = tk.Label(
            info_frame,
            text=template["name"],
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        name_label.pack(fill="x")
        
        details_label = tk.Label(
            info_frame,
            text=f"{template['subject']} • {template['duration']} min",
            font=("Arial", 10),
            bg="white",
            fg="#757575",
            anchor="w"
        )
        details_label.pack(fill="x", pady=(3, 0))
        
        # Right side - Action buttons
        button_frame = tk.Frame(content_frame, bg="white")
        button_frame.pack(side="right")
        
        edit_btn = tk.Button(
            button_frame,
            text="Edit",
            font=("Arial", 9),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=lambda: self.edit_template(template)
        )
        edit_btn.pack(side="left", padx=(0, 5))
        
        delete_btn = tk.Button(
            button_frame,
            text="Delete",
            font=("Arial", 9),
            bg="#F44336",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=lambda: self.delete_template(template)
        )
        delete_btn.pack(side="left")
    
    def create_template(self):
        def save_template_callback(template_data):
            # Assign a new ID
            template_data["id"] = self.template_id_counter
            self.template_id_counter += 1
            
            # Add template to the list
            self.lessons_data["templates"].append(template_data)
            
            # Re-render the content
            self.render_content()
            messagebox.showinfo("Success", "Template created successfully!")
        
        TemplateDialog(self.root, save_template_callback)
    
    def edit_template(self, template):
        def update_template_callback(updated_data):
            # Find and update the template
            for i, t in enumerate(self.lessons_data["templates"]):
                if t["id"] == template["id"]:
                    self.lessons_data["templates"][i] = updated_data
                    break
            
            # Re-render the content
            self.render_content()
            messagebox.showinfo("Success", "Template updated successfully!")
        
        TemplateDialog(self.root, update_template_callback, template)
    
    def delete_template(self, template):
        result = messagebox.askyesno(
            "Delete Template",
            f"Are you sure you want to delete the template '{template['name']}'?"
        )
        
        if result:
            # Remove the template
            self.lessons_data["templates"] = [
                t for t in self.lessons_data["templates"] if t["id"] != template["id"]
            ]
            
            # Re-render the content
            self.render_content()
            messagebox.showinfo("Success", "Template deleted successfully!")
    
    def create_day_card(self, parent, day_data):
        card_frame = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        card_frame.pack(fill="x", pady=(0, 10), padx=20)
        
        # Card header
        card_header = tk.Frame(card_frame, bg="white")
        card_header.pack(fill="x", padx=20, pady=(15, 10))
        
        day_label = tk.Label(
            card_header,
            text=day_data["day"],
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121"
        )
        day_label.pack(side="left")
        
        add_btn = tk.Button(
            card_header,
            text="+ Add Lesson",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            command=lambda: self.add_lesson(day_data)
        )
        add_btn.pack(side="right")
        
        # Lessons
        for lesson in day_data["lessons"]:
            self.create_lesson_item(card_frame, lesson)
    
    def create_lesson_item(self, parent, lesson):
        lesson_frame = tk.Frame(parent, bg="white")
        lesson_frame.pack(fill="x", padx=20, pady=10)
        
        # Blue vertical line
        line = tk.Frame(lesson_frame, bg="#2196F3", width=4)
        line.pack(side="left", fill="y", padx=(0, 15))
        
        lesson_content = tk.Frame(lesson_frame, bg="white")
        lesson_content.pack(side="left", fill="x", expand=True)
        
        lesson_title = tk.Label(
            lesson_content,
            text=lesson["title"],
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        lesson_title.pack(fill="x")
        
        # Progress bar
        progress_bg = tk.Canvas(lesson_content, height=8, bg="white", highlightthickness=0)
        progress_bg.pack(fill="x", pady=(8, 3))
        
        max_width = 400
        progress_width = int((lesson["progress"] / 100) * max_width)
        
        progress_bg.create_rectangle(0, 0, max_width, 8, fill="#E0E0E0", outline="")
        progress_bg.create_rectangle(0, 0, progress_width, 8, fill="#4CAF50", outline="")
        
        # Status label
        if lesson["progress"] == 100:
            status_text = "Complete ✓"
            status_color = "#4CAF50"
        else:
            status_text = f"{lesson['progress']}% complete"
            status_color = "#757575"
        
        status_label = tk.Label(
            lesson_content,
            text=status_text,
            font=("Arial", 9),
            bg="white",
            fg=status_color,
            anchor="w"
        )
        status_label.pack(fill="x")
    
    def create_info_banner(self, parent):
        info_frame = tk.Frame(parent, bg="#FFF9C4", relief="solid", borderwidth=1)
        info_frame.pack(fill="x", pady=10, padx=20)
        
        # Yellow vertical line
        yellow_line = tk.Frame(info_frame, bg="#FFC107", width=5)
        yellow_line.pack(side="left", fill="y")
        
        info_content = tk.Frame(info_frame, bg="#FFF9C4")
        info_content.pack(side="left", fill="x", expand=True, padx=15, pady=12)
        
        info_title = tk.Label(
            info_content,
            text="Auto-populated with standards:",
            font=("Arial", 10, "bold"),
            bg="#FFF9C4",
            fg="#212121",
            anchor="w"
        )
        info_title.pack(fill="x")
        
        info_text = tk.Label(
            info_content,
            text="System suggests aligned resources and activities based on curriculum.",
            font=("Arial", 10),
            bg="#FFF9C4",
            fg="#212121",
            anchor="w"
        )
        info_text.pack(fill="x")
    
    def add_lesson(self, day_data):
        def save_lesson_callback(lesson_data):
            # Add new lesson to the day
            day_data["lessons"].append({
                "title": f"{lesson_data['subject']} - {lesson_data['title']}",
                "progress": 0
            })
            # Re-render the content
            self.render_content()
            messagebox.showinfo("Success", "Lesson created successfully!")
        
        LessonDialog(self.root, save_lesson_callback)
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()


class ClassroomManagementApp:
    """Main application controller"""
    def __init__(self, root):
        self.root = root
        self.root.title("StreamlineEDU - Classroom Management Platform")
        self.root.geometry("800x700")
        
        # Create screens
        self.dashboard = DashboardScreen(root, self.show_lesson_planning)
        self.lesson_planning = LessonPlanningScreen(root, self.show_dashboard)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def show_dashboard(self):
        self.lesson_planning.hide()
        self.dashboard.show()
    
    def show_lesson_planning(self):
        self.dashboard.hide()
        self.lesson_planning.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClassroomManagementApp(root)
    root.mainloop()
