# -*- coding: utf-8 -*-
# theme_manager.py

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtWidgets import QApplication
from enum import Enum
from gui import constants

class ThemeColors(Enum):
    PRIMARY = "#2b2929"
    SECONDARY_BACKGROUND = "#1a1a1a"
    TERTIARY_BACKGROUND = "#262626"
    PRIMARY_BUTTONS = "#3b82f6"  # Changed from red to blue
    HOVER_BUTTONS = "#2563eb"    # Darker blue for hover
    TEXT_PRIMARY = "#d4d4d4"
    BORDER_COLOR = "rgba(82, 82, 82, 0.3)"
    ACCENT_COLOR = "#3b82f6"     # Blue accent color

class Fonts:
    """Central font management"""
    
    @staticmethod
    def get_default(size=constants.DEFAULT_FONT_SIZE, weight=QFont.Weight.Normal):
        font = QFont("Segoe UI", size)
        font.setWeight(weight)
        return font
    
    @staticmethod
    def get_bold(size=constants.DEFAULT_FONT_SIZE):
        return Fonts.get_default(size, QFont.Weight.Bold)

class ThemeManager:
    """Central theme management for the application"""
    
    @staticmethod
    def get_base_stylesheet():
        return f"""
            QWidget {{
                background-color: {ThemeColors.PRIMARY.value};
                color: {ThemeColors.TEXT_PRIMARY.value};
                font-family: 'Segoe UI', sans-serif;
            }}
            
            QPushButton {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
                border: none;
                padding: {constants.BUTTON_PADDING};
                border-radius: {constants.BUTTON_BORDER_RADIUS}px;
                color: white;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {ThemeColors.HOVER_BUTTONS.value};
            }}
            
            QPushButton:pressed {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background: {ThemeColors.PRIMARY.value};
                width: {constants.SCROLLBAR_WIDTH}px;
                margin: 15px 0 15px 0;
                border-radius: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                min-height: {constants.SCROLLBAR_MIN_HANDLE_HEIGHT}px;
                border-radius: 7px;
            }}
            
            QLineEdit {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.TERTIARY_BACKGROUND.value};
                padding: {constants.LINE_EDIT_PADDING}px;
                border-radius: {constants.BORDER_RADIUS}px;
                color: {ThemeColors.TEXT_PRIMARY.value};
            }}
            
            QComboBox {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.TERTIARY_BACKGROUND.value};
                border-radius: {constants.BORDER_RADIUS}px;
                padding: {constants.LINE_EDIT_PADDING}px;
                min-width: 6em;
            }}
            
            QTabWidget::pane {{
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.BORDER_COLOR.value};
                border-radius: {constants.BORDER_RADIUS}px;
                padding: {constants.LINE_EDIT_PADDING}px;
            }}
            
            QTabBar::tab {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                color: {ThemeColors.TEXT_PRIMARY.value};
                border-top-left-radius: {constants.BORDER_RADIUS}px;
                border-top-right-radius: {constants.BORDER_RADIUS}px;
                padding: {constants.TAB_BAR_PADDING};
                min-width: {constants.TAB_BAR_MIN_WIDTH}px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
                color: white;
            }}
            
            QTabBar::tab:hover:!selected {{
                background-color: {ThemeColors.TERTIARY_BACKGROUND.value};
                border-bottom: {constants.BORDER_WIDTH * 2}px solid {ThemeColors.PRIMARY_BUTTONS.value};
            }}
            
            QGroupBox {{
                color: {ThemeColors.TEXT_PRIMARY.value};
                font-weight: bold;
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.BORDER_COLOR.value};
                border-radius: {constants.GROUP_BOX_BORDER_RADIUS}px;
                margin-top: 12px;
                padding-top: 8px;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 5px;
            }}
            
            QFrame {{
                border-radius: {constants.BORDER_RADIUS}px;
            }}
            
            QCheckBox {{
                color: {ThemeColors.TEXT_PRIMARY.value};
                spacing: 8px;
            }}
            
            QCheckBox::indicator {{
                width: {constants.CHECKBOX_INDICATOR_SIZE}px;
                height: {constants.CHECKBOX_INDICATOR_SIZE}px;
                border: {constants.BORDER_WIDTH}px solid rgba(82, 82, 82, 0.7);
                border-radius: {constants.BORDER_RADIUS}px;
            }}
            
            QCheckBox::indicator:unchecked {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.PRIMARY_BUTTONS.value};
            }}
            
            QProgressBar {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                color: white;
                border: none;
                border-radius: {constants.BORDER_RADIUS}px;
                text-align: center;
                height: {constants.PROGRESS_BAR_HEIGHT}px;
            }}
            
            QProgressBar::chunk {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
                border-radius: {constants.BORDER_RADIUS}px;
            }}
        """

    @staticmethod
    def get_primary_button_stylesheet():
        return f"""
            QPushButton {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
                color: white;
                border: none;
                border-radius: {constants.BUTTON_BORDER_RADIUS}px;
                padding: {constants.BUTTON_PADDING};
                font-weight: bold;
                font-size: {constants.BUTTON_FONT_SIZE}px;
            }}
            QPushButton:hover {{
                background-color: {ThemeColors.HOVER_BUTTONS.value};
            }}
            QPushButton:pressed {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
            }}
            QPushButton:disabled {{
                background-color: #666666;
                color: #a3a3a3;
            }}
        """


    @staticmethod
    def get_secondary_button_stylesheet():
        return f"""
            QPushButton {{
                background-color: {ThemeColors.PRIMARY.value};
                color: {ThemeColors.PRIMARY_BUTTONS.value};
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.PRIMARY_BUTTONS.value};
                border-radius: {constants.BUTTON_BORDER_RADIUS}px;
                padding: {constants.BUTTON_PADDING};
                font-size: {constants.BUTTON_FONT_SIZE}px;
            }}
            QPushButton:hover {{
                background-color: {ThemeColors.TERTIARY_BACKGROUND.value};
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.HOVER_BUTTONS.value};
            }}
            QPushButton:pressed {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
                color: white;
            }}
            QPushButton:disabled {{
                background-color: {ThemeColors.PRIMARY.value};
                color: #666666;
                border: {constants.BORDER_WIDTH}px solid #666666;
            }}
        """


    @staticmethod
    def get_card_frame_stylesheet():
        return f"""
            QFrame {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                border-radius: {constants.FRAME_BORDER_RADIUS}px;
                padding: {constants.CARD_FRAME_PADDING}px;
                margin-bottom: {constants.CARD_FRAME_MARGIN}px;
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.BORDER_COLOR.value};
            }}
        """

    @staticmethod
    def apply_theme(app):
        """Apply the theme to the entire application"""
        app.setStyle("Fusion")
        
        # Set application-wide stylesheet
        app.setStyleSheet(ThemeManager.get_base_stylesheet())
        
        # Set up dark palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(ThemeColors.PRIMARY.value))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(ThemeColors.TEXT_PRIMARY.value))
        palette.setColor(QPalette.ColorRole.Base, QColor(ThemeColors.SECONDARY_BACKGROUND.value))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(ThemeColors.PRIMARY.value))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(ThemeColors.TEXT_PRIMARY.value))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(ThemeColors.TEXT_PRIMARY.value))
        palette.setColor(QPalette.ColorRole.Text, QColor(ThemeColors.TEXT_PRIMARY.value))
        palette.setColor(QPalette.ColorRole.Button, QColor(ThemeColors.PRIMARY_BUTTONS.value))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
        palette.setColor(QPalette.ColorRole.Link, QColor(ThemeColors.HOVER_BUTTONS.value))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(ThemeColors.HOVER_BUTTONS.value))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("white"))
        
        app.setPalette(palette)