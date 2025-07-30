import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from theme import Theme

DATA_FILE = "livestock_data.json"

# Set the theme mode here (dark or light)
Theme.use_dark_mode()  # Or Theme.use_light_mode()


class LivestockInventoryApp:
    def __init__(self, root):
        self.root = root
        self.data = self.load_data()
        self.filter_option = tk.StringVar(value="All")
        self.setup_ui()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                json_data = json.load(f)
                return json_data.get("livestock", [])
        return []

    def save_data(self):
        json_data = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                json_data = json.load(f)

        json_data["livestock"] = self.data

        with open(DATA_FILE, "w") as f:
            json.dump(json_data, f, indent=2)

    def get_next_tag_id(self, animal_type, count=1):
        """Generate next available tag ID(s) for given animal type"""
        existing_ids = {animal.get("id", "") for animal in self.data}

        # Get the prefix based on animal type
        prefix_map = {
            "Cattle": "C",
            "Sheep": "S",
            "Goat": "G",
            "Pig": "P",
            "Chicken": "CH",
            "Horse": "H",
            "Duck": "D",
            "Turkey": "T"
        }

        prefix = prefix_map.get(animal_type, animal_type[0].upper())

        # Find the highest existing number for this prefix
        max_num = 0
        for existing_id in existing_ids:
            if existing_id.startswith(prefix):
                try:
                    num = int(existing_id[len(prefix):])
                    max_num = max(max_num, num)
                except ValueError:
                    continue

        # Generate the required number of new IDs
        new_ids = []
        for i in range(count):
            new_ids.append(f"{prefix}{max_num + 1 + i:03d}")

        return new_ids if count > 1 else new_ids[0]

    def setup_ui(self):
        container = tk.Frame(self.root, bg=Theme.BG_LIGHT_GRAY)
        container.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(container, bg=Theme.BG_LIGHT_GRAY)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_frame = tk.Frame(header_frame, bg=Theme.BG_LIGHT_GRAY)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        title = tk.Label(title_frame, text="Livestock Inventory", font=Theme.get_font(Theme.FONT_SIZE_TITLE, "bold"),
                         bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK)
        title.pack(anchor="w")

        control_frame = tk.Frame(header_frame, bg=Theme.BG_LIGHT_GRAY)
        control_frame.pack(side=tk.RIGHT)

        filter_label = tk.Label(control_frame, text="Filter by Species:", bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_GRAY,
                                font=Theme.get_font())
        filter_label.pack(side=tk.LEFT, padx=(0, 5))

        self.filter_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.filter_option,
            values=["All"] + self.get_species(),
            state="readonly",
            font=Theme.get_font(),
            width=20
        )
        self.filter_dropdown.pack(side=tk.LEFT)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        add_btn = tk.Button(
            control_frame,
            text="Add Animal",
            font=Theme.get_font(Theme.FONT_SIZE_NORMAL, "bold"),
            bg=Theme.PRIMARY_GREEN,
            fg=Theme.TEXT_WHITE,
            padx=15,
            pady=5,
            relief="flat",
            cursor="hand2",
            command=self.open_add_window
        )
        add_btn.pack(side=tk.LEFT, padx=(10, 0))

        add_multiple_btn = tk.Button(
            control_frame,
            text="Add Multiple",
            font=Theme.get_font(Theme.FONT_SIZE_NORMAL, "bold"),
            bg=Theme.DARK_GREEN,
            fg=Theme.TEXT_WHITE,
            padx=15,
            pady=5,
            relief="flat",
            cursor="hand2",
            command=self.open_add_multiple_window
        )
        add_multiple_btn.pack(side=tk.LEFT, padx=(10, 0))

        subtitle = tk.Label(
            container,
            text="Manage your herd and individual animal records.",
            font=Theme.get_font(),
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.TEXT_GRAY
        )
        subtitle.pack(anchor="w", padx=22, pady=(0, 10))

        table_frame = tk.Frame(container, bg=Theme.BG_LIGHT_GRAY)
        table_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        columns = (
        "Tag ID", "Species", "Breed", "Age", "Weight", "Health", "Location", "Last Vaccination", "Next Vaccination")

        x_scroll = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        y_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )
        x_scroll.config(command=self.tree.xview)
        y_scroll.config(command=self.tree.yview)

        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=Theme.CARD_BG,
                        foreground=Theme.TEXT_DARK,
                        fieldbackground=Theme.CARD_BG,
                        font=Theme.get_font(),
                        rowheight=28)
        style.configure("Treeview.Heading",
                        font=Theme.get_font(weight="bold"),
                        background=Theme.BG_GRAY,
                        foreground=Theme.TEXT_WHITE)
        style.map("Treeview", background=[("selected", Theme.LIGHT_GREEN)])

        self.tree.tag_configure("evenrow", background=Theme.BG_LIGHT_GRAY)
        self.tree.tag_configure("oddrow", background=Theme.BG_WHITE)
        self.tree.tag_configure("due", background="#ffcccc")

        self.refresh_table()

        button_frame = tk.Frame(container, bg=Theme.BG_LIGHT_GRAY)
        button_frame.pack(pady=10)

        edit_btn = tk.Button(button_frame, text="Edit Selected", bg=Theme.DARK_GREEN, fg=Theme.TEXT_WHITE,
                             font=Theme.get_font(weight="bold"),
                             command=self.edit_selected)
        edit_btn.pack(side=tk.LEFT, padx=10)

        delete_btn = tk.Button(button_frame, text="Delete Selected", bg="#dc3545", fg=Theme.TEXT_WHITE,
                               font=Theme.get_font(weight="bold"),
                               command=self.delete_selected)
        delete_btn.pack(side=tk.LEFT, padx=10)

    def get_species(self):
        species = {animal.get("type") for animal in self.data if animal.get("type")}
        return sorted(species)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        today = datetime.today().date()
        due_found = False

        filter_val = self.filter_option.get()
        filtered_data = self.data if filter_val == "All" else [
            a for a in self.data if a.get("type") == filter_val
        ]

        for index, animal in enumerate(filtered_data):
            next_vac_str = animal.get("next_vaccination", "")
            is_due = False
            try:
                if next_vac_str:
                    next_vac_date = datetime.strptime(next_vac_str, "%Y-%m-%d").date()
                    is_due = next_vac_date <= today
            except:
                pass

            if is_due:
                due_found = True

            row = (
                animal.get("id", ""),
                animal.get("type", ""),
                animal.get("breed", ""),
                animal.get("age", ""),
                animal.get("weight", ""),
                animal.get("health", ""),
                animal.get("location", ""),
                animal.get("last_vaccination", ""),
                animal.get("next_vaccination", "")
            )
            tag = "due" if is_due else ("evenrow" if index % 2 == 0 else "oddrow")
            self.tree.insert("", tk.END, values=row, tags=(tag,))

        if due_found:
            messagebox.showwarning("Vaccination Alert", "Some animals are due for vaccination today or earlier.")

    def open_add_window(self):
        self.open_entry_window("Add Animal", "Save", self.add_entry)

    def open_add_multiple_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Multiple Animals")
        window.geometry("500x700")  # Made taller to accommodate all elements
        window.configure(bg=Theme.BG_LIGHT_GRAY)
        window.grab_set()
        window.resizable(True, True)  # Allow resizing if needed

        # Create a scrollable frame
        canvas = tk.Canvas(window, bg=Theme.BG_LIGHT_GRAY)
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Theme.BG_LIGHT_GRAY)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        # Main content in scrollable frame
        main_frame = scrollable_frame

        # Title
        title_label = tk.Label(main_frame, text="Batch Add Animals",
                               font=Theme.get_font(Theme.FONT_SIZE_TITLE, "bold"),
                               bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK)
        title_label.pack(pady=(0, 10))

        # Number of animals
        count_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        count_frame.pack(fill=tk.X, pady=5)
        tk.Label(count_frame, text="Number of Animals:", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        count_entry = tk.Entry(count_frame, font=Theme.get_font(), width=10)
        count_entry.pack(side=tk.RIGHT)
        count_entry.insert(0, "1")

        # Species
        species_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        species_frame.pack(fill=tk.X, pady=5)
        tk.Label(species_frame, text="Species:", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        species_combo = ttk.Combobox(species_frame,
                                     values=["Cattle", "Sheep", "Goat", "Pig", "Chicken", "Horse", "Duck", "Turkey"],
                                     font=Theme.get_font(), width=20)
        species_combo.pack(side=tk.RIGHT)
        species_combo.set("Cattle")

        # Breed
        breed_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        breed_frame.pack(fill=tk.X, pady=5)
        tk.Label(breed_frame, text="Breed:", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        breed_entry = tk.Entry(breed_frame, font=Theme.get_font(), width=20)
        breed_entry.pack(side=tk.RIGHT)

        # Age range
        age_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        age_frame.pack(fill=tk.X, pady=5)
        tk.Label(age_frame, text="Age Range (months):", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        age_inner_frame = tk.Frame(age_frame, bg=Theme.BG_LIGHT_GRAY)
        age_inner_frame.pack(side=tk.RIGHT)
        age_min_entry = tk.Entry(age_inner_frame, font=Theme.get_font(), width=8)
        age_min_entry.pack(side=tk.LEFT)
        tk.Label(age_inner_frame, text=" to ", bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        age_max_entry = tk.Entry(age_inner_frame, font=Theme.get_font(), width=8)
        age_max_entry.pack(side=tk.LEFT)

        # Weight range
        weight_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        weight_frame.pack(fill=tk.X, pady=5)
        tk.Label(weight_frame, text="Weight Range (kg):", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        weight_inner_frame = tk.Frame(weight_frame, bg=Theme.BG_LIGHT_GRAY)
        weight_inner_frame.pack(side=tk.RIGHT)
        weight_min_entry = tk.Entry(weight_inner_frame, font=Theme.get_font(), width=8)
        weight_min_entry.pack(side=tk.LEFT)
        tk.Label(weight_inner_frame, text=" to ", bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        weight_max_entry = tk.Entry(weight_inner_frame, font=Theme.get_font(), width=8)
        weight_max_entry.pack(side=tk.LEFT)

        # Health status
        health_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        health_frame.pack(fill=tk.X, pady=5)
        tk.Label(health_frame, text="Health Status:", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        health_combo = ttk.Combobox(health_frame,
                                    values=["Excellent", "Good", "Fair", "Under Observation", "Poor"],
                                    state="readonly", font=Theme.get_font(), width=20)
        health_combo.pack(side=tk.RIGHT)
        health_combo.set("Excellent")

        # Location
        location_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        location_frame.pack(fill=tk.X, pady=5)
        tk.Label(location_frame, text="Location:", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        location_entry = tk.Entry(location_frame, font=Theme.get_font(), width=20)
        location_entry.pack(side=tk.RIGHT)

        # Last vaccination
        last_vac_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        last_vac_frame.pack(fill=tk.X, pady=5)
        tk.Label(last_vac_frame, text="Last Vaccination:", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        last_vac_entry = tk.Entry(last_vac_frame, font=Theme.get_font(), width=20)
        last_vac_entry.pack(side=tk.RIGHT)

        # Next vaccination
        next_vac_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        next_vac_frame.pack(fill=tk.X, pady=5)
        tk.Label(next_vac_frame, text="Next Vaccination:", font=Theme.get_font(),
                 bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).pack(side=tk.LEFT)
        next_vac_entry = tk.Entry(next_vac_frame, font=Theme.get_font(), width=20)
        next_vac_entry.pack(side=tk.RIGHT)

        # Batch number option
        batch_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        batch_frame.pack(fill=tk.X, pady=10)
        batch_var = tk.BooleanVar(value=True)
        batch_check = tk.Checkbutton(batch_frame, text="Assign Batch Number", variable=batch_var,
                                     bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK, font=Theme.get_font(),
                                     selectcolor=Theme.BG_WHITE)
        batch_check.pack(side=tk.LEFT)

        batch_entry = tk.Entry(batch_frame, font=Theme.get_font(), width=15)
        batch_entry.pack(side=tk.RIGHT)
        batch_entry.insert(0, f"BATCH_{datetime.now().strftime('%Y%m%d')}")

        # Preview area - made smaller to save space
        preview_frame = tk.LabelFrame(main_frame, text="Preview", bg=Theme.BG_LIGHT_GRAY,
                                      fg=Theme.TEXT_DARK, font=Theme.get_font())
        preview_frame.pack(fill=tk.X, pady=10)  # Changed from fill=tk.BOTH, expand=True

        preview_text = tk.Text(preview_frame, height=6, font=Theme.get_font(size=8),  # Reduced height from 8 to 6
                               bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK)
        preview_scroll = tk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=preview_text.yview)
        preview_text.configure(yscrollcommand=preview_scroll.set)
        preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        def update_preview():
            try:
                count = int(count_entry.get())
                species = species_combo.get()

                if count > 50:
                    preview_text.delete(1.0, tk.END)
                    preview_text.insert(tk.END, "Maximum 50 animals per batch allowed.")
                    return

                tag_ids = self.get_next_tag_id(species, count)
                preview_text.delete(1.0, tk.END)
                preview_text.insert(tk.END, f"Will create {count} {species} animals:\n\n")

                for i, tag_id in enumerate(tag_ids):
                    preview_text.insert(tk.END, f"{i + 1}. Tag ID: {tag_id}\n")

            except ValueError:
                preview_text.delete(1.0, tk.END)
                preview_text.insert(tk.END, "Please enter a valid number of animals.")

        # Update preview when count or species changes
        count_entry.bind('<KeyRelease>', lambda e: update_preview())
        species_combo.bind('<<ComboboxSelected>>', lambda e: update_preview())

        # Preview button
        preview_btn = tk.Button(main_frame, text="Update Preview", command=update_preview,
                                bg=Theme.LIGHT_GREEN, fg=Theme.TEXT_DARK, font=Theme.get_font(),
                                padx=15, pady=3)  # Reduced padding
        preview_btn.pack(pady=5)

        # Initial preview
        update_preview()

        def add_multiple_animals():
            try:
                count = int(count_entry.get())
                if count <= 0 or count > 50:
                    messagebox.showerror("Error", "Please enter a number between 1 and 50.")
                    return

                species = species_combo.get()
                if not species:
                    messagebox.showerror("Error", "Please select a species.")
                    return

                breed = breed_entry.get()
                age_min = float(age_min_entry.get()) if age_min_entry.get() else 12
                age_max = float(age_max_entry.get()) if age_max_entry.get() else age_min
                weight_min = float(weight_min_entry.get()) if weight_min_entry.get() else 50
                weight_max = float(weight_max_entry.get()) if weight_max_entry.get() else weight_min
                health = health_combo.get()
                location = location_entry.get()
                last_vac = last_vac_entry.get()
                next_vac = next_vac_entry.get()

                batch_number = batch_entry.get() if batch_var.get() else ""

                # Generate tag IDs
                tag_ids = self.get_next_tag_id(species, count)

                # Create animals with varied attributes
                import random
                new_animals = []

                for i, tag_id in enumerate(tag_ids):
                    # Vary age and weight within range
                    age = round(random.uniform(age_min, age_max), 1)
                    weight = round(random.uniform(weight_min, weight_max), 1)

                    animal = {
                        "id": tag_id,
                        "type": species,
                        "breed": breed,
                        "age": age,
                        "weight": weight,
                        "health": health,
                        "location": location,
                        "last_vaccination": last_vac,
                        "next_vaccination": next_vac
                    }

                    if batch_number:
                        animal["batch"] = batch_number

                    new_animals.append(animal)

                # Add to data and save to JSON file
                self.data.extend(new_animals)
                self.save_data()  # This saves to livestock_data.json
                self.filter_dropdown['values'] = ["All"] + self.get_species()
                self.refresh_table()

                messagebox.showinfo("Success",
                                    f"Successfully added {count} {species} animals to the database!\nTag IDs: {', '.join(tag_ids[:5])}{'...' if len(tag_ids) > 5 else ''}")
                window.destroy()

            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Buttons frame - ensure it's always visible
        button_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT_GRAY)
        button_frame.pack(pady=20, fill=tk.X)  # Increased top padding

        # Center the buttons
        button_container = tk.Frame(button_frame, bg=Theme.BG_LIGHT_GRAY)
        button_container.pack()

        # Add Animals button
        save_btn = tk.Button(button_container, text="Add Animals", command=add_multiple_animals,
                             bg=Theme.PRIMARY_GREEN, fg=Theme.TEXT_WHITE,
                             font=Theme.get_font(weight="bold"), padx=30, pady=10,
                             relief="flat", cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=10)

        # Cancel button
        cancel_btn = tk.Button(button_container, text="Cancel", command=window.destroy,
                               bg="#dc3545", fg=Theme.TEXT_WHITE,
                               font=Theme.get_font(weight="bold"), padx=30, pady=10,
                               relief="flat", cursor="hand2")
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        window.bind_all("<MouseWheel>", _on_mousewheel)

    def open_entry_window(self, title, button_text, command, initial_values=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("400x500")
        window.configure(bg=Theme.BG_LIGHT_GRAY)
        window.grab_set()

        labels = [
            "Tag ID", "Species", "Breed", "Age", "Weight", "Health",
            "Location", "Last Vaccination (YYYY-MM-DD)", "Next Vaccination (YYYY-MM-DD)"
        ]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(window, text=label + ":", font=Theme.get_font(), bg=Theme.BG_LIGHT_GRAY, fg=Theme.TEXT_DARK).grid(
                row=i, column=0, sticky="e", padx=10, pady=5)

            # Use Combobox for Health field
            if label == "Health":
                entry = ttk.Combobox(
                    window,
                    values=["Excellent", "Good", "Fair", "Under Observation", "Poor"],
                    state="readonly",
                    font=Theme.get_font()
                )
                if initial_values:
                    entry.set(initial_values.get(label, "Excellent"))
                else:
                    entry.set("Excellent")
            else:
                entry = tk.Entry(window, font=Theme.get_font())
                if initial_values:
                    entry.insert(0, initial_values.get(label, ""))
                elif label == "Tag ID" and not initial_values:
                    # Auto-generate tag ID for new entries
                    entry.insert(0, "AUTO")
                    entry.config(state="readonly")

            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = entry

        def wrapped_command():
            command(entries, window)

        tk.Button(window, text=button_text, command=wrapped_command, bg=Theme.PRIMARY_GREEN, fg=Theme.TEXT_WHITE,
                  font=Theme.get_font(weight="bold"), padx=10, pady=5).grid(row=len(labels), columnspan=2, pady=20)

    def add_entry(self, entries, window):
        try:
            tag_id = entries["Tag ID"].get()
            species = entries["Species"].get()

            # Auto-generate tag ID if needed
            if tag_id == "AUTO" or not tag_id:
                tag_id = self.get_next_tag_id(species)

            new_record = {
                "id": tag_id,
                "type": species,
                "breed": entries["Breed"].get(),
                "age": int(entries["Age"].get()),
                "weight": float(entries["Weight"].get()),
                "health": entries["Health"].get(),
                "location": entries["Location"].get(),
                "last_vaccination": entries["Last Vaccination (YYYY-MM-DD)"].get(),
                "next_vaccination": entries["Next Vaccination (YYYY-MM-DD)"].get()
            }
            self.data.append(new_record)
            self.save_data()
            self.filter_dropdown['values'] = ["All"] + self.get_species()
            self.refresh_table()
            window.destroy()
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an entry to delete.")
            return

        confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected entry?")
        if confirm:
            values = self.tree.item(selected_item)["values"]
            tag_id = values[0]
            self.data = [animal for animal in self.data if animal.get("id") != tag_id]
            self.save_data()
            self.filter_dropdown['values'] = ["All"] + self.get_species()
            self.refresh_table()

    def edit_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an entry to edit.")
            return

        values = self.tree.item(selected_item)["values"]
        tag_id = values[0]
        record = next((a for a in self.data if a.get("id") == tag_id), None)
        if not record:
            messagebox.showerror("Error", "Selected record not found.")
            return

        label_map = {
            "Tag ID": "id",
            "Species": "type",
            "Breed": "breed",
            "Age": "age",
            "Weight": "weight",
            "Health": "health",
            "Location": "location",
            "Last Vaccination (YYYY-MM-DD)": "last_vaccination",
            "Next Vaccination (YYYY-MM-DD)": "next_vaccination"
        }
        initial_values = {k: str(record.get(v, "")) for k, v in label_map.items()}

        def save_edit(entries, window):
            try:
                record.update({
                    "id": entries["Tag ID"].get(),
                    "type": entries["Species"].get(),
                    "breed": entries["Breed"].get(),
                    "age": int(entries["Age"].get()),
                    "weight": float(entries["Weight"].get()),
                    "health": entries["Health"].get(),
                    "location": entries["Location"].get(),
                    "last_vaccination": entries["Last Vaccination (YYYY-MM-DD)"].get(),
                    "next_vaccination": entries["Next Vaccination (YYYY-MM-DD)"].get()
                })
                self.save_data()
                self.filter_dropdown['values'] = ["All"] + self.get_species()
                self.refresh_table()
                window.destroy()
            except Exception as e:
                messagebox.showerror("Input Error", f"Invalid input: {e}")

        self.open_entry_window("Edit Animal", "Save Changes", save_edit, initial_values)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Livestock Inventory")
    root.geometry("1200x600")
    app = LivestockInventoryApp(root)
    root.mainloop()