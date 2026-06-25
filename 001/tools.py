def multiply(a: int, b: int) -> int:
    return a * b


multiply_tool = {
    "type": "function",
    "function": {
        "name": "multiply",
        "description": "计算两个整数的乘积",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "第一个乘数"},
                "b": {"type": "integer", "description": "第二个乘数"},
            },
            "required": ["a", "b"],
        },
    }
}

tools_map = {"multiply": multiply}
