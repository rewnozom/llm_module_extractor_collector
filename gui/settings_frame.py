# -*- coding: utf-8 -*-
# settings_frame.py
import os
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QFileDialog, QGroupBox, QMessageBox
)
from PySide6.QtCore import Signal, Qt

from gui.theme_manager import ThemeManager, Fonts, ThemeColors
from gui import constants

class SettingsFrame(QFrame):
    """Frame for managing application settings"""
    
    # Signals
    path_changed = Signal(str, str)  # path_type, new_path
    appearance_mode_changed = Signal(str)
    scaling_changed = Signal(float)
    
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setup_ui()
        self.load_settings()
        self.setup_connections()
    
    def setup_ui(self):
        """Initialize the UI components"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(constants.SETTINGS_FRAME_LAYOUT_MARGIN, 
                                       constants.SETTINGS_FRAME_LAYOUT_MARGIN, 
                                       constants.SETTINGS_FRAME_LAYOUT_MARGIN, 
                                       constants.SETTINGS_FRAME_LAYOUT_MARGIN)
        self.layout.setSpacing(constants.SETTINGS_FRAME_SPACING)
        
        # Paths Section
        self.path_group = QGroupBox("Paths")
        self.path_group.setFont(Fonts.get_bold(constants.SETTINGS_GROUP_HEADER_FONT_SIZE))
        self.path_layout = QVBoxLayout(self.path_group)
        
        # Base Directory
        self.base_dir_layout = QHBoxLayout()
        self.base_dir_label = QLabel("Base Directory:")
        self.base_dir_input = QLineEdit()
        self.base_dir_input.setReadOnly(True)
        self.base_dir_button = QPushButton("Browse...")
        self.base_dir_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        self.base_dir_layout.addWidget(self.base_dir_label)
        self.base_dir_layout.addWidget(self.base_dir_input, 1)
        self.base_dir_layout.addWidget(self.base_dir_button)
        
        # Output Directory
        self.output_dir_layout = QHBoxLayout()
        self.output_dir_label = QLabel("Output Directory:")
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setReadOnly(True)
        self.output_dir_button = QPushButton("Browse...")
        self.output_dir_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        self.output_dir_layout.addWidget(self.output_dir_label)
        self.output_dir_layout.addWidget(self.output_dir_input, 1)
        self.output_dir_layout.addWidget(self.output_dir_button)
        
        self.path_layout.addLayout(self.base_dir_layout)
        self.path_layout.addLayout(self.output_dir_layout)
        
        self.layout.addWidget(self.path_group)
        
        # Appearance Section
        self.appearance_group = QGroupBox("Appearance")
        self.appearance_group.setFont(Fonts.get_bold(constants.SETTINGS_GROUP_HEADER_FONT_SIZE))
        self.appearance_layout = QVBoxLayout(self.appearance_group)
        
        # Appearance Mode
        self.appearance_mode_layout = QHBoxLayout()
        self.appearance_mode_label = QLabel("Appearance Mode:")
        self.appearance_mode_combo = QComboBox()
        self.appearance_mode_combo.addItems(["Light", "Dark", "System"])
        
        self.appearance_mode_layout.addWidget(self.appearance_mode_label)
        self.appearance_mode_layout.addWidget(self.appearance_mode_combo, 1)
        
        # UI Scaling
        self.scaling_layout = QHBoxLayout()
        self.scaling_label = QLabel("UI Scaling:")
        self.scaling_combo = QComboBox()
        self.scaling_combo.addItems(["80%", "90%", "100%", "110%", "120%"])
        
        self.scaling_layout.addWidget(self.scaling_label)
        self.scaling_layout.addWidget(self.scaling_combo, 1)
        
        self.appearance_layout.addLayout(self.appearance_mode_layout)
        self.appearance_layout.addLayout(self.scaling_layout)
        
        self.layout.addWidget(self.appearance_group)
        
        # File Specific Section
        self.file_specific_group = QGroupBox("File Specific")
        self.file_specific_group.setFont(Fonts.get_bold(constants.SETTINGS_GROUP_HEADER_FONT_SIZE))
        self.file_specific_layout = QVBoxLayout(self.file_specific_group)
        
        # Enable File Specific
        self.file_specific_layout.addWidget(QLabel("Enable File Specific:"))
        self.enable_file_specific_combo = QComboBox()
        self.enable_file_specific_combo.addItems(["True", "False"])
        self.file_specific_layout.addWidget(self.enable_file_specific_combo)
        
        self.layout.addWidget(self.file_specific_group)
        
        # Add stretch to push everything to the top
        self.layout.addStretch()
        
        # Apply styling
        self.setStyleSheet(ThemeManager.get_card_frame_stylesheet())
    
    def load_settings(self):
        """Load settings from the settings manager"""
        if not self.settings_manager:
            return
        
        # Load paths
        base_dir = self.settings_manager.get_setting("paths", "base_dir", "")
        output_dir = self.settings_manager.get_setting("paths", "output_dir", "")
        
        self.base_dir_input.setText(base_dir)
        self.output_dir_input.setText(output_dir)
        
        # Load file specific setting
        file_specific = self.settings_manager.get_setting("file_specific", "use_file_specific", False)
        self.enable_file_specific_combo.setCurrentText(str(file_specific))
        
        # Set default appearance
        self.appearance_mode_combo.setCurrentText("Dark")
        self.scaling_combo.setCurrentText("100%")
    
    def setup_connections(self):
        """Setup signal connections"""
        # Path buttons
        self.base_dir_button.clicked.connect(self.browse_base_dir)
        self.output_dir_button.clicked.connect(self.browse_output_dir)
        
        # Appearance controls
        self.appearance_mode_combo.currentTextChanged.connect(
            lambda text: self.appearance_mode_changed.emit(text)
        )
        self.scaling_combo.currentTextChanged.connect(self.handle_scaling_change)
        
        # File specific toggle
        self.enable_file_specific_combo.currentTextChanged.connect(self.handle_file_specific_change)
    
    def browse_base_dir(self):
        """Open file dialog to select base directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Base Directory",
            self.base_dir_input.text()
        )
        
        if directory:
            # Verify that the directory exists and is accessible
            if not os.path.isdir(directory):
                QMessageBox.warning(
                    self,
                    "Invalid Directory",
                    "The selected path is not a valid directory."
                )
                return
                
            self.base_dir_input.setText(directory)
            self.settings_manager.update_setting("paths", "base_dir", directory)
            self.path_changed.emit("base_dir", directory)
            
            # Optionally create a default output directory
            default_output = os.path.join(directory, "output")
            if not self.output_dir_input.text():
                self.output_dir_input.setText(default_output)
                self.settings_manager.update_setting("paths", "output_dir", default_output)
                self.path_changed.emit("output_dir", default_output)
    
    def browse_output_dir(self):
        """Open file dialog to select output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.output_dir_input.text() or self.base_dir_input.text()
        )
        
        if directory:
            self.output_dir_input.setText(directory)
            self.settings_manager.update_setting("paths", "output_dir", directory)
            self.path_changed.emit("output_dir", directory)
    
    def handle_scaling_change(self, scaling_text: str):
        """Handle UI scaling changes"""
        try:
            scaling_value = float(scaling_text.replace("%", "")) / 100.0
            self.scaling_changed.emit(scaling_value)
        except ValueError:
            pass
    
    def handle_file_specific_change(self, value: str):
        """Handle file specific setting change"""
        if self.settings_manager:
            self.settings_manager.update_setting(
                "file_specific", 
                "use_file_specific", 
                value == "True"
            )