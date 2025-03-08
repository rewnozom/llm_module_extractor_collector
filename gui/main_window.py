# -*- coding: utf-8 -*-
# main_window.py

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMessageBox, QDialog, QApplication, QStatusBar, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QTimer

from gui.theme_manager import ThemeManager, ThemeColors
from gui.settings_manager import SettingsManager
from gui.settings_frame import SettingsFrame
from gui.file_specific_frame import FileSpecificFrame
from gui.header_frame import HeaderFrame
from gui.extraction_frame import ExtractionFrame
from gui import constants

class SettingsDialog(QDialog):
    """Dialog for displaying settings"""
    
    def __init__(self, settings_frame, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(constants.SETTINGS_DIALOG_WIDTH, constants.SETTINGS_DIALOG_HEIGHT)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add settings frame
        layout.addWidget(settings_frame)

class MainWindow(QMainWindow):
    """Main application window with responsive design"""
    
    def __init__(self):
        super().__init__()
        self.settings_path = "./settings.toml"
        self.settings_manager = SettingsManager(self.settings_path)
        
        self.setWindowTitle("Project Manager")
        self.resize(constants.DEFAULT_WINDOW_WIDTH, constants.DEFAULT_WINDOW_HEIGHT)
        
        # Initialize UI with deferred loading for better startup performance
        self.setup_ui()
        
        # Apply theme
        QTimer.singleShot(100, lambda: ThemeManager.apply_theme(QApplication.instance()))
        
        # Update the path display
        QTimer.singleShot(200, self.update_path_displays)
        
        # Show status message
        self.statusBar().showMessage("Application ready", constants.STATUS_MESSAGE_DURATION)
    
    def setup_ui(self):
        """Initialize and setup the UI components"""
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(constants.MAIN_LAYOUT_MARGIN, constants.MAIN_LAYOUT_MARGIN, 
                                           constants.MAIN_LAYOUT_MARGIN, constants.MAIN_LAYOUT_MARGIN)
        self.main_layout.setSpacing(constants.MAIN_LAYOUT_SPACING)
        
        # Header - Prevent stretching by setting stretch factor to 0
        self.header_frame = HeaderFrame()
        self.main_layout.addWidget(self.header_frame, 0)  # Stretch factor of 0
        
        # Content area with split panels - Allow it to expand with stretch factor of 1
        self.content_area = QWidget()
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(constants.CONTENT_LAYOUT_MARGIN, constants.CONTENT_LAYOUT_MARGIN, 
                                         constants.CONTENT_LAYOUT_MARGIN, constants.CONTENT_LAYOUT_MARGIN)
        content_layout.setSpacing(constants.CONTENT_LAYOUT_SPACING)
        
        # Create splitter for resizable panels
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)  # Prevent panels from collapsing
        
        # Left panel (file specific)
        self.file_specific_frame = FileSpecificFrame(self.settings_manager)
        self.file_specific_frame.setMinimumWidth(constants.PANEL_MIN_WIDTH)  # Set minimum width
        
        # Right panel (extraction)
        self.extraction_frame = ExtractionFrame(self.settings_manager)
        self.extraction_frame.setMinimumWidth(constants.PANEL_MIN_WIDTH)  # Set minimum width
        
        # Add panels to splitter
        self.main_splitter.addWidget(self.file_specific_frame)
        self.main_splitter.addWidget(self.extraction_frame)
        
        # Set initial sizes
        self.main_splitter.setSizes([constants.SPLITTER_INITIAL_SIZE, constants.SPLITTER_INITIAL_SIZE])
        
        content_layout.addWidget(self.main_splitter)
        self.main_layout.addWidget(self.content_area, 1)  # Stretch factor of 1
        
        # Create status bar
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                color: {ThemeColors.TEXT_PRIMARY.value};
                padding: {constants.STATUS_BAR_PADDING}px;
                border-top: {constants.BORDER_WIDTH}px solid {ThemeColors.BORDER_COLOR.value};
                max-height: {constants.STATUS_BAR_MAX_HEIGHT}px;
            }}
        """)
        self.statusBar().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Create settings frame but don't add it to the layout
        # It will be shown in a dialog when requested
        self.settings_frame = SettingsFrame(self.settings_manager)
        
        # Setup connections
        self.setup_connections()
    
    def setup_connections(self):
        """Setup signal connections between components"""
        # Header connections
        self.header_frame.settings_requested.connect(self.show_settings_dialog)
        self.header_frame.about_requested.connect(self.show_about_dialog)
        self.header_frame.help_requested.connect(self.show_help_dialog)
        
        # File specific connections
        self.file_specific_frame.preset_changed.connect(self.handle_preset_change)
        self.file_specific_frame.files_added.connect(self.handle_files_added)
        
        # Extraction connections
        self.extraction_frame.extraction_started.connect(self.handle_extraction_started)
        self.extraction_frame.extraction_completed.connect(self.handle_extraction_completed)
        self.extraction_frame.extraction_failed.connect(self.handle_extraction_failed)
        
        # Settings connections
        self.settings_frame.path_changed.connect(self.handle_path_changed)
        self.settings_frame.appearance_mode_changed.connect(self.handle_appearance_changed)
        self.settings_frame.scaling_changed.connect(self.handle_scaling_changed)
        
        # IMPORTANT: Connect the preset signals between file_specific_frame and extraction_frame
        self.file_specific_frame.preset_changed.connect(self.extraction_frame.handle_preset_change)

    def update_path_displays(self):
        """Update path displays in the UI"""
        base_dir = self.settings_manager.get_setting("paths", "base_dir", "")
        if hasattr(self.extraction_frame, 'path_value'):
            if base_dir and os.path.isdir(base_dir):
                self.extraction_frame.path_value.setText(f"📁 {base_dir}")
                self.extraction_frame.path_value.setStyleSheet(f"""
                    color: {ThemeColors.TEXT_PRIMARY.value};
                    background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                    border: {constants.BORDER_WIDTH}px solid {ThemeColors.BORDER_COLOR.value};
                    border-radius: {constants.PATH_VALUE_BORDER_RADIUS}px;
                    padding: {constants.PATH_VALUE_PADDING};
                """)
            else:
                # Highlight missing path with a warning color
                self.extraction_frame.path_value.setText("📁 Not selected (required)")
                self.extraction_frame.path_value.setStyleSheet(f"""
                    color: #ff6b6b;
                    background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                    border: {constants.BORDER_WIDTH}px solid #ff6b6b;
                    border-radius: {constants.PATH_VALUE_BORDER_RADIUS}px;
                    padding: {constants.PATH_VALUE_PADDING};
                """)

    def show_settings_dialog(self):
        """Show the settings dialog"""
        dialog = SettingsDialog(self.settings_frame, self)
        dialog.exec()
    
    def show_about_dialog(self):
        """Show the about dialog"""
        QMessageBox.about(
            self,
            "About Project Manager",
            """<h3>Project Manager</h3>
            <p>A tool for extracting and managing code projects.</p>
            <p>Version 1.0.0</p>"""
        )
    
    def show_help_dialog(self):
        """Show the help dialog"""
        QMessageBox.information(
            self,
            "Help",
            """<h3>Project Manager Help</h3>
            <p><b>Standard Extraction:</b> Convert source code to structured formats</p>
            <p><b>Reverse Extraction:</b> Convert structured formats back to source code</p>
            <p><b>Presets:</b> Save and load file selections</p>"""
        )
    
    def handle_preset_change(self, preset_name, files):
        """Handle preset changes"""
        # Update status bar
        self.statusBar().showMessage(f"Preset '{preset_name}' selected with {len(files)} files", constants.STATUS_MESSAGE_DURATION)
        
        # Store current preset in settings
        self.settings_manager.update_setting("presets", "current_preset", preset_name)
        
        # Log for debugging
        print(f"MainWindow: Preset changed to '{preset_name}' with {len(files)} files")
    
    def handle_files_added(self, files):
        """Handle files being added to a preset"""
        if files:
            self.statusBar().showMessage(f"Added {len(files)} files to preset", constants.STATUS_MESSAGE_DURATION)
    
    def handle_extraction_started(self):
        """Handle extraction started event"""
        self.statusBar().showMessage("Extraction in progress...", 0)  # 0 = no timeout
        
        # Optional: Disable file specific panel during extraction
        self.file_specific_frame.setEnabled(False)
    
    def handle_extraction_completed(self):
        """Handle extraction completed event"""
        self.statusBar().showMessage("Extraction completed successfully", constants.STATUS_MESSAGE_DURATION)
        
        # Re-enable file specific panel
        self.file_specific_frame.setEnabled(True)
    
    def handle_extraction_failed(self, error_message):
        """Handle extraction failure event"""
        self.statusBar().showMessage(f"Extraction failed: {error_message}", constants.STATUS_MESSAGE_DURATION)
        
        # Re-enable file specific panel
        self.file_specific_frame.setEnabled(True)
    
    def handle_path_changed(self, path_type, new_path):
        """Handle path changes from settings"""
        if path_type == "base_dir":
            # Update the extraction frame path display
            if hasattr(self.extraction_frame, 'path_value'):
                if new_path and os.path.isdir(new_path):
                    self.extraction_frame.path_value.setText(f"📁 {new_path}")
                    self.extraction_frame.path_value.setStyleSheet(f"""
                        color: {ThemeColors.TEXT_PRIMARY.value};
                        background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                        border: {constants.BORDER_WIDTH}px solid {ThemeColors.BORDER_COLOR.value};
                        border-radius: {constants.PATH_VALUE_BORDER_RADIUS}px;
                        padding: {constants.PATH_VALUE_PADDING};
                    """)
                else:
                    self.extraction_frame.path_value.setText("📁 Not selected (required)")
                    self.extraction_frame.path_value.setStyleSheet(f"""
                        color: #ff6b6b;
                        background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                        border: {constants.BORDER_WIDTH}px solid #ff6b6b;
                        border-radius: {constants.PATH_VALUE_BORDER_RADIUS}px;
                        padding: {constants.PATH_VALUE_PADDING};
                    """)

    def handle_appearance_changed(self, mode):
        """Handle appearance mode changes"""
        # Apply theme based on mode
        ThemeManager.apply_theme(QApplication.instance())
    
    def handle_scaling_changed(self, scale_factor):
        """Handle UI scaling changes"""
        # Apply scaling to the application
        # This is a simplified implementation - in a real app,
        # you would use a more sophisticated scaling approach
        font = QApplication.instance().font()
        font.setPointSize(int(constants.DEFAULT_FONT_SIZE * scale_factor))
        QApplication.instance().setFont(font)
    
    def resizeEvent(self, event):
        """Handle window resize events for responsive layout"""
        super().resizeEvent(event)
        
        # Adjust layout based on window width
        width = event.size().width()
        
        if width < constants.RESPONSIVE_BREAKPOINT:
            # Compact layout for smaller screens
            self.main_splitter.setOrientation(Qt.Orientation.Vertical)
        else:
            # Side-by-side layout for larger screens
            self.main_splitter.setOrientation(Qt.Orientation.Horizontal)
            
        # Rebalance the splitter when orientation changes
        if width > constants.RESPONSIVE_BREAKPOINT and self.main_splitter.orientation() == Qt.Orientation.Horizontal:
            self.main_splitter.setSizes([width//2, width//2])
    
    def closeEvent(self, event):
        """Handle window close event with cleanup"""
        # Clean up any resources
        if hasattr(self.extraction_frame, 'cleanup'):
            self.extraction_frame.cleanup()
        
        event.accept()