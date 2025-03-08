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



