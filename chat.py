import os
import sys

# Ensure project root is always importable (CLI-safe)
sys.path.insert(0, os.path.dirname(__file__))
import json
from groq import Groq
from tools.calculate import calculate, calculate_schema
from tools.ls import ls, ls_schema
from tools.cat import cat, cat_schema
from tools.grep import grep, grep_schema

from dotenv import load_dotenv
load_dotenv()


# in python, class names are CamelCase
# non-class names (functions/variables) are in snake_case


class Chat:
    '''
    The Chat class sends messages to an LLM and talks like a pirate.
    It also support tool calling, including ls, cat, grep, and calculate.

    >>> chat = Chat()
    >>> isinstance(chat, Chat)
    True

    >>> chat = Chat()
    >>> calculate('238942 * 109347134')
    '{"result": 26127622892228}'
    >>> calculate('1/0')
    '{"error": "Invalid expression"}'

    >>> from unittest.mock import patch, mock_open
    >>> with patch("builtins.open", mock_open()) as m:
    ...     m.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1,
    ...     "bad byte")
    ...     cat(".coverage")
    'UnicodeDecodeError'

    >>> cat('tool.py')
    'FileNotFoundError'
    >>> cat('..')
    'Error: unsafe path'
    >>> cat('tools/util.py')
    'import os\\n\\n\\ndef is_path_safe(path):\\n    \\'\\'\\'\\n    Returns True if the path is safe (no absolute paths or traversal).\\n    >>> is_path_safe(\\'tools/ls.py\\')\\n    True\\n    >>> is_path_safe(\\'/etc/passwd\\')\\n    False\\n    >>> is_path_safe(\\'../secrets.py\\')\\n    False\\n    >>> is_path_safe(\\'src/../config.json\\')\\n    False\\n    \\'\\'\\'\\n    if os.path.isabs(path):\\n        return False\\n\\n    if ".." in path:\\n        return False\\n\\n    else:\\n        return True\\n'
    >>> ls('')
    'README.md __pycache__ chat.py pyproject.toml requirements.txt test_projects tools'
    >>> ls('tools')
    'tools/__pycache__ tools/calculate.py tools/cat.py tools/grep.py tools/ls.py tools/util.py'
    >>> ls('..')
    'Error: unsafe path'
    >>> ls('/Users/megantu/CSCI040/docsum')
    'Error: unsafe path'

    >>> grep('*/ls.py', '[z]')
    ''
    >>> grep('..None', '[z]')
    'Error: unsafe path'
    '''

    def __init__(self):
        '''
        Initializes the chat with default system prompt
        and tool definitions.
        '''
        self.client = Groq()
        self.MODEL = 'openai/gpt-oss-120b'
        self.messages = [
            {
                "role": "system",
                "content": "Talk like pirate. Do not change wording. Use tools to complete tasks when appropriate and return the output exactly. Otherwise respond directly and clearly.",
            },
        ]

    def send_message(self, message, temperature=0.0):
        '''
        Sends a message to the LLM and returns the assistant's response.
        >>> import json
        >>> chat = Chat()

        >>> class FakeMessage:
        ...     def __init__(self):
        ...         self.tool_calls = None
        ...         self.content = "Arrr, yer name be Bob, matey!"

        >>> class FakeResponse:
        ...     def __init__(self):
        ...         self.choices = [type("Choice", (), {"message": FakeMessage()})()]

        >>> chat.client.chat.completions.create = lambda *args, **kwargs: FakeResponse()

        >>> chat.send_message("Hello my name is Bob. What's my name?", temperature=0.0)
        'Arrr, yer name be Bob, matey!'

        >>> import json
        >>> chat = Chat()

        >>> class FakeToolCall:
        ...     def __init__(self):
        ...         self.function = type("Func", (), {
        ...             "name": "calculate",
        ...             "arguments": json.dumps({"expression": "123+456"})
        ...         })()
        ...         self.id = "1"

        >>> class FakeMessage:
        ...     def __init__(self):
        ...         self.tool_calls = [FakeToolCall()]
        ...         self.content = None

        >>> class FakeResponse1:
        ...     def __init__(self):
        ...         self.choices = [type("Choice", (), {"message": FakeMessage()})()]

        >>> class FakeMessage2:
        ...     def __init__(self):
        ...         self.tool_calls = None
        ...         self.content = "579"

        >>> class FakeResponse2:
        ...     def __init__(self):
        ...         self.choices = [type("Choice", (), {"message": FakeMessage2()})()]

        >>> calls = [FakeResponse1, FakeResponse2]

        >>> def fake_create(*args, **kwargs):
        ...     return calls.pop(0)()

        >>> chat.client.chat.completions.create = fake_create

        >>> chat.send_message("123+456")
        '579'

        >>> chat = Chat()

        >>> class FakeMessage:
        ...     def __init__(self):
        ...         self.tool_calls = None
        ...         self.content = "Arr, no tools needed!"

        >>> class FakeResponse:
        ...     def __init__(self):
        ...         self.choices = [type("Choice", (),
        ...         {"message": FakeMessage()})()]

        >>> def fake_create(*args, **kwargs):
        ...     return FakeResponse()
        >>>
        >>> chat.client.chat.completions.create = fake_create

        >>> result = chat.send_message("hello")
        >>> "no tools" in result.lower()
        True
        '''
        self.messages.append(
            {
                # system: never changes; user: changes a lot;
                'role': 'user',
                'content': message
            }
        )

        tools = [calculate_schema, ls_schema, cat_schema, grep_schema]

        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.MODEL,
            temperature=temperature,
            seed=0,
            tools=tools,
            tool_choice="auto",
        )
        response_message = chat_completion.choices[0].message
        tool_calls = response_message.tool_calls

        while tool_calls:
            self.messages.append(response_message)

            available_functions = {
                "calculate": calculate,
                "ls": ls,
                "cat": cat,
                "grep": grep,
            }

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_to_call = available_functions[function_name]

                function_response = function_to_call(**function_args)

                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
            chat_completion = self.client.chat.completions.create(
                model=self.MODEL,
                messages=self.messages,
                tools=tools,
                tool_choice="auto",
            )

            response_message = chat_completion.choices[0].message
            tool_calls = response_message.tool_calls

        result = (response_message.content or '').strip()

        self.messages.append({
            'role': 'assistant',
            'content': result,
        })
        
        return result


def repl(temperature=0.0):
    '''
    Runs an interactive REPL supporting slash commands and LLM chat.
    Slash commands (/ls, /cat, /grep) can be executed directly
    without calling the LLM.

    >>> from unittest.mock import patch
    >>> def monkey_input(prompt, user_inputs=['Hi','/ls .github', '/cat tool.py', '/grep */calculate.py x.*n', '/unknown']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> with patch('builtins.input', monkey_input), patch('chat.Chat') as MockChat:
    ...     MockChat.return_value.send_message.return_value = 'Hello!'
    ...     repl()
    chat> Hi
    Hello!
    chat> /ls .github
    .github/workflows
    chat> /cat tool.py
    FileNotFoundError
    chat> /grep */calculate.py x.*n
    def calculate(expression):
        Evaluate a mathematical expression
        '{"error": "Invalid expression"}'
        '{"error": "Invalid expression"}'
            result = eval(expression)  # Use safe evaluation in production
        except Exception:
            return json.dumps({"error": "Invalid expression"})
            "description": "Evaluate a mathematical expression",
                    "expression": {
                        "description": "The mathematical expression to evaluate",
                "required": ["expression"],
    <BLANKLINE>
    chat> /unknown
    Error: unknown command unknown
    <BLANKLINE>
    '''
    chat = Chat()
    try:
        while True:
            user_input = input('chat> ')
            if user_input.startswith('/'):
                parts = user_input[1:].split()
                command = parts[0]
                args = parts[1:]

                if command == 'ls':
                    result = ls(*args)
                    print(result)
                    chat.messages.append({
                        "role": "system",
                        "content": f'ls output: {result}'
                    })
                    continue

                elif command == 'cat':
                    output = cat(*args)
                    print(output)
                    continue

                elif command == 'grep':
                    output = grep(*args)
                    print(output)
                    continue

                else:
                    print(f'Error: unknown command {command}')
                    continue

            response = chat.send_message(user_input, temperature=temperature)
            if response.strip():
                print(response)
            else:
                print("Arrr... no answer from the sea today, matey.")
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()
