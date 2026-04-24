import subprocess
import sys
from tools.util import is_path_safe


def doctest(path):
    """
    This function runs doctest with the --verbose flag and returns the output.
    >>> print(doctest('tools/calculate.py'))
    Trying:
        calculate('238942 * 109347134')
    Expecting:
        '{"result": 26127622892228}'
    ok
    Trying:
        calculate('1/0')
    Expecting:
        '{"error": "Invalid expression"}'
    ok
    Trying:
        calculate('abc')
    Expecting:
        '{"error": "Invalid expression"}'
    ok
    1 items had no tests:
        calculate
    1 items passed all tests:
       3 tests in calculate.calculate
    3 tests in 2 items.
    3 passed and 0 failed.
    Test passed.

    Does not support absolute paths or directory traversal
    >>> doctest('..')
    'Error: unsafe path'
    >>> doctest('/etc/passwd')
    'Error: unsafe path'
    >>> doctest(None)
    "expected str, bytes or os.PathLike object"
    """
    if not is_path_safe(path):
        return "Error: unsafe path"
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'doctest', '-v', path],
            capture_output=True,
            text=True
        )
        return (result.stdout + result.stderr).strip()
    except Exception as e:
        return str(e)


doctest_schema = {
    "type": "function",
    "function": {
        "name": "doctest",
        "description": "Runs doctest and returns the verbose output",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the file"
                }
            },
            "required": ["path"]
        }
    }
}
