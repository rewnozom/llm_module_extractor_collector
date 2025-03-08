# -*- coding: utf-8 -*-
# file_specific_frame.py

import os
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QListWidget, QComboBox, QMessageBox, QFileDialog,
    QInputDialog
)
from PySide6.QtCore import Signal, Qt

from gui.theme_manager import ThemeManager, Fonts, ThemeColors
from gui import constants

class FileSpecificFrame(QFrame):
    """Frame for file specific controls and file list management"""
    
    # Signals
    preset_changed = Signal(str, list)  # preset_name, files
    files_added = Signal(list)  # List of added files
    
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setup_ui()
        self.setup_connections()
        self.load_presets()
    
    def setup_ui(self):
        """Initialize the UI components with fixed dimensions"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(constants.FILE_FRAME_LAYOUT_MARGIN, 
                                      constants.FILE_FRAME_LAYOUT_MARGIN, 
                                      constants.FILE_FRAME_LAYOUT_MARGIN, 
                                      constants.FILE_FRAME_LAYOUT_MARGIN)
        self.layout.setSpacing(constants.FILE_FRAME_SPACING)
        
        # Header
        self.header = QLabel("File Specific")
        self.header.setFont(Fonts.get_bold(constants.FILE_HEADER_FONT_SIZE))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.header)
        
        # File List
        self.layout.addWidget(QLabel("File List:"))
        self.file_listbox = QListWidget()
        self.file_listbox.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        # Set a minimum height to prevent excessive squeezing
        self.file_listbox.setMinimumHeight(constants.FILE_LIST_MIN_HEIGHT)
        self.layout.addWidget(self.file_listbox)
        
        # File Operation Buttons
        self.file_buttons_layout = QHBoxLayout()
        
        self.add_file_button = QPushButton("Add File")
        self.add_file_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        self.add_folder_button = QPushButton("Add Folder")
        self.add_folder_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        self.choose_output_button = QPushButton("Choose Output Directory")
        self.choose_output_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        self.file_buttons_layout.addWidget(self.add_file_button)
        self.file_buttons_layout.addWidget(self.add_folder_button)
        
        self.layout.addLayout(self.file_buttons_layout)
        self.layout.addWidget(self.choose_output_button)
        
        # Preset Controls
        self.layout.addWidget(QLabel("Presets:"))
        self.preset_combo = QComboBox()
        self.preset_combo.setMinimumWidth(constants.PRESET_COMBO_MIN_WIDTH)
        self.layout.addWidget(self.preset_combo)
        
        # Preset Buttons
        self.preset_buttons_layout = QVBoxLayout()
        
        self.add_preset_button = QPushButton("Add Preset")
        self.add_preset_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        self.auto_preset_button = QPushButton("Auto Preset")
        self.auto_preset_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        self.remove_preset_button = QPushButton("Remove Preset")
        self.remove_preset_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        
        self.preset_buttons_layout.addWidget(self.add_preset_button)
        self.preset_buttons_layout.addWidget(self.auto_preset_button)
        self.preset_buttons_layout.addWidget(self.remove_preset_button)
        
        self.layout.addLayout(self.preset_buttons_layout)
        
        # Apply styling
        self.setStyleSheet(ThemeManager.get_card_frame_stylesheet())
    
    def setup_connections(self):
        """Setup signal connections"""
        # File buttons
        self.add_file_button.clicked.connect(self.add_files)
        self.add_folder_button.clicked.connect(self.add_folder)
        self.choose_output_button.clicked.connect(self.choose_output_directory)
        
        # Preset controls
        self.preset_combo.currentTextChanged.connect(self.load_preset_files)
        self.add_preset_button.clicked.connect(self.add_preset)
        self.auto_preset_button.clicked.connect(self.auto_preset)
        self.remove_preset_button.clicked.connect(self.remove_preset)
        
        # File list events
        self.file_listbox.keyPressEvent = self.handle_key_press
    
    def load_presets(self):
        """Load presets from settings with improved error handling"""
        if not self.settings_manager:
            return
            
        try:
            presets = self.settings_manager.get_section("presets", {})
            
            # Clear existing items
            self.preset_combo.clear()
            
            # Extract all preset names except for 'current_preset'
            preset_names = [name for name in presets.keys() if name != 'current_preset']
            
            # Add preset names to combo box
            self.preset_combo.addItems(preset_names)
            
            # Select current preset if available
            current_preset = presets.get('current_preset', '')
            if current_preset and current_preset in preset_names:
                self.preset_combo.setCurrentText(current_preset)
            elif self.preset_combo.count() > 0:
                self.preset_combo.setCurrentIndex(0)
            
            # Load files for selected preset
            if self.preset_combo.currentText():
                self.load_preset_files(self.preset_combo.currentText())
        except Exception as e:
            print(f"Error loading presets: {e}")
            # Fallback to empty preset list
            self.preset_combo.clear()
    
    def load_preset_files(self, preset_name: str):
        """Load files for the selected preset with validation"""
        if not preset_name or not self.settings_manager:
            return
        
        try:
            # Clear existing items
            self.file_listbox.clear()
            
            # Get files for preset
            preset_files = self.settings_manager.get_setting("presets", preset_name, [])
            print(f"Loaded preset '{preset_name}' files: {preset_files}")
            
            # Check if preset_files is actually the preset name split into characters
            if preset_files == list(preset_name):
                print(f"ERROR: preset_files equals preset name split into characters: {preset_files}")
                preset_files = []
            
            # Validate list type
            if not isinstance(preset_files, list):
                print(f"Warning: preset '{preset_name}' files is not a list: {type(preset_files)}")
                if isinstance(preset_files, str):
                    preset_files = [preset_files]
                else:
                    preset_files = []
            
            # Add files to list
            self.file_listbox.addItems(preset_files)
            
            # Emit signal with preset files
            self.preset_changed.emit(preset_name, preset_files)
            
            # Update current preset in settings
            self.settings_manager.update_setting("presets", "current_preset", preset_name)
            
        except Exception as e:
            print(f"Error loading preset files: {e}")
    
    def add_files(self):
        """Open file dialog to add files to the current preset"""
        preset_name = self.preset_combo.currentText()
        if not preset_name:
            QMessageBox.warning(
                self,
                "No Preset Selected",
                "Please select a preset to add files to."
            )
            return
        
        base_dir = self.settings_manager.get_setting("paths", "base_dir", "")
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            base_dir
        )
        
        if files:
            self._add_files_to_preset(files)
    
    def add_folder(self):
        """Open directory dialog to add all files in a folder to the preset"""
        preset_name = self.preset_combo.currentText()
        if not preset_name:
            QMessageBox.warning(
                self,
                "No Preset Selected",
                "Please select a preset to add files to."
            )
            return
        
        base_dir = self.settings_manager.get_setting("paths", "base_dir", "")
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            base_dir
        )
        
        if folder:
            files = []
            for root, _, filenames in os.walk(folder):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            
            if files:
                self._add_files_to_preset(files)
    
    def _add_files_to_preset(self, files):
        """Helper method to add files to the current preset with better path handling"""
        preset_name = self.preset_combo.currentText()
        base_dir = self.settings_manager.get_setting("paths", "base_dir", "")
        preset_files = self.settings_manager.get_setting("presets", preset_name, [])
        
        # Ensure preset_files is a list
        if not isinstance(preset_files, list):
            preset_files = []
        
        # Check if preset_files equals the preset name split into characters
        if preset_files == list(preset_name):
            print(f"ERROR: preset_files equals preset name characters: {preset_files}")
            preset_files = []
        
        added_files = []
        
        for file_path in files:
            try:
                # Normalize file paths for consistent comparison
                norm_file_path = os.path.normpath(file_path)
                
                # Calculate relative path if inside base_dir
                if base_dir and os.path.commonpath([base_dir, norm_file_path]).startswith(base_dir):
                    relative_path = os.path.relpath(norm_file_path, base_dir)
                else:
                    # Use absolute path if outside base_dir
                    relative_path = norm_file_path
                
                # Normalize for platform consistency
                relative_path = relative_path.replace('\\', '/')
                
                # Add if not already in preset
                if relative_path not in preset_files:
                    preset_files.append(relative_path)
                    added_files.append(relative_path)
            except Exception as e:
                print(f"Error adding file {file_path}: {e}")
                # Continue with other files even if one fails
                continue
        
        if added_files:
            # Update settings
            self.settings_manager.update_setting("presets", preset_name, preset_files)
            self.load_preset_files(preset_name)
            self.files_added.emit(added_files)
    
    def choose_output_directory(self):
        """Open directory dialog to select output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Choose Output Directory",
            self.settings_manager.get_setting("paths", "output_dir", "")
        )
        
        if directory:
            self.settings_manager.update_setting("paths", "output_dir", directory)
    
    def add_preset(self):
        """Add a new preset with a user-specified name"""
        name, ok = QInputDialog.getText(
            self,
            "Add Preset",
            "Enter preset name:"
        )
        
        if ok and name:
            # Check if preset already exists
            presets = self.settings_manager.get_section("presets", {})
            if name in presets:
                QMessageBox.warning(
                    self,
                    "Preset Exists",
                    f"A preset named '{name}' already exists."
                )
                return
            
            # Add new preset
            self.settings_manager.update_setting("presets", name, [])
            
            # Update combo box
            self.preset_combo.addItem(name)
            self.preset_combo.setCurrentText(name)
            
            # Set as current preset
            self.settings_manager.update_setting("presets", "current_preset", name)
    
    def auto_preset(self):
        """Automatically create presets based on directory structure"""
        base_dir = self.settings_manager.get_setting("paths", "base_dir", "")
        if not base_dir:
            QMessageBox.warning(
                self,
                "Base Directory Missing",
                "Please set the base directory in settings before auto-generating presets."
            )
            return

        base_path = os.path.abspath(base_dir)
        new_presets = {}
        
        # Define directories to ignore
        IGNORED = {".pytest_cache", "build", "docs", "logs", "env", "venv", ".git",
                 "output", "temp", ".backups", "__pycache__"}
        
        try:
            for root, dirs, files in os.walk(base_path):
                # Skip ignored directories
                dirs[:] = [d for d in dirs if d not in IGNORED]
                
                # Skip base directory itself
                if root == base_path:
                    continue
                    
                # Get relative path for preset name
                try:
                    rel_path = os.path.relpath(root, base_path)
                    if rel_path == '.':
                        continue
                        
                    # Collect files in this directory
                    preset_files = []
                    for file in files:
                        if not file.startswith('.'):  # Skip hidden files
                            file_path = os.path.join(root, file)
                            try:
                                rel_file = os.path.relpath(file_path, base_path)
                                # Normalize path separators
                                rel_file = rel_file.replace('\\', '/')
                                preset_files.append(rel_file)
                            except ValueError:
                                continue
                    
                    if preset_files:
                        preset_name = rel_path.replace('\\', '/')
                        new_presets[preset_name] = preset_files
                        
                except ValueError:
                    continue
            
            if not new_presets:
                QMessageBox.information(
                    self,
                    "Auto Preset",
                    "No suitable directories found for creating presets."
                )
                return
                
            # Check if total presets will exceed maximum
            if len(new_presets) + self.preset_combo.count() > constants.MAX_PRESETS:
                reply = QMessageBox.question(
                    self,
                    "Maximum Presets Warning",
                    f"Adding {len(new_presets)} presets will exceed the recommended maximum of {constants.MAX_PRESETS}. Continue anyway?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return
                
            # Check if any preset has too many files
            for name, files in new_presets.items():
                if len(files) > constants.MAX_FILES_PER_PRESET:
                    reply = QMessageBox.question(
                        self,
                        "Large Preset Warning",
                        f"Preset '{name}' contains {len(files)} files, which exceeds the recommended maximum of {constants.MAX_FILES_PER_PRESET}. Continue anyway?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.No:
                        return
                elif len(files) > constants.FILE_WARNING_THRESHOLD:
                    QMessageBox.warning(
                        self,
                        "Large Preset Warning",
                        f"Preset '{name}' contains {len(files)} files, which may affect performance."
                    )
                
            # Update settings with new presets
            for name, files in new_presets.items():
                self.settings_manager.update_setting("presets", name, files)
            
            # Update UI
            self.load_presets()
            
            QMessageBox.information(
                self,
                "Auto Preset",
                f"Created {len(new_presets)} presets based on directory structure."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Auto Preset Error",
                f"An error occurred while generating presets: {str(e)}"
            )
    
    def remove_preset(self):
        """Remove the currently selected preset"""
        preset_name = self.preset_combo.currentText()
        if not preset_name:
            return
            
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove the preset '{preset_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove from settings
            self.settings_manager.remove_setting("presets", preset_name)
            
            # Remove from UI
            index = self.preset_combo.findText(preset_name)
            if index >= 0:
                self.preset_combo.removeItem(index)
            
            # Clear file list
            self.file_listbox.clear()
            
            # Notify other components
            self.preset_changed.emit(preset_name, [])


    def handle_key_press(self, event):
        """Handle key press events in the file list (e.g., Delete to remove files)"""
        if event.key() == Qt.Key.Key_Delete:
            self.remove_selected_files()
        else:
            # Call the parent implementation for other keys
            QListWidget.keyPressEvent(self.file_listbox, event)
    
    def remove_selected_files(self):
        """Remove selected files from the current preset"""
        preset_name = self.preset_combo.currentText()
        if not preset_name:
            return
        
        # Get selected items
        selected_items = self.file_listbox.selectedItems()
        if not selected_items:
            return
        
        # Get current preset files
        preset_files = self.settings_manager.get_setting("presets", preset_name, [])
        
        # Validate preset files
        if not isinstance(preset_files, list):
            print(f"Warning: preset '{preset_name}' files is not a list: {type(preset_files)}")
            if isinstance(preset_files, str):
                preset_files = [preset_files]
            else:
                preset_files = []
        
        # Check if preset_files equals the preset name split into characters
        if preset_files == list(preset_name):
            print(f"ERROR: preset_files equals preset name characters: {preset_files}")
            preset_files = []
        
        # Remove selected files
        for item in selected_items:
            file_path = item.text()
            if file_path in preset_files:
                preset_files.remove(file_path)
        
        # Update settings and UI
        self.settings_manager.update_setting("presets", preset_name, preset_files)
        self.load_preset_files(preset_name)
        
        # Notify other components
        self.preset_changed.emit(preset_name, preset_files)