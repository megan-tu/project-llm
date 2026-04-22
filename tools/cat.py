from tools.util import is_path_safe

def cat(file):
    """
    Opens a file and outputs its contents as a string.
    >>> from unittest.mock import patch, mock_open
    >>> with patch("builtins.open", mock_open()) as m:
    ...     m.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "invalid start byte")
    ...     cat("fake.txt")
    'UnicodeDecodeError'
    >>> cat('tool.py')
    'FileNotFoundError'
    >>> cat('..')
    'Error: unsafe path'
    >>> print(cat('tools/util.py'))
    import os


    def is_path_safe(path):
        '''
        Returns True if the path is safe (no absolute paths or traversal).
        >>> is_path_safe('tools/ls.py')
        True
        >>> is_path_safe('/etc/passwd')
        False
        >>> is_path_safe('../secrets.py')
        False
        >>> is_path_safe('src/../config.json')
        False
        '''
        if os.path.isabs(path):
            return False

        if ".." in path:
            return False

        else:
            return True
    """

    if not is_path_safe(file):
        return "Error: unsafe path"
    if file:
        try:
            with open(file) as f:
                return f.read()
        except UnicodeDecodeError:
            return 'UnicodeDecodeError'
        except FileNotFoundError:
            return 'FileNotFoundError'


cat_schema = {
    "type": "function",
    "function": {
        "name": "cat",
        "description": "Open a file and return its contents",
        "parameters": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The path of the file to read"
                }
            },
            "required": ["file"]
        }
    }
}
