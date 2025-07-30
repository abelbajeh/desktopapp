import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar
from theme import Theme
import json
import requests


class AIAssistantPage:
    def __init__(self, parent):
        with open("livestock_data.json", 'r') as file:
            data = json.load(file)
            self.user_name = data["profile"]["name"]
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        self.clear_content()

        self.container = tk.Frame(self.parent, bg=Theme.BG_WHITE)
        self.container.pack(fill=tk.BOTH, expand=True)

        header = tk.Label(
            self.container,
            text=f"How can I help, {self.user_name}?",
            font=Theme.get_font(Theme.FONT_SIZE_TITLE + 6, "bold"),
            bg=Theme.BG_WHITE,
            fg=Theme.PRIMARY_GREEN
        )
        header.pack(pady=(Theme.PADDING_LARGE, Theme.PADDING_MEDIUM))

        chat_frame = tk.Frame(self.container, bg=Theme.BG_WHITE)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.PADDING_LARGE)

        self.canvas = Canvas(chat_frame, bg=Theme.BG_LIGHT_GRAY, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(chat_frame, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.chat_inner = tk.Frame(self.canvas, bg=Theme.BG_LIGHT_GRAY)
        self.canvas.create_window((0, 0), window=self.chat_inner, anchor="nw")

        self.chat_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.typing_effect(f"Hi {self.user_name}, how can I help you today?")

        entry_container = tk.Frame(self.container, bg=Theme.BG_WHITE)
        entry_container.pack(fill=tk.X, padx=Theme.PADDING_LARGE, pady=(10, Theme.PADDING_LARGE))

        self.entry_frame = tk.Frame(entry_container, bg=Theme.BG_GRAY, bd=1)
        self.entry_frame.pack(fill=tk.X, expand=True, padx=0, pady=(0, 0))

        self.user_input = tk.Entry(
            self.entry_frame,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM),
            relief="flat",
            bd=0,
            bg=Theme.BG_GRAY,
            fg=Theme.TEXT_DARK
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10, padx=(10, 5), pady=5)
        self.user_input.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(
            self.entry_frame,
            text="➤",
            command=self.send_message,
            bg=Theme.PRIMARY_GREEN,
            fg=Theme.TEXT_WHITE,
            font=Theme.get_font(Theme.FONT_SIZE_LARGE, "bold"),
            relief="flat",
            width=4
        )
        send_btn.pack(side=tk.RIGHT, padx=(5, 10), pady=5)

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def send_message(self):
        user_message = self.user_input.get().strip()
        if not user_message:
            return

        self.add_chat_bubble(self.user_name, user_message, align="e", source="user")
        self.user_input.delete(0, tk.END)

        try:
            response = self.get_ai_response(user_message)
            self.add_scrolling_response("Assistant", response)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_chat_bubble(self, sender, message, align="w", source="bot"):
        outer = tk.Frame(self.chat_inner, bg=Theme.BG_LIGHT_GRAY)

        if align == "e":
            outer.pack(anchor="e", padx=(600, Theme.PADDING_MEDIUM), pady=(4, 4))
        else:
            outer.pack(anchor="w", padx=(Theme.PADDING_MEDIUM, 200), pady=(4, 4))

        bg_color = Theme.PRIMARY_GREEN if source == "user" else Theme.CARD_BG
        fg_color = Theme.TEXT_WHITE if source == "user" else Theme.TEXT_DARK

        bubble = tk.Label(
            outer,
            text=f"{message}",
            wraplength=500,
            justify="left" if align == "w" else "right",
            bg=bg_color,
            fg=fg_color,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM),
            relief="flat",
            bd=1,
            padx=Theme.PADDING_MEDIUM,
            pady=Theme.PADDING_SMALL
        )
        bubble.pack(side="left" if align == "w" else "right", padx=5, pady=5)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def add_scrolling_response(self, sender, message):
        outer = tk.Frame(self.chat_inner, bg=Theme.BG_LIGHT_GRAY)
        outer.pack(anchor="w", padx=(Theme.PADDING_MEDIUM, 200), pady=(4, 4))

        bg_color = Theme.CARD_BG
        fg_color = Theme.TEXT_DARK

        bubble = tk.Label(
            outer,
            text="",
            wraplength=500,
            justify="left",
            bg=bg_color,
            fg=fg_color,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM),
            relief="flat",
            bd=1,
            padx=Theme.PADDING_MEDIUM,
            pady=Theme.PADDING_SMALL
        )
        bubble.pack(side="left", padx=5, pady=5)

        def type_char(i=0):
            if i <= len(message):
                bubble.config(text=message[:i])
                self.canvas.update_idletasks()
                self.canvas.yview_moveto(1.0)
                bubble.after(30, lambda: type_char(i + 1))

        type_char()

    def typing_effect(self, message):
        sender = "Assistant"
        align = "w"
        source = "bot"

        outer = tk.Frame(self.chat_inner, bg=Theme.BG_LIGHT_GRAY)
        outer.pack(anchor="w", padx=(Theme.PADDING_MEDIUM, 200), pady=(4, 4))

        bg_color = Theme.CARD_BG
        fg_color = Theme.TEXT_DARK

        bubble = tk.Label(
            outer,
            text="",
            wraplength=500,
            justify="left",
            bg=bg_color,
            fg=fg_color,
            font=Theme.get_font(Theme.FONT_SIZE_MEDIUM),
            relief="flat",
            bd=1,
            padx=Theme.PADDING_MEDIUM,
            pady=Theme.PADDING_SMALL
        )
        bubble.pack(side="left", padx=5, pady=5)

        def type_char(i=0):
            if i <= len(message):
                bubble.config(text=message[:i])
                self.canvas.update_idletasks()
                self.canvas.yview_moveto(1.0)
                bubble.after(30, lambda: type_char(i + 1))

        type_char()



    def get_ai_response(self, prompt):
        API_URL = "https://router.huggingface.co/nebius/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }
        prompt= "keep your answers agro related.. if the preceeding statment isnt agricultural or small talk reply:'sorry i cant help---'" + prompt
        payload = {
            "model": "microsoft/phi-4",  # ✅ You MUST specify a model
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print("Error:", response.status_code)
            print(response.text)
            return "An error occurred."

    # Try it
    # print("Bot:", query("Hello! What is agrotech?"))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    Theme.use_dark_mode()
    AIAssistantPage(root)
    root.mainloop()