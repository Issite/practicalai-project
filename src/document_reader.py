import os
import json
import chromadb
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
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name="story_documents")
        self._load_documents()

    def _load_documents(self):
        """Loads documents from the specified directory into the ChromaDB collection."""
        # Load plot document
        with open(f"{self.directory}/plot.json", "r", encoding="utf-8") as f:
            plot_data = json.loads(f.read())
            header = plot_data.get("name", "Plot Summary") + ":" + plot_data.get("description", "")
            acts = [f"{k}: {v}" for k, v in plot_data.get("acts", {}).items()]
            self.collection.add(
                documents=[header] + acts,
                ids=["plot_0"] + [f"act_{i}" for i in range(len(acts))],
                metadatas=[{"type": "plot", "subtype": "description"}] + [{"type": "plot", "subtype": "act"} for _ in acts]
            )
        
        # Load character documents
        for filename in os.listdir(self.directory):
            if filename.endswith(".json") and filename != "plot.json":
                character_name = filename[:-5]  # Remove .json extension
                with open(f"{self.directory}/{filename}", "r", encoding="utf-8") as f:
                    character_data = json.loads(f.read())
                    header = character_data.get("name", character_name.capitalize()) + ":" + character_data.get("description", "")
                    attributes = [f"{k}: {v}" for k, v in character_data.get("attributes", {}).items()]
                    self.collection.add(
                        documents=[header] + attributes,
                        ids=[f"{character_name}_0"] + [f"{character_name}_{i}" for i in range(len(attributes))],
                        metadatas=[{"type": "character", "subtype": "description"}] + [{"type": "character", "subtype": "attribute"} for _ in attributes]
                    )

    def get_tools(self) -> list[Any]:
        """
        Returns a list of tools that the agent can use to read documents.

        :return: A list of tool functions that the agent can use to read documents.
        :rtype: list[Any]
        """

        @tool
        def get_act(act_name: str) -> str:
            """Gets a string representation of a specific act from the plot document.
            Args:
                act_name: The name of the act to retrieve
            Returns:
                A string representation of the specified act, including the names and descriptions of the characters involved in the act
            Raises:
                ValueError: If the specified act name is not found in the plot document
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
            Args:
                character_name: The name of the character to retrieve
            Returns:
                A string summary of the specified character, including their attributes and values
            Raises:
                ValueError: If the specified character name is not found in the character documents
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

        @tool
        def get_character_attributes(character_name: str) -> list[str]:
            """Gets a list of attributes for a specific character from the character documents.
            Args:
                character_name: The name of the character to retrieve
            Returns:
                A list of attribute names for the specified character, which
                can then be retrieved with the get_character_attribute tool.
            Raises:
                ValueError: If the specified character name is not found in the character documents
            """
            with open(f"{self.directory}/{character_name.lower()}.json", "r", encoding="utf-8") as f:
                character_data = json.load(f)
                attributes = character_data.get("attributes")
                if attributes is None:
                    raise ValueError(f"Character '{character_name}' not found in the character documents.")
            return list(attributes.keys())
        
        @tool
        def get_character_attribute(character_name: str, attribute_name: str) -> str:
            """Gets the value of a specific attribute for a specific character from the character documents.
            Args:
                character_name: The name of the character to retrieve
                attribute_name: The name of the attribute to retrieve
            Returns:
                The value of the specified attribute for the specified character.
            Raises:
                ValueError: If the specified character name or attribute name is not found in the character documents
            """
            with open(f"{self.directory}/{character_name.lower()}.json", "r", encoding="utf-8") as f:
                character_data = json.load(f)
                attributes = character_data.get("attributes")
                if attributes is None:
                    raise ValueError(f"Character '{character_name}' not found in the character documents.")
                value = attributes.get(attribute_name.lower())
                if value is None:
                    raise ValueError(f"Attribute '{attribute_name}' not found for character '{character_name}'.")
            return value
        
        @tool
        def get_character_sprites(character_name: str) -> list[str]:
            """Gets a list of sprite image paths for a specific character from the character documents.
            Args:
                character_name: The name of the character to retrieve
            Returns:
                A list of sprite keys for the specified character,
                which can then be used in the sprite_action() tool.
            Raises:
                ValueError: If the specified character name is not found in the character documents
            """
            with open(f"{self.directory}/{character_name.lower()}.json", "r", encoding="utf-8") as f:
                character_data = json.load(f)
                sprites = character_data.get("sprites")
                if sprites is None:
                    raise ValueError(f"Character '{character_name}' not found in the character documents.")
            return list(sprites.keys())

        return [
            get_act,
            get_character_summary,
            get_character_attributes,
            get_character_attribute,
            get_character_sprites
        ]