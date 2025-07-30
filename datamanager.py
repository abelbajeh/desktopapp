import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os


class DataManager:
    """Manages application data storage"""

    def __init__(self):
        self.data_file = "livestock_data.json"
        self.load_data()

    def load_data(self):
        """Load data from file or create default data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            else:
                self.create_default_data()
        except:
            self.create_default_data()

    def create_default_data(self):
        """Create default application data"""
        self.data = {
            "profile": {
                "name": "John Doe",
                "farm_name": "Green Valley Farm",
                "location": "Iowa, USA",
                "phone": "+1-555-0123",
                "email": "john@greenvalley.com",
                "established": "2015",
                "total_area": "500 acres",
                "profile_image": "default_profile.png"  # New field
            },
            "livestock": [
                {"id": "C001", "type": "Cattle", "breed": "Holstein", "age": 3, "weight": 650, "health": "Good",
                 "location": "Pasture A"},
                {"id": "C002", "type": "Cattle", "breed": "Angus", "age": 2, "weight": 580, "health": "Excellent",
                 "location": "Pasture B"},
                {"id": "S001", "type": "Sheep", "breed": "Merino", "age": 1, "weight": 75, "health": "Good",
                 "location": "Field C"},
                {"id": "P001", "type": "Pig", "breed": "Yorkshire", "age": 1, "weight": 180, "health": "Fair",
                 "location": "Pen 1"},
            ],
            "sales": [
                {"date": "2024-12-15", "animal_id": "C003", "type": "Cattle", "buyer": "Local Butcher", "price": 1200,
                 "weight": 600},
                {"date": "2024-12-10", "animal_id": "S002", "type": "Sheep", "buyer": "Wool Company", "price": 150,
                 "weight": 80},
                {"date": "2024-12-05", "animal_id": "P002", "type": "Pig", "buyer": "Farm Market", "price": 300,
                 "weight": 200},
            ]
        }
        self.save_data()

    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def get_profile(self):
        return self.data.get("profile", {})

    def update_profile(self, profile_data):
        self.data["profile"] = profile_data
        self.save_data()

    def get_profile_image_path(self):
        return self.get_profile().get("profile_image", "default_profile.png")

    def save_profile_image_path(self, path):
        self.data["profile"]["profile_image"] = path
        self.save_data()

    def get_livestock(self):
        return self.data.get("livestock", [])

    def add_animal(self, animal_data):
        self.data["livestock"].append(animal_data)
        self.save_data()

    def update_animal(self, animal_id, animal_data):
        livestock = self.data.get("livestock", [])
        for i, animal in enumerate(livestock):
            if animal.get("id") == animal_id:
                livestock[i] = animal_data
                self.save_data()
                return True
        return False

    def remove_animal(self, animal_id):
        livestock = self.data.get("livestock", [])
        self.data["livestock"] = [animal for animal in livestock if animal.get("id") != animal_id]
        self.save_data()

    def get_sales(self):
        return self.data.get("sales", [])

    def add_sale(self, sale_data):
        self.data["sales"].append(sale_data)
        self.save_data()
