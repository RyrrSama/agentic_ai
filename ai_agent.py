import os

import chat_model
import constants as CONSTANTS
from system_prompts import agent_prototyping, function_caller

response = None
MAX_INTERATION = 20
ITERATION = 0

# # DEBUGGER IMPORT
# import litellm

# litellm._turn_on_debug()
# # DEBUGGER IMPORT


def agent_loop(system_propmt):
    """ """
    INTERATION = 0
    model = chat_model.ChatModel(system_propmt)
    # Wait for model to responsed
    model.completion()
    while INTERATION < CONSTANTS.MAX_INTERATION:
        #    Get user input between each intraction
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        elif not user_input:
            model.completion()

        model.completion(user_input)
        INTERATION += 1


if __name__ == "__main__":
    # agent_loop(
    #     agent_prototyping.AGENT_CONTENT,
    # )

    agent_loop(function_caller.AGENT_RULE)
