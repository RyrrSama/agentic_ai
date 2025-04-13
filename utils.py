import inspect

import function_definition


def get_required_params(func):
    """
    Retrieves all required parameters for a given function.

    Args:
        func (function): The function object to inspect.

    Returns:
        list: A list of required parameter names.
    """
    required_params = []
    signature = inspect.signature(func)

    for param_name, param in signature.parameters.items():
        # Check if the parameter has no default value and is not *args/**kwargs
        if param.default == inspect.Parameter.empty and param.kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.KEYWORD_ONLY,
        ):
            required_params.append(param_name)

    return required_params


def get_tools_definition():
    """ """
    tools_mapper = {}
    tool = []
    current_module = inspect.getmembers(function_definition, inspect.isfunction)
    for name, func in current_module:
        tools_mapper[name] = func
        docstring = inspect.getdoc(func) or "No description available."
        signature = inspect.signature(func)

        tool_dict = {
            "type": "function",
            "function": {
                "name": name,
                "description": docstring,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": get_required_params(func),
                },
            },
        }

        properties = {}
        for param_name, param in signature.parameters.items():
            parameter_type = (
                str(param.annotation)
                if param.annotation != inspect.Parameter.empty
                else "string"
            )
            properties[param_name] = {"type": parameter_type}

        tool_dict["function"]["parameters"]["properties"] = properties
        tool.append(tool_dict)

    return tools_mapper, tool
