#!/usr/bin/env python3
"""
Rugby Referee Review System
Professional review application based on CRRDF framework

Copyright © 2025 Andrew Clarkson
All Rights Reserved

This application implements the Community Rugby Referee Development Framework (CRRDF).

Licensed under MIT License

Version: 2.0.6-phase5
"""

__version__ = "2.0.6-phase5"
__author__ = "Andrew Clarkson"
__copyright__ = "Copyright © 2025 Andrew Clarkson"
__license__ = "MIT"

# Application Constants
CRRDF_VERSION = "February 2025"

# Common Rugby Game Grades
GAME_GRADES = [
    "Division 1",
    "Southern Premier",
    "Central Premier",
    "Women's Division 1",
    "Premier 1st XV",
    "Division 2",
    "Division 3",
    "U20 Colts",
    "U21 Colts Division 1",
    "U21 Colts Division 2",
    "Women's Division 2",
    "High School",
    "Other"
]

import tkinter as tk
from tkinter import messagebox, filedialog
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    THEME_AVAILABLE = True
except ImportError:
    from tkinter import ttk
    THEME_AVAILABLE = False
    print("Warning: ttkbootstrap not available, using standard theme")

import json
from datetime import datetime
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from typing import Dict, List, Any
import matplotlib
matplotlib.use('TkAgg')  # Use Tk backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# CRRDF Framework Questions Database
CRRDF_QUESTIONS = {
    "technical": {
        "title": "Technical Pillar",
        "questions": [
            {
                "q": "How well did you apply the laws to keep the game safe?",
                "prompts": ["Think about scrum safety", "Tackle height compliance", "Dangerous play management"]
            },
            {
                "q": "Were your decisions based on actual player actions rather than assumptions?",
                "prompts": ["Pre-contest positioning", "Contest observation", "Post-contest management"]
            },
            {
                "q": "How effectively did you apply game innovations (e.g., tackle height, scrum offside)?",
                "prompts": ["Clarity on new laws", "Consistency of application", "Communication to players"]
            }
        ]
    },
    "tactical": {
        "title": "Tactical Pillar",
        "questions": [
            {
                "q": "Did you use tactical awareness in your decision-making?",
                "prompts": ["Impact vs. relevance of infringements", "Pressure and dominance assessment", "Intentional vs. accidental actions"]
            },
            {
                "q": "How appropriate was your advantage application?",
                "prompts": ["Team skill levels considered", "Game flow maintained", "Tactical vs. territorial advantage"]
            },
            {
                "q": "Were your running lines and positioning optimal for decision-making?",
                "prompts": ["Exit points from phases", "Contestable moments coverage", "Adaptation to game shape"]
            },
            {
                "q": "Did you show appropriate empathy based on game context?",
                "prompts": ["Skill level consideration", "Team tactics awareness", "Weather/conditions impact"]
            }
        ]
    },
    "management": {
        "title": "Management Pillar",
        "questions": [
            {
                "q": "Did you recognize and apply the right level of management for this game?",
                "prompts": ["Player temperament assessment", "Law knowledge and compliance levels", "Connection with captains"]
            },
            {
                "q": "How effectively did you manage player safety?",
                "prompts": ["Recognition of dangerous play", "Proactive safety management", "Work with key players"]
            },
            {
                "q": "What range of management strategies did you use?",
                "prompts": ["Captain engagement", "Verbal management balance", "Escalation when needed"]
            },
            {
                "q": "Did you identify and address game trends?",
                "prompts": ["Team tactics recognition", "Appropriate escalation", "Individual player management"]
            }
        ]
    },
    "mental": {
        "title": "Mental Pillar",
        "questions": [
            {
                "q": "How effective was your pre-game preparation?",
                "prompts": ["Mental preparation", "Game plan development", "Kit and logistics organization"]
            },
            {
                "q": "Did you identify and mitigate any 'clutter' affecting performance?",
                "prompts": ["External pressures recognized", "Strategies used to minimize impact", "Focus maintenance"]
            },
            {
                "q": "What key soft skills did you demonstrate?",
                "prompts": ["Fortitude in big moments", "Adaptability to game changes", "Resilience after challenges", "Presence and character"]
            }
        ]
    },
    "physical": {
        "title": "Physical Pillar",
        "questions": [
            {
                "q": "Did you keep up with play throughout the game?",
                "prompts": ["Fitness sufficiency", "Positioning for key moments", "Energy management"]
            }
        ]
    }
}

# GFA Categories with detailed descriptions
GFA_CATEGORIES = {
    "Tackle/Ruck": [
        ("Tackler", "Tackler obligations: release of ball carrier, clear release before playing ball, not sealing off"),
        ("Jackler", "Jackler at breakdown: on feet, clear release, legal entry gate, supporting own weight")
    ],
    "Scrum": [
        ("Stability", "Scrum stability & safety: early engagement, binding, collapse management, player welfare"),
        ("Push Straight", "Scrum law application: 1.5m push, wheel management, offside (feeding halfback)")
    ],
    "LO/Maul": [
        ("Fair Contest in the air", "Lineout contest: straight throw, fair jump, no early movement, safety in the air"),
        ("Legal maul set up", "Maul: legal formation, binding, use it call, obstruction, collapsing")
    ],
    "Space": [
        ("Kicks", "Kicks in general play: 10m offside, 50:22, contestable kicks, chasers, protection of kicker"),
        ("Breakdown/Maul", "Space at breakdown/maul: entry gate, offside lines, clear ruck/maul, quick ball vs contest")
    ],
    "Management": [
        ("Advantage", "Advantage application: territorial vs tactical, team skill consideration, materiality, clear calls"),
        ("Foul Play/Big Moments", "Foul play & pressure moments: cards, penalty tries, TMO, managing tensions, big calls")
    ]
}

RATING_SCALE = {
    1: "Unacceptable - Fails to demonstrate required awareness. Errors significantly impacted the game.",
    2: "Below Standard - Limited awareness. Errors had negative influence on the game.",
    3: "Satisfactory - Adequate level. Minor errors didn't materially affect the game. Meets minimum expectations.",
    4: "Sound - Good awareness and execution. Generally accurate and timely. Contributed positively.",
    5: "Excellent - Consistently high level. Accurate, proactive, adds clear value. Sets best practice example."
}


class PlaceholderEntry(tk.Entry):
    """Entry widget with placeholder text"""
    
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = '#999999'
        self.default_fg_color = kwargs.get('fg', 'black')
        
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        
        self.put_placeholder()
    
    def put_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg_color)
    
    def on_focus_out(self, event):
        if not self.get():
            self.put_placeholder()
    
    def get_value(self):
        """Get the actual value (empty string if only placeholder)"""
        current = self.get()
        return "" if current == self.placeholder else current


class PlaceholderText(tk.Text):
    """Text widget with placeholder text"""
    
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = '#999999'
        self.default_fg_color = kwargs.get('fg', 'black')
        
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        
        self.put_placeholder()
    
    def put_placeholder(self):
        if not self.get("1.0", "end-1c"):
            self.insert("1.0", self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def on_focus_in(self, event):
        if self.get("1.0", "end-1c") == self.placeholder:
            self.delete("1.0", tk.END)
            self.config(fg=self.default_fg_color)
    
    def on_focus_out(self, event):
        if not self.get("1.0", "end-1c"):
            self.put_placeholder()
    
    def get_value(self):
        """Get the actual value (empty string if only placeholder)"""
        current = self.get("1.0", "end-1c")
        return "" if current == self.placeholder else current


class ReviewSession:
    """Stores all review data for a game"""
    
    def __init__(self):
        self.metadata = {
            "game_grade": "",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "result": "",
            "referee": "",
            "coach": "",
            "date_completed": datetime.now().strftime("%Y-%m-%d")
        }
        self.goals = {
            "primary": "",
            "secondary": ""
        }
        self.difficulty = 5  # 1-10 scale
        self.reflections = {
            "goals_met": "",
            "what_went_well": "",
            "biggest_challenge": "",
            "taking_forward": ""
        }
        self.crrdf_reflections = {}
        self.gfa_scores = {}
        self.coach_feedback = ""


class CRRDFReviewApp:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Rugby Referee Review System")
        
        # Set minimum window size
        self.root.minsize(900, 700)
        
        # Start with a good default size
        self.root.geometry("1100x750")
        
        # Center window on screen
        self.center_window()
        
        # Allow window to be resizable
        self.root.resizable(True, True)
        
        self.session = ReviewSession()
        self.current_pillar = None
        self.current_question = 0
        
        # Set up reviews directory
        self.reviews_dir = Path.home() / "Documents" / "RugbyRefereeReviews"
        self.reviews_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up config file
        self.config_file = Path.home() / ".rugby_referee_review_config.json"
        self.config = self.load_config()
        
        # Check if first run
        if self.config.get('first_run', True):
            self.show_welcome_screen()
            return  # Don't continue with normal UI until welcome is done
        
        # Apply modern theme if available
        if THEME_AVAILABLE:
            style = ttk.Style("cosmo")  # Modern, professional theme
        else:
            style = ttk.Style()
            style.theme_use('clam')
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main container
        self.create_widgets()
    
    def get_review_filename(self, referee_name, date):
        """Generate standardized filename for review"""
        # Sanitize filename
        safe_name = "".join(c for c in referee_name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_name:
            safe_name = "Unknown"
        return self.reviews_dir / f"Review_{safe_name}_{date}.json"
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {"first_run": True}
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save config: {e}")
    
    def show_welcome_screen(self):
        """Show first-run welcome and setup screen"""
        # Clear any existing content
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create welcome screen
        welcome = tk.Frame(self.root, bg="white")
        welcome.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(welcome, bg="#1976D2", height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Welcome to", 
                font=("Segoe UI", 14), bg="#1976D2", fg="#E3F2FD").pack(pady=(20, 0))
        tk.Label(header, text="Rugby Referee Review System", 
                font=("Segoe UI", 24, "bold"), bg="#1976D2", fg="white").pack(pady=(5, 20))
        
        # Content
        content = tk.Frame(welcome, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        tk.Label(content, text="Let's personalize your experience", 
                font=("Segoe UI", 16, "bold"), bg="white", fg="#212121").pack(pady=(0, 10))
        
        tk.Label(content, text="This information will be used to auto-fill your review forms.", 
                font=("Segoe UI", 10), bg="white", fg="#757575").pack(pady=(0, 30))
        
        # Name field
        name_frame = tk.Frame(content, bg="white")
        name_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(name_frame, text="Your Full Name:", 
                font=("Segoe UI", 11, "bold"), bg="white", fg="#212121", anchor="w").pack(fill=tk.X, pady=(0, 5))
        tk.Label(name_frame, text="This will auto-fill the 'Referee' field in your reviews", 
                font=("Segoe UI", 9), bg="white", fg="#757575", anchor="w").pack(fill=tk.X, pady=(0, 5))
        
        name_entry = tk.Entry(name_frame, font=("Segoe UI", 12), width=40)
        name_entry.pack(fill=tk.X, pady=5)
        name_entry.focus()
        
        # Coach field
        coach_frame = tk.Frame(content, bg="white")
        coach_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(coach_frame, text="Preferred Coach Name (Optional):", 
                font=("Segoe UI", 11, "bold"), bg="white", fg="#212121", anchor="w").pack(fill=tk.X, pady=(0, 5))
        tk.Label(coach_frame, text="This will auto-fill the 'Coach' field in your reviews", 
                font=("Segoe UI", 9), bg="white", fg="#757575", anchor="w").pack(fill=tk.X, pady=(0, 5))
        
        coach_entry = tk.Entry(coach_frame, font=("Segoe UI", 12), width=40)
        coach_entry.pack(fill=tk.X, pady=5)
        
        # Error label
        error_label = tk.Label(content, text="", font=("Segoe UI", 10), 
                              bg="white", fg="#F44336")
        error_label.pack(pady=10)
        
        def complete_setup():
            """Save settings and continue"""
            name = name_entry.get().strip()
            
            if not name:
                error_label.config(text="Please enter your name")
                return
            
            coach = coach_entry.get().strip()
            
            # Save config
            self.config = {
                "first_run": False,
                "user_name": name,
                "coach_name": coach
            }
            self.save_config()
            
            # Clear welcome screen
            welcome.destroy()
            
            # Initialize normal UI
            if THEME_AVAILABLE:
                style = ttk.Style("cosmo")
            else:
                style = ttk.Style()
                style.theme_use('clam')
            
            self.create_menu_bar()
            self.create_widgets()
        
        # Buttons
        button_frame = tk.Frame(content, bg="white")
        button_frame.pack(pady=30)
        
        tk.Button(button_frame, text="Get Started", command=complete_setup,
                 font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white",
                 padx=40, pady=12, relief=tk.FLAT, cursor="hand2").pack()
        
        # Bind Enter key
        name_entry.bind('<Return>', lambda e: complete_setup())
        coach_entry.bind('<Return>', lambda e: complete_setup())
    
    def save_review_json(self):
        """Save current review to JSON file"""
        try:
            # Compile all review data
            review_data = {
                "version": __version__,
                "saved_at": datetime.now().isoformat(),
                "metadata": self.session.metadata,
                "goals": self.session.goals,
                "difficulty": self.session.difficulty,
                "reflections": self.session.reflections,
                "crrdf_reflections": self.session.crrdf_reflections if hasattr(self.session, 'crrdf_reflections') else {},
                "gfa_scores": self.session.gfa_scores,
                "coach_feedback": self.session.coach_feedback
            }
            
            # Generate filename
            filename = self.get_review_filename(
                self.session.metadata.get('referee', 'Unknown'),
                self.session.metadata.get('date', datetime.now().strftime("%Y-%m-%d"))
            )
            
            # Save to JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(review_data, f, indent=2, ensure_ascii=False)
            
            return filename
        except Exception as e:
            print(f"Failed to save JSON: {e}")
            return None
    
    def load_review_json(self, filename):
        """Load review from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                review_data = json.load(f)
            
            # Load into session
            self.session = ReviewSession()
            self.session.metadata = review_data.get('metadata', {})
            self.session.goals = review_data.get('goals', {})
            self.session.difficulty = review_data.get('difficulty', 5)
            self.session.reflections = review_data.get('reflections', {})
            self.session.crrdf_reflections = review_data.get('crrdf_reflections', {})
            self.session.gfa_scores = review_data.get('gfa_scores', {})
            self.session.coach_feedback = review_data.get('coach_feedback', "")
            
            # Also populate pillar_answers for display
            self.pillar_answers = review_data.get('crrdf_reflections', {}).copy()
            
            return True
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load review:\n{str(e)}")
            return False
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 1100
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Review", command=self.new_review)
        file_menu.add_command(label="Open Review...", command=self.open_review)
        file_menu.add_command(label="Browse All Reviews...", command=self.browse_reviews)
        file_menu.add_separator()
        file_menu.add_command(label="View Analytics", command=self.show_analytics_dashboard)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Personal Info", command=self.show_personal_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_dialog)
    
    def new_review(self):
        """Start a new review"""
        if messagebox.askyesno("New Review", "Start a new review? Any unsaved data will be lost."):
            self.session = ReviewSession()
            self.show_metadata_entry()
    
    def open_review(self):
        """Open an existing review"""
        filename = filedialog.askopenfilename(
            title="Open Review",
            initialdir=self.reviews_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename and self.load_review_json(filename):
            self.clear_content()  # Explicitly clear before loading
            messagebox.showinfo("Success", "Review loaded successfully!")
            self.show_metadata_entry()
    
    def browse_reviews(self):
        """Show review browser dialog"""
        browser = tk.Toplevel(self.root)
        browser.title("Browse Reviews")
        browser.geometry("800x600")
        browser.transient(self.root)
        
        # Center the dialog
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 400
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 300
        browser.geometry(f"800x600+{x}+{y}")
        
        # Header
        header = tk.Frame(browser, bg="#1976D2", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Review History", 
                font=("Segoe UI", 16, "bold"), bg="#1976D2", fg="white").pack(pady=15)
        
        # Main content
        content = tk.Frame(browser, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Search frame
        search_frame = tk.Frame(content, bg="white")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", font=("Segoe UI", 10), bg="white").pack(side=tk.LEFT, padx=(0, 5))
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Segoe UI", 10), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        def update_list(*args):
            populate_list(search_var.get())
        
        search_var.trace_add('write', update_list)
        
        tk.Button(search_frame, text="Refresh", command=lambda: populate_list(search_var.get()),
                 font=("Segoe UI", 9), bg="#E0E0E0", fg="#212121",
                 padx=10, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT)
        
        # Listbox with scrollbar
        list_frame = tk.Frame(content, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(list_frame, font=("Segoe UI", 10), yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Store file paths
        review_files = []
        
        def populate_list(search_term=""):
            """Populate listbox with reviews"""
            nonlocal review_files
            listbox.delete(0, tk.END)
            review_files = []
            
            # Get all JSON files
            try:
                json_files = sorted(self.reviews_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
            except:
                json_files = []
            
            for filepath in json_files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    referee = data.get('metadata', {}).get('referee', 'Unknown')
                    date = data.get('metadata', {}).get('date', 'Unknown')
                    game = data.get('metadata', {}).get('game_grade', 'Unknown')
                    
                    # Apply search filter
                    if search_term:
                        search_lower = search_term.lower()
                        if not (search_lower in referee.lower() or 
                               search_lower in date.lower() or 
                               search_lower in game.lower()):
                            continue
                    
                    display_text = f"{date} - {referee} - {game}"
                    listbox.insert(tk.END, display_text)
                    review_files.append(filepath)
                except:
                    pass
            
            if listbox.size() == 0:
                listbox.insert(tk.END, "No reviews found")
        
        def load_selected():
            """Load selected review"""
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a review to load")
                return
            
            idx = selection[0]
            if idx < len(review_files):
                if self.load_review_json(review_files[idx]):
                    browser.destroy()
                    self.clear_content()  # Explicitly clear before loading
                    messagebox.showinfo("Success", "Review loaded successfully!")
                    self.show_metadata_entry()
        
        def delete_selected():
            """Delete selected review"""
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a review to delete")
                return
            
            idx = selection[0]
            if idx < len(review_files):
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this review?"):
                    try:
                        review_files[idx].unlink()
                        populate_list(search_var.get())
                        messagebox.showinfo("Deleted", "Review deleted successfully")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete:\n{str(e)}")
        
        # Buttons
        button_frame = tk.Frame(content, bg="white")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(button_frame, text="Load", command=load_selected,
                 font=("Segoe UI", 10, "bold"), bg="#1976D2", fg="white",
                 padx=20, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(button_frame, text="Delete", command=delete_selected,
                 font=("Segoe UI", 10), bg="#F44336", fg="white",
                 padx=20, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Close", command=browser.destroy,
                 font=("Segoe UI", 10), bg="#E0E0E0", fg="#212121",
                 padx=20, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.RIGHT)
        
        # Populate initially
        populate_list()
        
        # Double-click to load
        listbox.bind('<Double-Button-1>', lambda e: load_selected())
    
    def show_analytics_dashboard(self):
        """Show analytics dashboard with charts and statistics"""
        # Load all reviews
        reviews = []
        try:
            json_files = sorted(self.reviews_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
        except:
            json_files = []
        
        for filepath in json_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    reviews.append(data)
            except:
                pass
        
        if len(reviews) == 0:
            messagebox.showinfo("No Data", "No reviews found. Complete some reviews first!")
            return
        
        # Create dashboard window
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Analytics Dashboard")
        dashboard.geometry("1200x800")
        dashboard.transient(self.root)
        
        # Center the dialog
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 600
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 400
        dashboard.geometry(f"1200x800+{x}+{y}")
        
        # Header
        header = tk.Frame(dashboard, bg="#1976D2", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="📊 Performance Analytics", 
                font=("Segoe UI", 18, "bold"), bg="#1976D2", fg="white").pack(pady=15)
        
        # Create scrollable content
        canvas = tk.Canvas(dashboard, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(dashboard, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg="white")
        
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=1150)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Statistics Section
        stats_frame = tk.Frame(content, bg="white")
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(stats_frame, text="Overview Statistics", 
                font=("Segoe UI", 16, "bold"), bg="white", fg="#1976D2").pack(anchor="w", pady=(0, 10))
        
        # Calculate stats
        total_reviews = len(reviews)
        dates = [r.get('metadata', {}).get('date', '') for r in reviews if r.get('metadata', {}).get('date')]
        date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
        
        grades = [r.get('metadata', {}).get('game_grade', '') for r in reviews if r.get('metadata', {}).get('game_grade')]
        most_common = max(set(grades), key=grades.count) if grades else "N/A"
        
        avg_difficulty = sum([r.get('difficulty', 5) for r in reviews]) / len(reviews) if reviews else 0
        
        # Display stats in grid
        stats_grid = tk.Frame(stats_frame, bg="white")
        stats_grid.pack(fill=tk.X)
        
        stats_data = [
            ("Total Reviews", str(total_reviews)),
            ("Date Range", date_range),
            ("Most Common Grade", most_common),
            ("Avg Difficulty", f"{avg_difficulty:.1f}/10")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            stat_box = tk.Frame(stats_grid, bg="#E3F2FD", relief=tk.RAISED, bd=1)
            stat_box.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            stats_grid.columnconfigure(i, weight=1)
            
            tk.Label(stat_box, text=label, font=("Segoe UI", 9), 
                    bg="#E3F2FD", fg="#757575").pack(pady=(10, 5))
            tk.Label(stat_box, text=value, font=("Segoe UI", 14, "bold"), 
                    bg="#E3F2FD", fg="#1976D2").pack(pady=(0, 10))
        
        # GFA Trends Chart
        chart_frame = tk.Frame(content, bg="white")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(chart_frame, text="GFA Score Trends", 
                font=("Segoe UI", 16, "bold"), bg="white", fg="#1976D2").pack(anchor="w", pady=(0, 10))
        
        # Calculate average GFA scores per review
        review_dates = []
        avg_scores = []
        
        for review in reviews:
            date = review.get('metadata', {}).get('date', '')
            if not date:
                continue
            
            gfa_scores = review.get('gfa_scores', {})
            if gfa_scores:
                scores = [v for v in gfa_scores.values() if isinstance(v, (int, float))]
                if scores:
                    review_dates.append(date)
                    avg_scores.append(sum(scores) / len(scores))
        
        if review_dates and avg_scores:
            # Create matplotlib figure
            fig = Figure(figsize=(10, 4), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            ax.plot(range(len(avg_scores)), avg_scores, marker='o', linewidth=2, 
                   markersize=8, color='#1976D2', label='Average GFA Score')
            ax.axhline(y=3, color='#FF9800', linestyle='--', label='Satisfactory (3.0)', alpha=0.7)
            ax.axhline(y=4, color='#4CAF50', linestyle='--', label='Sound (4.0)', alpha=0.7)
            
            ax.set_xlabel('Review Number', fontsize=11)
            ax.set_ylabel('Average Score', fontsize=11)
            ax.set_ylim(1, 5)
            ax.grid(True, alpha=0.3)
            ax.legend(loc='lower right')
            
            # Embed in tkinter
            canvas_widget = FigureCanvasTkAgg(fig, chart_frame)
            canvas_widget.draw()
            canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            tk.Label(chart_frame, text="Not enough GFA data to display chart", 
                    font=("Segoe UI", 11), bg="white", fg="#757575").pack(pady=20)
        
        # Recent Reviews Table
        table_frame = tk.Frame(content, bg="white")
        table_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(table_frame, text="Recent Reviews", 
                font=("Segoe UI", 16, "bold"), bg="white", fg="#1976D2").pack(anchor="w", pady=(0, 10))
        
        # Create table
        table = tk.Frame(table_frame, bg="white")
        table.pack(fill=tk.X)
        
        headers = ["Date", "Game Grade", "Difficulty", "Avg GFA Score"]
        for i, header in enumerate(headers):
            tk.Label(table, text=header, font=("Segoe UI", 10, "bold"), 
                    bg="#1976D2", fg="white", padx=10, pady=8).grid(row=0, column=i, sticky="ew")
        
        # Show last 10 reviews
        for idx, review in enumerate(reversed(reviews[-10:])):
            date = review.get('metadata', {}).get('date', 'N/A')
            grade = review.get('metadata', {}).get('game_grade', 'N/A')
            diff = review.get('difficulty', 'N/A')
            
            gfa_scores = review.get('gfa_scores', {})
            if gfa_scores:
                scores = [v for v in gfa_scores.values() if isinstance(v, (int, float))]
                avg_gfa = f"{sum(scores)/len(scores):.1f}" if scores else "N/A"
            else:
                avg_gfa = "N/A"
            
            bg_color = "#F5F5F5" if idx % 2 == 0 else "white"
            
            tk.Label(table, text=date, font=("Segoe UI", 9), 
                    bg=bg_color, padx=10, pady=6).grid(row=idx+1, column=0, sticky="ew")
            tk.Label(table, text=grade, font=("Segoe UI", 9), 
                    bg=bg_color, padx=10, pady=6).grid(row=idx+1, column=1, sticky="ew")
            tk.Label(table, text=str(diff), font=("Segoe UI", 9), 
                    bg=bg_color, padx=10, pady=6).grid(row=idx+1, column=2, sticky="ew")
            tk.Label(table, text=avg_gfa, font=("Segoe UI", 9), 
                    bg=bg_color, padx=10, pady=6).grid(row=idx+1, column=3, sticky="ew")
        
        # Close button
        button_frame = tk.Frame(content, bg="white")
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(button_frame, text="Close", command=dashboard.destroy,
                 font=("Segoe UI", 10, "bold"), bg="#1976D2", fg="white",
                 padx=30, pady=10, relief=tk.FLAT, cursor="hand2").pack()
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def show_about_dialog(self):
        """Show the About dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("500x400")
        about_window.resizable(False, False)
        
        # Center the dialog
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Calculate position
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
        about_window.geometry(f"500x400+{x}+{y}")
        
        # Header with color
        header = tk.Frame(about_window, bg="#1976D2", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Rugby Referee Review System", 
                font=("Segoe UI", 18, "bold"), bg="#1976D2", fg="white").pack(pady=20)
        
        # Content
        content = tk.Frame(about_window, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(content, text=f"Version {__version__}", 
                font=("Segoe UI", 11), bg="white", fg="#757575").pack(pady=5)
        
        tk.Label(content, text="", bg="white").pack(pady=5)  # Spacer
        
        tk.Label(content, text="Copyright © 2025 Andrew Clarkson", 
                font=("Segoe UI", 11, "bold"), bg="white", fg="#212121").pack(pady=5)
        
        tk.Label(content, text="All Rights Reserved", 
                font=("Segoe UI", 9), bg="white", fg="#757575").pack()
        
        tk.Label(content, text="", bg="white").pack(pady=10)  # Spacer
        
        tk.Label(content, text="Implements the Community Rugby Referee\nDevelopment Framework (CRRDF)", 
                font=("Segoe UI", 10), bg="white", fg="#212121", justify=tk.CENTER).pack(pady=5)
        
        tk.Label(content, text=f"CRRDF Framework: {CRRDF_VERSION}", 
                font=("Segoe UI", 9), bg="white", fg="#757575").pack(pady=2)
        
        tk.Label(content, text="", bg="white").pack(pady=10)  # Spacer
        
        tk.Label(content, text="Licensed under MIT License", 
                font=("Segoe UI", 9), bg="white", fg="#757575").pack()
        
        # Close button
        tk.Button(content, text="Close", command=about_window.destroy,
                 font=("Segoe UI", 10, "bold"), bg="#1976D2", fg="white",
                 padx=30, pady=8, relief=tk.FLAT, cursor="hand2").pack(pady=20)
    
    def show_personal_settings(self):
        """Show personal settings dialog"""
        settings = tk.Toplevel(self.root)
        settings.title("Personal Settings")
        settings.geometry("550x400")
        settings.resizable(False, False)
        
        # Center the dialog
        settings.transient(self.root)
        settings.grab_set()
        
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 275
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
        settings.geometry(f"550x400+{x}+{y}")
        
        # Header
        header = tk.Frame(settings, bg="#1976D2", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Personal Information", 
                font=("Segoe UI", 16, "bold"), bg="#1976D2", fg="white").pack(pady=15)
        
        # Content
        content = tk.Frame(settings, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        tk.Label(content, text="This information auto-fills your review forms", 
                font=("Segoe UI", 9), bg="white", fg="#757575").pack(pady=(0, 20))
        
        # Name field
        tk.Label(content, text="Your Full Name:", 
                font=("Segoe UI", 10, "bold"), bg="white", fg="#212121", anchor="w").pack(fill=tk.X, pady=(0, 5))
        
        name_entry = tk.Entry(content, font=("Segoe UI", 11), width=40, relief=tk.SOLID, bd=1)
        name_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        name_entry.insert(0, self.config.get("user_name", ""))
        
        # Coach field
        tk.Label(content, text="Preferred Coach Name (Optional):", 
                font=("Segoe UI", 10, "bold"), bg="white", fg="#212121", anchor="w").pack(fill=tk.X, pady=(0, 5))
        
        coach_entry = tk.Entry(content, font=("Segoe UI", 11), width=40, relief=tk.SOLID, bd=1)
        coach_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        coach_entry.insert(0, self.config.get("coach_name", ""))
        
        # Status label
        status_label = tk.Label(content, text="", font=("Segoe UI", 10), bg="white", height=2)
        status_label.pack(pady=10)
        
        def save_settings():
            """Save updated settings"""
            name = name_entry.get().strip()
            
            if not name:
                status_label.config(text="⚠ Name cannot be empty", fg="#F44336")
                return
            
            coach = coach_entry.get().strip()
            
            self.config["user_name"] = name
            self.config["coach_name"] = coach
            self.save_config()
            
            status_label.config(text="✓ Settings saved successfully!", fg="#4CAF50")
            self.root.after(1500, settings.destroy)
        
        # Buttons
        button_frame = tk.Frame(content, bg="white")
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Save Changes", command=save_settings,
                 font=("Segoe UI", 10, "bold"), bg="#4CAF50", fg="white",
                 padx=30, pady=10, relief=tk.FLAT, cursor="hand2",
                 activebackground="#45a049").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Cancel", command=settings.destroy,
                 font=("Segoe UI", 10), bg="#E0E0E0", fg="#212121",
                 padx=30, pady=10, relief=tk.FLAT, cursor="hand2",
                 activebackground="#d0d0d0").pack(side=tk.LEFT, padx=5)
    
    def create_widgets(self):
        """Create the main UI"""
        # Header with modern color
        header = tk.Frame(self.root, bg="#1976D2", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)  # Maintain fixed height
        
        title = tk.Label(header, text="Rugby Referee Review System", 
                        font=("Segoe UI", 18, "bold"), bg="#1976D2", fg="white")
        title.pack(pady=(15, 5))
        
        # Subtitle with copyright
        subtitle = tk.Label(header, text="Based on CRRDF Framework  •  © 2025 Andrew Clarkson", 
                           font=("Segoe UI", 9), bg="#1976D2", fg="#E3F2FD")
        subtitle.pack()
        
        # Main content area
        self.content = tk.Frame(self.root, bg="#FAFAFA")
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Start with metadata entry
        self.show_metadata_entry()
        
    def show_metadata_entry(self):
        """Game metadata entry screen"""
        self.clear_content()
        
        # Create scrollable canvas
        canvas = tk.Canvas(self.content, bg="#FAFAFA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FAFAFA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1050)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        frame = scrollable_frame
        
        tk.Label(frame, text="Game Information", font=("Segoe UI", 16, "bold"),
                bg="#FAFAFA", fg="#212121").pack(pady=10)
        
        # Input fields
        self.metadata_entries = {}
        
        # Game & Grade - Dropdown
        container = tk.Frame(frame, bg="#FAFAFA")
        container.pack(fill=tk.X, pady=5, padx=20)
        tk.Label(container, text="Game & Grade:", width=15, anchor="w",
                bg="#FAFAFA", font=("Segoe UI", 10, "bold"), fg="#212121").pack(side=tk.LEFT)
        
        grade_var = tk.StringVar(value=self.session.metadata.get('game_grade', ''))
        grade_combo = ttk.Combobox(container, textvariable=grade_var, values=GAME_GRADES, 
                                   font=("Segoe UI", 10), width=38, state='readonly')
        grade_combo.pack(side=tk.LEFT, padx=5)
        if not self.session.metadata.get('game_grade'):
            grade_combo.set('Select grade...')
        
        # Create a wrapper to match PlaceholderEntry interface
        class ComboWrapper:
            def __init__(self, combo, var):
                self.combo = combo
                self.var = var
            def get_value(self):
                val = self.var.get()
                return "" if val == "Select grade..." else val
        
        self.metadata_entries['game_grade'] = ComboWrapper(grade_combo, grade_var)
        
        # Date - Manual entry with format hint
        container = tk.Frame(frame, bg="#FAFAFA")
        container.pack(fill=tk.X, pady=5, padx=20)
        tk.Label(container, text="Date:", width=15, anchor="w",
                bg="#FAFAFA", font=("Segoe UI", 10, "bold"), fg="#212121").pack(side=tk.LEFT)
        
        # Parse existing date or use today
        date_value = self.session.metadata.get('date', datetime.now().strftime("%Y-%m-%d"))
        
        date_entry = PlaceholderEntry(container, placeholder="YYYY-MM-DD", width=40, font=("Segoe UI", 10))
        date_entry.pack(side=tk.LEFT, padx=5)
        
        # Set default value
        if date_value:
            date_entry.delete(0, tk.END)
            date_entry.insert(0, date_value)
            date_entry.config(fg=date_entry.default_fg_color)
        
        # Add "Today" button
        def set_today():
            date_entry.delete(0, tk.END)
            date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            date_entry.config(fg=date_entry.default_fg_color)
        
        tk.Button(container, text="Today", command=set_today,
                 font=("Segoe UI", 9), bg="#E0E0E0", fg="#212121",
                 padx=10, pady=4, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        self.metadata_entries['date'] = date_entry
        
        # Rest of fields - Text entries
        other_fields = [
            ("Result:", "result", "e.g., Home 24-17 Away"),
            ("Referee:", "referee", "Your name"),
            ("Coach:", "coach", "Coach name (optional)")
        ]
        
        for label, key, placeholder in other_fields:
            container = tk.Frame(frame, bg="#FAFAFA")
            container.pack(fill=tk.X, pady=5, padx=20)
            
            tk.Label(container, text=label, width=15, anchor="w",
                    bg="#FAFAFA", font=("Segoe UI", 10, "bold"), fg="#212121").pack(side=tk.LEFT)
            
            entry = PlaceholderEntry(container, placeholder=placeholder, width=40, font=("Segoe UI", 10))
            entry.pack(side=tk.LEFT, padx=5)
            self.metadata_entries[key] = entry
            
            # Populate with loaded data if it exists
            if self.session.metadata.get(key):
                entry.delete(0, tk.END)
                entry.insert(0, self.session.metadata[key])
                entry.config(fg=entry.default_fg_color)
            # Otherwise auto-fill from config for new reviews
            elif key == "referee" and self.config.get("user_name"):
                entry.delete(0, tk.END)
                entry.insert(0, self.config.get("user_name"))
                entry.config(fg=entry.default_fg_color)
            elif key == "coach" and self.config.get("coach_name"):
                entry.delete(0, tk.END)
                entry.insert(0, self.config.get("coach_name"))
                entry.config(fg=entry.default_fg_color)
        
        # Goals section
        tk.Label(frame, text="\nMatch Goals", font=("Segoe UI", 14, "bold"),
                bg="#FAFAFA", fg="#212121").pack(pady=10)
        
        tk.Label(frame, text="Primary Goal:", anchor="w", bg="#FAFAFA",
                font=("Segoe UI", 10, "bold"), fg="#212121").pack(fill=tk.X, padx=20)
        self.primary_goal = PlaceholderText(frame, placeholder="What is your main focus for this game? e.g., 'Improve accuracy in jackler decisions at breakdown'", 
                                           height=2, width=60, font=("Segoe UI", 10), wrap=tk.WORD)
        self.primary_goal.pack(padx=20, pady=5)
        
        # Populate with loaded data
        if self.session.goals.get('primary'):
            self.primary_goal.delete("1.0", tk.END)
            self.primary_goal.insert("1.0", self.session.goals['primary'])
            self.primary_goal.config(fg=self.primary_goal.default_fg_color)
        
        tk.Label(frame, text="Secondary Goal:", anchor="w", bg="#FAFAFA",
                font=("Segoe UI", 10, "bold"), fg="#212121").pack(fill=tk.X, padx=20)
        self.secondary_goal = PlaceholderText(frame, placeholder="Your secondary focus area? e.g., 'Better positioning at scrum time'", 
                                             height=2, width=60, font=("Segoe UI", 10), wrap=tk.WORD)
        self.secondary_goal.pack(padx=20, pady=5)
        
        # Populate with loaded data
        if self.session.goals.get('secondary'):
            self.secondary_goal.delete("1.0", tk.END)
            self.secondary_goal.insert("1.0", self.session.goals['secondary'])
            self.secondary_goal.config(fg=self.secondary_goal.default_fg_color)
        
        # Difficulty scale
        tk.Label(frame, text="\nGame Difficulty (1=Easy, 10=Very Hard):",
                bg="#FAFAFA", font=("Segoe UI", 10, "bold"), fg="#212121").pack(pady=10)
        
        self.difficulty_var = tk.IntVar(value=self.session.difficulty)
        
        # Display current value
        difficulty_value_label = tk.Label(frame, text=f"Current: {self.session.difficulty}", 
                                         font=("Segoe UI", 10), bg="#FAFAFA", fg="#1976D2")
        difficulty_value_label.pack()
        
        def update_difficulty_label(val):
            difficulty_value_label.config(text=f"Current: {val}")
        
        difficulty_scale = tk.Scale(frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                   variable=self.difficulty_var, length=300, 
                                   bg="#FAFAFA", highlightthickness=0,
                                   command=update_difficulty_label)
        difficulty_scale.pack()
        
        # Navigation with modern styling
        nav = tk.Frame(frame, bg="#FAFAFA")
        nav.pack(pady=20)
        
        tk.Button(nav, text="Next: Self Reflection", command=self.show_self_reflection,
                 font=("Segoe UI", 11, "bold"), bg="#00796B", fg="white",
                 padx=20, pady=10, relief=tk.FLAT, cursor="hand2").pack()
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def show_self_reflection(self):
        """Self reflection questions"""
        # Save metadata
        for key, entry in self.metadata_entries.items():
            self.session.metadata[key] = entry.get_value()
        self.session.goals["primary"] = self.primary_goal.get_value()
        self.session.goals["secondary"] = self.secondary_goal.get_value()
        self.session.difficulty = self.difficulty_var.get()
        
        self.clear_content()
        
        # Create scrollable canvas
        canvas = tk.Canvas(self.content, bg="#FAFAFA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FAFAFA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1050)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        frame = scrollable_frame
        
        tk.Label(frame, text="Self Reflection", font=("Segoe UI", 16, "bold"),
                bg="#FAFAFA", fg="#212121").pack(pady=10)
        
        questions = [
            ("Did I meet my goals - why or why not? Give examples:", "goals_met", 
             "Think about specific moments... e.g., 'Primary goal met - identified 8/10 jackler situations correctly. Secondary goal partly met - positioning at scrums good in first half but...'"),
            ("What areas went well and why? (relate to GFAs if possible):", "what_went_well",
             "Be specific... e.g., 'Tackle area management strong - clear communication on tackler release. Called advantage well when Blue under pressure in 34th min...'"),
            ("What was the biggest challenge? What would/could I do differently?:", "biggest_challenge",
             "Describe the challenge and your solution... e.g., 'Breakdown became messy in final 20 mins. Next time I'll be more proactive with warnings when I see the trend starting...'"),
            ("What am I taking into my next game?:", "taking_forward",
             "Your action points... e.g., 'Work on scrum positioning - stay wider to see both props. Keep using advantage effectively as today showed it helps game flow...'")
        ]
        
        self.reflection_entries = {}
        
        for question, key, placeholder in questions:
            tk.Label(frame, text=question, anchor="w", bg="#FAFAFA",
                    font=("Segoe UI", 10, "bold"), fg="#212121").pack(fill=tk.X, padx=20, pady=(10, 5))
            
            text = PlaceholderText(frame, placeholder=placeholder, height=4, width=70, 
                                  font=("Segoe UI", 10), wrap=tk.WORD)
            text.pack(padx=20, pady=5)
            self.reflection_entries[key] = text
            
            # Populate with loaded data
            if self.session.reflections.get(key):
                text.delete("1.0", tk.END)
                text.insert("1.0", self.session.reflections[key])
                text.config(fg=text.default_fg_color)
        
        # Navigation
        nav = tk.Frame(frame, bg="#FAFAFA")
        nav.pack(pady=20)
        
        tk.Button(nav, text="← Back", command=self.show_metadata_entry,
                 font=("Segoe UI", 10), bg="#E0E0E0", fg="#212121",
                 padx=15, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(nav, text="Next: CRRDF Deep Dive →", command=self.start_crrdf_questions,
                 font=("Segoe UI", 11, "bold"), bg="#00796B", fg="white",
                 padx=20, pady=10, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def start_crrdf_questions(self):
        """Begin CRRDF pillar-by-pillar questions"""
        # Save reflections
        for key, text_widget in self.reflection_entries.items():
            self.session.reflections[key] = text_widget.get_value()
        
        # Start with technical pillar
        self.pillars = list(CRRDF_QUESTIONS.keys())
        self.current_pillar_index = 0
        self.show_pillar_intro()
    
    def show_pillar_intro(self):
        """Show introduction to current pillar"""
        if self.current_pillar_index >= len(self.pillars):
            # All pillars complete, move to GFA scoring
            self.show_gfa_scoring()
            return
        
        pillar_name = self.pillars[self.current_pillar_index]
        pillar_data = CRRDF_QUESTIONS[pillar_name]
        
        self.clear_content()
        
        frame = tk.Frame(self.content, bg="#FAFAFA")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Pillar title
        tk.Label(frame, text=f"CRRDF: {pillar_data['title']}", 
                font=("Segoe UI", 18, "bold"), bg="#FAFAFA", fg="#1976D2").pack(pady=20)
        
        tk.Label(frame, text=f"This section has {len(pillar_data['questions'])} question(s).",
                font=("Segoe UI", 11), bg="#FAFAFA", fg="#757575").pack(pady=10)
        
        tk.Label(frame, text="Each question includes prompts to help you reflect deeply.\nBe specific with examples and time stamps where possible.",
                font=("Segoe UI", 10), bg="#FAFAFA", fg="#757575", justify=tk.CENTER).pack(pady=10)
        
        # Navigation
        nav = tk.Frame(frame, bg="#FAFAFA")
        nav.pack(pady=30)
        
        if self.current_pillar_index > 0:
            tk.Button(nav, text="← Back", command=self.previous_pillar,
                     font=("Segoe UI", 10), bg="#E0E0E0", fg="#212121",
                     padx=15, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(nav, text="Start Questions →", 
                 command=lambda: self.show_pillar_question(pillar_name, 0),
                 font=("Segoe UI", 11, "bold"), bg="#00796B", fg="white",
                 padx=20, pady=10, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
    
    def show_pillar_question(self, pillar_name, question_index):
        """Show a specific question from a pillar"""
        pillar_data = CRRDF_QUESTIONS[pillar_name]
        
        if question_index >= len(pillar_data['questions']):
            # Move to next pillar
            self.current_pillar_index += 1
            self.show_pillar_intro()
            return
        
        question_data = pillar_data['questions'][question_index]
        
        self.clear_content()
        
        frame = tk.Frame(self.content, bg="#FAFAFA")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress indicator
        progress_text = f"{pillar_data['title']} - Question {question_index + 1} of {len(pillar_data['questions'])}"
        tk.Label(frame, text=progress_text, font=("Segoe UI", 10), 
                bg="#FAFAFA", fg="#757575").pack(pady=5)
        
        # Question
        tk.Label(frame, text=question_data['q'], font=("Segoe UI", 13, "bold"),
                bg="#FAFAFA", fg="#212121", wraplength=800, justify=tk.LEFT).pack(pady=15, padx=20)
        
        # Prompts
        tk.Label(frame, text="Think about:", font=("Segoe UI", 10, "bold"),
                bg="#FAFAFA", fg="#00796B").pack(anchor=tk.W, padx=20)
        
        for prompt in question_data['prompts']:
            prompt_frame = tk.Frame(frame, bg="#FAFAFA")
            prompt_frame.pack(anchor=tk.W, padx=40, pady=2)
            tk.Label(prompt_frame, text="•", font=("Segoe UI", 10),
                    bg="#FAFAFA", fg="#00796B").pack(side=tk.LEFT)
            tk.Label(prompt_frame, text=prompt, font=("Segoe UI", 10),
                    bg="#FAFAFA", fg="#757575").pack(side=tk.LEFT, padx=5)
        
        # Answer area
        tk.Label(frame, text="\nYour Response:", font=("Segoe UI", 10, "bold"),
                bg="#FAFAFA", fg="#212121").pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        # Get or create text widget for this question
        key = f"{pillar_name}_{question_index}"
        if not hasattr(self, 'pillar_answers'):
            self.pillar_answers = {}
        
        text = PlaceholderText(frame, placeholder="Be specific with examples, include time stamps where relevant...",
                              height=6, width=80, font=("Segoe UI", 10), wrap=tk.WORD)
        text.pack(padx=20, pady=5)
        
        # Restore previous answer if it exists
        if key in self.pillar_answers:
            text.delete("1.0", tk.END)
            text.insert("1.0", self.pillar_answers[key])
        
        self.current_answer_widget = text
        self.current_answer_key = key
        
        # Navigation
        nav = tk.Frame(frame, bg="#FAFAFA")
        nav.pack(pady=20)
        
        if question_index > 0:
            tk.Button(nav, text="← Previous", 
                     command=lambda: [self.save_current_answer(), 
                                    self.show_pillar_question(pillar_name, question_index - 1)],
                     font=("Segoe UI", 10), bg="#E0E0E0", fg="#212121",
                     padx=15, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(nav, text="Next →" if question_index < len(pillar_data['questions']) - 1 else "Complete Pillar →",
                 command=lambda: [self.save_current_answer(), 
                                self.show_pillar_question(pillar_name, question_index + 1)],
                 font=("Segoe UI", 11, "bold"), bg="#00796B", fg="white",
                 padx=20, pady=10, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
    
    def save_current_answer(self):
        """Save the current answer"""
        if hasattr(self, 'current_answer_widget') and hasattr(self, 'current_answer_key'):
            answer = self.current_answer_widget.get_value()
            self.pillar_answers[self.current_answer_key] = answer
            
            # Also save to session
            if not hasattr(self.session, 'crrdf_reflections'):
                self.session.crrdf_reflections = {}
            self.session.crrdf_reflections[self.current_answer_key] = answer
    
    def previous_pillar(self):
        """Go back to previous pillar"""
        if self.current_pillar_index > 0:
            self.current_pillar_index -= 1
            self.show_pillar_intro()
    
    def show_gfa_scoring(self):
        """GFA scoring interface"""
        self.clear_content()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.content, bg="#FAFAFA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FAFAFA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        tk.Label(scrollable_frame, text="Game Focus Area Scoring", 
                font=("Segoe UI", 18, "bold"), bg="#FAFAFA", fg="#1976D2").pack(pady=15)
        
        tk.Label(scrollable_frame, text="Rate your performance in each focus area (1-5 scale)",
                font=("Segoe UI", 11), bg="#FAFAFA", fg="#757575").pack(pady=5)
        
        # Rating scale reference
        scale_frame = tk.Frame(scrollable_frame, bg="#E3F2FD", relief=tk.RIDGE, bd=1)
        scale_frame.pack(pady=15, padx=20, fill=tk.X)
        
        tk.Label(scale_frame, text="Rating Scale Reference:", font=("Segoe UI", 10, "bold"),
                bg="#E3F2FD", fg="#1976D2").pack(pady=5)
        
        for score, description in RATING_SCALE.items():
            tk.Label(scale_frame, text=f"{score} - {description}", 
                    font=("Segoe UI", 9), bg="#E3F2FD", fg="#212121",
                    wraplength=700, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=2)
        
        # GFA Categories
        self.gfa_vars = {}
        
        for category, aspects in GFA_CATEGORIES.items():
            # Category header
            cat_frame = tk.Frame(scrollable_frame, bg="#FFFFFF", relief=tk.RIDGE, bd=1)
            cat_frame.pack(pady=10, padx=20, fill=tk.X)
            
            tk.Label(cat_frame, text=category, font=("Segoe UI", 12, "bold"),
                    bg="#00796B", fg="white").pack(fill=tk.X, pady=5)
            
            for aspect_name, description in aspects:
                aspect_frame = tk.Frame(cat_frame, bg="#FFFFFF")
                aspect_frame.pack(fill=tk.X, padx=15, pady=8)
                
                # Aspect name and description
                label_frame = tk.Frame(aspect_frame, bg="#FFFFFF")
                label_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                tk.Label(label_frame, text=aspect_name, font=("Segoe UI", 10, "bold"),
                        bg="#FFFFFF", fg="#212121", anchor="w").pack(fill=tk.X)
                tk.Label(label_frame, text=description, font=("Segoe UI", 9),
                        bg="#FFFFFF", fg="#757575", wraplength=500, 
                        justify=tk.LEFT, anchor="w").pack(fill=tk.X)
                
                # Rating scale
                rating_frame = tk.Frame(aspect_frame, bg="#FFFFFF")
                rating_frame.pack(side=tk.RIGHT)
                
                var = tk.IntVar(value=3)
                self.gfa_vars[f"{category}_{aspect_name}"] = var
                
                for i in range(1, 6):
                    tk.Radiobutton(rating_frame, text=str(i), variable=var, value=i,
                                  bg="#FFFFFF", font=("Segoe UI", 9),
                                  selectcolor="#4CAF50").pack(side=tk.LEFT, padx=3)
        
        # Navigation
        nav = tk.Frame(scrollable_frame, bg="#FAFAFA")
        nav.pack(pady=20)
        
        tk.Button(nav, text="← Back to CRRDF", command=self.back_to_last_pillar,
                 font=("Segoe UI", 10), bg="#E0E0E0", fg="#212121",
                 padx=15, pady=8, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(nav, text="Save & Export", command=self.export_to_excel,
                 font=("Segoe UI", 11, "bold"), bg="#4CAF50", fg="white",
                 padx=20, pady=10, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def back_to_last_pillar(self):
        """Return to the last pillar"""
        self.current_pillar_index = len(self.pillars) - 1
        pillar_name = self.pillars[self.current_pillar_index]
        last_q = len(CRRDF_QUESTIONS[pillar_name]['questions']) - 1
        self.show_pillar_question(pillar_name, last_q)
    
    def export_to_excel(self):
        """Export review to Excel file"""
        # Save GFA scores
        for key, var in self.gfa_vars.items():
            self.session.gfa_scores[key] = var.get()
        
        # Auto-save JSON first
        json_filename = self.save_review_json()
        
        # Ask for Excel save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"Review_{self.session.metadata['referee']}_{self.session.metadata['date']}.xlsx"
        )
        
        if not filename:
            # Still saved JSON even if they cancel Excel
            if json_filename:
                messagebox.showinfo("Saved", f"Review saved to:\n{json_filename}")
            return
        
        try:
            self._create_excel_export(filename)
            if json_filename:
                messagebox.showinfo("Success", f"Review exported successfully!\n\nExcel: {filename}\nJSON: {json_filename}")
            else:
                messagebox.showinfo("Success", f"Review exported successfully to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
    
    def _create_excel_export(self, filename):
        """Create the Excel workbook"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Referee Review"
        
        # Styles
        header_font = Font(bold=True, size=14, color="FFFFFF")
        header_fill = PatternFill(start_color="1976D2", end_color="1976D2", fill_type="solid")
        subheader_font = Font(bold=True, size=12)
        subheader_fill = PatternFill(start_color="E3F2FD", end_color="E3F2FD", fill_type="solid")
        
        border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )
        
        row = 1
        
        # Title
        ws.merge_cells(f'A{row}:G{row}')
        cell = ws.cell(row, 1, "Rugby Referee Review")
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
        row += 1
        
        # Copyright
        ws.merge_cells(f'A{row}:G{row}')
        cell = ws.cell(row, 1, f"Based on CRRDF Framework  •  © 2025 Andrew Clarkson")
        cell.font = Font(size=9, italic=True)
        cell.alignment = Alignment(horizontal='center')
        row += 2
        
        # Metadata
        ws.cell(row, 1, "Game Information").font = subheader_font
        ws.cell(row, 1).fill = subheader_fill
        row += 1
        
        for key, label in [("game_grade", "Game & Grade:"), ("date", "Date:"), 
                           ("result", "Result:"), ("referee", "Referee:"), ("coach", "Coach:")]:
            ws.cell(row, 1, label).font = Font(bold=True)
            ws.cell(row, 2, self.session.metadata.get(key, ""))
            row += 1
        
        row += 1
        ws.cell(row, 1, "Match Goals").font = subheader_font
        ws.cell(row, 1).fill = subheader_fill
        row += 1
        
        ws.cell(row, 1, "Primary:").font = Font(bold=True)
        ws.cell(row, 2, self.session.goals.get("primary", ""))
        row += 1
        
        ws.cell(row, 1, "Secondary:").font = Font(bold=True)
        ws.cell(row, 2, self.session.goals.get("secondary", ""))
        row += 1
        
        ws.cell(row, 1, "Difficulty (1-10):").font = Font(bold=True)
        ws.cell(row, 2, str(self.session.difficulty))
        row += 2
        
        # Self Reflections
        ws.cell(row, 1, "Self Reflection").font = subheader_font
        ws.cell(row, 1).fill = subheader_fill
        row += 1
        
        for label, key in [("Goals Met:", "goals_met"), ("What Went Well:", "what_went_well"),
                          ("Biggest Challenge:", "biggest_challenge"), ("Taking Forward:", "taking_forward")]:
            ws.cell(row, 1, label).font = Font(bold=True)
            ws.merge_cells(f'B{row}:G{row}')
            ws.cell(row, 2, self.session.reflections.get(key, ""))
            ws.cell(row, 2).alignment = Alignment(wrap_text=True, vertical='top')
            row += 1
        
        row += 1
        
        # CRRDF Reflections
        ws.cell(row, 1, "CRRDF Framework Responses").font = subheader_font
        ws.cell(row, 1).fill = subheader_fill
        row += 1
        
        if hasattr(self, 'pillar_answers'):
            for pillar_name in self.pillars:
                pillar_data = CRRDF_QUESTIONS[pillar_name]
                ws.cell(row, 1, pillar_data['title']).font = Font(bold=True, size=11)
                row += 1
                
                for q_idx, question_data in enumerate(pillar_data['questions']):
                    key = f"{pillar_name}_{q_idx}"
                    ws.cell(row, 1, f"Q: {question_data['q']}").font = Font(bold=True)
                    row += 1
                    
                    ws.merge_cells(f'B{row}:G{row}')
                    ws.cell(row, 2, self.pillar_answers.get(key, ""))
                    ws.cell(row, 2).alignment = Alignment(wrap_text=True, vertical='top')
                    row += 1
                
                row += 1
        
        # GFA Scores
        ws.cell(row, 1, "Game Focus Area Scores").font = subheader_font
        ws.cell(row, 1).fill = subheader_fill
        row += 1
        
        # GFA Headers
        ws.cell(row, 1, "Category").font = Font(bold=True)
        ws.cell(row, 2, "Aspect").font = Font(bold=True)
        ws.cell(row, 3, "What this covers").font = Font(bold=True)
        ws.cell(row, 4, "Self Score").font = Font(bold=True)
        ws.cell(row, 5, "Coach Score").font = Font(bold=True)
        row += 1
        
        for category, aspects in GFA_CATEGORIES.items():
            for aspect_name, description in aspects:
                ws.cell(row, 1, category)
                ws.cell(row, 2, aspect_name)
                ws.cell(row, 3, description)
                key = f"{category}_{aspect_name}"
                ws.cell(row, 4, self.session.gfa_scores.get(key, ""))
                row += 1
        
        row += 1
        
        # Rating Scale
        ws.cell(row, 1, "Rating Scale").font = subheader_font
        ws.cell(row, 1).fill = subheader_fill
        row += 1
        
        for score, description in RATING_SCALE.items():
            ws.cell(row, 1, str(score)).font = Font(bold=True)
            ws.merge_cells(f'B{row}:G{row}')
            ws.cell(row, 2, description)
            ws.cell(row, 2).alignment = Alignment(wrap_text=True)
            row += 1
        
        # Column widths
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 50
        ws.column_dimensions['C'].width = 60
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 15
        
        wb.save(filename)
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content.winfo_children():
            widget.destroy()


def show_splash_screen(parent):
    """Display splash screen while app loads"""
    splash = tk.Toplevel(parent)
    splash.title("")
    splash.overrideredirect(True)  # Remove window decorations
    
    width = 500
    height = 300
    x = (splash.winfo_screenwidth() // 2) - (width // 2)
    y = (splash.winfo_screenheight() // 2) - (height // 2)
    splash.geometry(f'{width}x{height}+{x}+{y}')
    
    # Main frame
    frame = tk.Frame(splash, bg="#1976D2", relief=tk.RAISED, borderwidth=2)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # App title
    tk.Label(frame, text="Rugby Referee Review System", 
            font=("Segoe UI", 20, "bold"), bg="#1976D2", fg="white").pack(pady=(40, 10))
    
    # Version
    tk.Label(frame, text=f"Version {__version__}", 
            font=("Segoe UI", 11), bg="#1976D2", fg="#E3F2FD").pack(pady=5)
    
    # Copyright
    tk.Label(frame, text="", bg="#1976D2").pack(pady=10)  # Spacer
    tk.Label(frame, text="Copyright © 2025 Andrew Clarkson", 
            font=("Segoe UI", 10), bg="#1976D2", fg="white").pack(pady=5)
    
    # CRRDF
    tk.Label(frame, text="Based on CRRDF Framework", 
            font=("Segoe UI", 9, "italic"), bg="#1976D2", fg="#E3F2FD").pack(pady=2)
    
    # Loading message
    tk.Label(frame, text="", bg="#1976D2").pack(pady=15)  # Spacer
    loading_label = tk.Label(frame, text="Loading...", 
            font=("Segoe UI", 10), bg="#1976D2", fg="#E3F2FD")
    loading_label.pack(pady=10)
    
    # Progress bar
    progress = ttk.Progressbar(frame, mode='indeterminate', length=300)
    progress.pack(pady=10)
    progress.start(10)
    
    splash.update()
    return splash


def main():
    """Main entry point"""
    # Create main window first (hidden)
    if THEME_AVAILABLE:
        root = ttk.Window(themename="cosmo")
    else:
        root = tk.Tk()
    
    root.withdraw()  # Hide main window initially
    
    # Show splash screen
    splash = show_splash_screen(root)
    
    # Simulate loading (in real app, this is where you'd load resources)
    import time
    for i in range(20):  # 2 seconds total
        time.sleep(0.1)
        splash.update()
    
    # Close splash and show main app
    splash.destroy()
    root.deiconify()  # Show main window
    
    app = CRRDFReviewApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()