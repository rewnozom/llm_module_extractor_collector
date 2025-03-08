# -*- coding: utf-8 -*-
# main.py

import sys
import os
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.theme_manager import ThemeManager

def main():
    """Main entry point for the application"""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Project Manager")
    app.setOrganizationName("ProjectManager")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Apply theme
    ThemeManager.apply_theme(app)
    
    # Create and show main window
    main_window = MainWindow()
    main_window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()