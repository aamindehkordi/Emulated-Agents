import os
import astor
import ast

class CodeExtractor(ast.NodeVisitor):
    def __init__(self, include_strings=False):
        self.relevant_code = ""
        self.include_strings = include_strings

    def visit_ClassDef(self, node):
        self.process_node(node)

    def visit_FunctionDef(self, node):
        self.process_node(node)

    def visit_AsyncFunctionDef(self, node):
        self.process_node(node)

    def process_node(self, node):
        for child_node in ast.iter_child_nodes(node):
            if not isinstance(child_node, ast.Str) or self.include_strings:
                self.relevant_code += astor.to_source(child_node) + "\n"
            else:
                self.relevant_code += "\n"

class FileSearcher:
    def __init__(self, exclude=None, min_lines=25):
        if exclude is None:
            exclude = []
        self.exclude = exclude
        self.min_lines = min_lines

    def should_exclude(self, path):
        for pattern in self.exclude:
            if path.startswith('./'):
                path = path[2:]
            if path.startswith(pattern.replace('*', '')):
                return True
        return False

    def search(self, root='.'):
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if not self.should_exclude(path):
                    yield path

    def find_py_files(self, directory):
        py_files = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        lines = content.strip().split('\n')
                        if len(lines) >= self.min_lines:
                            py_files[file_path] = file_path
        return py_files

    def read_file_content(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def extract_relevant_code(self, file_content):
        tree = ast.parse(file_content)
        extractor = CodeExtractor()
        extractor.visit(tree)
        return extractor.relevant_code
