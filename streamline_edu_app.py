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
    def __init__(self, root, switch_to_lessons_callback, switch_to_parent_comm_callback):
        self.root = root
        self.switch_to_lessons = switch_to_lessons_callback
        self.switch_to_parent_comm = switch_to_parent_comm_callback
        
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
        
        # Create dashboard cards in 4x2 grid (4 columns, 2 rows)
        self.create_card(
            cards_container, 
            "1. Attendance Tracking", 
            "Track and manage student attendance",
            "#4CAF50",
            0, 0
        )
        
        # Lesson Planning card (clickable)
        self.create_card(
            cards_container,
            "2. Lesson Planning",
            "Plan and organize lessons",
            "#2196F3",
            0, 1,
            clickable=True,
            click_callback=self.switch_to_lessons
        )
        
        # Parent Communication card (clickable)
        self.create_card(
            cards_container,
            "3. Parent Communication",
            "Messages and updates",
            "#9C27B0",
            0, 2,
            clickable=True,
            click_callback=self.switch_to_parent_comm
        )
        
        self.create_card(
            cards_container,
            "4. IEP Progress Reports",
            "Individual education plans",
            "#F44336",
            0, 3
        )
        
        self.create_card(
            cards_container,
            "5. Assessment Documentation",
            "Manage student assessments",
            "#FF9800",
            1, 0
        )
        
        self.create_card(
            cards_container,
            "6. AI Intelligent Assistant",
            "Smart classroom assistant",
            "#00BCD4",
            1, 1
        )
        
        self.create_card(
            cards_container,
            "7. Reports & Compliance",
            "Generate reports and track compliance",
            "#795548",
            1, 2
        )
        
        self.create_card(
            cards_container,
            "8. Settings & Profile",
            "Manage your account",
            "#607D8B",
            1, 3
        )
        
    def create_card(self, parent, title, description, color, row, col, clickable=False, click_callback=None):
        card = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1,
            cursor="hand2" if clickable else ""
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        if clickable and click_callback:
            card.bind("<Button-1>", lambda e: click_callback())
            
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
        
        if clickable and click_callback:
            for widget in [card, content_frame, title_label, desc_label]:
                widget.bind("<Button-1>", lambda e: click_callback())
        
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


class MessageComposerDialog:
    """Dialog for composing or editing email messages"""
    def __init__(self, parent, callback, draft_data=None, mode="new"):
        self.callback = callback
        self.draft_data = draft_data
        self.mode = mode  # "new", "edit", or "review"
        self.dialog = tk.Toplevel(parent)
        
        title_map = {
            "new": "New Message",
            "edit": "Edit Draft",
            "review": "Review & Send Message"
        }
        self.dialog.title(title_map.get(mode, "Message Composer"))
        self.dialog.geometry("600x700")
        self.dialog.configure(bg="white")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"600x700+{x}+{y}")
        
        # Header
        header_text = title_map.get(mode, "Message Composer")
        if mode == "review":
            header_text = "Review AI-Generated Message"
        
        header = tk.Label(
            self.dialog,
            text=header_text,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        )
        header.pack(pady=20)
        
        # AI Badge for review mode
        if mode == "review":
            ai_badge = tk.Label(
                self.dialog,
                text="✨ AI Generated - Please review before sending",
                font=("Arial", 10),
                bg="#E3F2FD",
                fg="#2196F3",
                padx=15,
                pady=8
            )
            ai_badge.pack(pady=(0, 15))
        
        # Form container
        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # To (Recipient)
        tk.Label(
            form_frame,
            text="To: *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.to_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.to_entry.pack(fill="x", ipady=8, pady=(0, 15))
        if draft_data:
            self.to_entry.insert(0, draft_data.get("recipient", ""))
        
        # Subject
        tk.Label(
            form_frame,
            text="Subject: *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.subject_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.subject_entry.pack(fill="x", ipady=8, pady=(0, 15))
        if draft_data:
            self.subject_entry.insert(0, draft_data.get("subject", ""))
        
        # Message Body
        tk.Label(
            form_frame,
            text="Message: *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        # Text widget with scrollbar
        text_container = tk.Frame(form_frame, relief="solid", borderwidth=1)
        text_container.pack(fill="both", expand=True, pady=(0, 15))
        
        text_scrollbar = tk.Scrollbar(text_container)
        text_scrollbar.pack(side="right", fill="y")
        
        self.message_text = tk.Text(
            text_container,
            font=("Arial", 11),
            wrap="word",
            yscrollcommand=text_scrollbar.set
        )
        self.message_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        text_scrollbar.config(command=self.message_text.yview)
        
        if draft_data:
            # For review/edit mode, use the full preview text or generate a complete message
            if mode == "review":
                body = draft_data.get("preview", "") + "\n\nBest regards,\nYour Name\n\n---\nSent via StreamlineEDU"
            else:
                body = draft_data.get("body", draft_data.get("preview", ""))
            self.message_text.insert("1.0", body)
        
        # Priority checkbox
        self.priority_var = tk.BooleanVar()
        priority_check = tk.Checkbutton(
            form_frame,
            text="Mark as high priority",
            variable=self.priority_var,
            font=("Arial", 10),
            bg="white",
            fg="#212121"
        )
        priority_check.pack(anchor="w", pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Different button layouts based on mode
        if mode == "review":
            # Review mode: Edit Draft, Discard, Send
            discard_btn = tk.Button(
                button_frame,
                text="Discard",
                font=("Arial", 11),
                bg="#F44336",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8,
                command=self.discard_draft
            )
            discard_btn.pack(side="left")
            
            edit_draft_btn = tk.Button(
                button_frame,
                text="Edit Draft",
                font=("Arial", 11),
                bg="#9E9E9E",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8,
                command=self.switch_to_edit
            )
            edit_draft_btn.pack(side="left", padx=(10, 0))
            
            send_btn = tk.Button(
                button_frame,
                text="Send Message",
                font=("Arial", 11, "bold"),
                bg="#4CAF50",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                command=self.send_message
            )
            send_btn.pack(side="right")
        else:
            # New/Edit mode: Cancel, Save Draft, Send
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
            cancel_btn.pack(side="left")
            
            save_draft_btn = tk.Button(
                button_frame,
                text="Save Draft",
                font=("Arial", 11),
                bg="#9E9E9E",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8,
                command=self.save_draft
            )
            save_draft_btn.pack(side="left", padx=(10, 0))
            
            send_btn = tk.Button(
                button_frame,
                text="Send",
                font=("Arial", 11, "bold"),
                bg="#4CAF50",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                command=self.send_message
            )
            send_btn.pack(side="right")
    
    def send_message(self):
        recipient = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.message_text.get("1.0", "end-1c").strip()
        
        if not recipient:
            messagebox.showwarning("Validation Error", "Please enter a recipient.")
            return
        
        if not subject:
            messagebox.showwarning("Validation Error", "Please enter a subject.")
            return
        
        if not body:
            messagebox.showwarning("Validation Error", "Please enter a message.")
            return
        
        message_data = {
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "priority": self.priority_var.get(),
            "status": "sent",
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
        
        self.callback(message_data, "send")
        self.dialog.destroy()
        messagebox.showinfo("Success", f"Message sent to {recipient}!")
    
    def save_draft(self):
        recipient = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.message_text.get("1.0", "end-1c").strip()
        
        if not recipient and not subject and not body:
            messagebox.showwarning("Empty Draft", "Cannot save an empty draft.")
            return
        
        message_data = {
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "preview": body[:100] + "..." if len(body) > 100 else body,
            "priority": self.priority_var.get(),
            "status": "draft",
            "generated_time": "Just now"
        }
        
        self.callback(message_data, "save_draft")
        self.dialog.destroy()
        messagebox.showinfo("Saved", "Draft saved successfully!")
    
    def discard_draft(self):
        result = messagebox.askyesno(
            "Discard Draft",
            "Are you sure you want to discard this draft?"
        )
        if result:
            if self.draft_data:
                self.callback(self.draft_data, "discard")
            self.dialog.destroy()
    
    def switch_to_edit(self):
        """Switch from review mode to edit mode"""
        self.dialog.destroy()
        # Re-open in edit mode
        # This would be handled by the parent


class ParentCommunicationScreen:
    """Parent communication screen with messaging features"""
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.message_id_counter = 3  # For generating unique message IDs
        
        # Sample data for messages
        self.messages_data = {
            "drafts": [
                {
                    "id": 0,
                    "subject": "Re: Emma's Progress",
                    "preview": "Dear Mrs. Anderson, Emma has shown excellent progress in reading comprehension this week...",
                    "body": "Dear Mrs. Anderson,\n\nEmma has shown excellent progress in reading comprehension this week. She has been actively participating in group discussions and her test scores have improved significantly.\n\nShe particularly excelled in identifying main ideas and supporting details in the stories we've been reading. I'm very pleased with her dedication and effort.\n\nPlease let me know if you have any questions or would like to schedule a meeting to discuss her progress further.",
                    "recipient": "Mrs. Anderson",
                    "generated_time": "2 hrs ago",
                    "status": "draft"
                }
            ],
            "recent": [
                {
                    "id": 1,
                    "sender": "Mrs. Chen",
                    "subject": "Re: James homework assignment",
                    "time": "10:30 AM",
                    "unread": True
                },
                {
                    "id": 2,
                    "sender": "Mr. Garcia",
                    "subject": "Question about field trip permission",
                    "time": "Yesterday",
                    "unread": False
                }
            ]
        }
        
        self.frame = tk.Frame(root, bg="#f5f5f5")
        
        # Header
        header = tk.Frame(self.frame, bg="#9C27B0", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # StreamlineEDU branding
        branding_frame = tk.Frame(header, bg="#9C27B0")
        branding_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(
            branding_frame,
            text="StreamlineEDU",
            font=("Arial", 14, "bold"),
            bg="#9C27B0",
            fg="white"
        ).pack(anchor="w")
        
        header_label = tk.Label(
            branding_frame,
            text="Parent Communication",
            font=("Arial", 11),
            bg="#9C27B0",
            fg="#F3E5F5",
            anchor="w"
        )
        header_label.pack(anchor="w")
        
        # Navigation bar
        nav_frame = tk.Frame(self.frame, bg="#37474F", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)
        
        back_btn = tk.Label(
            nav_frame,
            text="← Back  Messages",
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
        
        # Main content area
        content_frame = tk.Frame(self.frame, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Inbox header with New Message button
        inbox_header = tk.Frame(content_frame, bg="white")
        inbox_header.pack(fill="x", pady=(0, 10))
        
        inbox_info = tk.Frame(inbox_header, bg="white")
        inbox_info.pack(side="left")
        
        inbox_label = tk.Label(
            inbox_info,
            text="Inbox",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        inbox_label.pack(anchor="w")
        
        needs_attention = tk.Label(
            inbox_info,
            text="5 messages need attention",
            font=("Arial", 10),
            bg="white",
            fg="#757575",
            anchor="w"
        )
        needs_attention.pack(anchor="w")
        
        new_msg_btn = tk.Button(
            inbox_header,
            text="+ New Message",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.create_new_message
        )
        new_msg_btn.pack(side="right")
        
        # Scrollable content
        canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # AI Drafts section
        self.create_ai_drafts_section(scrollable_frame)
        
        # Recent Messages section
        self.create_recent_messages_section(scrollable_frame)
        
        # Info banner
        self.create_info_banner(scrollable_frame)
        
        # Store references
        self.scrollable_frame = scrollable_frame
        
        # Enable mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def create_ai_drafts_section(self, parent):
        drafts_container = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        drafts_container.pack(fill="x", pady=(0, 15))
        
        # Header
        drafts_header = tk.Frame(drafts_container, bg="white")
        drafts_header.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(
            drafts_header,
            text="Drafts Generated by AI",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121"
        ).pack(side="left")
        
        tk.Label(
            drafts_header,
            text="AI Assisted",
            font=("Arial", 9),
            bg="#E3F2FD",
            fg="#2196F3",
            padx=8,
            pady=2
        ).pack(side="right")
        
        # Draft messages or empty state
        if not self.messages_data["drafts"]:
            empty_label = tk.Label(
                drafts_container,
                text="No drafts available. AI will generate helpful draft responses as needed.",
                font=("Arial", 10),
                bg="white",
                fg="#757575",
                anchor="w"
            )
            empty_label.pack(fill="x", padx=20, pady=(0, 15))
        else:
            for draft in self.messages_data["drafts"]:
                self.create_draft_item(drafts_container, draft)
    
    def create_draft_item(self, parent, draft):
        draft_frame = tk.Frame(parent, bg="#F5F5F5")
        draft_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Subject and time
        subject_frame = tk.Frame(draft_frame, bg="#F5F5F5")
        subject_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        tk.Label(
            subject_frame,
            text=draft["subject"],
            font=("Arial", 11, "bold"),
            bg="#F5F5F5",
            fg="#212121"
        ).pack(side="left")
        
        tk.Label(
            subject_frame,
            text=f"Generated {draft['generated_time']}",
            font=("Arial", 9),
            bg="#F5F5F5",
            fg="#757575"
        ).pack(side="right")
        
        # Preview text
        preview_label = tk.Label(
            draft_frame,
            text=draft["preview"],
            font=("Arial", 10),
            bg="#F5F5F5",
            fg="#424242",
            anchor="w",
            justify="left",
            wraplength=450
        )
        preview_label.pack(fill="x", padx=15, pady=(0, 10))
        
        # Action buttons
        button_frame = tk.Frame(draft_frame, bg="#F5F5F5")
        button_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        review_btn = tk.Button(
            button_frame,
            text="Review & Send",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=lambda: self.review_draft(draft)
        )
        review_btn.pack(side="left", padx=(0, 10))
        
        edit_btn = tk.Button(
            button_frame,
            text="Edit",
            font=("Arial", 10),
            bg="#9E9E9E",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=lambda: self.edit_draft(draft)
        )
        edit_btn.pack(side="left")
    
    def create_recent_messages_section(self, parent):
        recent_container = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        recent_container.pack(fill="x", pady=(0, 15))
        
        # Header
        tk.Label(
            recent_container,
            text="Recent Messages",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", padx=20, pady=(15, 10))
        
        # Recent messages
        for message in self.messages_data["recent"]:
            self.create_message_item(recent_container, message)
    
    def create_message_item(self, parent, message):
        message_frame = tk.Frame(
            parent, 
            bg="white",
            cursor="hand2"
        )
        message_frame.pack(fill="x", padx=20, pady=5)
        message_frame.bind("<Button-1>", lambda e: self.open_message(message))
        
        # Blue indicator line for unread
        if message.get("unread", False):
            indicator = tk.Frame(message_frame, bg="#2196F3", width=4)
            indicator.pack(side="left", fill="y", padx=(0, 10))
        else:
            # Spacer for alignment
            spacer = tk.Frame(message_frame, bg="white", width=4)
            spacer.pack(side="left", padx=(0, 10))
        
        # Message content
        content_frame = tk.Frame(message_frame, bg="white")
        content_frame.pack(side="left", fill="x", expand=True)
        content_frame.bind("<Button-1>", lambda e: self.open_message(message))
        
        # Sender and time
        header_frame = tk.Frame(content_frame, bg="white")
        header_frame.pack(fill="x")
        header_frame.bind("<Button-1>", lambda e: self.open_message(message))
        
        sender_label = tk.Label(
            header_frame,
            text=message["sender"],
            font=("Arial", 11, "bold" if message.get("unread", False) else "normal"),
            bg="white",
            fg="#212121"
        )
        sender_label.pack(side="left")
        sender_label.bind("<Button-1>", lambda e: self.open_message(message))
        
        time_label = tk.Label(
            header_frame,
            text=message["time"],
            font=("Arial", 9),
            bg="white",
            fg="#757575"
        )
        time_label.pack(side="right")
        time_label.bind("<Button-1>", lambda e: self.open_message(message))
        
        # Subject
        subject_label = tk.Label(
            content_frame,
            text=message["subject"],
            font=("Arial", 10),
            bg="white",
            fg="#616161",
            anchor="w"
        )
        subject_label.pack(fill="x", pady=(2, 8))
        subject_label.bind("<Button-1>", lambda e: self.open_message(message))
    
    def create_info_banner(self, parent):
        info_frame = tk.Frame(parent, bg="#FFFDE7", relief="solid", borderwidth=1)
        info_frame.pack(fill="x")
        
        # Yellow vertical line
        yellow_line = tk.Frame(info_frame, bg="#FBC02D", width=5)
        yellow_line.pack(side="left", fill="y")
        
        info_content = tk.Frame(info_frame, bg="#FFFDE7")
        info_content.pack(side="left", fill="x", expand=True, padx=15, pady=12)
        
        info_title = tk.Label(
            info_content,
            text="60% inbox reduction:",
            font=("Arial", 10, "bold"),
            bg="#FFFDE7",
            fg="#212121",
            anchor="w"
        )
        info_title.pack(fill="x")
        
        info_text = tk.Label(
            info_content,
            text="AI assistant handles common questions automatically, flagging only items needing personal attention.",
            font=("Arial", 10),
            bg="#FFFDE7",
            fg="#212121",
            anchor="w",
            wraplength=450,
            justify="left"
        )
        info_text.pack(fill="x")
    
    def create_new_message(self):
        def message_callback(message_data, action):
            if action == "send":
                # Add to recent messages
                self.messages_data["recent"].insert(0, {
                    "id": self.message_id_counter,
                    "sender": "You",
                    "subject": f"To: {message_data['recipient']} - {message_data['subject']}",
                    "time": message_data["timestamp"],
                    "unread": False
                })
                self.message_id_counter += 1
            elif action == "save_draft":
                # Add to drafts
                message_data["id"] = self.message_id_counter
                self.messages_data["drafts"].append(message_data)
                self.message_id_counter += 1
            
            # Refresh the display
            self.refresh_content()
        
        MessageComposerDialog(self.root, message_callback, mode="new")
    
    def review_draft(self, draft):
        def message_callback(message_data, action):
            if action == "send":
                # Remove from drafts
                self.messages_data["drafts"] = [
                    d for d in self.messages_data["drafts"] if d["id"] != draft["id"]
                ]
                # Add to recent messages
                self.messages_data["recent"].insert(0, {
                    "id": self.message_id_counter,
                    "sender": "You",
                    "subject": f"To: {message_data['recipient']} - {message_data['subject']}",
                    "time": message_data["timestamp"],
                    "unread": False
                })
                self.message_id_counter += 1
            elif action == "discard":
                # Remove from drafts
                self.messages_data["drafts"] = [
                    d for d in self.messages_data["drafts"] if d["id"] != draft["id"]
                ]
            
            # Refresh the display
            self.refresh_content()
        
        MessageComposerDialog(self.root, message_callback, draft_data=draft, mode="review")
    
    def edit_draft(self, draft):
        def message_callback(message_data, action):
            if action == "send":
                # Remove from drafts
                self.messages_data["drafts"] = [
                    d for d in self.messages_data["drafts"] if d["id"] != draft["id"]
                ]
                # Add to recent messages
                self.messages_data["recent"].insert(0, {
                    "id": self.message_id_counter,
                    "sender": "You",
                    "subject": f"To: {message_data['recipient']} - {message_data['subject']}",
                    "time": message_data["timestamp"],
                    "unread": False
                })
                self.message_id_counter += 1
            elif action == "save_draft":
                # Update the draft
                for i, d in enumerate(self.messages_data["drafts"]):
                    if d["id"] == draft["id"]:
                        message_data["id"] = draft["id"]
                        self.messages_data["drafts"][i] = message_data
                        break
            elif action == "discard":
                # Remove from drafts
                self.messages_data["drafts"] = [
                    d for d in self.messages_data["drafts"] if d["id"] != draft["id"]
                ]
            
            # Refresh the display
            self.refresh_content()
        
        MessageComposerDialog(self.root, message_callback, draft_data=draft, mode="edit")
    
    def refresh_content(self):
        """Refresh the scrollable content area"""
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Recreate sections
        self.create_ai_drafts_section(self.scrollable_frame)
        self.create_recent_messages_section(self.scrollable_frame)
        self.create_info_banner(self.scrollable_frame)
    
    def open_message(self, message):
        # Mark as read
        message["unread"] = False
        messagebox.showinfo("Message", f"From: {message['sender']}\n\n{message['subject']}")
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()


class ClassroomManagementApp:
    """Main application controller"""
    def __init__(self, root):
        self.root = root
        self.root.title("StreamlineEDU - Classroom Management Platform")
        self.root.geometry("1200x700")  # Wider to fit 4 columns
        
        # Create screens
        self.dashboard = DashboardScreen(root, self.show_lesson_planning, self.show_parent_communication)
        self.lesson_planning = LessonPlanningScreen(root, self.show_dashboard)
        self.parent_communication = ParentCommunicationScreen(root, self.show_dashboard)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def show_dashboard(self):
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.dashboard.show()
    
    def show_lesson_planning(self):
        self.dashboard.hide()
        self.parent_communication.hide()
        self.lesson_planning.show()
    
    def show_parent_communication(self):
        self.dashboard.hide()
        self.lesson_planning.hide()
        self.parent_communication.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClassroomManagementApp(root)
    root.mainloop()
