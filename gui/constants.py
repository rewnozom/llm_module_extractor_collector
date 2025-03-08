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
