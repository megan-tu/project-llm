import os
import glob
from git import Repo
from tools.util import is_path_safe


def rm(path):
    '''
    Deletes files matching a path or glob and commits it.
    >>> print(rm('test_examples/example1.py'))
    Removed 1 file(s)
    >>> print(rm('test_examples/*.txt'))
    Removed 2 file(s)

    Does not support absolute paths or directory traversal
    >>> rm('../bad.py')
    'Error: unsafe path'
    >>> rm('no_such_file_*.txt')
    ''
    >>> rm('test_examples/')
    ''
    rm('test_examples/*.does_not_exist')
    ''
    '''
    try:
        if not is_path_safe(path):
            return "Error: unsafe path"
        files = glob.glob(path)
        if not files:
            return ''
        removed_files = []
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
                removed_files.append(f)
        if not removed_files:
            return ''
        repo = Repo('.')
        repo.index.remove(removed_files)
        repo.index.commit(f'[docchat] rm {path}')
        return f"Removed {len(removed_files)} file(s)"
    except Exception as e:
        return str(e)


rm_schema = {
    "type": "function",
    "function": {
        "name": "rm",
        "description": "removes files and commits the action",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path that's removed",
                }
            },
            "required": ["path"],
        },
    },
}
