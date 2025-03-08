# -*- coding: utf-8 -*-

import sys
sys.setrecursionlimit(5000)


import os
from cx_Freeze import setup, Executable

# Ange vilka moduler och filer som ska inkluderas
build_exe_options = {
    "packages": ["os", "PySide6", "toml", "pandas"],
    "excludes": ["pywintypes", "pythoncom", "pywintypes310", "PySide6.QtDesigner"],
    "include_files": [
        "extraction_frame.py",
        "extractorz.py",
        "file_specific_frame.py",
        "header_frame.py",
        "main_window.py",
        "settings_frame.py",
        "settings_manager.py",
        "theme_manager.py",
        "settings.toml"
    ],
    "include_msvcr": True
}

# För GUI-applikationer på Windows används "Win32GUI" som base
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Project Module-Extractor Manager",
    version="2.0.0",
    description="`Project Module-Extractor Manager` is a flexible tool designed to efficiently gather, manage, and organize modules and components for `working with Large Language Models (LLMs)`. It enables fast and optimized extraction of code-based components into `Markdown` or `CSV`, streamlining workflows and making it easier to manage modular structures using `presets`.",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
