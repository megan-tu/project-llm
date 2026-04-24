import json
import os
from groq import Groq
from tools.calculate import calculate, calculate_schema
from tools.ls import ls, ls_schema
from tools.cat import cat, cat_schema
from tools.grep import grep, grep_schema
from tools.run_doctest import doctest, doctest_schema
from tools.write_files import write_files, write_files_schema
from tools.write_file import write_file, write_file_schema
from tools.rm import rm, rm_schema
import glob
from dotenv import load_dotenv
load_dotenv()


class Chat:
    '''
    The Chat class sends messages to an LLM and talks like a pirate.
    It also support tool calling, including ls, cat, grep, and calculate.
    '''

    def __init__(self):
        '''
        Initializes the chat with default system prompt
        and tool definitions.
        '''
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
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
                'role': 'user',
                'content': message
            }
        )

        tools = [calculate_schema, ls_schema, cat_schema, grep_schema, doctest_schema, write_files_schema, write_file_schema, rm_schema]

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
        if not tool_calls:
            result = (response_message.content or '').strip()
            self.messages.append({
                'role': 'assistant',
                'content': result,
            })
            return result

        if tool_calls:
            self.messages.append(response_message)

            available_functions = {
                "calculate": calculate,
                "ls": ls,
                "cat": cat,
                "grep": grep,
                "doctest": doctest,
                "write_files": write_files,
                "write_file": write_file,
                "rm": rm,
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


def repl(temperature=0.0, max_iterations=2):
    '''
    Runs an interactive REPL supporting slash commands and LLM chat.
    Slash commands (/ls, /cat, /grep) can be executed directly
    without calling the LLM.


    >>> def monkey_input(prompt, user_inputs=['/ls .github', '/cat tool.py']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> import builtins
    >>> builtins.input = monkey_input
    >>> repl(temperature=0.0)
    chat> /ls .github
    .github/workflows
    chat> /cat tool.py
    FileNotFoundError

    >>> def monkey_input(prompt, user_inputs=['/grep test_examples/*.py x', '/unknown']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> import builtins
    >>> builtins.input = monkey_input
    >>> repl(temperature=0.0)
    chat> /grep test_examples/*.py x
    x = 0
    x = 2
    x = 123
    <BLANKLINE>
    chat> /unknown
    Error: unknown command unknown
    '''
    chat = Chat()

    if not os.path.isdir('.git'):
        print("Error: .git folder not found")
        return
    if os.path.isfile("AGENTS.md"):
        content = cat("AGENTS.md")
        chat.messages.append({
            "role": "system",
            "content": content
        })

    try:
        count = 0
        while True:
            if count >= max_iterations:
                break
            count += 1
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
                    path = args[0]
                    regex = " ".join(args[1:])
                    result = grep(path, regex)
                    print(result)
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
