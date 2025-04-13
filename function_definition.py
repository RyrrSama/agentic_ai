import os


def read_txt_file(file_name):
    """
    Reads the content of a text file and returns it as a string.

    Args:
        file_name (str): The path to the text file to be read.

    Returns:
        str: The content of the file if successfully read.
             If the file is not found, returns an error message indicating the file was not found.
             If another exception occurs, returns a generic error message with the exception details.

    Raises:
        FileNotFoundError: If the specified file does not exist (handled internally).
        Exception: For any other errors that occur during file reading (handled internally).
    """
    try:
        with open(file_name, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file '{file_name}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"


def list_files_in_directory(directory, file_type=None):
    """
    Lists all files in the given directory and returns their full file paths in numbered points.
    Optionally filters files by the specified file type.

    Args:
        directory (str): The path to the directory.
        file_type (str, optional): The file extension to filter by (e.g., '.txt'). Defaults to None.

    Returns:
        str: A numbered list of full file paths of all files in the directory matching the file type.
             If the directory is not found, returns an error message.
             If another exception occurs, returns a generic error message with the exception details.
    """
    try:
        if not os.path.isdir(directory):
            return f"Error: The directory '{directory}' does not exist."

        files = os.listdir(directory)
        file_paths = [
            os.path.join(directory, file)
            for file in files
            if os.path.isfile(os.path.join(directory, file))
            and (file_type is None or file.endswith(file_type))
        ]

        if not file_paths:
            return (
                f"No files found in the directory '{directory}' matching the file type '{file_type}'."
                if file_type
                else f"No files found in the directory '{directory}'."
            )

        return "\n".join(
            [f"{i + 1}. {file_path}" for i, file_path in enumerate(file_paths)]
        )
    except Exception as e:
        return f"An error occurred: {e}"


def terminate(message):
    print(message)
