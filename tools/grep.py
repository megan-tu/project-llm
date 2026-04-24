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
    >>> print(grep('test_examples/*.py', 'x'))
    x = 0
    x = 2
    x = 123
    <BLANKLINE>
    >>> grep('*/bad_file.py', '[x]')
    'FileNotFoundError'
    >>> grep('test_examples/*.png', 'x')
    'UnicodeDecodeError'
    '''
    if not is_path_safe(path):
        return "Error: unsafe path"
    files = sorted(glob.glob(path))
    if not files:
        return 'FileNotFoundError'  
    result = ''
    for file in files:
        try:
            with open(file) as f:
                for line in f:
                    if re.search(regex, line):
                        result += line
        except UnicodeDecodeError:
            return "UnicodeDecodeError"
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
            "required": ["path", "regex"]
        }
    }
}
