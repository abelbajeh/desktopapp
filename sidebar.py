"""
Sidebar navigation module for the Dashboard App
Contains the Sidebar class with navigation functionality
"""

import tkinter as tk
from tkinter import ttk
from theme import Theme


class Sidebar:
    """Sidebar navigation component"""

    def __init__(self, parent, on_menu_click=None):
        self.parent = parent
        self.on_menu_click = on_menu_click
        self.active_item = "Dashboard"  # Default active item

        # Menu items configuration
        self.menu_items = [
            {"name": "Dashboard", "icon": "🏠"},
            {"name": "My Profile", "icon": "👤"},
            {"name": "Sales", "icon": "💰"},
            {"name": "Livestock", "icon": "🐄"},
            {"name": "Calculator", "icon": "🧮"},
            {"name": "AI Assistant","icon":"🤖"}
        ]

        self.create_sidebar()

    def create_sidebar(self):
        """Create the sidebar frame and navigation items"""
        # Main sidebar frame
        self.sidebar_frame = tk.Frame(
            self.parent,
            **Theme.get_sidebar_style()
        )
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        # Logo/Title section
        self.create_logo_section()

        # Navigation menu
        self.create_navigation_menu()

        # Footer section
        self.create_footer_section()

    def create_logo_section(self):
        """Create the logo/title section at the top"""
        logo_frame = tk.Frame(
            self.sidebar_frame,
            bg=Theme.BG_LIGHT_GRAY,
            height=80
        )
        logo_frame.pack(fill=tk.X, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_LARGE)
        logo_frame.pack_propagate(False)

        # App title
        title_label = tk.Label(
            logo_frame,
            text=self.active_item,
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.PRIMARY_GREEN,
            font=Theme.get_font(Theme.FONT_SIZE_TITLE, "bold")
        )
        title_label.pack(expand=True)

        # Subtitle
        subtitle_label = tk.Label(
            logo_frame,
            text="Livestock Management",
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.TEXT_GRAY,
            font=Theme.get_font(Theme.FONT_SIZE_SMALL)
        )
        subtitle_label.pack()

    def create_navigation_menu(self):
        """Create the navigation menu items"""
        self.nav_frame = tk.Frame(
            self.sidebar_frame,
            bg=Theme.BG_LIGHT_GRAY
        )
        self.nav_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.PADDING_MEDIUM)

        self.menu_buttons = {}

        for item in self.menu_items:
            self.create_menu_button(item)

    def create_menu_button(self, menu_item):
        """Create individual menu button"""
        name = menu_item["name"]
        icon = menu_item["icon"]

        # Button frame for better styling
        button_frame = tk.Frame(
            self.nav_frame,
            bg=Theme.BG_LIGHT_GRAY
        )
        button_frame.pack(fill=tk.X, pady=Theme.MARGIN_SMALL)

        # Menu button
        button = tk.Button(
            button_frame,
            text=f"{icon}  {name}",
            anchor="w",
            command=lambda n=name: self.on_menu_item_click(n),
            cursor="hand2",
            **Theme.get_button_style(name == self.active_item)
        )
        button.pack(fill=tk.X)

        # Store button reference
        self.menu_buttons[name] = button

        # Hover effects
        button.bind("<Enter>", lambda e, b=button, n=name: self.on_button_hover(b, n, True))
        button.bind("<Leave>", lambda e, b=button, n=name: self.on_button_hover(b, n, False))

    def create_footer_section(self):
        """Create footer section with additional info"""
        footer_frame = tk.Frame(
            self.sidebar_frame,
            bg=Theme.BG_LIGHT_GRAY,
            height=60
        )
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_LARGE)
        footer_frame.pack_propagate(False)

        # Version info
        version_label = tk.Label(
            footer_frame,
            text="v1.0.0",
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.TEXT_LIGHT,
            font=Theme.get_font(Theme.FONT_SIZE_SMALL)
        )
        version_label.pack(side=tk.BOTTOM)

        # User info
        user_label = tk.Label(
            footer_frame,
            text="👤 Farm Manager",
            bg=Theme.BG_LIGHT_GRAY,
            fg=Theme.TEXT_GRAY,
            font=Theme.get_font(Theme.FONT_SIZE_SMALL)
        )
        user_label.pack(side=tk.BOTTOM)

    def on_menu_item_click(self, item_name):
        """Handle menu item click"""
        if item_name != self.active_item:
            # Update active item
            old_active = self.active_item
            self.active_item = item_name

            # Update button styles
            self.update_button_styles(old_active, item_name)

            # Call callback if provided
            if self.on_menu_click:
                self.on_menu_click(item_name)

    def update_button_styles(self, old_active, new_active):
        """Update button styles when active item changes"""
        # Update old active button
        if old_active in self.menu_buttons:
            old_button = self.menu_buttons[old_active]
            old_button.config(**Theme.get_button_style(False))

        # Update new active button
        if new_active in self.menu_buttons:
            new_button = self.menu_buttons[new_active]
            new_button.config(**Theme.get_button_style(True))

    def on_button_hover(self, button, name, is_hover):
        """Handle button hover effects"""
        if name != self.active_item:  # Don't change active button
            if is_hover:
                button.config(bg=Theme.BG_GRAY)
            else:
                button.config(bg=Theme.BG_LIGHT_GRAY)

    def get_frame(self):
        """Get the sidebar frame"""
        return self.sidebar_frame

    def set_active_item(self, item_name):
        """Programmatically set active menu item"""
        if item_name in [item["name"] for item in self.menu_items]:
            old_active = self.active_item
            self.active_item = item_name
            self.update_button_styles(old_active, item_name)