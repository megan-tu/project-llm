from tools.util import is_path_safe


def cat(file):
    '''
    Opens a file and outputs its contents as a string.
    >>> cat('/Users/megantu/CSCI040/docsum/Trump_tweets_graph.png')
    'UnicodeDecodeError'
    >>> cat('tool.py')
    'FileNotFoundError'
    >>> cat('..')
    'Error: unsafe path'
    '''

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
