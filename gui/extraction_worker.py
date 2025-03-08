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