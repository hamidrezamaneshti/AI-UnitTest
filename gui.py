import tkinter as tk
from UnitTestGenerator import UnitTestGenerator


unit_test_generator = UnitTestGenerator()
root = tk.Tk()
root.title("Python Test Case Generator")

# Create buttons for browsing, regenerating, and saving test cases
browse_button = tk.Button(root, text="Browse", command=lambda: unit_test_generator.browse_function_file(code_text))
browse_button.pack()

code_label = tk.Label(root, text="Function Code:")
code_label.pack()

code_text = tk.Text(root, wrap=tk.WORD, height=10)
code_text.pack()

generate_button = tk.Button(root, text="Generate", command=lambda: unit_test_generator.regenerate_test_cases(code_text, test_cases_text))
generate_button.pack()

test_cases_label = tk.Label(root, text="Generated Test Cases:")
test_cases_label.pack()

test_cases_text = tk.Text(root, wrap=tk.WORD, height=10)
test_cases_text.pack()

save_button = tk.Button(root, text="Save", command=lambda: unit_test_generator.save_test_cases(test_cases_text))
save_button.pack()

root.mainloop()
