import ast
import openai
import tkinter as tk
from tkinter import filedialog

class UnitTestGenerator:
    def __init__(self):
        self.api_key = "Your API's open-ai"
        openai.api_key = self.api_key

    def extract_features_from_function(self, code: str):
        """
        Extract features from the given code such as function name, arguments, and return type.

        :param code: str
        :return: list of dictionaries containing function features
        """
        parsed_code = ast.parse(code)
        features = []

        for node in ast.walk(parsed_code):
            if isinstance(node, ast.FunctionDef):
                features.append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "return_type": None if not hasattr(node.returns, "id") else node.returns.id
                })
        return features

    def generate_unit_test_cases(self, function_data):
        """
        Generate unit test cases for the given function data using OpenAI API.

        :param function_data: dict
        :return: str
        """
        prompt = "Generate all var unit test cases for the following Python function:\n\n"
        prompt += f"Function name: {function_data['name']}\n"
        prompt += "Arguments:\n"

        for arg in function_data['args']:
            prompt += f"- {arg}\n"

        prompt += f"Return type: {function_data['return_type']}\n\n"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=800,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return response.choices[0].text.strip()

    def write_test_cases_to_file(self, test_cases: str, file_name: str):
        """
        Write test cases to a file.

        :param test_cases: str
        :param file_name: str
        """
        with open(file_name, "w") as file:
            file.write(test_cases)

    def browse_function_file(self, code_text):
        """
        Browse for a function file and display its content in the provided text widget.

        :param code_text: tkinter Text widget
        """
        file_path = filedialog.askopenfilename()
        with open(file_path, "r") as file:
            code = file.read()
            code_text.delete(1.0, tk.END)
            code_text.insert(tk.END, code)

    def regenerate_test_cases(self, code_text, test_cases_text):
        """
        Regenerate test cases for the code in the provided text widget and display them in the test_cases_text widget.

        :param code_text: tkinter Text widget
        :param test_cases_text: tkinter Text widget
        """
        code = code_text.get(1.0, tk.END)
        function_data = self.extract_features_from_function(code)
        if function_data:
            test_cases = self.generate_unit_test_cases(function_data[0])
            test_cases_text.delete(1.0, tk.END)
            test_cases_text.insert(tk.END, test_cases)
        else:
            test_cases_text.delete(1.0, tk.END)
            test_cases_text.insert(tk.END, "No functions found in the code.")

    def save_test_cases(self, test_cases_text):
        """
        Save test cases from the provided text widget to a file.

        :param test_cases_text: tkinter Text widget
        """
        test_cases = test_cases_text.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        self.write_test_cases_to_file(test_cases, file_path)


