"""
Utilities module for the Dashboard App
Contains helper functions for data generation and formatting
"""

import random
from datetime import datetime, timedelta
import json
import os

l_file = "livestock_data.json"
s_file = "sales_data.json"
class DataGenerator:
    """Class for generating random data for dashboard components"""
    def __init__(self):
        self.ldata = self.get_ldata(l_file)
        self.sdata = self.get_sdata(s_file)

    def get_ldata(self, data):
        if os.path.exists(data):
            with open(data, 'r') as f:
                Json_file = json.load(f)
            return Json_file
        return {}

    def get_sdata(self, data):
        if os.path.exists(data):
            with open(data, "r") as f:
                json_ile = json.load(f)
            return json_ile
        return {}

    # @staticmethod
    def generate_livestock_count(self):
        livestock = self.ldata.get("livestock")
        return len(livestock)

    def generate_revenue(self):

        sales = self.sdata.get("sales")
        cost = 0
        for i in sales:
            cost += i["total"]
        return cost

    def generate_health_percentage(self):
        """Generate health percentage based on actual livestock data"""
        livestock = self.ldata.get("livestock", [])

        if not livestock:
            return 0

        # Count animals by health status
        health_counts = {"Excellent": 0, "Good": 0, "Fair": 0, "Under Observation": 0, "Poor": 0}

        for animal in livestock:
            health_status = animal.get("health", "Unknown")
            if health_status in health_counts:
                health_counts[health_status] += 1

        total_animals = len(livestock)

        # Calculate weighted health percentage
        # Excellent=100%, Good=80%, Fair=60%, Under Observation=40%, Poor=20%
        health_weights = {"Excellent": 100, "Good": 80, "Fair": 60, "Under Observation": 40, "Poor": 20}

        total_weighted_score = 0
        for status, count in health_counts.items():
            total_weighted_score += count * health_weights[status]

        health_percentage = total_weighted_score / total_animals if total_animals > 0 else 0

        return round(health_percentage)

    @staticmethod
    def generate_standing_stock():
        """Generate random standing stock value"""
        return random.randint(80, 200)

    def generate_sales_trend_data(self, months=6):
        """Generate sales trend data from actual JSON file"""
        sales = self.sdata.get("sales", [])

        if not sales:
            return [], []

        # Group sales by month-year
        monthly_sales = {}
        for sale in sales:
            sale_date = datetime.strptime(sale["date"], "%Y-%m-%d")
            month_key = sale_date.strftime("%Y-%m")
            month_name = sale_date.strftime("%b")

            if month_key not in monthly_sales:
                monthly_sales[month_key] = {"name": month_name, "total": 0}

            monthly_sales[month_key]["total"] += sale["total"]

        # Sort by date and get last 'months' entries
        sorted_months = sorted(monthly_sales.items())
        recent_months = sorted_months[-months:] if len(sorted_months) >= months else sorted_months

        months_data = [month_data["name"] for _, month_data in recent_months]
        sales_data = [month_data["total"] for _, month_data in recent_months]

        return months_data, sales_data

    def generate_livestock_distribution(self):
        """Generate livestock distribution data from actual JSON file"""
        livestock = self.ldata.get("livestock", [])

        # Count animals by type
        type_counts = {}
        for animal in livestock:
            animal_type = animal.get("type", "Unknown")
            type_counts[animal_type] = type_counts.get(animal_type, 0) + 1

        # Extract categories and values
        categories = list(type_counts.keys())
        values = list(type_counts.values())

        return categories, values

    @staticmethod
    def format_currency(value):
        """Format value as currency"""
        return f"₦{value:,}"

    @staticmethod
    def format_percentage(value):
        """Format value as percentage"""
        return f"{value}%"

    @staticmethod
    def format_number(value):
        """Format number with commas"""
        return f"{value:,}"


class Colors:
    """Utility class for color management"""

    @staticmethod
    def get_chart_colors():
        """Get color palette for charts"""
        return ['#2ECC71', '#3498DB', '#E74C3C', '#F39C12', '#9B59B6', '#1ABC9C']

    @staticmethod
    def get_progress_color(percentage):
        """Get color based on progress percentage"""
        if percentage >= 90:
            return '#2ECC71'  # Green
        elif percentage >= 70:
            return '#F39C12'  # Orange
        else:
            return '#E74C3C'  # Red