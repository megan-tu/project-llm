import json
from groq import Groq
from tools.calculate import calculate, calculate_schema
from tools.ls import ls, ls_schema
from tools.cat import cat, cat_schema
from tools.grep import grep, grep_schema
import glob

from dotenv import load_dotenv
load_dotenv()

# I understand that you included this comment because I had written it
# in class, but you should not have excess comments like this in
# "production code"; only include comments that help the reader
# understand what your code does

class Chat:
    '''
    The Chat class sends messages to an LLM and talks like a pirate.
    It also support tool calling, including ls, cat, grep, and calculate.

    >>> chat = Chat()

    # none of the test cases I deleted test anything about this class;
    # they were all tests for your tools, and should be included in
    # the appropriate tools folder
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

        # these test cases are more complicated than the actual code,
        # so they don't provide the reader much insight into the code.
        # they also do not actually test much about the LLM usage;
        # it is possible to write much better tests than this,
        # but I'm not deducting any points though

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

        # this is mildly dangerout in that it can run into an infinite loop
        # if you are on a paid API, this could drain your entire bank account
        # if you give it a bad prompt that makes the AI want to use tools
        # forever; it is customary to do something like:
        #   for i in range(10)
        # so that the loop is guaranteed to end at some point
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
    chat> /grep */calculate.py x.*n # this is a very weird test case; it does not help me as a reader figure out what your code is "supposed" to do
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
    Hello!
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
