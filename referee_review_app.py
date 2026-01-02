#!/usr/bin/env python3
"""
ORRA Referee Review Application
Structured review system based on CRRDF framework
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.root.title("ORRA Referee Review System")
        self.root.geometry("1000x700")
        
        self.session = ReviewSession()
        self.current_pillar = None
        self.current_question = 0
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main container
        self.create_widgets()
        
    def create_widgets(self):
        """Create the main UI"""
        # Header
        header = tk.Frame(self.root, bg="#003366", height=60)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="ORRA Referee Review System", 
                        font=("Arial", 18, "bold"), bg="#003366", fg="white")
        title.pack(pady=15)
        
        # Main content area
        self.content = tk.Frame(self.root, bg="#f0f0f0")
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Start with metadata entry
        self.show_metadata_entry()
        
    def show_metadata_entry(self):
        """Game metadata entry screen"""
        self.clear_content()
        
        frame = tk.Frame(self.content, bg="#f0f0f0")
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Game Information", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack(pady=10)
        
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
            container = tk.Frame(frame, bg="#f0f0f0")
            container.pack(fill=tk.X, pady=5)
            
            tk.Label(container, text=label, width=15, anchor="w",
                    bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
            
            entry = PlaceholderEntry(container, placeholder=placeholder, width=40, font=("Arial", 10))
            entry.pack(side=tk.LEFT, padx=5)
            self.metadata_entries[key] = entry
        
        # Goals section
        tk.Label(frame, text="\nMatch Goals", font=("Arial", 14, "bold"),
                bg="#f0f0f0").pack(pady=10)
        
        tk.Label(frame, text="Primary Goal:", anchor="w", bg="#f0f0f0",
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=20)
        self.primary_goal = PlaceholderText(frame, placeholder="What is your main focus for this game? e.g., 'Improve accuracy in jackler decisions at breakdown'", 
                                           height=2, width=60, font=("Arial", 10), wrap=tk.WORD)
        self.primary_goal.pack(padx=20, pady=5)
        
        tk.Label(frame, text="Secondary Goal:", anchor="w", bg="#f0f0f0",
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=20)
        self.secondary_goal = PlaceholderText(frame, placeholder="Your secondary focus area? e.g., 'Better positioning at scrum time'", 
                                             height=2, width=60, font=("Arial", 10), wrap=tk.WORD)
        self.secondary_goal.pack(padx=20, pady=5)
        
        # Difficulty scale
        tk.Label(frame, text="\nGame Difficulty (1=Easy, 10=Very Hard):",
                bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=10)
        
        self.difficulty_var = tk.IntVar(value=5)
        difficulty_scale = tk.Scale(frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                   variable=self.difficulty_var, length=300)
        difficulty_scale.pack()
        
        # Navigation
        nav = tk.Frame(frame, bg="#f0f0f0")
        nav.pack(pady=20)
        
        tk.Button(nav, text="Next: Self Reflection", command=self.show_self_reflection,
                 font=("Arial", 11, "bold"), bg="#00796b", fg="white",
                 padx=20, pady=10).pack()
        
    def show_self_reflection(self):
        """Self reflection questions"""
        # Save metadata
        for key, entry in self.metadata_entries.items():
            self.session.metadata[key] = entry.get_value()
        self.session.goals["primary"] = self.primary_goal.get_value()
        self.session.goals["secondary"] = self.secondary_goal.get_value()
        self.session.difficulty = self.difficulty_var.get()
        
        self.clear_content()
        
        frame = tk.Frame(self.content, bg="#f0f0f0")
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Self Reflection", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack(pady=10)
        
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
            tk.Label(frame, text=question, anchor="w", bg="#f0f0f0",
                    font=("Arial", 10, "bold")).pack(fill=tk.X, padx=20, pady=(10, 5))
            
            text = PlaceholderText(frame, placeholder=placeholder, height=4, width=70, 
                                  font=("Arial", 10), wrap=tk.WORD)
            text.pack(padx=20, pady=5)
            self.reflection_entries[key] = text
        
        # Navigation
        nav = tk.Frame(frame, bg="#f0f0f0")
        nav.pack(pady=20)
        
        tk.Button(nav, text="← Back", command=self.show_metadata_entry,
                 font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(nav, text="Next: CRRDF Deep Dive →", command=self.start_crrdf_questions,
                 font=("Arial", 11, "bold"), bg="#00796b", fg="white",
                 padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
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
        
        self.current_pillar = self.pillars[self.current_pillar_index]
        pillar_data = CRRDF_QUESTIONS[self.current_pillar]
        
        self.clear_content()
        
        frame = tk.Frame(self.content, bg="#f0f0f0")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress indicator
        progress_text = f"Pillar {self.current_pillar_index + 1} of {len(self.pillars)}"
        tk.Label(frame, text=progress_text, font=("Arial", 10),
                bg="#f0f0f0", fg="#666").pack(pady=5)
        
        tk.Label(frame, text=pillar_data["title"], font=("Arial", 18, "bold"),
                bg="#f0f0f0", fg="#00796b").pack(pady=20)
        
        # Description based on pillar
        descriptions = {
            "technical": "Law application, decision-making based on player actions, game innovations",
            "tactical": "Tactical awareness, advantage application, positioning, game context",
            "management": "Game management level, safety, strategies, captain interaction",
            "mental": "Preparation, managing clutter, coachability, soft skills",
            "physical": "Fitness, keeping up with play, positioning"
        }
        
        tk.Label(frame, text=descriptions.get(self.current_pillar, ""),
                font=("Arial", 11), bg="#f0f0f0", wraplength=600).pack(pady=10)
        
        tk.Label(frame, text=f"\n{len(pillar_data['questions'])} questions to help deepen your reflection",
                font=("Arial", 10), bg="#f0f0f0").pack(pady=10)
        
        # Navigation
        nav = tk.Frame(frame, bg="#f0f0f0")
        nav.pack(pady=40)
        
        tk.Button(nav, text="Begin Questions →", command=self.show_crrdf_question,
                 font=("Arial", 12, "bold"), bg="#00796b", fg="white",
                 padx=30, pady=15).pack()
    
    def show_crrdf_question(self):
        """Show individual CRRDF question"""
        pillar_data = CRRDF_QUESTIONS[self.current_pillar]
        
        if self.current_question >= len(pillar_data["questions"]):
            # Move to next pillar
            self.current_question = 0
            self.current_pillar_index += 1
            self.show_pillar_intro()
            return
        
        question_data = pillar_data["questions"][self.current_question]
        
        self.clear_content()
        
        frame = tk.Frame(self.content, bg="#f0f0f0")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress
        progress = f"{pillar_data['title']} - Q{self.current_question + 1}/{len(pillar_data['questions'])}"
        tk.Label(frame, text=progress, font=("Arial", 10), bg="#f0f0f0",
                fg="#666").pack(pady=5)
        
        # Question
        q_frame = tk.Frame(frame, bg="white", relief=tk.RAISED, borderwidth=2)
        q_frame.pack(fill=tk.X, padx=30, pady=20)
        
        tk.Label(q_frame, text=question_data["q"], font=("Arial", 13, "bold"),
                bg="white", wraplength=650, justify=tk.LEFT).pack(padx=20, pady=15)
        
        # Prompts
        if question_data.get("prompts"):
            prompt_frame = tk.Frame(frame, bg="#e3f2fd")
            prompt_frame.pack(fill=tk.X, padx=40, pady=10)
            
            tk.Label(prompt_frame, text="Think about:", font=("Arial", 10, "italic"),
                    bg="#e3f2fd").pack(anchor="w", padx=15, pady=5)
            
            for prompt in question_data["prompts"]:
                tk.Label(prompt_frame, text=f"• {prompt}", font=("Arial", 10),
                        bg="#e3f2fd", wraplength=600, justify=tk.LEFT).pack(
                        anchor="w", padx=30, pady=2)
        
        # Answer area
        tk.Label(frame, text="Your reflection:", font=("Arial", 11, "bold"),
                bg="#f0f0f0").pack(anchor="w", padx=40, pady=(20, 5))
        
        # Create helpful placeholder based on the question type
        placeholder_text = "Be specific with examples, include time stamps if possible, describe what you did and the impact it had..."
        
        self.current_answer = PlaceholderText(frame, placeholder=placeholder_text,
                                             height=8, width=70, font=("Arial", 10), wrap=tk.WORD)
        self.current_answer.pack(padx=40, pady=5)
        
        # Navigation
        nav = tk.Frame(frame, bg="#f0f0f0")
        nav.pack(pady=20)
        
        if self.current_question > 0 or self.current_pillar_index > 0:
            tk.Button(nav, text="← Previous", command=self.previous_question,
                     font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        next_text = "Next Question →" if self.current_question < len(pillar_data["questions"]) - 1 else "Complete Pillar →"
        tk.Button(nav, text=next_text, command=self.save_and_next_question,
                 font=("Arial", 11, "bold"), bg="#00796b", fg="white",
                 padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    def previous_question(self):
        """Go back to previous question"""
        if self.current_question > 0:
            self.current_question -= 1
        else:
            self.current_pillar_index -= 1
            if self.current_pillar_index >= 0:
                self.current_pillar = self.pillars[self.current_pillar_index]
                pillar_data = CRRDF_QUESTIONS[self.current_pillar]
                self.current_question = len(pillar_data["questions"]) - 1
        
        self.show_crrdf_question()
    
    def save_and_next_question(self):
        """Save current answer and move to next"""
        pillar_data = CRRDF_QUESTIONS[self.current_pillar]
        question_data = pillar_data["questions"][self.current_question]
        
        # Save answer
        key = f"{self.current_pillar}_{self.current_question}"
        self.session.crrdf_reflections[key] = {
            "pillar": pillar_data["title"],
            "question": question_data["q"],
            "answer": self.current_answer.get_value()
        }
        
        self.current_question += 1
        self.show_crrdf_question()
    
    def show_gfa_scoring(self):
        """Game Focus Area scoring"""
        self.clear_content()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.content, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(scrollable_frame, text="Game Focus Areas (GFA) Scoring",
                font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        tk.Label(scrollable_frame, text="Rate your performance in each area (1-5 scale)",
                font=("Arial", 11), bg="#f0f0f0").pack(pady=5)
        
        self.gfa_entries = {}
        
        for category, aspects in GFA_CATEGORIES.items():
            # Category header
            cat_frame = tk.Frame(scrollable_frame, bg="#00796b")
            cat_frame.pack(fill=tk.X, padx=20, pady=(15, 0))
            
            tk.Label(cat_frame, text=category, font=("Arial", 12, "bold"),
                    bg="#00796b", fg="white").pack(padx=10, pady=8)
            
            # Aspects - now tuples with (name, description)
            for aspect_name, aspect_desc in aspects:
                aspect_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, borderwidth=1)
                aspect_frame.pack(fill=tk.X, padx=30, pady=5)
                
                # Left side - aspect name and description
                left_frame = tk.Frame(aspect_frame, bg="white")
                left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                tk.Label(left_frame, text=aspect_name, font=("Arial", 10, "bold"),
                        bg="white", anchor="w").pack(fill=tk.X)
                
                tk.Label(left_frame, text=aspect_desc, font=("Arial", 9),
                        bg="white", fg="#666", anchor="w", wraplength=500, justify=tk.LEFT).pack(fill=tk.X, pady=(2, 0))
                
                # Right side - radio buttons
                score_var = tk.IntVar(value=3)
                self.gfa_entries[f"{category}_{aspect_name}"] = score_var
                
                score_frame = tk.Frame(aspect_frame, bg="white")
                score_frame.pack(side=tk.RIGHT, padx=10)
                
                for i in range(1, 6):
                    rb = tk.Radiobutton(score_frame, text=str(i), variable=score_var,
                                       value=i, font=("Arial", 10), bg="white")
                    rb.pack(side=tk.LEFT, padx=5)
        
        # Rating scale reference
        scale_frame = tk.Frame(scrollable_frame, bg="#fff3cd", relief=tk.RAISED, borderwidth=2)
        scale_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(scale_frame, text="Rating Scale Reference:", font=("Arial", 10, "bold"),
                bg="#fff3cd").pack(anchor="w", padx=10, pady=5)
        
        for rating, desc in RATING_SCALE.items():
            tk.Label(scale_frame, text=f"{rating}: {desc}", font=("Arial", 9),
                    bg="#fff3cd", wraplength=700, justify=tk.LEFT).pack(
                    anchor="w", padx=20, pady=2)
        
        # Navigation
        nav = tk.Frame(scrollable_frame, bg="#f0f0f0")
        nav.pack(pady=20)
        
        tk.Button(nav, text="← Back", command=self.start_crrdf_questions,
                 font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(nav, text="Save & Export →", command=self.export_review,
                 font=("Arial", 12, "bold"), bg="#00796b", fg="white",
                 padx=30, pady=15).pack(side=tk.LEFT, padx=5)
    
    def export_review(self):
        """Export review to Excel"""
        # Save GFA scores
        for key, var in self.gfa_entries.items():
            self.session.gfa_scores[key] = var.get()
        
        # Get save location
        filename = f"Referee_Review_{self.session.metadata['referee']}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=filename
        )
        
        if not filepath:
            return
        
        try:
            self.create_excel_report(filepath)
            messagebox.showinfo("Success", f"Review saved to:\n{filepath}")
            
            # Ask if user wants to start another review
            if messagebox.askyesno("New Review", "Would you like to start another review?"):
                self.session = ReviewSession()
                self.show_metadata_entry()
            else:
                self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save review:\n{str(e)}")
    
    def create_excel_report(self, filepath):
        """Create Excel file matching ORRA format"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Review"
        
        # Styles
        header_font = Font(bold=True, size=12)
        title_font = Font(bold=True, size=14)
        label_font = Font(bold=True, size=10)
        
        header_fill = PatternFill(start_color="003366", end_color="003366", fill_type="solid")
        category_fill = PatternFill(start_color="00796b", end_color="00796b", fill_type="solid")
        
        white_font = Font(color="FFFFFF", bold=True)
        
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Title
        ws.merge_cells('C4:E4')
        ws['C4'] = "ORRA Review Document 2026"
        ws['C4'].font = title_font
        ws['C4'].alignment = Alignment(horizontal='center')
        
        # Metadata
        ws['B6'] = "Game & Grade:"
        ws['B6'].font = label_font
        ws['C6'] = self.session.metadata['game_grade']
        ws['F6'] = "Referee:"
        ws['F6'].font = label_font
        ws['G6'] = self.session.metadata['referee']
        
        ws['B7'] = "Date:"
        ws['B7'].font = label_font
        ws['C7'] = self.session.metadata['date']
        ws['F7'] = "Coach:"
        ws['F7'].font = label_font
        ws['G7'] = self.session.metadata['coach']
        
        ws['B8'] = "Result:"
        ws['B8'].font = label_font
        ws['C8'] = self.session.metadata['result']
        ws['F8'] = "Date completed:"
        ws['F8'].font = label_font
        ws['G8'] = self.session.metadata['date_completed']
        
        # Match Goals
        ws['B10'] = "Match Goals"
        ws['B10'].font = header_font
        ws['C10'] = "My key focus for this game is"
        ws['C11'] = self.session.goals['primary']
        ws['C10'].font = label_font
        
        ws['C12'] = "My secondary focus area is"
        ws['C12'].font = label_font
        ws['C13'] = self.session.goals['secondary']
        
        # Difficulty
        ws['B15'] = f"How hard did I find this game to referee? {self.session.difficulty}/10"
        ws['B15'].font = label_font
        
        # Self Reflection
        current_row = 17
        ws[f'B{current_row}'] = "Self Reflection and Game Overview"
        ws[f'B{current_row}'].font = header_font
        current_row += 1
        
        reflection_questions = [
            ("Did I meet my goals - why or why not, give some examples?", "goals_met", "Primary Goal / Secondary Goal"),
            ("What areas of the game went well and why? (will likely relate to GFAs)", "what_went_well", ""),
            ("What was the biggest challenge in the game? What would/could I do differently next time?", "biggest_challenge", ""),
            ("What am I taking into my next game?", "taking_forward", "")
        ]
        
        for question, key, note in reflection_questions:
            ws[f'B{current_row}'] = question
            ws[f'B{current_row}'].font = label_font
            ws[f'C{current_row}'] = self.session.reflections.get(key, "")
            if note:
                ws[f'D{current_row}'] = note
            current_row += 1
        
        # CRRDF Deep Dive Section
        current_row += 2
        ws[f'B{current_row}'] = "CRRDF Framework Deep Dive"
        ws[f'B{current_row}'].font = title_font
        ws[f'B{current_row}'].fill = header_fill
        ws[f'B{current_row}'].font = white_font
        current_row += 1
        
        for pillar in self.pillars:
            pillar_data = CRRDF_QUESTIONS[pillar]
            ws[f'B{current_row}'] = pillar_data['title']
            ws[f'B{current_row}'].font = header_font
            ws[f'B{current_row}'].fill = category_fill
            ws[f'B{current_row}'].font = white_font
            current_row += 1
            
            for q_idx in range(len(pillar_data['questions'])):
                key = f"{pillar}_{q_idx}"
                if key in self.session.crrdf_reflections:
                    reflection = self.session.crrdf_reflections[key]
                    ws[f'B{current_row}'] = reflection['question']
                    ws[f'B{current_row}'].font = label_font
                    current_row += 1
                    ws[f'C{current_row}'] = reflection['answer']
                    ws[f'C{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
                    current_row += 1
            
            current_row += 1
        
        # GFA Scores
        current_row += 1
        ws[f'B{current_row}'] = "GFA"
        ws[f'D{current_row}'] = "GFA aspect"
        ws[f'E{current_row}'] = "What this covers"
        ws[f'F{current_row}'] = "Referee score"
        ws[f'G{current_row}'] = "Coach score"
        
        for cell_ref in [f'B{current_row}', f'D{current_row}', f'E{current_row}', f'F{current_row}', f'G{current_row}']:
            ws[cell_ref].font = label_font
            ws[cell_ref].border = border
        
        current_row += 1
        
        for category, aspects in GFA_CATEGORIES.items():
            for i, (aspect_name, aspect_desc) in enumerate(aspects):
                if i == 0:
                    ws[f'B{current_row}'] = category
                    ws[f'B{current_row}'].font = label_font
                
                ws[f'D{current_row}'] = aspect_name
                ws[f'E{current_row}'] = aspect_desc
                ws[f'E{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
                ws[f'E{current_row}'].font = Font(size=9, color="666666")
                
                key = f"{category}_{aspect_name}"
                if key in self.session.gfa_scores:
                    ws[f'F{current_row}'] = self.session.gfa_scores[key]
                
                for cell_ref in [f'B{current_row}', f'D{current_row}', f'E{current_row}', f'F{current_row}', f'G{current_row}']:
                    ws[cell_ref].border = border
                
                current_row += 1
        
        # Rating scale reference
        current_row += 2
        for rating, desc in RATING_SCALE.items():
            ws[f'B{current_row}'] = rating
            ws[f'C{current_row}'] = desc
            ws[f'C{current_row}'].alignment = Alignment(wrap_text=True)
            current_row += 1
        
        # Adjust column widths
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 50
        ws.column_dimensions['D'].width = 25
        ws.column_dimensions['E'].width = 60
        ws.column_dimensions['F'].width = 15
        ws.column_dimensions['G'].width = 15
        
        wb.save(filepath)
    
    def clear_content(self):
        """Clear current content area"""
        for widget in self.content.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    app = CRRDFReviewApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()