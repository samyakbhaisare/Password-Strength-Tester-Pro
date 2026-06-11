import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import re
import math

try:
    import pyperclip
except ImportError:
    pyperclip = None


class PasswordStrengthTester:

    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Tester Pro")
        self.root.geometry("900x750")
        self.root.minsize(900, 750)

        # ==========================
        # COLORS
        # ==========================

        self.BG = "#1E1E2E"
        self.CARD = "#2A2A3C"
        self.TEXT = "#FFFFFF"
        self.ACCENT = "#4CAF50"

        self.RED = "#E74C3C"
        self.ORANGE = "#F39C12"
        self.YELLOW = "#F1C40F"
        self.LIGHT_GREEN = "#2ECC71"
        self.GREEN = "#27AE60"

        self.root.configure(bg=self.BG)

        self.setup_styles()
        self.create_variables()
        self.create_widgets()

    # ==================================
    # VARIABLES
    # ==================================

    def create_variables(self):

        self.password_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar()

    # ==================================
    # STYLES
    # ==================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=24
        )

    # ==================================
    # MAIN UI
    # ==================================

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Password Strength Tester Pro",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 26, "bold")
        )

        title.pack(pady=20)

        subtitle = tk.Label(
            self.root,
            text="Real-Time Password Analysis & Secure Generator",
            bg=self.BG,
            fg="#BBBBBB",
            font=("Segoe UI", 11)
        )

        subtitle.pack()

        # ==================================
        # MAIN CARD
        # ==================================

        self.main_card = tk.Frame(
            self.root,
            bg=self.CARD,
            bd=0
        )

        self.main_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.create_password_section()
        self.create_strength_section()
        self.create_requirements_section()
        self.create_feedback_section()
        self.create_buttons_section()

    # ==================================
    # PASSWORD SECTION
    # ==================================

    def create_password_section(self):

        frame = tk.Frame(
            self.main_card,
            bg=self.CARD
        )

        frame.pack(fill="x", padx=20, pady=15)

        tk.Label(
            frame,
            text="Password",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        entry_frame = tk.Frame(
            frame,
            bg=self.CARD
        )

        entry_frame.pack(
            fill="x",
            pady=10
        )

        self.password_entry = tk.Entry(
            entry_frame,
            textvariable=self.password_var,
            show="*",
            font=("Segoe UI", 14),
            relief="flat",
            bd=10
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.password_entry.bind(
            "<KeyRelease>",
            self.analyze_password
        )

        self.show_button = tk.Button(
            entry_frame,
            text="Show",
            width=6,
            bg="#3A3A4F",
            fg="white",
            relief="flat",
            command=self.toggle_password
        )

        self.show_button.pack(
            side="right",
            padx=5
        )

    # ==================================
    # STRENGTH SECTION
    # ==================================

    def create_strength_section(self):

        frame = tk.Frame(
            self.main_card,
            bg=self.CARD
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.progress = ttk.Progressbar(
            frame,
            length=700,
            mode="determinate",
            style="Custom.Horizontal.TProgressbar"
        )

        self.progress.pack(fill="x")

        self.strength_label = tk.Label(
            frame,
            text="Strength: N/A",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 14, "bold")
        )

        self.strength_label.pack(
            pady=10
        )

        self.score_label = tk.Label(
            frame,
            text="Score: 0/100",
            bg=self.CARD,
            fg="#DDDDDD",
            font=("Segoe UI", 11)
        )

        self.score_label.pack()

        self.entropy_label = tk.Label(
            frame,
            text="Entropy: 0 bits",
            bg=self.CARD,
            fg="#DDDDDD",
            font=("Segoe UI", 11)
        )

        self.entropy_label.pack()


        # ==================================
    # REQUIREMENTS SECTION
    # ==================================

    def create_requirements_section(self):

        frame = tk.LabelFrame(
            self.main_card,
            text=" Password Requirements ",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold")
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.requirements_label = tk.Label(
            frame,
            text="Start typing a password...",
            justify="left",
            anchor="w",
            bg=self.CARD,
            fg="white",
            font=("Consolas", 11)
        )

        self.requirements_label.pack(
            anchor="w",
            padx=10,
            pady=5
        )

    # ==================================
    # FEEDBACK SECTION
    # ==================================

    def create_feedback_section(self):

        frame = tk.LabelFrame(
            self.main_card,
            text=" Feedback & Suggestions ",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold")
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.feedback_text = tk.Text(
            frame,
            height=3,
            bg="#1B1B28",
            fg="white",
            insertbackground="white",
            font=("Segoe UI", 10),
            relief="flat"
        )

        self.feedback_text.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.feedback_text.insert(
            "1.0",
            "Password suggestions will appear here."
        )

        self.feedback_text.config(state="disabled")

    # ==================================
    # ANALYSIS ENGINE
    # ==================================

    def analyze_password(self, event=None):

        password = self.password_var.get()

        try:

            score = 0

            length_ok = len(password) >= 8
            upper_ok = bool(re.search(r"[A-Z]", password))
            lower_ok = bool(re.search(r"[a-z]", password))
            digit_ok = bool(re.search(r"\d", password))
            special_ok = bool(
                re.search(
                    r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]",
                    password
                )
            )

            rules = [
                ("Minimum 8 Characters", length_ok),
                ("Uppercase Letter", upper_ok),
                ("Lowercase Letter", lower_ok),
                ("Number", digit_ok),
                ("Special Character", special_ok)
            ]

            # ==========================
            # SCORE SYSTEM
            # ==========================

            if length_ok:
                score += 20

            if upper_ok:
                score += 15

            if lower_ok:
                score += 15

            if digit_ok:
                score += 15

            if special_ok:
                score += 15

            if len(password) >= 12:
                score += 10

            if len(password) >= 16:
                score += 10

            score = min(score, 100)

            # ==========================
            # ENTROPY
            # ==========================

            entropy = self.calculate_entropy(password)

            # ==========================
            # REQUIREMENTS
            # ==========================

            requirement_text = " | ".join(
                [
                    f"{'[OK]' if status else '[X]'} {name}"
                    for name, status in rules
                ]
            )

            self.requirements_label.config(
                text=requirement_text
            )

            # ==========================
            # FEEDBACK
            # ==========================

            suggestions = []

            if not length_ok:
                suggestions.append(
                    "- Increase password length to at least 8 characters."
                )

            if not upper_ok:
                suggestions.append(
                    "- Add uppercase letters."
                )

            if not lower_ok:
                suggestions.append(
                    "- Add lowercase letters."
                )

            if not digit_ok:
                suggestions.append(
                    "- Add numeric characters."
                )

            if not special_ok:
                suggestions.append(
                    "- Add special symbols."
                )

            if score >= 90:
                suggestions.append(
                    "- Excellent password security."
                )

            self.feedback_text.config(
                state="normal"
            )

            self.feedback_text.delete(
                "1.0",
                tk.END
            )

            if suggestions:

                rows = []

                for i in range(0, len(suggestions),3):
                    rows.append(" | ".join(suggestions[i:i+3]))

                self.feedback_text.insert(
                    tk.END,
                    "\n".join(rows)
                )
            else:
                self.feedback_text.insert(
                    tk.END,
                    "Password meets all security requirements."
                )

            self.feedback_text.config(
                state="disabled"
            )

            self.update_strength_meter(
                score,
                entropy
            )

        except Exception as e:

            messagebox.showerror(
                "Analysis Error",
                str(e)
            )

    # ==================================
    # ENTROPY CALCULATOR
    # ==================================

    def calculate_entropy(self, password):

        if not password:
            return 0

        charset_size = 0

        if re.search(r"[a-z]", password):
            charset_size += 26

        if re.search(r"[A-Z]", password):
            charset_size += 26

        if re.search(r"\d", password):
            charset_size += 10

        if re.search(
            r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]",
            password
        ):
            charset_size += 32

        if charset_size == 0:
            return 0

        entropy = len(password) * math.log2(charset_size)

        return round(entropy, 2)

    # ==================================
    # STRENGTH METER
    # ==================================

    def update_strength_meter(
        self,
        score,
        entropy
    ):

        self.progress["value"] = score

        if score < 25:

            level = "Very Weak"
            color = self.RED

        elif score < 50:

            level = "Weak"
            color = self.ORANGE

        elif score < 70:

            level = "Medium"
            color = self.YELLOW

        elif score < 85:

            level = "Strong"
            color = self.LIGHT_GREEN

        else:

            level = "Very Strong"
            color = self.GREEN

        self.strength_label.config(
            text=f"Strength: {level}",
            fg=color
        )

        self.score_label.config(
            text=f"Score: {score}/100"
        )

        self.entropy_label.config(
            text=f"Entropy: {entropy} bits"
        )


        # ==================================
    # BUTTONS SECTION
    # ==================================

    def create_buttons_section(self):

        frame = tk.Frame(
            self.main_card,
            bg=self.CARD
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.generate_btn = tk.Button(
            frame,
            text="Generate Password",
            bg="#3498DB",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            command=self.generate_password
        )

        self.generate_btn.grid(
            row=0,
            column=0,
            padx=5
        )

        self.copy_btn = tk.Button(
            frame,
            text="Copy Password",
            bg="#2ECC71",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            command=self.copy_password
        )

        self.copy_btn.grid(
            row=0,
            column=1,
            padx=5
        )

        self.clear_btn = tk.Button(
            frame,
            text="Clear",
            bg="#E74C3C",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            command=self.clear_fields
        )

        self.clear_btn.grid(
            row=0,
            column=2,
            padx=5
        )


    # ==================================
    # SHOW / HIDE PASSWORD
    # ==================================

    def toggle_password(self):

        if self.password_entry.cget("show") == "*":

            self.password_entry.config(
                show=""
            )

            self.show_button.config(
                text=" Hide"
            )

        else:

            self.password_entry.config(
                show="*"
            )

            self.show_button.config(
                text="Show"
            )

    # ==================================
    # SECURE PASSWORD GENERATOR
    # ==================================

    def generate_password(self):

        try:

            uppercase = secrets.choice(
                string.ascii_uppercase
            )

            lowercase = secrets.choice(
                string.ascii_lowercase
            )

            digit = secrets.choice(
                string.digits
            )

            special = secrets.choice(
                "!@#$%^&*()_+-="
            )

            remaining = [
                secrets.choice(
                    string.ascii_letters +
                    string.digits +
                    "!@#$%^&*()_+-="
                )
                for _ in range(12)
            ]

            password_list = [
                uppercase,
                lowercase,
                digit,
                special
            ] + remaining

            secrets.SystemRandom().shuffle(
                password_list
            )

            password = "".join(
                password_list
            )

            self.password_var.set(
                password
            )

            self.analyze_password()

            self.generate_btn.config(
                text="Generated"
            )

            self.root.after(
                2000,
                lambda: self.generate_btn.config(text="Generate Password")
            )

        except Exception as e:

            messagebox.showerror(
                "Generator Error",
                str(e)
            )

    # ==================================
    # COPY PASSWORD
    # ==================================

    def copy_password(self):

        password = self.password_var.get()

        if not password:

            messagebox.showwarning(
                "Warning",
                "Please enter or generate a password first."
            )

            return

        if pyperclip is None:

            messagebox.showerror(
                "Missing Dependency",
                "Install pyperclip:\n\npip install pyperclip"
            )

            return

        try:

            pyperclip.copy(
                password
            )


            self.copy_btn.config(
                text="Copied"
            )

            self.root.after(
                2000,
                lambda: self.copy_btn.config(text="Copy Password")
            )

        except Exception as e:

            messagebox.showerror(
                "Copy Error",
                str(e)
            )

    # ==================================
    # CLEAR FIELDS
    # ==================================

    def clear_fields(self):

        self.password_var.set("")

        self.password_entry.config(
            show="*"
        )

        self.show_button.config(
            text="Show"
        )

        self.progress["value"] = 0

        self.strength_label.config(
            text="Strength: N/A",
            fg="white"
        )

        self.score_label.config(
            text="Score: 0/100"
        )

        self.entropy_label.config(
            text="Entropy: 0 bits"
        )

        self.requirements_label.config(
            text="Start typing a password..."
        )

        self.feedback_text.config(
            state="normal"
        )

        self.feedback_text.delete(
            "1.0",
            tk.END
        )

        self.feedback_text.insert(
            tk.END,
            "Password suggestions will appear here."
        )

        self.feedback_text.config(
            state="disabled"
        )

        self.clear_btn.config(
                text="Cleard"
        )

        self.root.after(
            2000,
            lambda: self.clear_btn.config(text="Clear")
        )


# ==================================
# MAIN
# ==================================

def main():

    root = tk.Tk()

    app = PasswordStrengthTester(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()