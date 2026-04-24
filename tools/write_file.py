from tools.write_files import write_files


def write_file(path, contents, commit_message):
    '''
    Writes a single file and commits it using write_files.
    >>> print(write_file('test_examples/file1.py', 'x = 123', 'file1'))
    1 item had no tests:
        file1
    0 tests in 1 item.
    0 passed.
    Test passed.
    >>> print(write_file('test_examples/file2.txt', 'x = 456', 'file2'))
    Wrote 1 files and committed.

    Does not support absolute paths or directory traversal
    >>> write_file('..', 'x', 'msg')
    'Error: unsafe path'
    >>> write_file('../some_file.py', 'x', 'msg')
    'Error: unsafe path'
    '''

    return write_files(
        [{'path': path, 'contents': contents}],
        commit_message
    )


write_file_schema = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes a single file and commits it",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the file"
                },
                "contents": {
                    "type": "string",
                    "description": "content of the file"
                },
                "commit_message": {
                    "type": "string"
                }
            },
            "required": ["path", "contents", "commit_message"]
        }
    }
}
