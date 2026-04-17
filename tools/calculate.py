import json


def calculate(expression):
    '''
    Evaluate a mathematical expression

    >>> calculate('238942 * 109347134')
    '{"result": 26127622892228}'
    >>> calculate('1/0')
    '{"error": "Invalid expression"}'
    >>> calculate('abc')
    '{"error": "Invalid expression"}'
    '''
    try:
        result = eval(expression)  # Use safe evaluation in production
        return json.dumps({"result": result})
    except Exception:
        return json.dumps({"error": "Invalid expression"})


calculate_schema = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a mathematical expression",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate",
                }
            },
            "required": ["expression"],
        },
    },
}
