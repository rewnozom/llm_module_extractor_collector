# Project Details

# Table of Contents
- [..\gui\settings_frame.py](#-gui-settings_framepy)
- [..\main.py](#-mainpy)
- [..\gui\extraction_frame.py](#-gui-extraction_framepy)
- [..\gui\file_specific_frame.py](#-gui-file_specific_framepy)
- [..\gui\theme_manager.py](#-gui-theme_managerpy)
- [..\gui\settings_manager.py](#-gui-settings_managerpy)
- [..\gui\constants.py](#-gui-constantspy)
- [..\gui\extraction_worker.py](#-gui-extraction_workerpy)
- [..\gui\header_frame.py](#-gui-header_framepy)
- [..\gui\extractorz.py](#-gui-extractorzpy)
- [..\gui\__init__.py](#-gui-__init__py)
- [..\gui\main_window.py](#-gui-main_windowpy)


# ..\..\gui\settings_frame.py
## File: ..\..\gui\settings_frame.py

```py
# ..\..\gui\settings_frame.py
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
```

---

# ..\..\main.py
## File: ..\..\main.py

```py
# ..\..\main.py
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
```

---

# ..\..\gui\extraction_frame.py
## File: ..\..\gui\extraction_frame.py

```py
# ..\..\gui\extraction_frame.py
# -*- coding: utf-8 -*-
# extraction_frame.py

import os
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QProgressBar, QCheckBox, QFileDialog, QMessageBox, QTabWidget,
    QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QCursor

from gui.theme_manager import ThemeManager, Fonts, ThemeColors
from gui.extraction_worker import ExtractionWorker
# Import the extractor classes accordingly
from gui.extractorz import CSVEx, MarkdownEx, ReverseCSVEx, ReverseMarkdownEx
from gui import constants

class ExtractionFrame(QFrame):
    """Frame for handling extraction operations with fixed UI height"""
    
    # Signals
    extraction_started = Signal()
    extraction_completed = Signal()
    extraction_failed = Signal(str)
    
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setup_ui()
        self.setup_connections()
        
        # Initialize worker instances
        self.csv_worker = None
        self.markdown_worker = None
        
        # Initialize current preset
        self.current_preset = ""
        self.current_preset_files = []
    
    def setup_ui(self):
        """Initialize the UI components with fixed sizes to prevent window expansion"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(constants.MAIN_LAYOUT_MARGIN, constants.MAIN_LAYOUT_MARGIN, 
                                    constants.MAIN_LAYOUT_MARGIN, constants.MAIN_LAYOUT_MARGIN)
        self.layout.setSpacing(constants.MAIN_LAYOUT_SPACING)
        
        # Set minimum width to avoid excessive squeezing
        self.setMinimumWidth(constants.MIN_FRAME_WIDTH)
        
        # Set size policy to prevent vertical expansion
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Create tabs for different extraction modes
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
        """)
        
        # Standard extraction tab
        self.standard_tab = QFrame()
        self.setup_standard_tab()
        self.tabs.addTab(self.standard_tab, "Standard Extraction")
        
        # Reverse extraction tab
        self.reverse_tab = QFrame()
        self.setup_reverse_tab()
        self.tabs.addTab(self.reverse_tab, "Reverse Extraction")
        
        self.layout.addWidget(self.tabs)
        
        # Extraction options
        self.options_frame = QFrame()
        options_layout = QVBoxLayout(self.options_frame)
        options_layout.setContentsMargins(constants.INNER_LAYOUT_MARGIN, constants.INNER_LAYOUT_MARGIN, 
                                        constants.INNER_LAYOUT_MARGIN, constants.INNER_LAYOUT_MARGIN)
        options_layout.setSpacing(constants.INNER_LAYOUT_SPACING)
        
        # Skapa en lista för checkboxar som ska visas
        visible_checkboxes = []
        
        # Kontrollera feature-flaggor och lägg till motsvarande checkbox endast om aktiverad
        if constants.FEATURE_EXTRACT_CSV_ENABLED:
            self.extract_csv_checkbox = QCheckBox("Extract - CSV")
            self.extract_csv_checkbox.setChecked(False)  # Selected by default
            self.extract_csv_checkbox.setToolTip("Extract data to CSV format")
            self.extract_csv_checkbox.setMinimumHeight(constants.CHECKBOX_MIN_HEIGHT)
            self.extract_csv_checkbox.setMinimumWidth(constants.CHECKBOX_MIN_WIDTH)
            visible_checkboxes.append(self.extract_csv_checkbox)
        else:
            # Skapa ändå checkboxen men göm den, så att resten av koden som refererar till den fortfarande fungerar
            self.extract_csv_checkbox = QCheckBox("Extract - CSV")
            self.extract_csv_checkbox.hide()
        
        if constants.FEATURE_EXTRACT_MARKDOWN_ENABLED:
            self.extract_markdown_checkbox = QCheckBox("Extract - Markdown")
            self.extract_markdown_checkbox.setChecked(True)  # Selected by default
            self.extract_markdown_checkbox.setToolTip("Extract data to Markdown format")
            self.extract_markdown_checkbox.setMinimumHeight(constants.CHECKBOX_MIN_HEIGHT)
            self.extract_markdown_checkbox.setMinimumWidth(constants.CHECKBOX_MIN_WIDTH)
            visible_checkboxes.append(self.extract_markdown_checkbox)
        else:
            # Skapa ändå checkboxen men göm den
            self.extract_markdown_checkbox = QCheckBox("Extract - Markdown")
            self.extract_markdown_checkbox.hide()
        
        # Lägg till synliga checkboxar i layouten
        for checkbox in visible_checkboxes:
            options_layout.addWidget(checkbox)
        
        # Om inga checkboxar är synliga, kanske vi vill lägga till en platshållare eller ett meddelande
        if not visible_checkboxes:
            placeholder_label = QLabel("No extraction methods available")
            placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            options_layout.addWidget(placeholder_label)
        
        self.options_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                border: 1px solid {ThemeColors.BORDER_COLOR.value};
                border-radius: 4px;
            }}
            QCheckBox {{
                color: {ThemeColors.TEXT_PRIMARY.value};
            }}
        """)
        
        # Fixed height for options frame
        self.options_frame.setFixedHeight(constants.OPTIONS_FRAME_HEIGHT)
        
        self.layout.addWidget(self.options_frame)
        
        # Path display and run button
        self.path_frame = QFrame()
        path_layout = QHBoxLayout(self.path_frame)
        path_layout.setContentsMargins(constants.INNER_LAYOUT_MARGIN, constants.INNER_LAYOUT_MARGIN, 
                                    constants.INNER_LAYOUT_MARGIN, constants.INNER_LAYOUT_MARGIN)
        path_layout.setSpacing(constants.INNER_LAYOUT_SPACING)
        
        self.path_label = QLabel("Working Directory:")
        self.path_label.setToolTip("Click to select working directory")
        
        # Make the path value clickable with better styling
        self.path_value = QLabel("Not selected")
        self.path_value.setStyleSheet(f"""
            color: {ThemeColors.TEXT_PRIMARY.value};
            background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
            border: 1px solid {ThemeColors.BORDER_COLOR.value};
            border-radius: 4px;
            padding: 5px 10px;
        """)
        self.path_value.setToolTip("Click to select working directory")
        self.path_value.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Add folder icon indicator (unicode character)
        self.path_value.setText("📁 Not selected")
        
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_value, 1)
        
        self.path_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                border: 1px solid {ThemeColors.BORDER_COLOR.value};
                border-radius: 4px;
            }}
        """)
        
        self.path_frame.setFixedHeight(constants.PATH_FRAME_HEIGHT)
        self.layout.addWidget(self.path_frame)
        
        # Run button
        self.run_button = QPushButton("Run Extraction")
        self.run_button.setStyleSheet(ThemeManager.get_primary_button_stylesheet())
        self.run_button.setToolTip("Start the extraction process")
        
        # Fixed height for run button
        self.run_button.setFixedHeight(constants.RUN_BUTTON_HEIGHT)
        
        self.layout.addWidget(self.run_button)
        
        # Create a container frame that will always take up the same space,
        # whether progress is visible or not
        self.progress_container = QFrame()
        self.progress_container.setFixedHeight(constants.PROGRESS_CONTAINER_HEIGHT)
        progress_container_layout = QVBoxLayout(self.progress_container)
        progress_container_layout.setContentsMargins(0, 0, 0, 0)
        progress_container_layout.setSpacing(0)
        
        # Progress section
        self.progress_frame = QFrame()
        self.progress_frame.setFixedHeight(constants.PROGRESS_CONTAINER_HEIGHT)
        
        progress_layout = QVBoxLayout(self.progress_frame)
        progress_layout.setContentsMargins(constants.INNER_LAYOUT_MARGIN, constants.INNER_LAYOUT_MARGIN, 
                                        constants.INNER_LAYOUT_MARGIN, constants.INNER_LAYOUT_MARGIN)
        progress_layout.setSpacing(constants.INNER_LAYOUT_SPACING)
        
        # CSV Progress - visa bara om feature är aktiverad
        if constants.FEATURE_EXTRACT_CSV_ENABLED:
            self.csv_group = QFrame()
            csv_layout = QVBoxLayout(self.csv_group)
            csv_layout.setContentsMargins(0, 0, 0, 0)
            csv_layout.setSpacing(5)
            
            self.csv_label = QLabel("CSV Progress:")
            self.csv_progress = QProgressBar()
            self.csv_status = QLabel("")
            
            csv_layout.addWidget(self.csv_label)
            csv_layout.addWidget(self.csv_progress)
            csv_layout.addWidget(self.csv_status)
            
            progress_layout.addWidget(self.csv_group)
        else:
            # Skapa dolda komponenter för att bibehålla referenserna
            self.csv_group = QFrame()
            self.csv_label = QLabel("CSV Progress:")
            self.csv_progress = QProgressBar()
            self.csv_status = QLabel("")
            self.csv_group.hide()
        
        # Markdown Progress - visa bara om feature är aktiverad
        if constants.FEATURE_EXTRACT_MARKDOWN_ENABLED:
            self.markdown_group = QFrame()
            markdown_layout = QVBoxLayout(self.markdown_group)
            markdown_layout.setContentsMargins(0, 0, 0, 0)
            markdown_layout.setSpacing(5)
            
            self.markdown_label = QLabel("Markdown Progress:")
            self.markdown_progress = QProgressBar()
            self.markdown_status = QLabel("")
            
            markdown_layout.addWidget(self.markdown_label)
            markdown_layout.addWidget(self.markdown_progress)
            markdown_layout.addWidget(self.markdown_status)
            
            progress_layout.addWidget(self.markdown_group)
        else:
            # Skapa dolda komponenter för att bibehålla referenserna
            self.markdown_group = QFrame()
            self.markdown_label = QLabel("Markdown Progress:")
            self.markdown_progress = QProgressBar()
            self.markdown_status = QLabel("")
            self.markdown_group.hide()
        
        self.progress_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                border: 1px solid {ThemeColors.BORDER_COLOR.value};
                border-radius: 4px;
            }}
        """)
        
        # Add progress frame to container
        progress_container_layout.addWidget(self.progress_frame)
        
        # Create a placeholder frame to take up the same space
        # This will be shown when progress is hidden
        self.placeholder_frame = QFrame()
        self.placeholder_frame.setFixedHeight(constants.PROGRESS_CONTAINER_HEIGHT)
        self.placeholder_frame.setStyleSheet("background: transparent;")
        progress_container_layout.addWidget(self.placeholder_frame)
        
        # Initially hide progress but show placeholder
        self.progress_frame.hide()
        self.placeholder_frame.show()
        
        # Add the container to the main layout
        self.layout.addWidget(self.progress_container)
        
        # Apply styling
        self.setStyleSheet(ThemeManager.get_card_frame_stylesheet())
        
        # Make sure we have a fixed height
        self.setFixedHeight(self.sizeHint().height())


    def setup_standard_tab(self):
        """Setup the standard extraction tab"""
        layout = QVBoxLayout(self.standard_tab)
        layout.setContentsMargins(constants.TAB_CONTENT_MARGIN, constants.TAB_CONTENT_MARGIN, 
                                constants.TAB_CONTENT_MARGIN, constants.TAB_CONTENT_MARGIN)
        layout.setSpacing(constants.TAB_CONTENT_SPACING)
        
        # Information label
        info_label = QLabel(
            "Standard extraction converts source code files into structured formats."
        )
        info_label.setFont(Fonts.get_default(constants.NORMAL_FONT_SIZE))
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # Button to select input directory
        self.select_input_button = QPushButton("Select Input Directory")
        self.select_input_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        self.select_input_button.setToolTip("Select the directory containing source code files")
        layout.addWidget(self.select_input_button)
        
        # Button to select output directory
        self.select_output_button = QPushButton("Select Output Directory")
        self.select_output_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        self.select_output_button.setToolTip("Select the directory where extracted files will be saved")
        layout.addWidget(self.select_output_button)
        
        layout.addStretch()
    
    def setup_reverse_tab(self):
        """Setup the reverse extraction tab"""
        layout = QVBoxLayout(self.reverse_tab)
        layout.setContentsMargins(constants.TAB_CONTENT_MARGIN, constants.TAB_CONTENT_MARGIN, 
                                constants.TAB_CONTENT_MARGIN, constants.TAB_CONTENT_MARGIN)
        layout.setSpacing(constants.TAB_CONTENT_SPACING)
        
        # Information label
        info_label = QLabel(
            "Reverse extraction converts structured formats back into source code files."
        )
        info_label.setFont(Fonts.get_default(constants.NORMAL_FONT_SIZE))
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # CSV controls
        csv_label = QLabel("CSV Extraction:")
        csv_label.setFont(Fonts.get_bold(constants.NORMAL_FONT_SIZE))
        layout.addWidget(csv_label)
        
        self.select_csv_button = QPushButton("Select CSV File")
        self.select_csv_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        self.select_csv_button.setToolTip("Select the CSV file to extract from")
        layout.addWidget(self.select_csv_button)
        
        self.select_csv_output_button = QPushButton("Select CSV Output Directory")
        self.select_csv_output_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        self.select_csv_output_button.setToolTip("Select the directory where CSV extracted files will be saved")
        layout.addWidget(self.select_csv_output_button)
        
        # Markdown controls
        markdown_label = QLabel("Markdown Extraction:")
        markdown_label.setFont(Fonts.get_bold(constants.NORMAL_FONT_SIZE))
        layout.addWidget(markdown_label)
        
        self.select_markdown_button = QPushButton("Select Markdown File")
        self.select_markdown_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        self.select_markdown_button.setToolTip("Select the Markdown file to extract from")
        layout.addWidget(self.select_markdown_button)
        
        self.select_markdown_output_button = QPushButton("Select Markdown Output Directory")
        self.select_markdown_output_button.setStyleSheet(ThemeManager.get_secondary_button_stylesheet())
        self.select_markdown_output_button.setToolTip("Select the directory where Markdown extracted files will be saved")
        layout.addWidget(self.select_markdown_output_button)
        
        layout.addStretch()
    
    def setup_connections(self):
        """Setup signal connections"""
        # Standard tab connections
        self.select_input_button.clicked.connect(self.select_input_directory)
        self.select_output_button.clicked.connect(self.select_output_directory)
        
        # Reverse tab connections
        self.select_csv_button.clicked.connect(self.select_csv_file)
        self.select_csv_output_button.clicked.connect(self.select_csv_output_directory)
        self.select_markdown_button.clicked.connect(self.select_markdown_file)
        self.select_markdown_output_button.clicked.connect(self.select_markdown_output_directory)
        
        # Working directory connections
        self.path_value.mousePressEvent = self.select_working_directory
        
        # Run button
        self.run_button.clicked.connect(self.run_extraction)
        
        # Tab switching
        self.tabs.currentChanged.connect(self.handle_tab_change)
        
        # Listen for preset changes from parent window
        parent = self.parent()
        if parent and hasattr(parent, 'file_specific_frame'):
            parent.file_specific_frame.preset_changed.connect(self.handle_preset_change)
    
    def handle_preset_change(self, preset_name, files):
        """Handle updates when a preset is changed"""
        self.current_preset = preset_name
        self.current_preset_files = files.copy()
        print(f"Extraction Frame: Preset changed to '{preset_name}' with {len(files)} files")
    
    def handle_tab_change(self, index):
        """Handle tab changes and update UI accordingly"""
        # Update checkboxes based on tab
        if index == 0:  # Standard extraction
            self.extract_csv_checkbox.setChecked(True)
            self.extract_markdown_checkbox.setChecked(True)
        else:  # Reverse extraction
            # We typically only do one type of reverse extraction at a time
            self.extract_csv_checkbox.setChecked(True)
            self.extract_markdown_checkbox.setChecked(False)
    
    def select_working_directory(self, event):
        """Open file dialog to select working directory when clicking on path value"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Working Directory",
            self.settings_manager.get_setting("paths", "base_dir", "")
        )
        
        if directory:
            if not os.path.isdir(directory):
                QMessageBox.warning(
                    self,
                    "Invalid Directory",
                    "The selected path is not a valid directory."
                )
                return
                
            # Update settings and UI
            self.settings_manager.update_setting("paths", "base_dir", directory)
            self.path_value.setText(f"📁 {directory}")
            
            # Reset error styling if it was applied
            self.path_value.setStyleSheet(f"""
                color: {ThemeColors.TEXT_PRIMARY.value};
                background-color: {ThemeColors.SECONDARY_BACKGROUND.value};
                border: 1px solid {ThemeColors.BORDER_COLOR.value};
                border-radius: 4px;
                padding: 5px 10px;
            """)
            
            # Automatically set output directory if not already set
            output_dir = self.settings_manager.get_setting("paths", "output_dir", "")
            if not output_dir:
                default_output = os.path.join(directory, "output")
                self.settings_manager.update_setting("paths", "output_dir", default_output)
    
    def select_input_directory(self):
        """Open file dialog to select input directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Input Directory",
            self.settings_manager.get_setting("paths", "base_dir", "")
        )
        
        if directory:
            self.settings_manager.update_setting("paths", "base_dir", directory)
            self.path_value.setText(f"📁 {directory}")
    
    def select_output_directory(self):
        """Open file dialog to select output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.settings_manager.get_setting("paths", "output_dir", "")
        )
        
        if directory:
            self.settings_manager.update_setting("paths", "output_dir", directory)
    
    def select_csv_file(self):
        """Open file dialog to select CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            self.settings_manager.get_setting("paths", "base_dir", ""),
            "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
        )
        
        if file_path:
            self.settings_manager.update_setting("paths", "select_csv_reverse_file", file_path)
    
    def select_csv_output_directory(self):
        """Open file dialog to select CSV output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select CSV Output Directory",
            self.settings_manager.get_setting("paths", "output_dir", "")
        )
        
        if directory:
            self.settings_manager.update_setting("paths", "select_csv_output_reverse_dir", directory)
    
    def select_markdown_file(self):
        """Open file dialog to select Markdown file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Markdown File",
            self.settings_manager.get_setting("paths", "base_dir", ""),
            "Markdown Files (*.md);;All Files (*)"
        )
        
        if file_path:
            self.settings_manager.update_setting("paths", "select_markdown_reverse_file", file_path)
    
    def select_markdown_output_directory(self):
        """Open file dialog to select Markdown output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Markdown Output Directory",
            self.settings_manager.get_setting("paths", "output_dir", "")
        )
        
        if directory:
            self.settings_manager.update_setting("paths", "select_markdown_output_reverse_dir", directory)
    
    def run_extraction(self):
        """Run the extraction process based on current settings"""
        # Check if base directory is set
        base_dir = self.settings_manager.get_setting("paths", "base_dir", "")
        if not base_dir or not os.path.isdir(base_dir):
            QMessageBox.warning(
                self,
                "No Working Directory",
                "Please select a valid working directory first by clicking on the path display."
            )
            return
            
        # Get current tab
        current_tab = self.tabs.currentWidget()
        
        if current_tab == self.standard_tab:
            self.run_standard_extraction()
        else:
            self.run_reverse_extraction()
    
    def run_standard_extraction(self):
        """Run the standard extraction process with improved file handling"""
        # Get paths
        base_dir = self.settings_manager.get_setting("paths", "base_dir", "")
        output_dir = self.settings_manager.get_setting("paths", "output_dir", "")
        
        # Improved validation - check if path exists
        if not base_dir or not os.path.isdir(base_dir):
            QMessageBox.warning(
                self,
                "Invalid Input Directory",
                "Please select a valid input directory first."
            )
            return
        
        if not output_dir:
            # Default output directory inside the base directory
            output_dir = os.path.join(base_dir, "output")
            self.settings_manager.update_setting("paths", "output_dir", output_dir)
        
        # Create output directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Output Directory Error",
                f"Failed to create output directory: {str(e)}"
            )
            return
            
        # Check which extractions to run
        run_csv = self.extract_csv_checkbox.isChecked()
        run_markdown = self.extract_markdown_checkbox.isChecked()
        
        if not run_csv and not run_markdown:
            QMessageBox.warning(
                self,
                "No Extraction Selected",
                "Please select at least one extraction type."
            )
            return
        
        # Get file specific mode
        use_file_specific = self.settings_manager.get_setting("file_specific", "use_file_specific", False)
        specific_files = []
        
        # Get files from current preset if file specific is enabled
        if use_file_specific and self.current_preset and self.current_preset_files:
            specific_files = self.current_preset_files
            print(f"Using specific files from preset '{self.current_preset}': {len(specific_files)} files")
            
            if len(specific_files) == 0:
                QMessageBox.warning(
                    self,
                    "No Files in Preset",
                    f"The selected preset '{self.current_preset}' contains no files. Please add files to the preset first."
                )
                return
                
            # Add check for too many files
            if len(specific_files) > 5000:
                reply = QMessageBox.question(
                    self,
                    "Large File Count Warning",
                    f"You are about to process {len(specific_files)} files, which might take a long time. Continue?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return
        
        # Show progress UI by swapping frames instead of hiding/showing
        self.placeholder_frame.hide()
        self.progress_frame.show()
        
        self.csv_group.setVisible(run_csv)
        self.markdown_group.setVisible(run_markdown)
        self.run_button.setEnabled(False)
        
        # Reset progress bars
        if run_csv:
            self.csv_progress.setValue(0)
            self.csv_status.setText("Starting extraction...")
        
        if run_markdown:
            self.markdown_progress.setValue(0)
            self.markdown_status.setText("Starting extraction...")
        
        # Signal that extraction has started
        self.extraction_started.emit()
        
        # Run CSV extraction
        if run_csv:
            try:
                self.csv_worker = ExtractionWorker(
                    CSVEx,
                    base_dir,
                    output_dir,
                    self.settings_manager.settings_path
                )
                
                # Set file list if using specific files
                if use_file_specific and specific_files:
                    # Add attribute to worker for the extractor to use
                    self.csv_worker.specific_files = specific_files
                    print(f"Added {len(specific_files)} files to CSV worker")
                
                # Connect signals
                self.csv_worker.progress_updated.connect(self.update_csv_progress)
                self.csv_worker.status_updated.connect(self.update_csv_status)
                self.csv_worker.extraction_complete.connect(self.handle_csv_completed)
                self.csv_worker.extraction_error.connect(self.handle_extraction_error)
                
                # Start worker
                self.csv_worker.start()
                print("Started CSV extraction worker")
            except Exception as e:
                self.handle_extraction_error(f"CSV extraction setup error: {str(e)}")
        
        # Run Markdown extraction
        if run_markdown:
            try:
                self.markdown_worker = ExtractionWorker(
                    MarkdownEx,
                    base_dir,
                    output_dir,
                    self.settings_manager.settings_path
                )
                
                # Set file list if using specific files
                if use_file_specific and specific_files:
                    # Add attribute to worker for the extractor to use
                    self.markdown_worker.specific_files = specific_files
                    print(f"Added {len(specific_files)} files to Markdown worker")
                
                # Connect signals
                self.markdown_worker.progress_updated.connect(self.update_markdown_progress)
                self.markdown_worker.status_updated.connect(self.update_markdown_status)
                self.markdown_worker.extraction_complete.connect(self.handle_markdown_completed)
                self.markdown_worker.extraction_error.connect(self.handle_extraction_error)
                
                # Start worker
                self.markdown_worker.start()
                print("Started Markdown extraction worker")
            except Exception as e:
                self.handle_extraction_error(f"Markdown extraction setup error: {str(e)}")
  
    def run_reverse_extraction(self):
        """Run the reverse extraction process"""
        # Check which tab we're in
        current_tab_index = self.tabs.currentIndex()
        
        # Get paths based on extraction type
        if current_tab_index == 1:  # Reverse tab
            # CSV extraction
            if self.extract_csv_checkbox.isChecked():
                csv_file = self.settings_manager.get_setting("paths", "select_csv_reverse_file", "")
                csv_output = self.settings_manager.get_setting("paths", "select_csv_output_reverse_dir", "")
                
                # Improved validation
                if not csv_file or not os.path.isfile(csv_file):
                    QMessageBox.warning(
                        self,
                        "Invalid CSV File",
                        "Please select a valid CSV file."
                    )
                    return
                    
                if not csv_output or not os.path.isdir(os.path.dirname(csv_output)):
                    QMessageBox.warning(
                        self,
                        "Invalid Output Directory",
                        "Please select a valid output directory."
                    )
                    return
                
                # Show progress UI by swapping frames
                self.placeholder_frame.hide()
                self.progress_frame.show()
                
                self.csv_group.show()
                self.markdown_group.hide()
                self.run_button.setEnabled(False)
                
                # Reset progress
                self.csv_progress.setValue(0)
                self.csv_status.setText("Starting reverse CSV extraction...")
                
                # Signal extraction start
                self.extraction_started.emit()
                
                # Run reverse CSV extraction
                try:
                    self.csv_worker = ExtractionWorker(
                        ReverseCSVEx,
                        csv_file,
                        csv_output,
                        self.settings_manager.settings_path
                    )
                    
                    # Connect signals
                    self.csv_worker.progress_updated.connect(self.update_csv_progress)
                    self.csv_worker.status_updated.connect(self.update_csv_status)
                    self.csv_worker.extraction_complete.connect(self.handle_csv_completed)
                    self.csv_worker.extraction_error.connect(self.handle_extraction_error)
                    
                    # Start worker
                    self.csv_worker.start()
                    print("Started reverse CSV extraction")
                except Exception as e:
                    self.handle_extraction_error(f"Reverse CSV extraction setup error: {str(e)}")
            
            # Markdown extraction
            elif self.extract_markdown_checkbox.isChecked():
                md_file = self.settings_manager.get_setting("paths", "select_markdown_reverse_file", "")
                md_output = self.settings_manager.get_setting("paths", "select_markdown_output_reverse_dir", "")
                
                # Improved validation
                if not md_file or not os.path.isfile(md_file):
                    QMessageBox.warning(
                        self,
                        "Invalid Markdown File",
                        "Please select a valid Markdown file."
                    )
                    return
                
                # Handle case where output is a list
                if isinstance(md_output, list):
                    md_output = md_output[0] if md_output else ""
                    
                if not md_output or not os.path.isdir(os.path.dirname(md_output)):
                    QMessageBox.warning(
                        self,
                        "Invalid Output Directory",
                        "Please select a valid output directory."
                    )
                    return
                
                # Show progress UI by swapping frames
                self.placeholder_frame.hide()
                self.progress_frame.show()
                
                self.csv_group.hide()
                self.markdown_group.show()
                self.run_button.setEnabled(False)
                
                # Reset progress
                self.markdown_progress.setValue(0)
                self.markdown_status.setText("Starting reverse Markdown extraction...")
                
                # Signal extraction start
                self.extraction_started.emit()
                
                # Run reverse Markdown extraction
                try:
                    self.markdown_worker = ExtractionWorker(
                        ReverseMarkdownEx,
                        md_file,
                        md_output,
                        self.settings_manager.settings_path
                    )
                    
                    # Connect signals
                    self.markdown_worker.progress_updated.connect(self.update_markdown_progress)
                    self.markdown_worker.status_updated.connect(self.update_markdown_status)
                    self.markdown_worker.extraction_complete.connect(self.handle_markdown_completed)
                    self.markdown_worker.extraction_error.connect(self.handle_extraction_error)
                    
                    # Start worker
                    self.markdown_worker.start()
                    print("Started reverse Markdown extraction")
                except Exception as e:
                    self.handle_extraction_error(f"Reverse Markdown extraction setup error: {str(e)}")
            
            else:
                QMessageBox.warning(
                    self,
                    "No Extraction Selected",
                    "Please select at least one extraction type."
                )

    def update_csv_progress(self, value):
        """Update CSV progress bar"""
        self.csv_progress.setValue(value)
    
    def update_csv_status(self, message):
        """Update CSV status label"""
        self.csv_status.setText(message)
    
    def update_markdown_progress(self, value):
        """Update Markdown progress bar"""
        self.markdown_progress.setValue(value)
    
    def update_markdown_status(self, message):
        """Update Markdown status label"""
        self.markdown_status.setText(message)
    
    def handle_csv_completed(self):
        """Handle CSV extraction completion"""
        print("CSV extraction completed")
        self.csv_group.hide()
        
        # Check if all extractions are complete
        self.check_all_completed()
    
    def handle_markdown_completed(self):
        """Handle Markdown extraction completion"""
        print("Markdown extraction completed")
        self.markdown_group.hide()
        
        # Check if all extractions are complete
        self.check_all_completed()
    
    def check_all_completed(self):
        """Check if all extractions are complete and update UI accordingly"""
        all_complete = True
        
        if self.extract_csv_checkbox.isChecked() and self.csv_group.isVisible():
            all_complete = False
        
        if self.extract_markdown_checkbox.isChecked() and self.markdown_group.isVisible():
            all_complete = False
        
        if all_complete:
            # Switch back to placeholder instead of hiding progress frame
            self.progress_frame.hide()
            self.placeholder_frame.show()
            
            self.run_button.setEnabled(True)
            self.extraction_completed.emit()
            
            # Show message after UI is stable
            QMessageBox.information(
                self,
                "Extraction Complete",
                "All extraction tasks have completed successfully."
            )

    def handle_extraction_error(self, error_message):
        """Handle extraction errors"""
        print(f"Extraction error: {error_message}")
        
        # Switch back to placeholder instead of hiding progress frame
        self.progress_frame.hide()
        self.placeholder_frame.show()
        
        self.run_button.setEnabled(True)
        self.extraction_failed.emit(error_message)
        
        QMessageBox.critical(
            self,
            "Extraction Error",
            f"An error occurred during extraction:\n{error_message}"
        )
    
    def cleanup(self):
        """Clean up resources and threads properly"""
        print("Cleaning up extraction frame resources")
        
        # Stop and clean up CSV worker
        if hasattr(self, 'csv_worker') and self.csv_worker:
            if self.csv_worker.isRunning():
                print("Stopping CSV worker")
                self.csv_worker.stop()
                self.csv_worker.wait()
            self.csv_worker = None
        
        # Stop and clean up Markdown worker
        if hasattr(self, 'markdown_worker') and self.markdown_worker:
            if self.markdown_worker.isRunning():
                print("Stopping Markdown worker")
                self.markdown_worker.stop()
                self.markdown_worker.wait()
            self.markdown_worker = None




```

---

# ..\..\gui\file_specific_frame.py
## File: ..\..\gui\file_specific_frame.py

```py
# ..\..\gui\file_specific_frame.py
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
```

---

# ..\..\gui\theme_manager.py
## File: ..\..\gui\theme_manager.py

```py
# ..\..\gui\theme_manager.py
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
```

---

# ..\..\gui\settings_manager.py
## File: ..\..\gui\settings_manager.py

```py
# ..\..\gui\settings_manager.py
# -*- coding: utf-8 -*-
# settings_manager.py

import os
import toml
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from pathlib import Path
from PySide6.QtCore import QObject, Signal

@dataclass
class SettingsData:
    """Data class for storing settings with type hints"""
    paths: Dict[str, str]
    files: Dict[str, list]
    directories: Dict[str, list]
    file_specific: Dict[str, Any]
    output: Dict[str, str]
    metrics: Dict[str, str]
    presets: Dict[str, list]

class SettingsManager(QObject):
    """Settings Manager for application configuration"""
    
    # Signal emitted when settings are modified
    settings_changed = Signal()  
    
    def __init__(self, settings_path: str):
        super().__init__()
        self._settings_path = Path(settings_path).resolve()
        self._settings: Optional[SettingsData] = None
        self._load_settings()
    
    def _create_default_settings(self) -> SettingsData:
        """Create default settings structure"""
        return SettingsData(
            paths={
                "base_dir": "",
                "output_dir": "",
                "select_csv_reverse_file": "",
                "select_csv_output_reverse_dir": "",
                "select_markdown_reverse_file": "",
                "select_markdown_output_reverse_dir": "",
                "path_style": "system"
            },
            files={
                "ignored_extensions": [".exe", ".dll"],
                "ignored_files": ["file_to_ignore.txt"]
            },
            directories={"ignored_directories": ["dir_to_ignore"]},
            file_specific={
                "use_file_specific": False,
                "specific_files": [""]
            },
            output={
                "markdown_file_prefix": "Full_Project",
                "csv_file_prefix": "Detailed_Project"
            },
            metrics={"size_unit": "KB"},
            presets={"default": [], "current_preset": "default"}  # Added current_preset
        )
    
    def _load_settings(self) -> None:
        """Load settings with error handling and path normalization"""
        try:
            if not self._settings_path.exists():
                self._settings = self._create_default_settings()
                self._save_settings()
                return

            with self._settings_path.open('r', encoding='utf-8') as f:
                content = f.read().replace('\\', '/')
                data = toml.loads(content)
                
            # Convert loaded data to SettingsData
            self._settings = SettingsData(**data)
            
            # Ensure current_preset exists
            if 'current_preset' not in self._settings.presets:
                self._settings.presets['current_preset'] = next(iter(self._settings.presets.keys()), "default")
                
            self._normalize_paths()
            
        except Exception as e:
            print(f"Error loading settings: {e}")
            self._settings = self._create_default_settings()
            self._save_settings()
    
    def _normalize_paths(self) -> None:
        """Normalize all paths in settings"""
        if not self._settings:
            return
            
        def normalize(value: Any) -> Any:
            if isinstance(value, str) and ('/' in value or '\\' in value):
                return str(Path(value).resolve())
            if isinstance(value, list):
                return [normalize(item) for item in value]
            if isinstance(value, dict):
                return {k: normalize(v) for k, v in value.items()}
            return value

        self._settings.paths = normalize(self._settings.paths)
    
    def _save_settings(self) -> None:
        """Save settings with proper path handling"""
        if not self._settings:
            return
            
        try:
            # Ensure directory exists
            self._settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert SettingsData to dict and save
            settings_dict = {
                field: getattr(self._settings, field)
                for field in self._settings.__annotations__
            }
            
            with self._settings_path.open('w', encoding='utf-8') as f:
                toml.dump(settings_dict, f)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def update_setting(self, section: str, key: str, value: Any) -> None:
        """Update a setting value, create it if missing, and emit change signal"""
        if not self._settings:
            return

        # Access or create the section dictionary
        section_dict = getattr(self._settings, section, None)
        if section_dict is None:
            section_dict = {}
            setattr(self._settings, section, section_dict)

        # Special handling for current_preset to ensure it's a string, not a list
        if section == "presets" and key == "current_preset":
            section_dict[key] = value
        # Standard handling for other settings
        elif isinstance(section_dict, dict):
            if key not in section_dict:
                # Create a new preset if it doesn't exist
                section_dict[key] = value if isinstance(value, list) else [value]
            elif isinstance(section_dict[key], list) and isinstance(value, list):
                # Append items to an existing list if `value` is a list
                section_dict[key] = list(set(section_dict[key] + value))  # Remove duplicates
            else:
                section_dict[key] = value

            # Save the updated settings to the file
            self._save_settings()
            self.settings_changed.emit()
        else:
            print(f"Section '{section}' is not a dictionary or does not exist in settings.")
            print(f"Section '{section}' is not a dictionary or does not exist in settings.")

    @property
    def settings_path(self) -> str:
        """Expose the settings path as a read-only property."""
        return str(self._settings_path)

    @property
    def settings(self) -> Optional[SettingsData]:
        """Property to access settings data"""
        return self._settings

    def get_setting(self, section: str, key: Optional[str] = None, default: Any = None) -> Any:
        """Safely get a setting value or entire section if key is None"""
        if not self._settings or not hasattr(self._settings, section):
            return default

        section_dict = getattr(self._settings, section)
        if key is None:
            return section_dict
        return section_dict.get(key, default)
    
    def get_section(self, section: str, default: Any = None) -> Any:
        """Retrieve the entire section dictionary"""
        if not self._settings or not hasattr(self._settings, section):
            return default
        return getattr(self._settings, section)
    
    def remove_setting(self, section: str, key: str) -> None:
        """Remove a setting key from a section"""
        if not self._settings or not hasattr(self._settings, section):
            return

        section_dict = getattr(self._settings, section)
        if isinstance(section_dict, dict) and key in section_dict:
            # Don't remove current_preset
            if section == "presets" and key == "current_preset":
                print("Cannot remove current_preset setting")
                return
                
            del section_dict[key]
            
            # If we removed the current preset, update current_preset to another preset
            if section == "presets" and section_dict.get("current_preset") == key:
                next_preset = next(iter([k for k in section_dict.keys() if k != "current_preset"]), "")
                section_dict["current_preset"] = next_preset
            
            self._save_settings()
            self.settings_changed.emit()


```

---

# ..\..\gui\constants.py
## File: ..\..\gui\constants.py

```py
# ..\..\gui\constants.py
# -*- coding: utf-8 -*-
# constants.py

"""
Centraliserad konfiguration med konstanter för applikationens UI element.
Används för att enkelt ändra storlekar, marginaler och andra UI-parametrar.
"""

## ------------ ## Theme-Manager - inställningar ## ------------ ##

# Font sizes (utökat)
DEFAULT_FONT_SIZE = 10           # Standard fontstorlek för applikationen

# UI Component dimensions
BUTTON_BORDER_RADIUS = 4         # Hörnradie för knappar
FRAME_BORDER_RADIUS = 8          # Hörnradie för frames
CHECKBOX_INDICATOR_SIZE = 16     # Storlek på checkbox indikatorer
GROUP_BOX_BORDER_RADIUS = 6      # Hörnradie för grupplådor
CARD_FRAME_PADDING = 15          # Inre padding för card frames
CARD_FRAME_MARGIN = 15           # Yttre marginal för card frames
SCROLLBAR_WIDTH = 14             # Bredd på scrollbars
SCROLLBAR_MIN_HANDLE_HEIGHT = 30 # Minsta höjd på scrollbar handles
LINE_EDIT_PADDING = 5            # Padding för text inputs
TAB_BAR_PADDING = "8px 12px"     # Padding för tab bar flikar
TAB_BAR_MIN_WIDTH = 80           # Minsta bredd för tab bar flikar

## ------------ ## Allmänna UI-inställningar ## ------------ ##
# Layout spacing
MAIN_LAYOUT_MARGIN = 10          # Marginaler runt huvudlayout
MAIN_LAYOUT_SPACING = 8          # Mellanrum mellan widgets i huvudlayout
INNER_LAYOUT_MARGIN = 8          # Marginaler för inre layouts
INNER_LAYOUT_SPACING = 5         # Mellanrum mellan widgets i inre layouts

# Minimum dimensions
MIN_FRAME_WIDTH = 280            # Minsta bredd för frames
BORDER_RADIUS = 4                # Standardradie för hörn
BORDER_WIDTH = 1                 # Standardbredd på ramar

# Font sizes
HEADER_FONT_SIZE = 13            # Storlek på rubriker
NORMAL_FONT_SIZE = 9             # Storlek på normal text
BUTTON_FONT_SIZE = 10            # Storlek på knappar

# Button padding (kan användas i stylesheet)
BUTTON_PADDING = "6px 12px"      # Padding för knappar

# Animation durations (millisekunder)
STATUS_MESSAGE_DURATION = 3000   # Varaktighet för statusmeddelanden

## ------------ ## MainWindow ## ------------ ##
# Main window dimensions
DEFAULT_WINDOW_WIDTH = 1100      # Standardbredd för huvudfönster
DEFAULT_WINDOW_HEIGHT = 750      # Standardhöjd för huvudfönster
RESPONSIVE_BREAKPOINT = 750      # Breakpoint för responsiv layout
STATUSBAR_HEIGHT = 20            # Höjd på statusbaren

# Layout settings
MAIN_LAYOUT_MARGIN = 0           # Marginaler för huvudlayout i MainWindow
MAIN_LAYOUT_SPACING = 0          # Mellanrum i huvudlayout i MainWindow
CONTENT_LAYOUT_MARGIN = 10       # Marginaler för contentlayout i MainWindow
CONTENT_LAYOUT_SPACING = 10      # Mellanrum i contentlayout i MainWindow

# Panel dimensions
PANEL_MIN_WIDTH = 300            # Minsta bredd för paneler
SPLITTER_INITIAL_SIZE = 600      # Initial storlek för splitter-delar
SPLITTER_DEFAULT_RATIO = 0.45    # Standardförhållande mellan vänster och höger panel

# Status bar
STATUS_BAR_PADDING = 3           # Padding för statusbar
STATUS_BAR_MAX_HEIGHT = 24       # Maxhöjd för statusbar
PATH_VALUE_PADDING = "5px 10px"  # Padding för sökvägsvisning
PATH_VALUE_BORDER_RADIUS = 4     # Hörnradie för sökvägsvisning


## ------------ ## Settings Dialog ## ------------ ##
SETTINGS_DIALOG_WIDTH = 550      # Bredd på inställningsdialogen
SETTINGS_DIALOG_HEIGHT = 350     # Höjd på inställningsdialogen

## ------------ ## HeaderFrame ## ------------ ##
HEADER_HEIGHT = 60               # Höjd på header-ramen
HEADER_TITLE_FONT_SIZE = 18      # Storlek på rubriktexten i header
HEADER_BUTTON_WIDTH = 40         # Bredd på header-knapparna
HEADER_LAYOUT_MARGIN_H = 10      # Horisontell marginal för header-layout
HEADER_LAYOUT_MARGIN_V = 5       # Vertikal marginal för header-layout
HEADER_MENU_ITEM_PADDING = "8px 16px"  # Padding för poster i header-menyn

## ------------ ## FileSpecificFrame ## ------------ ##
FILE_LIST_MIN_HEIGHT = 150       # Minsta höjd för fillistan
PRESET_COMBO_MIN_WIDTH = 100     # Minsta bredd för preset-comboboxen
FILE_FRAME_LAYOUT_MARGIN = 15    # Marginaler för FileSpecificFrame layout
FILE_FRAME_SPACING = 10          # Avstånd mellan element i FileSpecificFrame
FILE_HEADER_FONT_SIZE = 14       # Storlek på rubriktexten i FileSpecificFrame

# Preset management
MAX_PRESETS = 20                 # Maxantal presets
MAX_FILES_PER_PRESET = 5000      # Maxantal filer per preset
FILE_WARNING_THRESHOLD = 1000    # Visa varning om fler än detta antal filer

## ------------ ## ExtractionFrame ## ------------ ##
# Frame heights
PROGRESS_CONTAINER_HEIGHT = 150  # Höjd på progress container
OPTIONS_FRAME_HEIGHT = 80        # Höjd på options frame
RUN_BUTTON_HEIGHT = 35           # Höjd på run button
PATH_FRAME_HEIGHT = 45           # Höjd på sökvägsrutan

# Tab dimensions
TAB_CONTENT_MARGIN = 8           # Marginaler för innehåll i tabbar
TAB_CONTENT_SPACING = 10         # Mellanrum mellan widgets i tabbar

# Extraction controls
CHECKBOX_MIN_HEIGHT = 25         # Minsta höjd för checkboxes
CHECKBOX_MIN_WIDTH = 120         # Minsta bredd för checkboxes
PROGRESS_BAR_HEIGHT = 18         # Höjd på progressbarer

## ------------ ## SettingsFrame ## ------------ ##
SETTINGS_GROUP_SPACING = 10      # Mellanrum mellan grupperna i inställningarna
SETTINGS_FIELD_HEIGHT = 30       # Höjd på inställningsfält
SETTINGS_FRAME_LAYOUT_MARGIN = 15    # Marginaler för SettingsFrame layout
SETTINGS_FRAME_SPACING = 15      # Avstånd mellan element i SettingsFrame
SETTINGS_GROUP_HEADER_FONT_SIZE = 11  # Fontstorlek för grupprubrikerna i inställningar

## ------------ ## Dialoger och popups ## ------------ ##
MESSAGE_BOX_WIDTH = 400          # Bredd på meddelandeboxar
CONFIRMATION_DIALOG_WIDTH = 350  # Bredd på bekräftelsedialoger
DIALOG_BUTTON_HEIGHT = 32        # Höjd på dialogknappar


## ------------ ## Feature Flags ## ------------ ##
# Sätt dessa till True för att aktivera, False för att inaktivera & göm dom från GUI

## ------------ ## Standard Extractions Flags ## ------------ ##
FEATURE_EXTRACT_CSV_ENABLED = False       # Aktivera / (Göm+inaktivera) Extract CSV funktionalitet
FEATURE_EXTRACT_MARKDOWN_ENABLED = True   # Aktivera / (Göm+inaktivera)  Extract MARKDOWN funktionalitet

## ------------ ## Reverse Extractions Flags ## ------------ ##
FEATURE_REVERSE_CSV_EXTRACTION_ENABLED = True # Aktivera / (Göm+inaktivera) Reverse Extraction funktionalitet
FEATURE_REVERSE_MARKDOWNEXTRACTION_ENABLED = True # Aktivera / (Göm+inaktivera) Reverse Extraction funktionalitet

```

---

# ..\..\gui\extraction_worker.py
## File: ..\..\gui\extraction_worker.py

```py
# ..\..\gui\extraction_worker.py
# -*- coding: utf-8 -*-
# extraction_worker.py

import os
from PySide6.QtCore import QThread, Signal

class ExtractionWorker(QThread):
    """Worker thread for extraction operations with improved file handling"""
    
    # Signals
    progress_updated = Signal(int)
    status_updated = Signal(str)
    extraction_complete = Signal()
    extraction_error = Signal(str)
    
    def __init__(self, extractor_class, input_path, output_path, settings_path=None):
        super().__init__()
        self.extractor_class = extractor_class
        self.input_path = input_path
        self.output_path = output_path
        self.settings_path = settings_path
        self._stop_requested = False
        
        # Add specific_files attribute (empty by default)
        self.specific_files = []

    def run(self):
        """Execute the extraction process with proper file handling"""
        try:
            # Debug the specific files before processing
            if hasattr(self, 'specific_files') and self.specific_files:
                print(f"ExtractionWorker specific_files before processing: {self.specific_files}")
                # Validate files - skip single character entries which are usually errors
                self.specific_files = [f for f in self.specific_files if isinstance(f, str) and len(f) > 1]
                print(f"Filtered to {len(self.specific_files)} valid files")
            
            # Create extractor instance
            if self.extractor_class.__name__ in ['CSVEx', 'MarkdownEx', 'ReverseCSVEx', 'ReverseMarkdownEx']:
                # These classes take settings_path as a parameter
                extractor = self.extractor_class(
                    self.input_path,
                    self.output_path,
                    self.settings_path
                )
            else:
                # Generic fallback if class doesn't match expected pattern
                extractor = self.extractor_class(
                    self.input_path,
                    self.output_path
                )
            
            # Process and validate specific files
            valid_specific_files = []
            if hasattr(self, 'specific_files') and self.specific_files:
                # Check if specific_files is a string instead of a list (which would be an error)
                if isinstance(self.specific_files, str):
                    print(f"ERROR: specific_files is a string '{self.specific_files}' not a list!")
                    # Convert to a list with the string as a single item
                    self.specific_files = [self.specific_files]
                
                for file_path in self.specific_files:
                    # Skip if file_path is a single character (likely parsing error)
                    if isinstance(file_path, str) and len(file_path) <= 1:
                        print(f"Skipping invalid file path: '{file_path}'")
                        continue
                        
                    # Handle relative vs absolute paths
                    full_path = file_path
                    if isinstance(file_path, str) and not os.path.isabs(file_path):
                        full_path = os.path.join(self.input_path, file_path)
                        
                    # Fix potential path separator issues
                    full_path = os.path.normpath(full_path)
                    
                    # Only add file if it exists
                    if os.path.exists(full_path):
                        valid_specific_files.append(file_path)  # Keep original relative path
                        print(f"Added valid file: {file_path}")
                    else:
                        print(f"Warning: File does not exist: {full_path}")
                
                # Log the processed files
                print(f"Processed {len(valid_specific_files)} valid files out of {len(self.specific_files)} specified")
                
                # Set the validated files to the extractor
                if valid_specific_files:
                    if hasattr(extractor, 'set_specific_files'):
                        extractor.set_specific_files(valid_specific_files)
                        print("Called set_specific_files method on extractor")
                    else:
                        extractor.specific_files = valid_specific_files
                        print("Set specific_files attribute directly on extractor")
                else:
                    print("Warning: No valid files to process!")
            
            # Connect progress and status callbacks
            if hasattr(extractor, 'update_progress'):
                extractor.update_progress = self.update_progress
            if hasattr(extractor, 'update_status'):
                extractor.update_status = self.update_status
            
            # Run extraction
            if not self._stop_requested:
                extractor.run()
                
            # Signal completion
            if not self._stop_requested:
                self.extraction_complete.emit()
                
        except Exception as e:
            # Add more details to the error message
            import traceback
            error_trace = traceback.format_exc()
            detailed_error = f"{str(e)}\n\nTraceback:\n{error_trace}"
            print(f"Extraction error: {detailed_error}")
            
            # Signal error
            self.extraction_error.emit(str(e))
    
    def update_progress(self, value):
        """Update progress value"""
        self.progress_updated.emit(value)
    
    def update_status(self, message):
        """Update status message"""
        self.status_updated.emit(message)
    
    def stop(self):
        """Request worker to stop"""
        self._stop_requested = True
```

---

# ..\..\gui\header_frame.py
## File: ..\..\gui\header_frame.py

```py
# ..\..\gui\header_frame.py
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
```

---

# ..\..\gui\extractorz.py
## File: ..\..\gui\extractorz.py

```py
# ..\..\gui\extractorz.py
# -*- coding: utf-8 -*-
# ./extractorz.py

from PySide6.QtCore import QObject, Signal, Slot

import os
import pandas as pd

import os
import pandas as pd
import os
import re
import toml
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any

import os
import re
import toml
import zipfile
import shutil
import pandas as pd
from pathlib import Path
import os
import re
import toml
import zipfile
import shutil
import pandas as pd
from pathlib import Path



class MarkdownEx:
    def __init__(self, base_dir, output_dir, settings_path):
        self.base_dir = os.path.normpath(base_dir).replace('\\', '/')
        self.output_dir = os.path.normpath(output_dir).replace('\\', '/')
        self.extract_dir = os.path.normpath(os.path.join(base_dir, 'extract')).replace('\\', '/')
        self.settings_path = os.path.normpath(settings_path).replace('\\', '/')
        self.settings = self.load_settings()
        self.update_progress = None  # For GUI progress
        self.update_status = None    # For GUI status messages
        self._is_running = True
        os.makedirs(self.output_dir, exist_ok=True)

    def stop(self):
        """Stop the extraction process gracefully."""
        self._is_running = False

    def load_settings(self):
        """Load TOML settings and normalize paths."""
        try:
            settings = toml.load(self.settings_path)
            self.normalize_paths(settings)
            
            # Ensure paths section exists
            if 'paths' not in settings:
                settings['paths'] = {}
            
            # Always set Windows as default path style if not specified
            settings['paths']['path_style'] = settings['paths'].get('path_style', 'windows')
            
            return settings
        except toml.TomlDecodeError as e:
            print(f"Error loading settings: {e}")
            raise

    def normalize_paths(self, settings_dict):
        """Recursively normalize all paths in the loaded settings."""
        for section in settings_dict:
            for key, value in settings_dict[section].items():
                if isinstance(value, str) and ('/' in value or '\\' in value):
                    settings_dict[section][key] = os.path.normpath(value).replace('\\', '/')
                elif isinstance(value, list):
                    settings_dict[section][key] = [
                        os.path.normpath(item).replace('\\', '/') 
                        if isinstance(item, str) and ('/' in item or '\\' in item) else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    self.normalize_paths(value)

    def save_settings(self):
        """If your app needs to write updated settings, implement here."""
        with open(self.settings_path, 'w') as settings_file:
            toml.dump(self.settings, settings_file)

    def should_skip_directory(self, dir_path):
        """Check if directory should be skipped based on 'skip_paths' or ignored dirs."""
        for skip_path in self.settings['paths'].get('skip_paths', []):
            if dir_path.startswith(skip_path) or os.path.basename(dir_path) in self.settings['directories']['ignored_directories']:
                return True
        return False

    def format_path(self, relative_path):
        """Format the path based on the selected path style."""
        path = relative_path.replace('/', os.sep)
        # Default to windows style if path_style is not set or is invalid
        path_style = self.settings.get('paths', {}).get('path_style', 'windows')
        if path_style.lower() != 'unix':  # If not explicitly unix, use windows
            formatted_path = os.path.join('..', path).replace('/', '\\')
        else:
            formatted_path = os.path.join('.', path).replace('\\', '/')
        return formatted_path

    def get_files_in_directory(self, directory):
        """
        Collect all eligible files in 'directory' unless
        'use_file_specific' is True, in which case only use 'specific_files'.
        """
        if self.settings['file_specific']['use_file_specific']:
            return [
                os.path.normpath(os.path.join(directory, file))
                for file in self.settings['file_specific']['specific_files']
            ]

        file_paths = []
        ignored_extensions = set(self.settings['files']['ignored_extensions'])
        ignored_files = set(self.settings['files']['ignored_files'])

        for root, dirs, files in os.walk(directory):
            if not self._is_running:
                if self.update_status:
                    self.update_status("Markdown extraction stopped by user.")
                break

            # Skip directories if needed
            if self.should_skip_directory(os.path.relpath(root, directory)):
                dirs[:] = []
                continue

            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in self.settings['directories']['ignored_directories']]

            for file in files:
                if not self._is_running:
                    if self.update_status:
                        self.update_status("Markdown extraction stopped by user.")
                    break

                if file in ignored_files:
                    continue
                if os.path.splitext(file)[1].lower() in ignored_extensions:
                    continue
                file_paths.append(os.path.normpath(os.path.join(root, file)))

        return file_paths

    @staticmethod
    def is_binary_file(file_path):
        """Heuristic check if a file is binary by looking for NULL bytes."""
        try:
            file_path = os.path.normpath(file_path)
            with open(file_path, 'rb') as file:
                data = file.read(1024)
            if not data:
                return False
            if b'\0' in data:
                return True
            return False
        except Exception as e:
            print(f"Error checking if file is binary: {str(e)}")
            return True

    def create_table_of_contents(self, file_paths):
        """Generate a simple Table of Contents with links referencing local anchors."""
        toc = "# Table of Contents\n"
        for file_path in file_paths:
            if not self._is_running:
                if self.update_status:
                    self.update_status("Markdown extraction stopped by user.")
                break
            relative_path = os.path.relpath(file_path, self.extract_dir)
            # Make anchor-friendly
            anchor = relative_path.replace(' ', '-').replace('.', '').replace('\\', '-').replace('/', '-')
            toc += f"- [{relative_path}](#{anchor})\n"
        return toc

    def create_where_file_lines(self, file_lines_info):
        """
        Create a helper section documenting start/end lines for each file block,
        plus an example snippet for re-extracting code blocks from the final Markdown.
        
        The generated snippet now uses a placeholder '{generated_file_name}' which
        should be replaced (or formatted) at runtime with the actual generated file name.
        """
        content = (
            "## Where each File line for each ## File: ..\\filename: \n\n"
            "## To extract code blocks from this markdown file, use the following Python script:\n\n"
            "```python\n"
            "def extract_code_blocks(file_path, instructions):\n"
            "    with open(file_path, 'r') as file:\n"
            "        lines = file.readlines()\n"
            "    for instruction in instructions:\n"
            "        file_name = instruction['file']\n"
            "        start_line = instruction['start_line'] - 1\n"
            "        end_line = instruction['end_line']\n"
            "        code = ''.join(lines[start_line:end_line])\n"
            "        print(f\"## Extracted Code from {file_name}\")\n"
            "        print(code)\n"
            "        print(\"#\" * 80)\n\n"
            "# Example instructions\n"
            "instructions = [\n"
            "    {'file': '../example.py', 'start_line': 1, 'end_line': 10},\n"
            "]\n\n"
            "file_path = '{generated_file_name}'\n"
            "extract_code_blocks(file_path, instructions)\n"
            "```\n\n"
        )
        for file_path, (start_line, end_line) in file_lines_info.items():
            if not self._is_running:
                if self.update_status:
                    self.update_status("Markdown extraction stopped by user.")
                break
            content += f"## File: {file_path}\n"
            content += f"Line = {start_line}, Starts = {start_line + 2}, Ends = {end_line + 1}\n\n"
        return content

    def create_markdown_for_files(self, file_paths: List[str]) -> Tuple[str, str]:
        """
        Enhanced markdown creation supporting multiple format styles.
        """
        toc = self.create_table_of_contents(file_paths) + "\n\n"
        markdown_content = "# Project Details\n\n" + toc
        file_lines_info = {}
        line_counter = markdown_content.count('\n') + 1
        
        total_files = len(file_paths)
        for idx, file_path in enumerate(file_paths, 1):
            if not self._is_running:
                if self.update_status:
                    self.update_status("Markdown extraction stopped by user.")
                break
                
            try:
                file_path = os.path.normpath(file_path)
                relative_path = os.path.relpath(file_path, self.extract_dir)
                formatted_path = self.format_path(relative_path)
                
                # Determine comment style based on file type
                comment_prefix = self._get_comment_prefix(file_path)
                
                if self.is_binary_file(file_path):
                    markdown_content += (
                        f"# File: {formatted_path}\n\n"
                        f"**Binary file cannot be displayed.**\n\n"
                        "---\n\n"
                    )
                    line_counter += 5
                else:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    file_extension = os.path.splitext(file_path)[1].lower().lstrip('.')
                    
                    # Create section with multiple reference formats
                    section_content = (
                        f"# {formatted_path}\n"
                        f"## File: {formatted_path}\n\n"
                        f"```{file_extension}\n"
                        f"{comment_prefix} {formatted_path}\n"
                        f"{content}\n"
                        "```\n\n"
                        "---\n\n"
                    )
                    
                    start_line = line_counter
                    line_counter += section_content.count('\n')
                    end_line = line_counter - 1
                    
                    file_lines_info[formatted_path] = (start_line, end_line)
                    markdown_content += section_content
                    
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
                if self.update_status:
                    self.update_status(f"Error processing file: {os.path.basename(file_path)}")
                continue
                
            if self.update_progress:
                self.update_progress(int(idx * 100 / total_files))
                
        where_file_lines = self.create_where_file_lines(file_lines_info)
        return markdown_content, where_file_lines

    def _get_comment_prefix(self, file_path: str) -> str:
        """
        Get appropriate comment prefix based on file type.
        """
        comment_styles = {
            '.py': '#',
            '.rb': '#',
            '.sh': '#',
            '.yml': '#',
            '.yaml': '#',
            '.js': '//',
            '.jsx': '//',
            '.ts': '//',
            '.tsx': '//',
            '.java': '//',
            '.cpp': '//',
            '.c': '//',
            '.cs': '//',
            '.php': '//',
            '.go': '//',
            '.swift': '//',
            '.kt': '//',
            '.rs': '//',
            '.dart': '//',
            '.lua': '--',
            '.sql': '--',
            '.hs': '--',
            '.elm': '--',
            '.vim': '"',
            '.r': '#',
            '.ps1': '#',
            '.matlab': '%',
            '.octave': '%',
        }
        
        ext = os.path.splitext(file_path)[1].lower()
        return comment_styles.get(ext, '#')

    def save_markdown(self, markdown_content, where_file_lines, output_dir, preset_name=None):
        """
        Save the generated markdown content and companion file.
        If preset_name is provided, use it (with slashes replaced by underscores)
        as the prefix. Otherwise, fall back to the settings prefix.
        """
        if preset_name:
            prefix = preset_name.replace('/', '_').replace('\\', '_')
        else:
            prefix = self.settings['output']['markdown_file_prefix']
        
        existing_files = [
            f for f in os.listdir(output_dir)
            if f.startswith(prefix) and f.endswith('.md')
        ]
        # Only match files with two-digit index suffix
        existing_files = [f for f in existing_files if re.match(rf'{re.escape(prefix)}_\d{{2}}\.md', f)]
        
        if not existing_files:
            main_output_path = os.path.join(output_dir, f'{prefix}_00.md')
            where_file_lines_path = os.path.join(output_dir, f'{prefix}_00_where_each_file_line_is.md')
        else:
            existing_files.sort()
            last_file = existing_files[-1]
            last_index = int(last_file.split('_')[-1].split('.')[0])
            next_index = last_index + 1
            main_output_path = os.path.join(output_dir, f'{prefix}_{next_index:02d}.md')
            where_file_lines_path = os.path.join(output_dir, f'{prefix}_{next_index:02d}_where_each_file_line_is.md')
        
        with open(main_output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        with open(where_file_lines_path, 'w', encoding='utf-8') as f:
            f.write(where_file_lines)
            
        return main_output_path, where_file_lines_path

    def run(self):
        """Main entry point for running the Markdown extraction."""
        if not os.path.exists(self.settings_path):
            raise FileNotFoundError(f"Settings file not found: {self.settings_path}")

        output_dir = self.settings['paths']['output_dir']
        presets = self.settings.get('presets', {})
        
        # Filter out the 'current_preset' key from presets
        preset_names = [name for name in presets.keys() if name != 'current_preset']
        total_presets = len(preset_names)

        if total_presets == 0:
            if self.update_status:
                self.update_status("No presets found in settings")
            return

        for idx, preset_name in enumerate(preset_names, 1):
            if not self._is_running:
                if self.update_status:
                    self.update_status("Markdown extraction stopped by user.")
                break

            if self.update_status:
                self.update_status(f"Processing preset {idx}/{total_presets}: {preset_name}")

            try:
                preset_output_dir = os.path.normpath(os.path.join(output_dir, preset_name)).replace('\\', '/')
                os.makedirs(preset_output_dir, exist_ok=True)

                specific_files = presets[preset_name]
                # Skip if preset_name is 'current_preset' or specific_files is not a list
                if preset_name == 'current_preset' or not isinstance(specific_files, list):
                    print(f"Skipping preset '{preset_name}': Not a valid preset or file list")
                    continue
                    
                file_paths = [
                    os.path.normpath(os.path.join(self.base_dir, file)).replace('\\', '/')
                    for file in specific_files
                ]

                if not file_paths:
                    if self.update_status:
                        self.update_status(f"No files found for preset: {preset_name}")
                    continue

                markdown_content, where_file_lines = self.create_markdown_for_files(file_paths)
                # Pass preset_name to use its derived prefix
                main_output_path, where_file_lines_path = self.save_markdown(
                    markdown_content,
                    where_file_lines,
                    preset_output_dir,
                    preset_name
                )

                if self.update_status:
                    self.update_status(f"Created files:\n{main_output_path}\n{where_file_lines_path}")

                if self.update_progress:
                    self.update_progress(int(idx * 100 / total_presets))

            except Exception as e:
                error_message = f"Error processing preset {preset_name}: {str(e)}"
                print(error_message)
                if self.update_status:
                    self.update_status(error_message)
                continue

        if self.update_status and self._is_running:
            self.update_status("Markdown extraction complete for all presets")



class CSVEx:
    def __init__(self, base_dir, output_dir, settings_path):
        self.base_dir = os.path.normpath(base_dir).replace('\\', '/')
        self.output_dir = os.path.normpath(output_dir).replace('\\', '/')
        self.extracted_dir = os.path.normpath(os.path.join(base_dir, 'extracted')).replace('\\', '/')
        self.settings_path = os.path.normpath(settings_path).replace('\\', '/')
        self.settings = self.load_settings()
        self.update_progress = None  # For GUI progress
        self.update_status = None    # For GUI status messages
        self._is_running = True
        os.makedirs(self.output_dir, exist_ok=True)

    def stop(self):
        """Stop the extraction process gracefully."""
        self._is_running = False

    def load_settings(self):
        """Load TOML settings for CSV extraction."""
        try:
            settings = toml.load(self.settings_path)
            self.normalize_paths(settings)
            return settings
        except toml.TomlDecodeError as e:
            print(f"Error loading settings: {e}")
            raise

    def normalize_paths(self, settings_dict):
        """Normalize all string paths in the loaded CSV settings."""
        for section in settings_dict:
            for key, value in settings_dict[section].items():
                if isinstance(value, str) and ('/' in value or '\\' in value):
                    settings_dict[section][key] = os.path.normpath(value).replace('\\', '/')
                elif isinstance(value, list):
                    settings_dict[section][key] = [
                        os.path.normpath(item).replace('\\', '/') 
                        if isinstance(item, str) and ('/' in item or '\\' in item) else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    self.normalize_paths(value)

    def save_settings(self):
        """If your app needs to write updated settings, implement here."""
        with open(self.settings_path, 'w') as settings_file:
            toml.dump(self.settings, settings_file)

    @staticmethod
    def extract_zip(zip_path, extract_to):
        """
        Simple static method to extract a ZIP file.
        If you need progress or cancellation checks, do them here.
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    @staticmethod
    def count_file_metrics(file_path):
        """Count basic metrics: total chars, total words, total lines."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                char_count = len(content)
                word_count = len(content.split())
                line_count = content.count("\n") + 1
            return char_count, word_count, line_count
        except Exception as e:
            print(f"Error counting metrics for {file_path}: {str(e)}")
            return 0, 0, 0

    @staticmethod
    def count_classes_functions_variables(file_path):
        """
        Count naive occurrences of 'class', 'def', and simple 'variable = ' patterns.
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                class_count = len(re.findall(r'\bclass\b', content))
                function_count = len(re.findall(r'\bdef\b', content))
                variable_count = len(re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\s*=\s*', content))
            return class_count, function_count, variable_count
        except Exception as e:
            print(f"Error counting code elements for {file_path}: {str(e)}")
            return 0, 0, 0

    def should_skip_directory(self, dir_path):
        """Check if a directory should be skipped based on settings."""
        skip_paths = self.settings['paths'].get('skip_paths', [])
        for skip_path in skip_paths:
            if dir_path.startswith(skip_path) or os.path.basename(dir_path) in self.settings['directories']['ignored_directories']:
                return True
        return False

    def generate_directory_tree_with_detailed_metrics(self):
        """Traverse files and build a list of [Path, Metrics, Code] for each."""
        if self.update_status:
            self.update_status("Gathering file list...")

        if self.settings['file_specific']['use_file_specific']:
            # If only using specific files
            file_paths = [
                os.path.join(self.base_dir, file)
                for file in self.settings['file_specific']['specific_files']
            ]
        else:
            file_paths = []
            ignored_extensions = set(self.settings['files']['ignored_extensions'])
            ignored_files = set(self.settings['files']['ignored_files'])

            for root_dir, dirs, files in os.walk(self.base_dir):
                if not self._is_running:
                    if self.update_status:
                        self.update_status("CSV extraction stopped by user.")
                    break

                if self.should_skip_directory(os.path.relpath(root_dir, self.base_dir)):
                    dirs[:] = []
                    continue

                dirs[:] = [d for d in dirs if d not in self.settings['directories']['ignored_directories']]

                for file in files:
                    if not self._is_running:
                        if self.update_status:
                            self.update_status("CSV extraction stopped by user.")
                        break

                    if file in ignored_files:
                        continue

                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext in ignored_extensions:
                        continue

                    file_path = os.path.join(root_dir, file)
                    file_paths.append(file_path)

        if not file_paths:
            if self.update_status:
                self.update_status("No files found to process")
            return []

        directory_tree = []
        total_files = len(file_paths)

        for idx, file_path in enumerate(file_paths, 1):
            if not self._is_running:
                if self.update_status:
                    self.update_status("CSV extraction stopped by user.")
                break

            if self.update_status:
                self.update_status(f"Processing file {idx}/{total_files}: {os.path.basename(file_path)}")

            try:
                relative_path = os.path.relpath(file_path, self.base_dir)
                size_kb = os.path.getsize(file_path) / 1024

                char_count, word_count, line_count = self.count_file_metrics(file_path)
                class_count, function_count, variable_count = self.count_classes_functions_variables(file_path)

                metrics = (
                    f"{size_kb:.2f}{self.settings['metrics']['size_unit']},"
                    f"C{char_count},W{word_count},L{line_count},"
                    f"CL{class_count},F{function_count},V{variable_count}"
                )

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                directory_tree.append([relative_path, metrics, content])

            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
                if self.update_status:
                    self.update_status(f"Error processing file: {os.path.basename(file_path)}")
                continue

            if self.update_progress:
                self.update_progress(int(idx * 100 / total_files))

        return directory_tree

    def get_next_output_file_path(self, preset_output_dir, preset_name=None):
        """
        Find an Excel filename that follows the pattern and use the preset-derived prefix
        if preset_name is provided.
        """
        if preset_name:
            prefix = preset_name.replace('/', '_').replace('\\', '_')
        else:
            prefix = self.settings['output']['csv_file_prefix']

        existing_files = [
            f for f in os.listdir(preset_output_dir)
            if f.startswith(prefix) and f.endswith('.xlsx')
        ]

        if not existing_files:
            return os.path.join(preset_output_dir, f'{prefix}_00.xlsx')

        existing_files.sort()
        last_file = existing_files[-1]
        last_index = int(last_file.split('_')[-1].split('.')[0])
        next_index = last_index + 1
        next_file_name = f'{prefix}_{next_index:02d}.xlsx'
        return os.path.join(preset_output_dir, next_file_name)

    @staticmethod
    def clear_extracted_directory(extracted_dir):
        """Utility to clear out the extracted directory if needed."""
        if not os.path.exists(extracted_dir):
            return
        try:
            for root_dir, dirs, files in os.walk(extracted_dir):
                for file in files:
                    os.remove(os.path.join(root_dir, file))
                for d in dirs:
                    shutil.rmtree(os.path.join(root_dir, d))
        except Exception as e:
            print(f"Error clearing extracted directory: {str(e)}")

    def save_to_excel(self, data, file_path):
        """
        Convert the data list [[Path, Metrics, Code], ...] to a DataFrame
        and save it to an .xlsx file with auto-adjusted column widths.
        """
        if not data:
            if self.update_status:
                self.update_status("No data to save to Excel")
            return

        try:
            if self.update_status:
                self.update_status("Creating Excel workbook...")

            df = pd.DataFrame(data, columns=["Path", "Metrics", "Code"])
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')

            if self.update_status:
                self.update_status("Adjusting column widths...")

            worksheet = writer.sheets['Sheet1']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).map(len).max(), len(col))
                worksheet.set_column(idx, idx, max_length)

            writer.close()

            if self.update_status:
                self.update_status(f"Excel file saved successfully: {os.path.basename(file_path)}")

        except Exception as e:
            print(f"Error saving Excel file: {str(e)}")
            if self.update_status:
                self.update_status(f"Error saving Excel file: {str(e)}")
            raise

    def run(self):
        """Main entry point for CSV extraction, saving results to Excel."""
        if not os.path.exists(self.settings_path):
            raise FileNotFoundError(f"Settings file not found: {self.settings_path}")

        try:
            if self.update_status:
                self.update_status("Starting extraction process...")

            presets = self.settings.get('presets', {})
            # Filter out the 'current_preset' key from presets
            preset_names = [name for name in presets.keys() if name != 'current_preset']
            total_presets = len(preset_names)

            if total_presets == 0:
                if self.update_status:
                    self.update_status("No presets found in settings")
                return

            for idx, preset_name in enumerate(preset_names, 1):
                if not self._is_running:
                    if self.update_status:
                        self.update_status("CSV extraction stopped by user.")
                    break

                if self.update_status:
                    self.update_status(f"Processing preset {idx}/{total_presets}: {preset_name}")

                try:
                    preset_output_dir = os.path.normpath(os.path.join(self.output_dir, preset_name))
                    os.makedirs(preset_output_dir, exist_ok=True)

                    specific_files = presets[preset_name]
                    # Skip if preset_name is 'current_preset' or specific_files is not a list
                    if preset_name == 'current_preset' or not isinstance(specific_files, list):
                        print(f"Skipping preset '{preset_name}': Not a valid preset or file list")
                        continue

                    file_paths = [
                        os.path.normpath(os.path.join(self.base_dir, file))
                        for file in specific_files
                    ]

                    if not file_paths:
                        if self.update_status:
                            self.update_status(f"No files found for preset: {preset_name}")
                        continue

                    if self.update_status:
                        self.update_status(f"Generating directory tree for preset: {preset_name}")

                    directory_tree_with_detailed_metrics = self.generate_directory_tree_with_detailed_metrics()

                    if self.update_status:
                        self.update_status(f"Saving to Excel file for preset: {preset_name}")

                    # Pass preset_name so that the filename uses the preset-derived prefix
                    output_file_path = self.get_next_output_file_path(preset_output_dir, preset_name)
                    self.save_to_excel(directory_tree_with_detailed_metrics, output_file_path)

                    if self.update_status:
                        self.update_status(
                            f"Extraction complete for preset: {preset_name}. File saved: {output_file_path}"
                        )

                except Exception as e:
                    error_message = f"Error processing preset {preset_name}: {str(e)}"
                    print(error_message)
                    if self.update_status:
                        self.update_status(error_message)
                    continue

            if self.update_status and self._is_running:
                self.update_status("CSV extraction complete for all presets")

        except Exception as e:
            error_message = f"Error during CSV extraction: {str(e)}"
            print(error_message)
            if self.update_status:
                self.update_status(error_message)
            raise


@dataclass
class CodeBlock:
    path: str
    language: str
    content: str
    style: str
    update_class: Optional[str] = None

class ReverseMarkdownEx:
    def __init__(self, markdown_path: str, output_dir: str, settings_path: Optional[str] = None):
        """Initialize the markdown extractor with enhanced update capabilities."""
        self.markdown_path = markdown_path
        self.output_dir = os.path.normpath(output_dir).replace('\\', '/')
        self.settings_path = os.path.normpath(settings_path).replace('\\', '/') if settings_path else None
        self.settings = self.load_settings() if settings_path else {'paths': {'path_style': 'windows'}}
        self.update_progress = None  # For GUI progress
        self.update_status = None    # For GUI status messages
        self._is_running = True
        
        # Initialize regex patterns for class handling
        self.class_pattern = re.compile(
            r'class\s+(?P<class_name>\w+)[\s\(].*?(?=\n\s*(?:class|$))', 
            re.DOTALL
        )

    def stop(self):
        """Stop the reverse extraction process gracefully."""
        self._is_running = False

    def load_settings(self) -> Dict[str, Any]:
        """Load TOML settings and normalize paths."""
        try:
            if self.settings_path:
                settings = toml.load(self.settings_path)
                # Ensure we have the required structure
                if not isinstance(settings, dict):
                    settings = {'paths': {'path_style': 'windows'}}
                elif 'paths' not in settings:
                    settings['paths'] = {'path_style': 'windows'}
                elif 'path_style' not in settings['paths']:
                    settings['paths']['path_style'] = 'windows'
                
                self.normalize_paths(settings)
                return settings
            return {'paths': {'path_style': 'windows'}}
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {'paths': {'path_style': 'windows'}}

    def normalize_paths(self, settings_dict: Dict[str, Any]) -> None:
        """Recursively normalize all paths in the loaded settings."""
        for section in settings_dict:
            for key, value in settings_dict[section].items():
                if isinstance(value, str) and ('/' in value or '\\' in value):
                    settings_dict[section][key] = os.path.normpath(value).replace('\\', '/')
                elif isinstance(value, list):
                    settings_dict[section][key] = [
                        os.path.normpath(item).replace('\\', '/') 
                        if isinstance(item, str) and ('/' in item or '\\' in item) else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    self.normalize_paths(value)

    def format_path(self, relative_path: str) -> str:
        """Format the path based on the selected path style."""
        path = relative_path.replace('\\', '/')
        if self.settings['paths']['path_style'] == 'windows':
            formatted_path = os.path.join('..', path).replace('/', '\\')
        else:
            formatted_path = os.path.join('.', path).replace('\\', '/')
        return formatted_path

    def extract_code_blocks(self, content: str) -> List[CodeBlock]:
        """
        Enhanced extraction of code blocks supporting multiple formats.
        Handles various path locations and formats.
        """
        code_blocks = []
        
        # Define all pattern sets
        header_patterns = [
            (r'^#\s*(?:title\s*=\s*)(.*?\.[\w]+)$', False),
            (r'^#+\s*(?:File|Path|Location|Source|Module Path|Container Path):\s*(.*?\.[\w]+)$', False),
            (r'^#\s*\[(.*?\.[\w]+)\]$', False),
            (r'^#\s*(.*?\.[\w]+)$', False),
        ]
        
        code_comment_patterns = [
            (r'^(?://|#)\s*(.*?\.[\w]+)$', False),
            (r'^(?://|#)\s*\[(.*?\.[\w]+)\]$', False),
            (r'^(?://|#)\s*(?:File|Path|Location|Source):\s*(.*?\.[\w]+)$', False),
        ]
        
        section_patterns = [
            r'^\s*---\s*$',
            r'^\s*\*\*\*\s*$',
            r'^\s*___\s*$',
            r'^#+\s*.*$'
        ]
        
        # Split content into sections using any delimiter
        sections = self._split_into_sections(content, section_patterns)
        
        for section in sections:
            try:
                # Extract path from section header or content
                file_path = None
                code_content = None
                language = None
                
                # Try header patterns first
                for pattern, is_update in header_patterns:
                    matches = re.finditer(pattern, section, re.MULTILINE)
                    for match in matches:
                        file_path = match.group(1)
                        break
                    if file_path:
                        break
                
                # Look for code blocks
                code_block_pattern = r'```(\w+)\n(.*?)```'
                code_matches = list(re.finditer(code_block_pattern, section, re.DOTALL))
                
                if code_matches:
                    for code_match in code_matches:
                        language = code_match.group(1)
                        code_content = code_match.group(2).strip()
                        
                        # If no path found in header, try code comments
                        if not file_path:
                            code_lines = code_content.split('\n')
                            if code_lines:
                                for pattern, is_update in code_comment_patterns:
                                    comment_match = re.match(pattern, code_lines[0])
                                    if comment_match:
                                        file_path = comment_match.group(1)
                                        # Remove the comment line if path was found there
                                        code_content = '\n'.join(code_lines[1:]).strip()
                                        break
                
                if file_path and code_content:
                    normalized_path = self._normalize_path(file_path)
                    code_blocks.append(CodeBlock(
                        path=normalized_path,
                        language=language or self._detect_language(normalized_path),
                        content=code_content,
                        style='windows' if '\\' in file_path else 'unix'
                    ))
                    
            except Exception as e:
                print(f"Error processing section: {str(e)}")
                continue
                
        return code_blocks

    def _split_into_sections(self, content: str, section_patterns: List[str]) -> List[str]:
        """
        Split content into sections based on various delimiter patterns.
        """
        # Combine all patterns into one
        combined_pattern = '|'.join(f'({pattern})' for pattern in section_patterns)
        
        # Split content
        sections = []
        current_section = []
        
        for line in content.split('\n'):
            if any(re.match(pattern, line) for pattern in section_patterns):
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
            current_section.append(line)
            
        if current_section:
            sections.append('\n'.join(current_section))
            
        return sections if sections else [content]

    def _detect_language(self, file_path: str) -> str:
        """
        Detect programming language from file extension.
        """
        ext_to_language = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.html': 'html',
            '.css': 'css',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.m': 'objective-c',
            '.sh': 'bash',
            '.ps1': 'powershell',
            '.sql': 'sql',
            '.r': 'r',
            '.dart': 'dart',
            '.vue': 'vue',
            '.elm': 'elm',
            '.ex': 'elixir',
            '.erl': 'erlang',
            '.fs': 'fsharp',
            '.hs': 'haskell',
            '.jl': 'julia',
            '.lua': 'lua',
            '.ml': 'ocaml',
            '.pl': 'perl',
            '.rkt': 'racket',
        }
        
        ext = os.path.splitext(file_path)[1].lower()
        return ext_to_language.get(ext, 'text')

    def _normalize_path(self, path: str) -> str:
        """
        Normalize file paths to a consistent format.
        Handles various path formats and styles.
        """
        # Remove brackets, parentheses, etc.
        path = re.sub(r'[\[\]()]', '', path)
        
        # Remove common prefixes
        path = re.sub(r'^(?:file://|path:|source:|location:)\s*', '', path, flags=re.IGNORECASE)
        
        # Normalize separators
        path = path.replace('\\', '/').strip()
        
        # Handle relative paths
        if not path.startswith(('.', '/', '\\')):
            path = './' + path
            
        return path

    def update_class_in_file(self, file_path: str, class_name: str, new_content: str) -> bool:
        """Update a specific class in a file while preserving all other content."""
        try:
            # Read existing file content
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return False

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the target class using improved pattern
            class_pattern = re.compile(
                f'class\\s+{re.escape(class_name)}\\s*(?:\\([^)]*\\))?\\s*:\\s*[^#]*?(?=\\s*class\\s+|$)',
                re.DOTALL | re.MULTILINE
            )

            match = class_pattern.search(content)
            if not match:
                print(f"Class {class_name} not found in {file_path}")
                return False

            # Get the full match and its position
            start = match.start()
            end = match.end()

            # Print debug info
            print(f"Found class {class_name} at position {start}-{end}")
            print("Original content around match:")
            context_before = content[max(0, start-50):start]
            context_after = content[end:min(len(content), end+50)]
            print(f"Before: {context_before}")
            print(f"After: {context_after}")

            # Construct updated content
            updated = content[:start] + new_content + content[end:]

            # Write the updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated)

            print(f"Successfully updated class {class_name} in {file_path}")
            return True

        except Exception as e:
            print(f"Error updating class {class_name} in {file_path}: {str(e)}")
            return False

    def run(self) -> None:
        """Process the markdown content and create/update files."""
        try:
            print("1. Starting ReverseMarkdownEx.run()")

            if not os.path.exists(self.markdown_path):
                print(f"Error: Markdown file not found at {self.markdown_path}")
                raise FileNotFoundError(f"Markdown file not found: {self.markdown_path}")

            print("2. Loading Markdown file...")
            if self.update_status:
                self.update_status("Loading Markdown file...")

            with open(self.markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"3. Read {len(content)} bytes from file")

            # Extract all code blocks
            print("4. Extracting code blocks...")
            code_blocks = self.extract_code_blocks(content)
            print(f"5. Found {len(code_blocks)} code blocks")
            total_blocks = len(code_blocks)

            if total_blocks == 0:
                print("6. No code blocks found")
                if self.update_status:
                    self.update_status("No valid code blocks found to extract.")
                return

            processed_count = 0
            for idx, block in enumerate(code_blocks, 1):
                if not self._is_running:
                    print("Process stopped by user")
                    if self.update_status:
                        self.update_status("Extraction stopped by user.")
                    return

                try:
                    print(f"7. Processing block {idx}/{total_blocks}: {block.path}")
                    file_path = block.path
                    relative_path = file_path.replace('\\', '/').replace('../', '').replace('./', '')
                    full_path = os.path.join(self.output_dir, relative_path).replace('\\', '/')
                    
                    # Create directory
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    print(f"8. Created directory: {os.path.dirname(full_path)}")

                    if block.update_class:
                        # Handle class update
                        if os.path.exists(full_path):
                            success = self.update_class_in_file(full_path, block.update_class, block.content)
                            if success:
                                processed_count += 1
                    else:
                        # Handle full file creation/update
                        print(f"9. Writing to file: {full_path}")
                        with open(full_path, 'w', encoding='utf-8') as out_file:
                            cleaned_content = block.content.strip()
                            out_file.write(cleaned_content)
                            processed_count += 1
                            print(f"10. Successfully wrote file {processed_count}")

                    if self.update_progress:
                        progress = int(idx * 100 / total_blocks)
                        print(f"11. Progress: {progress}%")
                        self.update_progress(progress)

                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
                    continue

            print(f"12. Extraction complete. Processed {processed_count} files")
            if self.update_status and self._is_running:
                if processed_count > 0:
                    self.update_status(f"Successfully processed {processed_count} files in: {self.output_dir}")
                else:
                    self.update_status("No files were processed.")

        except Exception as e:
            print(f"Fatal error during extraction: {str(e)}")
            if self.update_status:
                self.update_status(f"Error during extraction: {str(e)}")
            raise


def reverse_markdown_extraction(markdown_path: str, output_dir: str, settings_path: Optional[str] = None) -> None:
    """Convenience function for reversing markdown -> files."""
    extractor = ReverseMarkdownEx(markdown_path, output_dir, settings_path)
    extractor.run()

class ReverseCSVEx:
    def __init__(self, file_path, output_dir):
        self.file_path = file_path
        self.output_dir = os.path.normpath(output_dir).replace('\\', '/')
        self.update_progress = None  # For GUI progress
        self.update_status = None    # For GUI status messages
        self._is_running = True

    def stop(self):
        """Stop the reverse extraction process gracefully."""
        self._is_running = False

    def run(self):
        """Reverse the CSV extraction process by recreating files from an Excel sheet."""
        try:
            if self.update_status:
                self.update_status("Loading Excel file...")

            df = pd.read_excel(self.file_path)
            total_files = len(df)

            if total_files == 0:
                if self.update_status:
                    self.update_status("No records found in the Excel file.")
                return

            for idx, row in df.iterrows():
                if not self._is_running:
                    if self.update_status:
                        self.update_status("Reverse CSV extraction stopped by user.")
                    break

                try:
                    out_path = os.path.join(self.output_dir, row['Path'])
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)

                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(row['Code'])

                    if self.update_progress:
                        self.update_progress(int((idx + 1) * 100 / total_files))

                except Exception as e:
                    print(f"Error processing file {row['Path']}: {str(e)}")
                    if self.update_status:
                        self.update_status(f"Error processing {row['Path']}: {str(e)}")
                    continue

            if self.update_status and self._is_running:
                self.update_status(f"Files have been recreated in: {self.output_dir}")

        except Exception as e:
            print(f"Error during reverse CSV extraction: {str(e)}")
            if self.update_status:
                self.update_status(f"Error during reverse CSV extraction: {str(e)}")
            raise


def reverse_csv_extraction(file_path, output_dir):
    """Convenience function for reversing Excel -> files."""
    extractor = ReverseCSVEx(file_path, output_dir)
    extractor.run()




# Generic worker class for extractions
class ExtractorWorker(QObject):
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)
    status = Signal(str)

    def __init__(self, extractor):
        super().__init__()
        self.extractor = extractor
        self._is_running = True

        # Connect extractor's updates to worker signals
        if hasattr(self.extractor, "update_progress"):
            self.extractor.update_progress = self.progress.emit
        if hasattr(self.extractor, "update_status"):
            self.extractor.update_status = self.status.emit

    @Slot()
    def run(self):
        try:
            if self._is_running:
                self.extractor.run()
                self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        """Stop the extraction process."""
        self._is_running = False
        if hasattr(self.extractor, "stop"):
            self.extractor.stop()

# Re-export publicly so the GUI or other code can import from here
__all__ = [
    "MarkdownEx",
    "CSVEx",
    "ReverseMarkdownEx",
    "reverse_markdown_extraction",
    "ReverseCSVEx",
    "reverse_csv_extraction",
    "ExtractorWorker",  # Add ExtractorWorker to exports
]

```

---

# ..\..\gui\__init__.py
## File: ..\..\gui\__init__.py

```py
# ..\..\gui\__init__.py

```

---

# ..\..\gui\main_window.py
## File: ..\..\gui\main_window.py

```py
# ..\..\gui\main_window.py
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
```

---

