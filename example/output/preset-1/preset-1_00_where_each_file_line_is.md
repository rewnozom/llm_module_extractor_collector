## Where each File line for each ## File: ..\filename: 

## To extract code blocks from this markdown file, use the following Python script:

```python
def extract_code_blocks(file_path, instructions):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for instruction in instructions:
        file_name = instruction['file']
        start_line = instruction['start_line'] - 1
        end_line = instruction['end_line']
        code = ''.join(lines[start_line:end_line])
        print(f"## Extracted Code from {file_name}")
        print(code)
        print("#" * 80)

# Example instructions
instructions = [
    {'file': '../example.py', 'start_line': 1, 'end_line': 10},
]

file_path = '{generated_file_name}'
extract_code_blocks(file_path, instructions)
```

## File: ..\..\gui\settings_frame.py
Line = 18, Starts = 20, Ends = 237

## File: ..\..\main.py
Line = 237, Starts = 239, Ends = 278

## File: ..\..\gui\extraction_frame.py
Line = 278, Starts = 280, Ends = 1192

## File: ..\..\gui\file_specific_frame.py
Line = 1192, Starts = 1194, Ends = 1706

## File: ..\..\gui\theme_manager.py
Line = 1706, Starts = 1708, Ends = 1974

## File: ..\..\gui\settings_manager.py
Line = 1974, Starts = 1976, Ends = 2189

## File: ..\..\gui\constants.py
Line = 2189, Starts = 2191, Ends = 2336

## File: ..\..\gui\extraction_worker.py
Line = 2336, Starts = 2338, Ends = 2475

## File: ..\..\gui\header_frame.py
Line = 2475, Starts = 2477, Ends = 2599

## File: ..\..\gui\extractorz.py
Line = 2599, Starts = 2601, Ends = 3874

## File: ..\..\gui\__init__.py
Line = 3874, Starts = 3876, Ends = 3884

## File: ..\..\gui\main_window.py
Line = 3884, Starts = 3886, Ends = 4188

