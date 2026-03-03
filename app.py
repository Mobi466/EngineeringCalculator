import customtkinter as ctk
import math
from functools import partial

# -----------------------------
# Appearance
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -----------------------------
# Safe Math Functions
# -----------------------------
safe_dict = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "log": math.log10,
    "ln": math.log,
    "sqrt": math.sqrt,
    "pi": math.pi,
    "e": math.e,
    "factorial": math.factorial,
    "pow": pow,
}

# -----------------------------
# Calculator Class
# -----------------------------
class EngineeringCalculator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Ultimate Engineering Calculator")
        self.geometry("600x800")
        self.resizable(False, False)
        self.expression = ""

        # Entry
        self.entry = ctk.CTkEntry(self, font=("Consolas", 28), justify="right")
        self.entry.pack(padx=20, pady=(20,5), fill="x")

        # History
        self.history = ctk.CTkTextbox(self, height=180, state="disabled")
        self.history.pack(padx=20, pady=5, fill="x")

        # Frame دکمه‌ها
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.create_buttons()

        # Theme toggle
        self.theme_button = ctk.CTkButton(self, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(pady=10)

    # -----------------------------
    # Button Actions
    # -----------------------------
    def click(self, value):
        self.expression += str(value)
        self.update_entry()

    def clear(self):
        self.expression = ""
        self.update_entry()

    def calculate(self):
        try:
            result = eval(self.expression, {"__builtins__": None}, safe_dict)
            self.add_history(f"{self.expression} = {result}")
            self.expression = str(result)
            self.update_entry()
        except:
            self.expression = ""
            self.update_entry("Error")

    # -----------------------------
    # Helpers
    # -----------------------------
    def update_entry(self, text=None):
        self.entry.delete(0, "end")
        self.entry.insert(0, text if text else self.expression)

    def add_history(self, text):
        self.history.configure(state="normal")
        self.history.insert("end", text + "\n")
        self.history.configure(state="disabled")
        self.history.see("end")

    # -----------------------------
    # Toggle Theme حرفه‌ای
    # -----------------------------
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)

        # بازسازی کامل دکمه‌ها
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.create_buttons()

    # -----------------------------
    # Create Buttons با پرانتز و گیومه واضح
    # -----------------------------
    def create_buttons(self):
        button_layout = [
            ["7","8","9","/","sqrt("],
            ["4","5","6","*","pow("],
            ["1","2","3","-","("],
            ["0",".","=","+",")"],
            ["sin(","cos(","tan(","log(","ln("],
            ["pi","e","factorial(","C"],
            ["'", '"']  # گیومه تک و دوتایی
        ]

        for row in button_layout:
            frame = ctk.CTkFrame(self.button_frame)
            frame.pack(fill="both", expand=True, padx=5, pady=5)
            for btn in row:
                if btn == "=":
                    action = self.calculate
                elif btn == "C":
                    action = self.clear
                else:
                    action = partial(self.click, btn)
                ctk.CTkButton(
                    frame,
                    text=btn,
                    command=action,
                    font=("Consolas", 20, "bold"),
                    width=60,
                    height=60
                ).pack(side="left", expand=True, fill="both", padx=5, pady=5)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app = EngineeringCalculator()
    app.mainloop()