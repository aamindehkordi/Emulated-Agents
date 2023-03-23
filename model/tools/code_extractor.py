import astor, os, ast

class CodeExtractor(ast.NodeVisitor):
    def __init__(self):
        self.relevant_code = ""

    def visit_ClassDef(self, node):
        self.relevant_code += astor.to_source(node) + "\n"

    def visit_FunctionDef(self, node):
        self.relevant_code += astor.to_source(node) + "\n"

    def visit_AsyncFunctionDef(self, node):
        self.relevant_code += astor.to_source(node) + "\n"

def extract_relevant_code(file_content):
    tree = ast.parse(file_content)
    extractor = CodeExtractor()
    extractor.visit(tree)
    return extractor.relevant_code

def find_py_files(directory, min_lines=25):
    py_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    lines = content.strip().split('\n')
                    if len(lines) >= min_lines:
                        py_files[file_path] = file_path
    return py_files

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()
