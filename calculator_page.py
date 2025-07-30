import tkinter as tk
from tkinter import messagebox, ttk
from theme import Theme

class CalculatorPage:
    def __init__(self, parent):
        self.parent = parent
        self.calculator_type = tk.StringVar(value="Feed Cost")
        self.show_calculator()

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def show_calculator(self):
        self.clear_content()

        container = tk.Frame(self.parent)
        container.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(container, bg=Theme.BG_WHITE)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(container, bg=Theme.BG_LIGHT_GRAY, width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        header_frame = tk.Frame(left_frame, bg=Theme.BG_WHITE)
        header_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            header_frame,
            text="🧮 Farm Calculator",
            font=Theme.get_font(20, "bold"),
            bg=Theme.BG_WHITE,
            fg=Theme.PRIMARY_GREEN
        ).pack(anchor="w")

        # Dropdown menu to select calculator type
        type_frame = tk.Frame(left_frame, bg=Theme.BG_WHITE)
        type_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(
            type_frame, text="Select Calculator:",
            bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
            font=Theme.get_font()
        ).pack(side=tk.LEFT)

        type_dropdown = ttk.Combobox(
            type_frame, textvariable=self.calculator_type,
            values=["Feed Cost", "Profit", "BMI"], state="readonly",
            font=Theme.get_font(), width=20
        )
        type_dropdown.pack(side=tk.LEFT, padx=10)
        type_dropdown.bind("<<ComboboxSelected>>", lambda e: self.render_selected_calculator(calculator_frame))

        separator = tk.Frame(left_frame, height=2, bd=0, relief=tk.SUNKEN, bg=Theme.BG_GRAY)
        separator.pack(fill=tk.X, padx=20, pady=5)

        calculator_frame = tk.Frame(left_frame, bg=Theme.BG_WHITE)
        calculator_frame.pack(fill=tk.BOTH, expand=True)

        self.calculator_frame = calculator_frame
        self.render_selected_calculator(calculator_frame)
        self.build_standard_calculator(right_frame)

    def render_selected_calculator(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        calc_type = self.calculator_type.get()
        if calc_type == "Feed Cost":
            self.build_feed_cost_calculator(frame)
        elif calc_type == "Profit":
            self.build_profit_calculator(frame)
        elif calc_type == "BMI":
            self.build_bmi_calculator(frame)

    def create_input_row(self, parent, label_text, entry_var):
        row = tk.Frame(parent, bg=Theme.BG_WHITE)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text=label_text, bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK, width=25, anchor='w', font=Theme.get_font()).pack(side=tk.LEFT, padx=10)
        entry = tk.Entry(row, textvariable=entry_var, width=20, font=Theme.get_font())
        entry.pack(side=tk.LEFT)
        return entry

    def build_feed_cost_calculator(self, parent):
        self.feed_animals_var = tk.StringVar()
        self.feed_per_animal_var = tk.StringVar()
        self.feed_cost_per_lb_var = tk.StringVar()
        self.feed_days_var = tk.StringVar()

        frame = tk.LabelFrame(parent, text="Feed Cost Calculator", font=Theme.get_font(14, "bold"), bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK)
        frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_input_row(frame, "Number of Animals:", self.feed_animals_var)
        self.create_input_row(frame, "Feed per Animal (lbs/day):", self.feed_per_animal_var)
        self.create_input_row(frame, "Cost per lb ($):", self.feed_cost_per_lb_var)
        self.create_input_row(frame, "Days:", self.feed_days_var)

        tk.Button(
            frame,
            text="Calculate Feed Cost",
            command=self.calculate_feed_cost,
            bg=Theme.PRIMARY_GREEN,
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(12, "bold"),
            padx=10, pady=5
        ).pack(pady=5)

        self.feed_result = tk.Label(frame, text="Total Feed Cost: ₦0.00", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK, font=Theme.get_font(14, "bold"))
        self.feed_result.pack(pady=5)

    def build_profit_calculator(self, parent):
        self.sale_price_var = tk.StringVar()
        self.purchase_cost_var = tk.StringVar()
        self.total_feed_cost_var = tk.StringVar()
        self.vet_cost_var = tk.StringVar()
        self.other_expenses_var = tk.StringVar()

        frame = tk.LabelFrame(parent, text="Profit Calculator", font=Theme.get_font(14, "bold"), bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK)
        frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_input_row(frame, "Sale Price (₦):", self.sale_price_var)
        self.create_input_row(frame, "Purchase Cost (₦):", self.purchase_cost_var)
        self.create_input_row(frame, "Feed Cost (₦):", self.total_feed_cost_var)
        self.create_input_row(frame, "Veterinary Cost (₦):", self.vet_cost_var)
        self.create_input_row(frame, "Other Expenses (₦):", self.other_expenses_var)

        tk.Button(
            frame,
            text="Calculate Profit",
            command=self.calculate_profit,
            bg="#4285F4",
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(12, "bold"),
            padx=10, pady=5
        ).pack(pady=5)

        self.profit_result = tk.Label(frame, text="Net Profit: ₦0.00", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK, font=Theme.get_font(14, "bold"))
        self.profit_result.pack(pady=5)

    def build_bmi_calculator(self, parent):
        self.bmi_weight_var = tk.StringVar()
        self.bmi_height_var = tk.StringVar()

        frame = tk.LabelFrame(parent, text="Livestock BMI Calculator", font=Theme.get_font(14, "bold"), bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK)
        frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_input_row(frame, "Weight (kg):", self.bmi_weight_var)
        self.create_input_row(frame, "Height (cm):", self.bmi_height_var)

        tk.Button(
            frame,
            text="Calculate BMI",
            command=self.calculate_bmi,
            bg='ORANGE',
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(12, "bold"),
            padx=10, pady=5
        ).pack(pady=5)

        self.bmi_result = tk.Label(frame, text="BMI: 0.00", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK, font=Theme.get_font(14, "bold"))
        self.bmi_result.pack(pady=5)

    def build_standard_calculator(self, frame):
        tk.Label(frame, text="STANDARD CALCULATOR", font=Theme.get_font(14, "bold"), bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(pady=10)
        self.calc_entry = tk.Entry(frame, font=Theme.get_font(20), justify="right")
        self.calc_entry.pack(padx=10, pady=20, fill=tk.X)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"]
        ]

        for row_values in buttons:
            row = tk.Frame(frame, bg=Theme.BG_LIGHT_GRAY)
            row.pack(padx=10, pady=2, fill=tk.X)
            for val in row_values:
                b = tk.Button(
                    row, text=val, font=("consolas", 12), width=10, height=3,
                    bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                    command=lambda v=val: self.evaluate_calculator_input(v)
                )
                b.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)

    def evaluate_calculator_input(self, value):
        if value == "=":
            try:
                result = eval(self.calc_entry.get())
                self.calc_entry.delete(0, tk.END)
                self.calc_entry.insert(0, str(result))
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
        else:
            self.calc_entry.insert(tk.END, value)

    def calculate_feed_cost(self):
        try:
            animals = float(self.feed_animals_var.get() or 0)
            feed_per_animal = float(self.feed_per_animal_var.get() or 0)
            cost_per_lb = float(self.feed_cost_per_lb_var.get() or 0)
            days = float(self.feed_days_var.get() or 0)
            total_cost = animals * feed_per_animal * cost_per_lb * days
            self.feed_result.config(text=f"Total Feed Cost: ₦{total_cost:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def calculate_profit(self):
        try:
            sale_price = float(self.sale_price_var.get() or 0)
            purchase_cost = float(self.purchase_cost_var.get() or 0)
            feed_cost = float(self.total_feed_cost_var.get() or 0)
            vet_cost = float(self.vet_cost_var.get() or 0)
            other_expenses = float(self.other_expenses_var.get() or 0)

            total_expenses = purchase_cost + feed_cost + vet_cost + other_expenses
            net_profit = sale_price - total_expenses
            self.profit_result.config(text=f"Net Profit: ₦{net_profit:.2f}")

            if net_profit > 0:
                self.profit_result.config(fg=Theme.SUCCESS_GREEN)
            elif net_profit < 0:
                self.profit_result.config(fg=Theme.ERROR_RED)
            else:
                self.profit_result.config(fg=Theme.TEXT_DARK)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def calculate_bmi(self):
        try:
            weight = float(self.bmi_weight_var.get() or 0)
            height = float(self.bmi_height_var.get() or 0)
            if height == 0:
                messagebox.showerror("Error", "Height cannot be zero")
                return
            bmi = (weight / (height * height)) * 703
            self.bmi_result.config(text=f"BMI: {bmi:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
