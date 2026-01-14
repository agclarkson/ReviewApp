#!/usr/bin/env python3
"""
Rugby Referee Review System
Professional review application based on CRRDF framework

Copyright © 2025 Andrew Clarkson
All Rights Reserved

This application implements the Community Rugby Referee Development Framework (CRRDF).

Licensed under MIT License

Version: 2.0.2-phase2
"""

__version__ = "2.0.2-phase2"
__author__ = "Andrew Clarkson"
__copyright__ = "Copyright © 2025 Andrew Clarkson"
__license__ = "MIT"

# Application Constants
CRRDF_VERSION = "February 2025"

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
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_dialog)
    
    def new_review(self):
        """Start a new review"""
        if messagebox.askyesno("New Review", "Start a new review? Any unsaved data will be lost."):
            self.session = ReviewSession()
            self.show_metadata_entry()
    
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
        if THEME_AVAILABLE:
            style = ttk.Style("cosmo")  # Modern, professional theme
        else:
            style = ttk.Style()
            style.theme_use('clam')
        
        # Create main container
        self.create_widgets()
        
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
        fields = [
            ("Game & Grade:", "game_grade", "e.g., Premier 1, Senior 2"),
            ("Date:", "date", self.session.metadata["date"]),
            ("Result:", "result", "e.g., Home 24-17 Away"),
            ("Referee:", "referee", "Your name"),
            ("Coach:", "coach", "Coach name (optional)")
        ]
        
        self.metadata_entries = {}
        for label, key, placeholder in fields:
            container = tk.Frame(frame, bg="#FAFAFA")
            container.pack(fill=tk.X, pady=5, padx=20)
            
            tk.Label(container, text=label, width=15, anchor="w",
                    bg="#FAFAFA", font=("Segoe UI", 10, "bold"), fg="#212121").pack(side=tk.LEFT)
            
            entry = PlaceholderEntry(container, placeholder=placeholder, width=40, font=("Segoe UI", 10))
            entry.pack(side=tk.LEFT, padx=5)
            self.metadata_entries[key] = entry
        
        # Goals section
        tk.Label(frame, text="\nMatch Goals", font=("Segoe UI", 14, "bold"),
                bg="#FAFAFA", fg="#212121").pack(pady=10)
        
        tk.Label(frame, text="Primary Goal:", anchor="w", bg="#FAFAFA",
                font=("Segoe UI", 10, "bold"), fg="#212121").pack(fill=tk.X, padx=20)
        self.primary_goal = PlaceholderText(frame, placeholder="What is your main focus for this game? e.g., 'Improve accuracy in jackler decisions at breakdown'", 
                                           height=2, width=60, font=("Segoe UI", 10), wrap=tk.WORD)
        self.primary_goal.pack(padx=20, pady=5)
        
        tk.Label(frame, text="Secondary Goal:", anchor="w", bg="#FAFAFA",
                font=("Segoe UI", 10, "bold"), fg="#212121").pack(fill=tk.X, padx=20)
        self.secondary_goal = PlaceholderText(frame, placeholder="Your secondary focus area? e.g., 'Better positioning at scrum time'", 
                                             height=2, width=60, font=("Segoe UI", 10), wrap=tk.WORD)
        self.secondary_goal.pack(padx=20, pady=5)
        
        # Difficulty scale
        tk.Label(frame, text="\nGame Difficulty (1=Easy, 10=Very Hard):",
                bg="#FAFAFA", font=("Segoe UI", 10, "bold"), fg="#212121").pack(pady=10)
        
        self.difficulty_var = tk.IntVar(value=5)
        
        # Display current value
        difficulty_value_label = tk.Label(frame, text="Current: 5", 
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
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"Review_{self.session.metadata['referee']}_{self.session.metadata['date']}.xlsx"
        )
        
        if not filename:
            return
        
        try:
            self._create_excel_export(filename)
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