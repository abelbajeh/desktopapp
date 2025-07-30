import tkinter as tk
from tkinter import messagebox
import webbrowser
import json
import os
from theme import Theme
from sidebar import Sidebar
from summary_cards import SummaryCards
from charts import Charts
from datamanager import DataManager
from profile import ProfilePage
from livestock_inventory import LivestockInventoryApp
from calculator_page import CalculatorPage
from ai_assistant_page import AIAssistantPage  # ✅ AI Assistant Page Import
from sales_page import SalesPage
import json
CONFIG_FILE = "config.json"
data = "livestock_data.json"
class DashboardApp:
    def __init__(self):
        self.root = tk.Tk()
        self.config = self.load_config()
        self.dark_mode = self.config.get("dark_mode", False)

        if self.dark_mode:
            Theme.use_dark_mode()
        else:
            Theme.use_light_mode()

        self.setup_window()
        self.current_page = "Dashboard"
        self.create_main_layout()
        self.create_menu_bar()
        self.data_manager = DataManager()


    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"dark_mode": self.dark_mode}, f)

    def setup_window(self):
        self.root.title("Farm Dashboard - Livestock Management System")
        self.root.geometry(f"{Theme.WINDOW_MIN_WIDTH}x{Theme.WINDOW_MIN_HEIGHT}")
        self.root.minsize(Theme.WINDOW_MIN_WIDTH, Theme.WINDOW_MIN_HEIGHT)
        self.root.configure(bg=Theme.BG_WHITE)
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_main_layout(self):
        self.main_container = tk.Frame(self.root, bg=Theme.BG_WHITE)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        self.sidebar = Sidebar(self.main_container, self.on_menu_click)
        self.content_frame = tk.Frame(self.main_container, bg=Theme.BG_WHITE)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.load_dashboard_content()

    def get_data(self, data):
        if os.path.exists(data):
            with open(data, 'r') as f:
                Json_file = json.load(f)
            return Json_file
        return {}
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh Data", command=self.refresh_all_data)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Dashboard", command=lambda: self.on_menu_click("Dashboard"))
        view_menu.add_command(label="My Profile", command=lambda: self.on_menu_click("My Profile"))
        view_menu.add_command(label="Sales", command=lambda: self.on_menu_click("Sales"))
        view_menu.add_command(label="Livestock", command=lambda: self.on_menu_click("Livestock"))
        view_menu.add_command(label="Calculator", command=lambda: self.on_menu_click("Calculator"))
        view_menu.add_command(label="AI Assistant", command=lambda: self.on_menu_click("AI Assistant"))  # ✅ Fixed
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_command(label="Contact Us", command=self.open_contact_link)

    def open_contact_link(self):
        webbrowser.open("http://tronicstart.kesug.com")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        Theme.use_dark_mode() if self.dark_mode else Theme.use_light_mode()
        self.save_config()
        self.root.configure(bg=Theme.BG_WHITE)
        self.clear_content_frame()
        self.main_container.destroy()
        self.create_main_layout()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_dashboard_content(self):
        self.clear_content_frame()
        self.create_page_header("Dashboard", "🏠", "Welcome to your farm management dashboard")
        self.summary_cards = SummaryCards(self.content_frame)
        self.charts = Charts(self.content_frame)
        self.create_refresh_section()

    def create_refresh_section(self):
        refresh_frame = tk.Frame(self.content_frame, bg=Theme.BG_WHITE)
        refresh_frame.pack(fill=tk.X, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_MEDIUM)

        refresh_button = tk.Button(
            refresh_frame,
            text="🔄 Refresh Data",
            bg=Theme.PRIMARY_GREEN,
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM, "bold"),
            relief="flat",
            bd=0,
            padx=Theme.PADDING_LARGE,
            pady=Theme.PADDING_MEDIUM,
            cursor="hand2",
            command=self.refresh_all_data
        )
        refresh_button.pack(side=tk.RIGHT)
        refresh_button.bind("<Enter>", lambda e: refresh_button.config(bg=Theme.DARK_GREEN))
        refresh_button.bind("<Leave>", lambda e: refresh_button.config(bg=Theme.PRIMARY_GREEN))

    def create_page_header(self, title, icon, description):
        header_frame = tk.Frame(self.content_frame, bg=Theme.BG_WHITE)
        header_frame.pack(fill=tk.X, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_LARGE)

        title_frame = tk.Frame(header_frame, bg=Theme.BG_WHITE)
        title_frame.pack(fill=tk.X)

        tk.Label(title_frame, text=icon, bg=Theme.BG_WHITE,
                 font=Theme.get_font(Theme.FONT_SIZE_TITLE)).pack(side=tk.LEFT)

        tk.Label(title_frame, text=title, bg=Theme.BG_WHITE, fg=Theme.TEXT_DARK,
                 font=Theme.get_font(Theme.FONT_SIZE_TITLE, "bold")).pack(side=tk.LEFT, padx=(Theme.PADDING_MEDIUM, 0))

        tk.Label(header_frame, text=description, bg=Theme.BG_WHITE,
                 fg=Theme.TEXT_GRAY, font=Theme.get_font(Theme.FONT_SIZE_MEDIUM)).pack(anchor="w", pady=(Theme.PADDING_SMALL, 0))

    def on_menu_click(self, menu_item):
        self.current_page = menu_item
        self.clear_content_frame()

        if menu_item == "Dashboard":
            self.load_dashboard_content()
        elif menu_item == "My Profile":
            ProfilePage(self.content_frame, self.data_manager).show()
        elif menu_item == "Sales":
            SalesPage(self.content_frame, self.data_manager)
        elif menu_item == "Livestock":
            LivestockInventoryApp(self.content_frame)
        elif menu_item == "Calculator":
            CalculatorPage(self.content_frame)
        elif menu_item == "AI Assistant":
            AIAssistantPage(self.content_frame)  # ✅ Fix: store reference
        else:
            self.load_placeholder_content(menu_item)

    def load_placeholder_content(self, title):
        self.clear_content_frame()
        self.create_page_header(title, "ℹ️", f"This is the {title.lower()} page")

    def refresh_all_data(self):
        if self.current_page == "Dashboard":
            if hasattr(self, 'summary_cards'):
                self.summary_cards.refresh_data()
            if hasattr(self, 'charts'):
                self.charts.refresh_charts()
            self.show_status_message("Data refreshed successfully!", "success")
        else:
            self.show_status_message("Switch to Dashboard to refresh data", "info")

    def show_status_message(self, message, msg_type="info"):
        if msg_type == "success":
            messagebox.showinfo("Success", message)
        elif msg_type == "error":
            messagebox.showerror("Error", message)
        else:
            messagebox.showinfo("Info", message)

    def export_report(self):
        messagebox.showinfo("Export", "Report export functionality will be added soon.")

    def show_about(self):
        messagebox.showinfo("About", "Farm Dashboard v1.0\nBuilt with Tkinter")

    def show_user_guide(self):
        messagebox.showinfo("User Guide", "1. Dashboard\n2. My Profile\n3. Sales\n...")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    try:
        app = DashboardApp()
        app.run()
    except Exception as e:
        print("Startup error:", e)
        messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    main()
