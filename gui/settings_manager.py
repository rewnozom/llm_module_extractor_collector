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

