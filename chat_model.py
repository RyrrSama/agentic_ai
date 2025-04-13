import json

from litellm import completion, supports_function_calling
from litellm.litellm_core_utils.streaming_handler import CustomStreamWrapper

import constants as CONSTANTS
import utils


class ChatModel:
    """
    ChatModel is a class that manages interactions with a language model (LLM).
    It handles chat memory, system prompts, user inputs, and assistant responses.
    The class supports streaming responses and provides utility functions for
    extracting and parsing content.

    Attributes:
        __memory (list): A list of dictionaries representing the conversation history.
        __tools (list): A list of tools or configurations for the chat model.
        __model (str): The name or identifier of the language model.
        __api_key (str): The API key for authenticating with the language model service.
        __max_count (int): The maximum number of tokens to generate in the response.
        __time_out (int): The timeout duration for the API request.
        __base_url (str): The base URL for the language model API.
    """

    def __init__(self, system_prompt=None, tools=[], memory=[]):
        """
        Initializes the ChatModel instance with optional system prompts, tools, and memory.

        Args:
            system_prompt (str, optional): A system-generated prompt or message to initialize the chat.
            tools (list, optional): A list of tools or configurations for the chat model. Defaults to an empty list.
            memory (list, optional): A list of dictionaries representing the initial conversation history. Defaults to an empty list.
        """
        self.__memory = memory
        self.__tools = tools
        self.__tool_mapper = {}
        self.__append_system_prompt(system_prompt)
        self.intitate_model()

    def support_function_calls(self):
        """ """
        return supports_function_calling(model=self.__model)

    def intitate_model(self):
        """
        Initializes the model configuration using constants defined in the CONSTANTS module.
        This includes the model name, API key, maximum token count, timeout, and base URL.
        """
        self.__model = CONSTANTS.MODEL
        self.__api_key = CONSTANTS.APIKEY
        self.__max_count = CONSTANTS.MAX_TOKENS
        self.__time_out = CONSTANTS.TIMEOUT
        self.__base_url = CONSTANTS.API_BASE_URL
        self.__tool_mapper, tools = utils.get_tools_definition()
        self.__tools.extend(tools)

    def __excute_action(self, response):
        """Executes the tool passed in and returns its result.

        Args:
        response (Message): The Message object containing information about the selected action.

        Returns:
        str: A string representation of the function's return value

        Raises:
        KeyError: If a valid function is not provided for the requested tool.
                  It also raises an Exception if the function call fails.

        """
        tool = response.choices[0].message.tool_calls[0]
        # Update assistant for function calls input
        self.__append_assistant_response(json.dumps(tool))
        tool_name = tool.function.name
        tool_args = json.loads(tool.function.arguments)
        function_object = CONSTANTS.FUNCTION_MAPPER.get(tool_name)
        if function_object:
            try:
                result = CONSTANTS.FUNCTION_MAPPER[tool_name](**tool_args)
                # Update function call result to memory
                self.__append_user_input(str(result))
                return result

            except Exception as e:
                self.__append_user_input(
                    f"ERROR: Failed to excute the tool '{tool_name}'. Please see exception mesg for more info.\n{e}"
                )
                # raise KeyError(
                #     f"ERROR: Failed to excute the tool '{tool_name}'. Please see exception mesg for more info.\n{e}"
                # )
        else:
            self.__append_user_input(
                f"ERROR: Provided Tool '{tool_name}' not defined. Please provided a vaild Tool to excute."
            )
        # raise KeyError(
        #     f"ERROR: Provided Tool '{tool_name}' not defined. Please provided a vaild Tool to excute."
        # )

    def __update_chat_memory(self, role, prompt):
        """
        Updates the chat memory by appending a new message.

        Args:
            role (str): The role of the message sender (e.g., "user", "system", "assistant").
            prompt (str): The content of the message.
        """
        self.__memory.append({"role": role, "content": prompt})

    def __append_system_prompt(self, system_prompt):
        """
        Appends a system prompt to the chat memory.

        Args:
            system_prompt (str): The system-generated prompt or message.
        """
        self.__update_chat_memory("system", system_prompt)

    def __append_user_input(self, user_input):
        """
        Appends a user input to the chat memory.

        Args:
            user_input (str): The user's input message.
        """
        self.__update_chat_memory("user", user_input)

    def __append_assistant_response(self, response):
        """
        Appends an assistant's response to the chat memory.

        Args:
            response (str): The assistant's response message.
        """
        self.__update_chat_memory("assistant", response)

    def extract_content(self, response, render=True):
        """
        Extracts and optionally renders the content from the response.

        Args:
            response (CustomStreamWrapper or dict): The response object from the chat model.
            render (bool, optional): Whether to print the content in real-time. Defaults to True.

        Returns:
            str: The full response content as a string.
        """
        full_response = ""
        if not isinstance(response, CustomStreamWrapper):
            return response.choices[0].message.content
        else:
            full_response = ""
            print("Agentic AI: ", end="")
            for chunk in response:
                content = chunk["choices"][0]["delta"]["content"]
                if render:
                    if content:
                        print(
                            content, end="", flush=True
                        )  # Print without newline and flush output
                full_response += content or ""
            if render:
                print()  # Add a newline after the response is fully generated
            return full_response

    @staticmethod
    def parse_segment(content, segment_name):
        """
        Extracts and parses a JSON segment block from a given response string.

        This function searches for a specific segment block in the response string
        that starts with a delimiter in the format "```<segment_name>" and ends with "```".
        It extracts the content within this block and attempts to parse it as JSON.

        Args:
            content (str): The response string containing the segment block.
            segment_name (str): The name of the segment block to extract, e.g., "action".

        Returns:
            dict: The parsed JSON object from the segment block, or None if the segment block is not found.

        Raises:
            ValueError: If the JSON parsing fails due to invalid JSON format.
        """
        if f"```{segment_name}" in content:
            content = content.split(f"```{segment_name}")[1]
            segment = content[: content.find("```")]
            try:
                return json.loads(segment)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Failed to parse segment '{segment_name}' from response content: {e}"
                )

        return None

    def completion(self, message=None, role="user", stream=True):
        """
        Generates a response from the chat model using the provided message history
        and optional tools, with support for streaming responses.

        Args:
            message (str, optional): The user's input message to be added to the conversation history.
            role (str, optional): The role of the message sender (e.g., "user"). Defaults to "user".
            stream (bool, optional): Whether to stream the response in chunks for real-time interaction. Defaults to True.

        Returns:
            str: The generated response content from the chat model.

        Raises:
            ValueError: If required configurations such as `MODEL`, `APIKEY`, `MAX_TOKENS`,
                `TIMEOUT`, or `API_BASE_URL` are missing or invalid in the `CONSTANTS` module.
        """
        if message:
            # Update message to memory
            self.__update_chat_memory(role=role, prompt=message)

        response = completion(
            model=self.__model,
            api_key=self.__api_key,
            max_tokens=self.__max_count,
            timeout=self.__time_out,
            base_url=self.__base_url,
            messages=self.__memory,
            tools=self.__tools,
            stream=stream,
        )
        # Check if model support function calling
        if self.support_function_calls():
            self.function_calling(response)

        # Extract context response
        content = self.extract_content(response, render=stream)
        try:
            segment = ChatModel.parse_segment(content, segment_name="action")
        except json.JSONDecodeError:
            error_msg = "ERROR: Your response doesn't have 'Action' block to excute. follow the given instruction."
            # Update chat memory with error
            self.__append_user_input(error_msg)
            return

        # # Update Assistant Content to memory
        # self.__append_assistant_response(segment)

        # Run tool
        # self.__excute_action(response)

        return content

    def function_calling(self, response):
        """"""
        response_message = response.choices[0].message
        # Update the conversation
        self.__append_assistant_response(response_message)
        tool_calls = response_message.tools_calling or []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function = self.__tool_mapper.get(function_name)
            if not function:
                raise KeyError(
                    f"Function {function_name} not defined. Please provide vailf function."
                )

            function_args = json.loads(tool_call.function.arguments)
            function(function_args)
