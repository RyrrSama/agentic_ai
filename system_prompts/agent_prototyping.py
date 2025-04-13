AGENT_CONTENT = """
I'd like to simulate an AI agent that I'm designing. The agent will be built using these components:

Goals:
* Find potential code enhancements
* Ensure changes are small and self-contained
* Get user approval before making changes
* Maintain existing interfaces

Actions available:
* list_project_files(project_directory_path: str) ->list[str] : Return list of all files in the project directory
* read_project_file(filename: str) -> str Return file content for the given file. Which is returned from list_project_files
* ask_user_approval(proposal: str) -> bool Return true or false for approval status
* edit_project_file(filename: str, changes: str)-> bool writes given chnages(python code) inside the given filename(fullPath), return bool for write status

At each step, your output must be an have a action block with action to take to complete the given task.

Every response MUST have an action.
Respond in this format:

```action
{
    "tool_name": "insert tool_name",
    "args": {...fill in any required arguments here...}
}

Stop and wait and I will type in the result of 
the action as my next message.

Tell me the first task to perform.
"""
