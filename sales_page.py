import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import random
from theme import Theme


class SalesPage:
    def __init__(self, parent_frame, data_manager=None):
        self.parent_frame = parent_frame
        self.data_manager = data_manager
        self.sales_data = self.load_sales_data()
        self.create_page()

    def load_sales_data(self):
        """Load sales data from JSON file or create sample data"""
        sales_file = "sales_data.json"
        if os.path.exists(sales_file):
            try:
                with open(sales_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Create sample data if file doesn't exist
        return self.create_sample_sales_data()

    def create_sample_sales_data(self):
        """Create sample sales data"""
        sample_data = {
            "sales": [
                {
                    "id": 1,
                    "animal": "Cattle",
                    "price": 500000,
                    "quantity": 5,
                    "date": "2025-06-15",
                    "total": 2500000
                },
                {
                    "id": 2,
                    "animal": "Goat",
                    "price": 200000,
                    "quantity": 10,
                    "date": "2025-06-18",
                    "total": 2000000
                },
                {
                    "id": 3,
                    "animal": "Sheep",
                    "price": 250000,
                    "quantity": 8,
                    "date": "2025-06-20",
                    "total": 2000000
                },
                {
                    "id": 4,
                    "animal": "Chicken",
                    "price": 25000,
                    "quantity": 11,
                    "date": "2025-06-25",
                    "total": 275000
                }
            ]
        }
        self.save_sales_data(sample_data)
        return sample_data

    def save_sales_data(self, data):
        """Save sales data to JSON file"""
        try:
            with open("sales_data.json", 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving sales data: {e}")

    def calculate_totals(self):
        """Calculate total sales, transactions, animals sold, and average sale"""
        sales = self.sales_data.get("sales", [])
        if not sales:
            return 0, 0, 0, 0

        total_sales = sum(sale["total"] for sale in sales)
        total_transactions = len(sales)
        total_animals = sum(sale["quantity"] for sale in sales)
        avg_sale = total_sales / total_transactions if total_transactions > 0 else 0

        return total_sales, total_transactions, total_animals, avg_sale

    def create_page(self):
        """Create the main sales page"""
        self.create_header()
        self.create_summary_cards()
        self.create_content_area()

    def create_header(self):
        """Create page header with title and add sale button"""
        header_frame = tk.Frame(self.parent_frame, bg=Theme.BG_WHITE)
        header_frame.pack(fill=tk.X, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_LARGE)

        # Title
        title_label = tk.Label(
            header_frame,
            text="Sales Dashboard",
            bg=Theme.BG_WHITE,
            fg=Theme.TEXT_DARK,
            font=Theme.get_font(Theme.FONT_SIZE_TITLE, "bold")
        )
        title_label.pack(side=tk.LEFT)

        # Add Sale Button
        add_sale_btn = tk.Button(
            header_frame,
            text="+ Add Sale",
            bg=Theme.PRIMARY_GREEN,
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold"),
            relief="flat",
            bd=0,
            padx=Theme.PADDING_LARGE,
            pady=Theme.PADDING_SMALL,
            cursor="hand2",
            command=self.add_sale_dialog
        )
        add_sale_btn.pack(side=tk.RIGHT)

        # Hover effects
        add_sale_btn.bind("<Enter>", lambda e: add_sale_btn.config(bg=Theme.DARK_GREEN))
        add_sale_btn.bind("<Leave>", lambda e: add_sale_btn.config(bg=Theme.PRIMARY_GREEN))

    def create_summary_cards(self):
        """Create summary cards showing key metrics"""
        cards_frame = tk.Frame(self.parent_frame, bg=Theme.BG_WHITE)
        cards_frame.pack(fill=tk.X, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_MEDIUM)

        total_sales, transactions, animals_sold, avg_sale = self.calculate_totals()

        # Card data
        cards_data = [
            {
                "title": "Total Sales",
                "value": f"₦{total_sales:,}",
                "icon": "💰",
                "color": Theme.PRIMARY_GREEN
            },
            {
                "title": "Transactions",
                "value": str(transactions),
                "icon": "📋",
                "color": Theme.LIGHT_GREEN
            },
            {
                "title": "Animals Sold",
                "value": str(animals_sold),
                "icon": "🐄",
                "color": Theme.DARK_GREEN
            },
            {
                "title": "Avg Sale",
                "value": f"₦{avg_sale:,.0f}",
                "icon": "📈",
                "color": Theme.PRIMARY_GREEN
            }
        ]

        # Create cards
        for i, card_data in enumerate(cards_data):
            card_frame = tk.Frame(
                cards_frame,
                bg=Theme.BG_LIGHT_GRAY,
                relief="flat",
                bd=1
            )
            card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=Theme.PADDING_SMALL)

            # Icon and value
            icon_label = tk.Label(
                card_frame,
                text=card_data["icon"],
                bg=Theme.BG_LIGHT_GRAY,
                font=Theme.get_font(24)
            )
            icon_label.pack(pady=(Theme.PADDING_LARGE, Theme.PADDING_SMALL))

            value_label = tk.Label(
                card_frame,
                text=card_data["value"],
                bg=Theme.BG_LIGHT_GRAY,
                fg=Theme.TEXT_DARK,
                font=Theme.get_font(Theme.FONT_SIZE_LARGE, "bold")
            )
            value_label.pack()

            title_label = tk.Label(
                card_frame,
                text=card_data["title"],
                bg=Theme.BG_LIGHT_GRAY,
                fg=Theme.TEXT_GRAY,
                font=Theme.get_font(Theme.FONT_SIZE_SMALL)
            )
            title_label.pack(pady=(Theme.PADDING_SMALL, Theme.PADDING_LARGE))

    def create_content_area(self):
        """Create the main content area with chart and sales list"""
        content_frame = tk.Frame(self.parent_frame, bg=Theme.BG_WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_MEDIUM)

        # Chart section (left side)
        chart_frame = tk.Frame(content_frame, bg=Theme.BG_LIGHT_GRAY, relief="flat", bd=1)
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, Theme.PADDING_MEDIUM))

        self.create_sales_chart(chart_frame)

        # Sales list section (right side)
        list_frame = tk.Frame(content_frame, bg=Theme.BG_LIGHT_GRAY, relief="flat", bd=1)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_sales_list(list_frame)

    def create_sales_chart(self, parent):
        """Create a simple sales trend chart"""
        # Chart title
        title_label = tk.Label(
            parent,
            text="Sales Trend",
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.TEXT_DARK,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold")
        )
        title_label.pack(pady=Theme.PADDING_MEDIUM)

        # Create canvas for chart
        chart_canvas = tk.Canvas(
            parent,
            bg=Theme.BG_WHITE,
            height=300,
            highlightthickness=0
        )
        chart_canvas.pack(fill=tk.BOTH, expand=True, padx=Theme.PADDING_MEDIUM, pady=Theme.PADDING_MEDIUM)

        # Draw simple line chart
        self.draw_sales_chart(chart_canvas)

    def draw_sales_chart(self, canvas):
        """Draw a simple line chart on the canvas"""
        canvas.update_idletasks()
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1 or height <= 1:
            canvas.after(100, lambda: self.draw_sales_chart(canvas))
            return

        # Chart margins
        margin = 40
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin

        # Get actual sales data for chart
        sales = self.sales_data.get("sales", [])
        if not sales:
            # No data message
            canvas.create_text(width / 2, height / 2, text="No sales data available",
                               fill=Theme.TEXT_GRAY, font=Theme.get_font(Theme.FONT_SIZE_MEDIUM))
            return

        # Sort sales by date and aggregate by date
        sales_by_date = {}
        for sale in sales:
            date = sale["date"]
            if date not in sales_by_date:
                sales_by_date[date] = 0
            sales_by_date[date] += sale["total"]

        # Sort dates and get values
        sorted_dates = sorted(sales_by_date.keys())
        data_points = [sales_by_date[date] / 1000000 for date in sorted_dates]  # Convert to millions
        labels = [date.split('-')[1] + '-' + date.split('-')[2] for date in sorted_dates]  # MM-DD format

        if len(data_points) < 2:
            canvas.create_text(width / 2, height / 2, text="Need at least 2 data points for chart",
                               fill=Theme.TEXT_GRAY, font=Theme.get_font(Theme.FONT_SIZE_MEDIUM))
            return

        # Draw axes
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill=Theme.TEXT_GRAY, width=2)
        canvas.create_line(margin, margin, margin, height - margin, fill=Theme.TEXT_GRAY, width=2)

        # Get max value for scaling
        max_value = max(data_points)
        scale_factor = max_value * 1.1  # Add 10% padding

        # Draw y-axis labels
        for i in range(6):
            y = height - margin - (i * chart_height / 5)
            value = (i * scale_factor / 5)
            canvas.create_text(margin - 15, y, text=f"₦{value:.1f}M", fill=Theme.TEXT_GRAY, font=("Arial", 8))
            canvas.create_line(margin - 3, y, margin + 3, y, fill=Theme.TEXT_GRAY)

        # Draw data line
        if len(data_points) > 1:
            points = []
            for i, point in enumerate(data_points):
                x = margin + (i * chart_width / (len(data_points) - 1))
                y = height - margin - (point * chart_height / scale_factor)
                points.extend([x, y])

                # Draw point
                canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=Theme.PRIMARY_GREEN, outline=Theme.PRIMARY_GREEN,
                                   width=2)

            # Draw line
            if len(points) >= 4:
                canvas.create_line(points, fill=Theme.PRIMARY_GREEN, width=3, smooth=True)

        # Draw x-axis labels
        for i, label in enumerate(labels):
            if i < len(data_points):
                x = margin + (i * chart_width / (len(data_points) - 1))
                canvas.create_text(x, height - margin + 15, text=label, fill=Theme.TEXT_GRAY, font=("Arial", 8))

    def create_sales_list(self, parent):
        """Create the sales list with recent transactions"""
        # List title
        title_label = tk.Label(
            parent,
            text="Recent Sales",
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.TEXT_DARK,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold")
        )
        title_label.pack(pady=Theme.PADDING_MEDIUM)

        # Create scrollable frame
        canvas = tk.Canvas(parent, bg=Theme.BG_LIGHT_GRAY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Theme.BG_LIGHT_GRAY)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Sales list content
        self.create_sales_items(scrollable_frame)

    def create_sales_items(self, parent):
        """Create individual sales items"""
        sales = self.sales_data.get("sales", [])

        if not sales:
            # No sales message
            no_sales_label = tk.Label(
                parent,
                text="No sales records found.\nClick 'Add Sale' to get started!",
                bg=Theme.BG_LIGHT_GRAY,
                fg=Theme.TEXT_GRAY,
                font=Theme.get_font(Theme.FONT_SIZE_MEDIUM),
                justify=tk.CENTER
            )
            no_sales_label.pack(pady=50)
            return

        # Sort sales by date (newest first)
        sorted_sales = sorted(sales, key=lambda x: x["date"], reverse=True)

        for sale in sorted_sales:
            item_frame = tk.Frame(parent, bg=Theme.BG_WHITE, relief="flat", bd=1)
            item_frame.pack(fill=tk.X, padx=Theme.PADDING_MEDIUM, pady=Theme.PADDING_SMALL)

            # Left side - icon and info
            left_frame = tk.Frame(item_frame, bg=Theme.BG_WHITE)
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=Theme.PADDING_MEDIUM,
                            pady=Theme.PADDING_MEDIUM)

            # Icon based on animal type
            icon = self.get_animal_icon(sale["animal"])
            icon_label = tk.Label(
                left_frame,
                text=icon,
                bg=Theme.BG_WHITE,
                font=Theme.get_font(16)
            )
            icon_label.pack(side=tk.LEFT, padx=(0, Theme.PADDING_SMALL))

            # Sale info
            info_frame = tk.Frame(left_frame, bg=Theme.BG_WHITE)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Animal and price
            animal_price = tk.Label(
                info_frame,
                text=f"{sale['animal']} - ₦{sale['price']:,}",
                bg=Theme.BG_WHITE,
                fg=Theme.TEXT_DARK,
                font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold")
            )
            animal_price.pack(anchor="w")

            # Quantity and date
            details = tk.Label(
                info_frame,
                text=f"Quantity: {sale['quantity']} • Date: {sale['date']} • Total: ₦{sale['total']:,}",
                bg=Theme.BG_WHITE,
                fg=Theme.TEXT_GRAY,
                font=Theme.get_font(Theme.FONT_SIZE_SMALL)
            )
            details.pack(anchor="w")

            # Right side - actions
            actions_frame = tk.Frame(item_frame, bg=Theme.BG_WHITE)
            actions_frame.pack(side=tk.RIGHT, padx=Theme.PADDING_MEDIUM, pady=Theme.PADDING_MEDIUM)

            # Edit button
            edit_btn = tk.Button(
                actions_frame,
                text="✏️",
                bg=Theme.BG_WHITE,
                fg=Theme.TEXT_GRAY,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda s=sale: self.edit_sale(s)
            )
            edit_btn.pack(side=tk.RIGHT, padx=Theme.PADDING_SMALL)

            # Delete button
            delete_btn = tk.Button(
                actions_frame,
                text="🗑️",
                bg=Theme.BG_WHITE,
                fg=Theme.TEXT_GRAY,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda s=sale: self.delete_sale(s)
            )
            delete_btn.pack(side=tk.RIGHT)

            # Hover effects for buttons
            edit_btn.bind("<Enter>", lambda e, btn=edit_btn: btn.config(bg=Theme.BG_LIGHT_GRAY))
            edit_btn.bind("<Leave>", lambda e, btn=edit_btn: btn.config(bg=Theme.BG_WHITE))
            delete_btn.bind("<Enter>", lambda e, btn=delete_btn: btn.config(bg=Theme.BG_LIGHT_GRAY))
            delete_btn.bind("<Leave>", lambda e, btn=delete_btn: btn.config(bg=Theme.BG_WHITE))

    def get_animal_icon(self, animal):
        """Get appropriate icon for animal type"""
        icons = {
            "Cattle": "🐄",
            "Goat": "🐐",
            "Sheep": "🐑",
            "Chicken": "🐔",
            "Pig": "🐷",
            "Duck": "🦆"
        }
        return icons.get(animal, "🐾")

    def add_sale_dialog(self):
        """Open dialog to add new sale"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Add New Sale")
        dialog.geometry("400x450")
        dialog.configure(bg=Theme.BG_WHITE)
        dialog.resizable(False, False)

        # Center the dialog
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.grab_set()

        # Form fields
        fields = {}

        # Title
        title_label = tk.Label(
            dialog,
            text="Add New Sale",
            bg=Theme.BG_WHITE,
            fg=Theme.TEXT_DARK,
            font=Theme.get_font(Theme.FONT_SIZE_LARGE, "bold")
        )
        title_label.pack(pady=(20, 10))

        # Animal type
        tk.Label(dialog, text="Animal Type:", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(pady=(10, 5))
        animal_var = tk.StringVar(value="Cattle")
        animal_combo = ttk.Combobox(dialog, textvariable=animal_var, width=30,
                                    values=["Cattle", "Goat", "Sheep", "Chicken", "Pig", "Duck"],
                                    state="readonly")
        animal_combo.pack(pady=5)
        fields["animal"] = animal_var

        # Price
        tk.Label(dialog, text="Price per Unit (₦):", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(pady=(10, 5))
        price_var = tk.StringVar()
        price_entry = tk.Entry(dialog, textvariable=price_var, width=32, font=Theme.get_font(Theme.FONT_SIZE_MEDIUM))
        price_entry.pack(pady=5)
        fields["price"] = price_var

        # Quantity
        tk.Label(dialog, text="Quantity:", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(pady=(10, 5))
        quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(dialog, textvariable=quantity_var, width=32,
                                  font=Theme.get_font(Theme.FONT_SIZE_MEDIUM))
        quantity_entry.pack(pady=5)
        fields["quantity"] = quantity_var

        # Date
        tk.Label(dialog, text="Date (YYYY-MM-DD):", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(pady=(10, 5))
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = tk.Entry(dialog, textvariable=date_var, width=32, font=Theme.get_font(Theme.FONT_SIZE_MEDIUM))
        date_entry.pack(pady=5)
        fields["date"] = date_var

        # Buttons
        button_frame = tk.Frame(dialog, bg=Theme.BG_WHITE)
        button_frame.pack(pady=30)

        save_btn = tk.Button(
            button_frame,
            text="Save Sale",
            bg=Theme.PRIMARY_GREEN,
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self.save_new_sale(fields, dialog)
        )
        save_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.TEXT_DARK,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # Hover effects
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg=Theme.DARK_GREEN))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=Theme.PRIMARY_GREEN))

        # Focus on first field
        price_entry.focus_set()

    def save_new_sale(self, fields, dialog):
        """Save new sale to data"""
        try:
            animal = fields["animal"].get()
            price = int(fields["price"].get())
            quantity = int(fields["quantity"].get())
            date = fields["date"].get()

            # Validate inputs
            if not animal:
                messagebox.showerror("Error", "Please select an animal type.")
                return
            if price <= 0:
                messagebox.showerror("Error", "Price must be greater than 0.")
                return
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0.")
                return

            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")

            total = price * quantity

            # Generate new ID
            existing_ids = [sale["id"] for sale in self.sales_data["sales"]]
            new_id = max(existing_ids) + 1 if existing_ids else 1

            # Create new sale
            new_sale = {
                "id": new_id,
                "animal": animal,
                "price": price,
                "quantity": quantity,
                "date": date,
                "total": total
            }

            self.sales_data["sales"].append(new_sale)
            self.save_sales_data(self.sales_data)

            dialog.destroy()
            self.refresh_page()
            messagebox.showinfo("Success", "Sale added successfully!")

        except ValueError as e:
            messagebox.showerror("Error",
                                 "Please enter valid numbers for price and quantity, and valid date format (YYYY-MM-DD).")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def edit_sale(self, sale):
        """Edit existing sale"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Edit Sale")
        dialog.geometry("400x450")
        dialog.configure(bg=Theme.BG_WHITE)
        dialog.resizable(False, False)

        # Center the dialog
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.grab_set()

        # Form fields
        fields = {}

        # Title
        title_label = tk.Label(
            dialog,
            text="Edit Sale",
            bg=Theme.BG_WHITE,
            fg=Theme.TEXT_DARK,
            font=Theme.get_font(Theme.FONT_SIZE_LARGE, "bold")
        )
        title_label.pack(pady=(20, 10))

        # Animal type
        tk.Label(dialog, text="Animal Type:", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(pady=(10, 5))
        animal_var = tk.StringVar(value=sale["animal"])
        animal_combo = ttk.Combobox(dialog, textvariable=animal_var, width=30,
                                    values=["Cattle", "Goat", "Sheep", "Chicken", "Pig", "Duck"],
                                    state="readonly")
        animal_combo.pack(pady=5)
        fields["animal"] = animal_var

        # Price
        tk.Label(dialog, text="Price per Unit (₦):", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(pady=(10, 5))
        price_var = tk.StringVar(value=str(sale["price"]))
        price_entry = tk.Entry(dialog, textvariable=price_var, width=32, font=Theme.get_font(Theme.FONT_SIZE_MEDIUM))
        price_entry.pack(pady=5)
        fields["price"] = price_var

        # Quantity
        tk.Label(dialog, text="Quantity:", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(pady=(10, 5))
        quantity_var = tk.StringVar(value=str(sale["quantity"]))
        quantity_entry = tk.Entry(dialog, textvariable=quantity_var, width=32,
                                  font=Theme.get_font(Theme.FONT_SIZE_MEDIUM))
        quantity_entry.pack(pady=5)
        fields["quantity"] = quantity_var

        # Date
        tk.Label(dialog, text="Date (YYYY-MM-DD):", bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(pady=(10, 5))
        date_var = tk.StringVar(value=sale["date"])
        date_entry = tk.Entry(dialog, textvariable=date_var, width=32, font=Theme.get_font(Theme.FONT_SIZE_MEDIUM))
        date_entry.pack(pady=5)
        fields["date"] = date_var

        # Buttons
        button_frame = tk.Frame(dialog, bg=Theme.BG_WHITE)
        button_frame.pack(pady=30)

        save_btn = tk.Button(
            button_frame,
            text="Update Sale",
            bg=Theme.PRIMARY_GREEN,
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self.update_sale(sale["id"], fields, dialog)
        )
        save_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.TEXT_DARK,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # Hover effects
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg=Theme.DARK_GREEN))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=Theme.PRIMARY_GREEN))

        # Focus on first field
        price_entry.focus_set()

    def update_sale(self, sale_id, fields, dialog):
        """Update existing sale"""
        try:
            animal = fields["animal"].get()
            price = int(fields["price"].get())
            quantity = int(fields["quantity"].get())
            date = fields["date"].get()

            # Validate inputs
            if not animal:
                messagebox.showerror("Error", "Please select an animal type.")
                return
            if price <= 0:
                messagebox.showerror("Error", "Price must be greater than 0.")
                return
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0.")
                return

            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")

            total = price * quantity

            # Find and update the sale
            for sale in self.sales_data["sales"]:
                if sale["id"] == sale_id:
                    sale["animal"] = animal
                    sale["price"] = price
                    sale["quantity"] = quantity
                    sale["date"] = date
                    sale["total"] = total
                    break

            self.save_sales_data(self.sales_data)

            dialog.destroy()
            self.refresh_page()
            messagebox.showinfo("Success", "Sale updated successfully!")

        except ValueError as e:
            messagebox.showerror("Error",
                                 "Please enter valid numbers for price and quantity, and valid date format (YYYY-MM-DD).")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def refresh_page(self):
        """Refresh the entire page to show updated data"""
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Reload sales data
        self.sales_data = self.load_sales_data()

        # Recreate the page
        self.create_page()

    def delete_sale(self, sale):
        """Delete a sale record"""
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this sale?\n\n"
            f"Animal: {sale['animal']}\n"
            f"Price: ₦{sale['price']:,}\n"
            f"Quantity: {sale['quantity']}\n"
            f"Date: {sale['date']}\n"
            f"Total: ₦{sale['total']:,}",
            icon="warning"
        )

        if result:
            try:
                # Remove the sale from the sales list
                self.sales_data["sales"] = [s for s in self.sales_data["sales"] if s["id"] != sale["id"]]

                # Save the updated data
                self.save_sales_data(self.sales_data)

                # Refresh the page to show updated data
                self.refresh_page()

                # Show success message
                messagebox.showinfo("Success", "Sale deleted successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting the sale: {str(e)}")

        # If user clicked 'No', do nothing