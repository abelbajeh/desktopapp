import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import os

import datamanager
from theme import Theme

class ProfilePage:
    def __init__(self, parent, data_manager):
        self.parent = parent
        self.data_manager = data_manager
        self.profile_entries = {}
        self.profile_image_path = self.data_manager.get_profile().get("image", "default_profile.png")
        self.image_label = None

    def show(self):
        """Display the profile management page"""
        self.clear_content()
        content = self.create_scrollable_frame()

        # Header
        header_frame = tk.Frame(content, bg=Theme.BG_WHITE)
        header_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(
            header_frame,
            text="👤 My Profile",
            font=Theme.get_font(24, "bold"),
            bg=Theme.BG_WHITE,
            fg=Theme.TEXT_DARK
        ).pack(anchor="w")

        # Image and Form Container
        top_frame = tk.Frame(content, bg=Theme.BG_WHITE)
        top_frame.pack(fill=tk.BOTH, padx=20, pady=10)

        # Profile form
        form_frame = tk.LabelFrame(
            top_frame,
            text="Farm Information",
            font=Theme.get_font(Theme.FONT_SIZE_LARGE, "bold"),
            bg=Theme.BG_WHITE,
            fg=Theme.TEXT_DARK,
            bd=1,
            relief="solid",
        )
        form_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=150)

        profile_data = self.data_manager.get_profile()
        fields = [
            ("Name", "name"),
            ("Farm Name", "farm_name"),
            ("Location", "location"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("Established", "established"),
            ("Total Area", "total_area")
        ]

        for label, key in fields:
            row_frame = tk.Frame(form_frame, bg=Theme.BG_WHITE)
            row_frame.pack(fill=tk.X, padx=50, pady=5)

            tk.Label(
                row_frame,
                text=f"{label}:",
                width=15,
                anchor="w",
                bg=Theme.BG_WHITE,
                fg=Theme.TEXT_DARK,
                font=Theme.get_font(Theme.FONT_SIZE_NORMAL)
            ).pack(side=tk.LEFT)

            entry = tk.Entry(
                row_frame,
                font=Theme.get_font(Theme.FONT_SIZE_NORMAL),
                width=60,
                bg=Theme.BG_LIGHT_GRAY,
                fg=Theme.TEXT_DARK,
                relief="solid",
                bd=1
            )
            entry.pack(side=tk.LEFT, padx=(10, 0))
            entry.insert(0, profile_data.get(key, ""))

            self.profile_entries[key] = entry

        # Buttons
        button_frame = tk.Frame(form_frame, bg=Theme.BG_WHITE)
        button_frame.pack(fill=tk.X, padx=150, pady=20)

        save_button = tk.Button(
            button_frame,
            text="💾 Save Changes",
            command=self.save_profile,
            bg=Theme.PRIMARY_GREEN,
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(Theme.FONT_SIZE_NORMAL, "bold"),
            padx=20,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        save_button.pack(side=tk.LEFT, padx=(0, 10))

        reset_button = tk.Button(
            button_frame,
            text="🔁 Reset",
            command=self.reset_profile,
            bg=Theme.DARK_GREEN,
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(Theme.FONT_SIZE_NORMAL, "bold"),
            padx=20,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        reset_button.pack(side=tk.LEFT)

        # Image section
        image_frame = tk.Frame(top_frame, bg=Theme.BG_WHITE)
        image_frame.pack(side=tk.TOP, padx=200)

        self.image_label = tk.Label(image_frame, bg=Theme.BG_WHITE, cursor="hand2")
        self.image_label.pack(pady=5)
        self.display_profile_image()

        self.image_label.bind("<Button-1>", lambda e: self.select_image())

        tk.Label(
            image_frame,
            text="Click image to upload",
            font=Theme.get_font(Theme.FONT_SIZE_SMALL),
            bg=Theme.BG_WHITE,
            fg=Theme.TEXT_GRAY
        ).pack()

    def display_profile_image(self):
        try:
            image = Image.open(self.profile_image_path).convert("RGBA")
        except Exception:
            image = Image.open("default_profile.png").convert("RGBA")

        size = 160
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.ANTIALIAS

        image = image.resize((size, size), resample)

        # Create circular mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        circular_image = Image.new("RGBA", (size, size))
        circular_image.paste(image, (0, 0), mask=mask)

        photo = ImageTk.PhotoImage(circular_image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference

    def select_image(self):
        old_path = self.profile_image_path if self.profile_image_path != "default_profile.png" else None

        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if file_path:
            self.profile_image_path = file_path
            self.display_profile_image()
            if old_path and os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except Exception:
                    pass

    def save_profile(self):
        profile_data = {key: entry.get() for key, entry in self.profile_entries.items()}
        profile_data["image"] = self.profile_image_path
        self.data_manager.update_profile(profile_data)
        messagebox.showinfo("Success", "Profile updated successfully!")

    def reset_profile(self):
        profile_data = self.data_manager.get_profile()
        self.profile_image_path = profile_data.get("image", "default_profile.png")
        self.display_profile_image()
        for key, entry in self.profile_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, profile_data.get(key, ""))

    def create_scrollable_frame(self):
        canvas = tk.Canvas(self.parent, bg=Theme.BG_WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Theme.BG_WHITE)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="right", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
