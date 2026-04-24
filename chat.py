import json
import os
from groq import Groq
from tools.calculate import calculate, calculate_schema
from tools.ls import ls, ls_schema
from tools.cat import cat, cat_schema
from tools.grep import grep, grep_schema
from tools.doctest import doctest, doctest_schema
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

        >>> response = chat.send_message('hello, my name is Bob', temperature=0.0)
        >>> 'Bob' in response
        True
        >>> response = chat.send_message("123+456")
        >>> '579' in response
        True
        >>> response = chat.send_message("does this question use tools?")
        >>> 'no tools' in response.lower()
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

        for i in range(10):
            while tool_calls:
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

    >>> def monkey_input(prompt, user_inputs=['/grep */cat.py True', '/unknown']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> import builtins
    >>> builtins.input = monkey_input
    >>> repl(temperature=0.0)
    chat> /grep */cat.py True
    Returns True if the path is safe (no absolute paths or traversal).
        True
            return True
    <BLANKLINE>
    Hello!
    chat> /unknown
    Error: unknown command unknown
    <BLANKLINE>
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
                    pattern = args[0]
                    search_term = args[1]
                    files = glob.glob(pattern)
                    if not files:
                        print('')
                        continue
                    for f in files:
                        output = grep(f, search_term)
                        if output:
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
