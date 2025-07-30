class Theme:
    # Color palettes (light)
    LIGHT_COLORS = {
        "PRIMARY_GREEN": "#2ECC71",
        "LIGHT_GREEN": "#58D68D",
        "DARK_GREEN": "#27AE60",

        # Additional colors for better UI
        "SECONDARY_BLUE": "#3498DB",
        "LIGHT_BLUE": "#5DADE2",
        "DARK_BLUE": "#2980B9",

        "ORANGE": "#F39C12",
        "LIGHT_ORANGE": "#F7DC6F",
        "DARK_ORANGE": "#E67E22",

        "PURPLE": "#9B59B6",
        "LIGHT_PURPLE": "#BB8FCE",
        "DARK_PURPLE": "#8E44AD",

        "DANGER_RED": "#E74C3C",
        "LIGHT_RED": "#F1948A",
        "DARK_RED": "#C0392B",

        "SUCCESS_GREEN": "#27AE60",
        "WARNING_YELLOW": "#F1C40F",
        "INFO_BLUE": "#3498DB",

        "BG_WHITE": "#FFFFFF",
        "BG_LIGHT_GRAY": "#F8F9FA",
        "BG_GRAY": "#E9ECEF",
        "BG_DARK_GRAY": "#6C757D",

        "TEXT_DARK": "#2C3E50",
        "TEXT_GRAY": "#6C757D",
        "TEXT_LIGHT": "#ADB5BD",
        "TEXT_WHITE": "#FFFFFF",

        "CARD_BG": "#FFFFFF",
        "CARD_BORDER": "#E9ECEF",
        "CARD_SHADOW": "#00000010",
    }

    # Dark mode palette
    DARK_COLORS = {
        "PRIMARY_GREEN": "#27AE60",
        "LIGHT_GREEN": "#2ECC71",
        "DARK_GREEN": "#1E8449",

        # Additional colors for better UI (dark mode)
        "SECONDARY_BLUE": "#2980B9",
        "LIGHT_BLUE": "#3498DB",
        "DARK_BLUE": "#1F618D",

        "ORANGE": "#E67E22",
        "LIGHT_ORANGE": "#F39C12",
        "DARK_ORANGE": "#D35400",

        "PURPLE": "#8E44AD",
        "LIGHT_PURPLE": "#9B59B6",
        "DARK_PURPLE": "#7D3C98",

        "DANGER_RED": "#C0392B",
        "LIGHT_RED": "#E74C3C",
        "DARK_RED": "#A93226",

        "SUCCESS_GREEN": "#1E8449",
        "WARNING_YELLOW": "#D4AC0D",
        "INFO_BLUE": "#2980B9",

        "BG_WHITE": "#1E1E1E",
        "BG_LIGHT_GRAY": "#2C2C2C",
        "BG_GRAY": "#3A3A3A",
        "BG_DARK_GRAY": "#4A4A4A",

        "TEXT_DARK": "#EAECEE",
        "TEXT_GRAY": "#B0B0B0",
        "TEXT_LIGHT": "#888888",
        "TEXT_WHITE": "#FFFFFF",

        "CARD_BG": "#2B2B2B",
        "CARD_BORDER": "#3A3A3A",
        "CARD_SHADOW": "#FFFFFF10",
    }

    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SMALL = 9
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_LARGE = 14
    FONT_SIZE_XLARGE = 16
    FONT_SIZE_TITLE = 18

    # Dimensions
    SIDEBAR_WIDTH = 200
    CARD_HEIGHT = 120
    CARD_PADDING = 20
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 700

    # Spacing
    PADDING_SMALL = 5
    PADDING_MEDIUM = 10
    PADDING_LARGE = 20
    MARGIN_SMALL = 5
    MARGIN_MEDIUM = 10
    MARGIN_LARGE = 20

    # Active theme
    _colors = LIGHT_COLORS

    # Dynamically bind keys to color values
    @classmethod
    def _refresh_colors(cls):
        for key, value in cls._colors.items():
            setattr(cls, key, value)

    @classmethod
    def use_light_mode(cls):
        """Switch to light mode"""
        cls._colors = cls.LIGHT_COLORS
        cls._refresh_colors()

    @classmethod
    def use_dark_mode(cls):
        """Switch to dark mode"""
        cls._colors = cls.DARK_COLORS
        cls._refresh_colors()

    @classmethod
    def get_font(cls, size=None, weight="normal"):
        """Get font tuple for tkinter widgets"""
        font_size = size or cls.FONT_SIZE_NORMAL
        return (cls.FONT_FAMILY, font_size, weight)

    @classmethod
    def get_sidebar_style(cls):
        return {
            'bg': cls.BG_LIGHT_GRAY,
            'width': cls.SIDEBAR_WIDTH,
            'relief': 'flat',
            'bd': 0
        }

    @classmethod
    def get_button_style(cls, active=False):
        if active:
            return {
                'bg': cls.PRIMARY_GREEN,
                'fg': cls.TEXT_WHITE,
                'relief': 'flat',
                'bd': 0,
                'font': cls.get_font(cls.FONT_SIZE_MEDIUM, "bold"),
                'padx': cls.PADDING_LARGE,
                'pady': cls.PADDING_MEDIUM
            }
        else:
            return {
                'bg': cls.BG_LIGHT_GRAY,
                'fg': cls.TEXT_DARK,
                'relief': 'flat',
                'bd': 0,
                'font': cls.get_font(cls.FONT_SIZE_MEDIUM),
                'padx': cls.PADDING_LARGE,
                'pady': cls.PADDING_MEDIUM
            }

    @classmethod
    def get_card_style(cls):
        return {
            'bg': cls.CARD_BG,
            'relief': 'solid',
            'bd': 1,
            'highlightbackground': cls.CARD_BORDER,
            'highlightthickness': 1
        }

    @classmethod
    def get_title_style(cls):
        return {
            'bg': cls.CARD_BG,
            'fg': cls.TEXT_DARK,
            'font': cls.get_font(cls.FONT_SIZE_TITLE, "bold")
        }

    @classmethod
    def get_value_style(cls):
        return {
            'bg': cls.CARD_BG,
            'fg': cls.PRIMARY_GREEN,
            'font': cls.get_font(cls.FONT_SIZE_XLARGE, "bold")
        }

    @classmethod
    def get_subtitle_style(cls):
        return {
            'bg': cls.CARD_BG,
            'fg': cls.TEXT_GRAY,
            'font': cls.get_font(cls.FONT_SIZE_SMALL)
        }

    # Additional style methods for enhanced UI
    @classmethod
    def get_success_button_style(cls):
        return {
            'bg': cls.SUCCESS_GREEN,
            'fg': cls.TEXT_WHITE,
            'relief': 'flat',
            'bd': 0,
            'font': cls.get_font(cls.FONT_SIZE_MEDIUM, "bold"),
            'padx': cls.PADDING_LARGE,
            'pady': cls.PADDING_MEDIUM
        }

    @classmethod
    def get_danger_button_style(cls):
        return {
            'bg': cls.DANGER_RED,
            'fg': cls.TEXT_WHITE,
            'relief': 'flat',
            'bd': 0,
            'font': cls.get_font(cls.FONT_SIZE_MEDIUM, "bold"),
            'padx': cls.PADDING_LARGE,
            'pady': cls.PADDING_MEDIUM
        }

    @classmethod
    def get_info_button_style(cls):
        return {
            'bg': cls.INFO_BLUE,
            'fg': cls.TEXT_WHITE,
            'relief': 'flat',
            'bd': 0,
            'font': cls.get_font(cls.FONT_SIZE_MEDIUM, "bold"),
            'padx': cls.PADDING_LARGE,
            'pady': cls.PADDING_MEDIUM
        }

    @classmethod
    def get_warning_button_style(cls):
        return {
            'bg': cls.WARNING_YELLOW,
            'fg': cls.TEXT_DARK,
            'relief': 'flat',
            'bd': 0,
            'font': cls.get_font(cls.FONT_SIZE_MEDIUM, "bold"),
            'padx': cls.PADDING_LARGE,
            'pady': cls.PADDING_MEDIUM
        }