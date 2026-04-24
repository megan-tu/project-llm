from tools.util import is_path_safe
import glob


def ls(folder=None):
    '''
    Lists files in the current directory.

    >>> ls('')
    'AGENTS.md README.md Trump_tweets_graph.png __pycache__ chat.py demo example_3 pyproject.toml requirements.txt test.txt test_examples test_projects tools'
    >>> ls('tools')
    'AGENTS.md README.md Trump_tweets_graph.png __pycache__ chat.py demo example_3 pyproject.toml requirements.txt test.txt test_examples test_projects tools'
    >>> ls('../secrets')
    'Error: unsafe path'
    >>> ls('/Users/megantu/CSCI040/docsum')
    'Error: unsafe path'
    >>> ls(None)
    ''
    '''
    if folder is None:
        folder = ''
    if folder and not is_path_safe(folder):
        return "Error: unsafe path"
    if folder:
        result = ''
        result = sorted(glob.glob(folder + '/*'))
        return ' '.join(result)
    else:
        result = ''
        result = sorted(glob.glob('*'))
        return ' '.join(result)


ls_schema = {
    "type": "function",
    "function": {
        "name": "ls",
        "description": "list files in directory",
        "parameters": {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "description": "The folder in which the files are listed",
                }
            },
            "required": ["folder"],
        },
    },
}
