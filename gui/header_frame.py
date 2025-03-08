# -*- coding: utf-8 -*-
# header_frame.py (updated)

from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QMenu, QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon, QAction

from gui.theme_manager import ThemeManager, Fonts, ThemeColors
from gui import constants

class HeaderFrame(QFrame):
    """Header bar with navigation and menu access"""
    
    # Signals
    settings_requested = Signal()
    help_requested = Signal()
    about_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Initialize the UI components"""
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(constants.MAIN_LAYOUT_MARGIN, 
                                      constants.INNER_LAYOUT_MARGIN, 
                                      constants.MAIN_LAYOUT_MARGIN, 
                                      constants.INNER_LAYOUT_MARGIN)
        self.layout.setSpacing(constants.INNER_LAYOUT_SPACING)
        
        # App logo/title
        self.title_label = QLabel("Project Module-Extractor Manager")
        self.title_label.setFont(Fonts.get_bold(constants.HEADER_TITLE_FONT_SIZE))
        
        # Navigation buttons
        self.settings_button = QPushButton("Settings")
        self.settings_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        # Menu button
        self.menu_button = QPushButton("☰")  # Hamburger menu icon
        self.menu_button.setFixedWidth(constants.HEADER_BUTTON_WIDTH)
        self.menu_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        # Add widgets to layout
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        self.layout.addWidget(self.settings_button)
        self.layout.addWidget(self.menu_button)
        
        # Fixed height to prevent excessive vertical growth
        self.setFixedHeight(constants.HEADER_HEIGHT)
        
        # Set size policies to prevent unwanted stretching
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        # Apply styling
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                border-bottom: {constants.BORDER_WIDTH}px solid {ThemeColors.BORDER_COLOR.value};
                min-height: {constants.HEADER_HEIGHT}px;
                max-height: {constants.HEADER_HEIGHT}px;
            }}
            QLabel {{
                color: {ThemeColors.TEXT_PRIMARY.value};
            }}
        """)
        
        # Create menu
        self.menu = QMenu(self)
        self.menu.setStyleSheet(f"""
            QMenu {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                color: {ThemeColors.TEXT_PRIMARY.value};
                border: {constants.BORDER_WIDTH}px solid {ThemeColors.BORDER_COLOR.value};
                border-radius: {constants.BORDER_RADIUS}px;
            }}
            QMenu::item {{
                padding: {constants.BUTTON_PADDING};
            }}
            QMenu::item:selected {{
                background-color: {ThemeColors.PRIMARY_BUTTONS.value};
                color: white;
            }}
        """)
        
        # Add menu actions
        self.settings_action = QAction("Settings", self)
        self.help_action = QAction("Help", self)
        self.about_action = QAction("About", self)
        
        self.menu.addAction(self.settings_action)
        self.menu.addSeparator()
        self.menu.addAction(self.help_action)
        self.menu.addAction(self.about_action)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.settings_button.clicked.connect(self.settings_requested.emit)
        self.menu_button.clicked.connect(self.show_menu)
        
        # Menu actions
        self.settings_action.triggered.connect(self.settings_requested.emit)
        self.help_action.triggered.connect(self.help_requested.emit)
        self.about_action.triggered.connect(self.about_requested.emit)
    
    def show_menu(self):
        """Show the menu at the menu button position"""
        pos = self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft())
        self.menu.exec(pos)