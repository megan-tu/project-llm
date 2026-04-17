from tools.util import is_path_safe
import glob


def ls(folder=None):
    '''
    Lists files in the current directory.

    >>> ls('')
    'README.md __pycache__ build chat.py
    cmc_csci040_MeganTu.egg-info dist htmlcov markdown-project
    megan-tu.github.io pyproject.toml requirements.txt
    test_projects tools venv'

    >>> ls('tools')
    'tools/__pycache__ tools/calculate.py
    tools/cat.py tools/grep.py tools/ls.py tools/util.py'
    >>> ls('..')
    'Error: unsafe path'
    >>> ls('/Users/megantu/CSCI040/docsum')
    'Error: unsafe path'
    '''
    if not is_path_safe(folder):
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
