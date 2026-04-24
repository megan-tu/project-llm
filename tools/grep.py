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
    x = 123
    x = 2
    <BLANKLINE>
    '''
    if not is_path_safe(path):
        return "Error: unsafe path"
    result = ''

    files = sorted(glob.glob(path))

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
            "required": ["path", "regex"]
        }
    }
}
