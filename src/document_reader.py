import json
import markdownfrom typing import Any
from smolagents import tool
from typing import Any
from smolagents import tool

class DocumentReader:
    """A class for reading documents from a specified directory."""

    def __init__(self, directory: str):
        """
        Initializes the DocumentReader with a directory path.

        :param self: The instance of the DocumentReader class.
        :param directory: The directory path containing the documents to read.
        :type directory: str
        """
        self.directory = directory

    def get_tools(self) -> list[Any]:
        """
        Returns a list of tools that the agent can use to read documents.

        :return: A list of tool functions that the agent can use to read documents.
        :rtype: list[Any]
        """

        @tool
        def get_act(act_name: str) -> str:
            """Gets a string representation of a specific act from the plot document.

            :param act_name: The name of the act to retrieve.
            :type act_name: str
            :return: The string representation of the specified act.
            :rtype: str
            """

            with open(f"{self.directory}/plot.json", "r", encoding="utf-8") as f:
                plot_data = json.load(f)
                act = plot_data["acts"].get(act_name.lower())
                if act is None:
                    raise ValueError(f"Act '{act_name}' not found in the plot document.")
                
                output = ""
                for name, description in act.items():
                    output += f"{name.capitalize()}:\n{description}\n\n"
                return output.strip()
            
        @tool
        def get_character_summary(character_name: str) -> str:
            """Gets a string summary of a specific character from the character documents.

            :param character_name: The name of the character to retrieve.
            :type character_name: str
            :return: The string summary of the specified character.
            :rtype: str
            """

            with open(f"{self.directory}/{character_name.lower()}.json", "r", encoding="utf-8") as f:
                character_data = json.load(f)
                attributes = character_data.get("attributes")
                if attributes is None:
                    raise ValueError(f"Character '{character_name}' not found in the character documents.")
            output = f"{character_name.capitalize()}:\n"
            for key, value in attributes.items():
                output += f"  {key.capitalize()}: {value}\n"
            return output.strip()

        return [get_act, get_character_summary]