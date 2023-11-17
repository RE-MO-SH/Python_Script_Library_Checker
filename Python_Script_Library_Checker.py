import tkinter as tk
from tkinter import filedialog, scrolledtext
import ast

def check_libraries():
    file_path = file_path_var.get()
    if not file_path:
        append_result("Please select a Python script file.")
        return

    try:
        with open(file_path, "r") as file:
            tree = ast.parse(file.read())
    except Exception as e:
        append_result(f"Error reading the script: {str(e)}")
        return

    required_libraries = set()
    optional_libraries = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                lib_name = alias.name.split('.')[0]
                required_libraries.add(lib_name)
        elif isinstance(node, ast.ImportFrom):
            lib_name = node.module.split('.')[0]
            required_libraries.add(lib_name)

    script_name = file_path.split("/")[-1]  # Extracting script name from the path

    if required_libraries:
        append_result(f"Required Libraries for {script_name}:")
        for lib in required_libraries:
            append_result(f"- {lib}")
        for lib in optional_libraries:
            append_result(f"- {lib}")
    else:
        append_result(f"No external libraries are required for {script_name}.")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    file_path_var.set(file_path)

def append_result(text):
    result_text.config(state=tk.NORMAL)
    result_text.insert(tk.END, f"{text}\n")
    result_text.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Python Script Library Checker")

# File path variable
file_path_var = tk.StringVar()

# Labels and Text
label = tk.Label(root, text="Select a Python script file:")
label.pack(pady=10)

file_path_entry = tk.Entry(root, textvariable=file_path_var, state=tk.DISABLED, width=40)
file_path_entry.pack(pady=5)

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
result_text.pack(pady=10)
result_text.config(state=tk.DISABLED)

# Buttons
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

check_button = tk.Button(root, text="Check Libraries", command=check_libraries)
check_button.pack(pady=10)

# Run the GUI
root.mainloop()
