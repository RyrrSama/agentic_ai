import os

import function_definition

# Model CONSTANTS
MAX_INTERATION = 10
MAX_TOKENS = os.getenv("MAX_TOKEN", 1024)
TIMEOUT = os.getenv("TIMEOUT", 10000)
MODEL = os.getenv("MODEL")
APIKEY = os.getenv("APIKEY", "")
API_BASE_URL = os.getenv("API_BASE_URL", "")

# FUNCTION CALLING CONSTANTS
FUNCTION_MAPPER = {
    "read_text_file": function_definition.read_txt_file,
    "list_files_in_directory": function_definition.list_files_in_directory,
    "terminate": function_definition.terminate,
}
