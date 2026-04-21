import os
import glob
import re
from tools.util import is_path_safe


def grep(path, regex):
    '''
    Searches files for regex matches and returns matching lines.
    >>> grep('*/ls.py', '[z]')
    ''
    >>> grep('..None', '[z]')
    'Error: unsafe path'

    # still ugly
    >>> grep('*/calculate.py', 'x.*n')
    'def calculate(expression):\\n    Evaluate a mathematical expression\\n    \\'{"error": "Invalid expression"}\\'\\n    \\'{"error": "Invalid expression"}\\'\\n        result = eval(expression)  # Use safe evaluation in production\\n    except Exception:\\n        return json.dumps({"error": "Invalid expression"})\\n        "description": "Evaluate a mathematical expression",\\n                "expression": {\\n                    "description": "The mathematical expression to evaluate",\\n            "required": ["expression"],\\n'
    '''
    if not is_path_safe(path):
        return "Error: unsafe path"
    result = ''

    files = glob.glob(path)

    for file in files:
        if not os.path.isfile(file):
            continue

        try:
            with open(file) as f:
                for line in f:
                    if re.search(regex, line):
                        result += line
        except (FileNotFoundError, UnicodeDecodeError):
            continue
    return result


grep_schema = {
    "type": "function",
    "function": {
        "name": "grep",
        "description": "outputs lines that pattern match in a given file",
        "parameters": {
            "type": "object",
            "properties": {
                "regex": {
                    "type": "string",
                    "description": "The regular expression to search for."
                },
                "path": {
                    "type": "string",
                    "description": "The path of the file to read."
                }
            },
            "required": ["regex", "path"]
        }
    }
}
