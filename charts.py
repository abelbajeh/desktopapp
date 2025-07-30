"""
Charts module for the Dashboard App
Contains matplotlib charts embedded in Tkinter
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from theme import Theme
from utils import DataGenerator


class Charts:
    """Charts component for displaying data visualizations"""

    def __init__(self, parent):
        self.parent = parent
        self.data_generator = DataGenerator()  # Create instance to use non-static methods
        self.setup_matplotlib_style()
        self.create_charts_container()
        self.create_charts()

    def setup_matplotlib_style(self):
        """Configure matplotlib styling to match app theme"""
        plt.style.use('default')
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Segoe UI', 'Arial', 'sans-serif'],
            'font.size': 9,
            'axes.labelcolor': Theme.TEXT_DARK,
            'axes.edgecolor': Theme.BG_GRAY,
            'axes.linewidth': 0.5,
            'axes.grid': True,
            'axes.grid.axis': 'y',
            'grid.color': Theme.BG_GRAY,
            'grid.linewidth': 0.5,
            'grid.alpha': 0.7,
            'xtick.color': Theme.TEXT_GRAY,
            'ytick.color': Theme.TEXT_GRAY,
            'figure.facecolor': Theme.BG_WHITE,
            'axes.facecolor': Theme.BG_WHITE
        })

    def create_charts_container(self):
        """Create the main container for charts"""
        self.charts_frame = tk.Frame(self.parent, bg=Theme.BG_WHITE)
        self.charts_frame.pack(fill=tk.BOTH, expand=True,
                               padx=Theme.PADDING_LARGE, pady=Theme.PADDING_MEDIUM)

    def create_charts(self):
        """Create both charts side by side"""
        left_frame = tk.Frame(self.charts_frame, bg=Theme.BG_WHITE)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, Theme.PADDING_MEDIUM))

        right_frame = tk.Frame(self.charts_frame, bg=Theme.BG_WHITE)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(Theme.PADDING_MEDIUM, 0))

        self.create_sales_trend_chart(left_frame)
        self.create_livestock_distribution_chart(right_frame)

    def create_sales_trend_chart(self, parent):
        chart_container = self.create_chart_container(parent, "Sales Trend")
        months, sales_data = self.data_generator.generate_sales_trend_data(6)

        fig = Figure(figsize=(6, 4), dpi=100, facecolor=Theme.BG_WHITE)
        ax = fig.add_subplot(111)

        ax.plot(months, sales_data,
                color=Theme.PRIMARY_GREEN,
                linewidth=2.5,
                marker='o',
                markersize=6,
                markerfacecolor=Theme.PRIMARY_GREEN,
                markeredgecolor=Theme.BG_WHITE,
                markeredgewidth=2)

        ax.set_title('Monthly Sales Performance', fontsize=12, fontweight='bold', color=Theme.TEXT_DARK, pad=20)
        ax.set_xlabel('Month', fontsize=10, color=Theme.TEXT_GRAY)
        ax.set_ylabel('Sales (₦)', fontsize=10, color=Theme.TEXT_GRAY)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, p: f'₦{x / 1000000:.1f}M' if x >= 1000000 else f'₦{x / 1000:.0f}K'))

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(Theme.BG_GRAY)
        ax.spines['bottom'].set_color(Theme.BG_GRAY)

        fig.tight_layout(pad=2.0)

        canvas = FigureCanvasTkAgg(fig, chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_livestock_distribution_chart(self, parent):
        chart_container = self.create_chart_container(parent, "Livestock Distribution")
        categories, values = self.data_generator.generate_livestock_distribution()

        fig = Figure(figsize=(6, 4), dpi=100, facecolor=Theme.BG_WHITE)
        ax = fig.add_subplot(111)

        # Use more colors to handle dynamic categories
        colors = [Theme.PRIMARY_GREEN, Theme.LIGHT_GREEN, Theme.DARK_GREEN, '#F39C12', '#9B59B6', '#1ABC9C']
        # Cycle through colors if we have more categories than colors
        chart_colors = [colors[i % len(colors)] for i in range(len(categories))]

        bars = ax.bar(categories, values, color=chart_colors, alpha=0.8, edgecolor=Theme.BG_WHITE, linewidth=1)

        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + max(values) * 0.02,
                    f'{value}', ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color=Theme.TEXT_DARK)

        ax.set_title('Livestock by Category', fontsize=12, fontweight='bold', color=Theme.TEXT_DARK, pad=20)
        ax.set_xlabel('Category', fontsize=10, color=Theme.TEXT_GRAY)
        ax.set_ylabel('Count', fontsize=10, color=Theme.TEXT_GRAY)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(Theme.BG_GRAY)
        ax.spines['bottom'].set_color(Theme.BG_GRAY)

        ax.set_ylim(0, max(values) * 1.2 if values else 1)
        fig.tight_layout(pad=2.0)

        canvas = FigureCanvasTkAgg(fig, chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_chart_container(self, parent, title):
        container = tk.Frame(parent, **Theme.get_card_style())
        container.pack(fill=tk.BOTH, expand=True, pady=Theme.MARGIN_SMALL)

        title_frame = tk.Frame(container, bg=Theme.CARD_BG)
        title_frame.pack(fill=tk.X, padx=Theme.PADDING_LARGE, pady=(Theme.PADDING_LARGE, Theme.PADDING_MEDIUM))

        title_label = tk.Label(
            title_frame,
            text=title,
            **Theme.get_title_style(),
            anchor="w"
        )
        title_label.pack(side=tk.LEFT)

        chart_area = tk.Frame(container, bg=Theme.CARD_BG)
        chart_area.pack(fill=tk.BOTH, expand=True, padx=Theme.PADDING_LARGE, pady=(0, Theme.PADDING_LARGE))

        return chart_area

    def refresh_charts(self):
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
        self.create_charts()

    def get_frame(self):
        return self.charts_frame