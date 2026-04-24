from git import Repo
from tools.run_doctest import doctest as run_doctest
from tools.util import is_path_safe


def write_files(files, commit_message):
    '''
    This function writes multiple files and commits them.

    >>> print(write_files([{"path": "test_examples/example1.py", "contents": "x = 0"},{"path": "test_examples/example2.py", "contents": "x = 2"}], "examples"))
    1 items had no tests:
        example1
    0 tests in 1 items.
    0 passed and 0 failed.
    Test passed.
    <BLANKLINE>
    1 items had no tests:
        example2
    0 tests in 1 items.
    0 passed and 0 failed.
    Test passed.
    >>> print(write_files([{"path": "test_examples/test1.txt", "contents": "x = 3"}], "txt files"))
    Wrote 1 files and committed.
    >>> write_files([], "test")
    'Wrote 0 files and committed.'

    Does not support absolute paths or directory traversal
    >>> write_files([{"path": "../bad.py", "contents": "x = 1"}], "msg")
    'Error: unsafe path'
    '''

    try:
        for file in files:
            if not is_path_safe(file['path']):
                return "Error: unsafe path"
        repo = Repo('.')
        written_paths = []
        doctest_outputs = []
        for file in files:
            path = file['path']
            contents = file['contents']
            with open(path, 'w', encoding='utf-8') as f:
                if not contents.endswith('\n'):
                    contents += '\n'
                f.write(contents)
            written_paths.append(path)
            if path.endswith('.py'):
                doctest_outputs.append(run_doctest(path))
        repo.index.add(written_paths)
        repo.index.commit(f"[docchat] {commit_message}")
        if doctest_outputs:
            return "\n\n".join(doctest_outputs)
        return f"Wrote {len(written_paths)} files and committed."
    except Exception as e:
        return str(e)


write_files_schema = {
    "type": "function",
    "function": {
        "name": "write_files",
        "description": "writes multiple files and commits them",
        "parameters": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "contents": {"type": "string"}
                        },
                        "required": ["path", "contents"]
                    }
                },
                "commit_message": {
                    "type": "string"
                }
            },
            "required": ["files", "commit_message"]
        }
    }
}
