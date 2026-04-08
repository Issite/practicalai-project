import json


class RpyCharacter:
    """
    Represents a character in the Ren'py story. Contains information relevent
    to character atributes, such as name, sprite files, and dialogue style, as
    well as information relevent to the agent, such as profile information and
    example dialogue.
    """

    def __init__(self, name: str, sprites: dict[str, str], attributes: dict[str, str]):
        self.name = name
        self.sprites = sprites
        self.attributes = attributes

    def from_json(file_contents: str) -> "RpyCharacter":
        """
        Parses a character definition file and creates an RpyCharacter object.

        :param file_contents: str - The contents of the character definition file (in JSON format)
        :return: RpyCharacter - An RpyCharacter object created from the file contents
        """
        data = json.loads(file_contents)
        character = RpyCharacter(data["name"], data["sprites"], data["attributes"])
        return character