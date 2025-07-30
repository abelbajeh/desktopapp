"""
Summary cards module for the Dashboard App
Contains the SummaryCards class for displaying key metrics
"""

import tkinter as tk
from tkinter import ttk
from theme import Theme
from utils import DataGenerator, Colors


class SummaryCards:
    """Summary cards component for displaying key metrics"""

    def __init__(self, parent):
        self.parent = parent
        self.cards_data = []
        self.create_cards()

    def create_cards(self):
        """Create the summary cards container and individual cards"""
        # Main container frame
        self.cards_frame = tk.Frame(
            self.parent,
            bg=Theme.BG_WHITE
        )
        self.cards_frame.pack(fill=tk.X, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_MEDIUM)

        # Generate data
        self.generate_card_data()

        # Create individual cards
        self.create_individual_cards()

    def generate_card_data(self):
        """Generate random data for cards"""
        self.cards_data = [
            {
                "title": "Total Livestock",
                "value": DataGenerator.format_number(DataGenerator().generate_livestock_count()),
                "subtitle": "Active Animals",
                "icon": "🐄",
                "color": Theme.PRIMARY_GREEN
            },
            {
                "title": "Total Revenue",
                "value": DataGenerator.format_currency(DataGenerator().generate_revenue()),
                "subtitle": "This Month",
                "icon": "💰",
                "color": Theme.DARK_GREEN
            },
            {
                "title": "Herd Health",
                "value": DataGenerator.format_percentage(DataGenerator().generate_health_percentage()),
                "subtitle": "Overall Status",
                "icon": "❤️",
                "color": Theme.PRIMARY_GREEN,
                "has_progress": True,
                "progress_value": DataGenerator().generate_health_percentage()
            },
            {
                "title": "Standing Stock",
                "value": DataGenerator.format_number(DataGenerator.generate_standing_stock()),
                "subtitle": "Available Units",
                "icon": "📦",
                "color": Theme.LIGHT_GREEN
            }
        ]

    def create_individual_cards(self):
        """Create individual summary cards"""
        for i, card_data in enumerate(self.cards_data):
            self.create_card(card_data, i)

    def create_card(self, card_data, index):
        """Create a single summary card"""
        # Card container
        card_frame = tk.Frame(
            self.cards_frame,
            **Theme.get_card_style(),
            height=Theme.CARD_HEIGHT
        )
        card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=Theme.MARGIN_MEDIUM)
        card_frame.pack_propagate(False)

        # Card content container
        content_frame = tk.Frame(
            card_frame,
            bg=Theme.CARD_BG
        )
        content_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)

        # Top section (icon and title)
        top_frame = tk.Frame(content_frame, bg=Theme.CARD_BG)
        top_frame.pack(fill=tk.X)

        # Icon
        icon_label = tk.Label(
            top_frame,
            text=card_data["icon"],
            bg=Theme.CARD_BG,
            font=Theme.get_font(Theme.FONT_SIZE_LARGE)
        )
        icon_label.pack(side=tk.LEFT)

        # Title
        title_label = tk.Label(
            top_frame,
            text=card_data["title"],
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_GRAY,
            font=Theme.get_font(Theme.FONT_SIZE_SMALL),
            anchor="w"
        )
        title_label.pack(side=tk.LEFT, padx=(Theme.PADDING_MEDIUM, 0))

        # Value section
        value_frame = tk.Frame(content_frame, bg=Theme.CARD_BG)
        value_frame.pack(fill=tk.X, pady=(Theme.PADDING_MEDIUM, 0))

        value_label = tk.Label(
            value_frame,
            text=card_data["value"],
            bg=Theme.CARD_BG,
            fg=card_data["color"],
            font=Theme.get_font(Theme.FONT_SIZE_XLARGE, "bold"),
            anchor="w"
        )
        value_label.pack(side=tk.LEFT)

        # Progress bar for health card
        if card_data.get("has_progress", False):
            self.create_progress_bar(content_frame, card_data["progress_value"])

        # Subtitle
        subtitle_label = tk.Label(
            content_frame,
            text=card_data["subtitle"],
            **Theme.get_subtitle_style(),
            anchor="w"
        )
        subtitle_label.pack(side=tk.BOTTOM, anchor="w")

        # Hover effects
        self.add_hover_effects(card_frame)

    def create_progress_bar(self, parent, value):
        """Create progress bar for health card"""
        progress_frame = tk.Frame(parent, bg=Theme.CARD_BG)
        progress_frame.pack(fill=tk.X, pady=(Theme.PADDING_SMALL, 0))

        # Progress bar background
        progress_bg = tk.Frame(
            progress_frame,
            bg=Theme.BG_GRAY,
            height=8
        )
        progress_bg.pack(fill=tk.X)

        # Progress bar fill
        progress_width = int((value / 100) * 200)  # Max width of 200px
        progress_fill = tk.Frame(
            progress_bg,
            bg=Colors.get_progress_color(value),
            height=8,
            width=progress_width
        )
        progress_fill.pack(side=tk.LEFT)

    def add_hover_effects(self, card_frame):
        """Add hover effects to cards"""

        def on_enter(event):
            card_frame.config(highlightbackground=Theme.PRIMARY_GREEN)

        def on_leave(event):
            card_frame.config(highlightbackground=Theme.CARD_BORDER)

        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)

        # Bind to all child widgets as well
        for child in card_frame.winfo_children():
            self.bind_hover_to_children(child, on_enter, on_leave)

    def bind_hover_to_children(self, widget, on_enter, on_leave):
        """Recursively bind hover events to child widgets"""
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

        for child in widget.winfo_children():
            self.bind_hover_to_children(child, on_enter, on_leave)

    def refresh_data(self):
        """Refresh card data with new random values"""
        # Clear existing cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Regenerate data and create new cards
        self.generate_card_data()
        self.create_individual_cards()

    def get_frame(self):
        """Get the cards frame"""
        return self.cards_frame

    def create_scrollable_frame(self):
        """Create a scrollable frame inside content_frame"""
        canvas = tk.Canvas(self.content_frame, bg=Theme.BG_WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Theme.BG_WHITE)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame
