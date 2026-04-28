from typing import Any
from smolagents import tool
from src.rpy_character import RpyCharacter


class ScriptWriter:
    """
    A class that acts as a translation layer between the agent and Ren'py script.
    It provides tools that the agent can use to write Ren'py scripts, and also
    handles the conversion of the agent's output into valid Ren'py script format.
    """

    def __init__(
        self,
        characters: list[str],
        plot_file: str,
        output_file: str,
        print_mode: str = "both",
    ):
        """
        Initializes the ScriptWriter with the given characters, plot file, and output file.

        :param characters: list[str] - A list of RpyCharacter filepaths
        :param plot_file: str - The path to the plot file
        :param output_file: str - The path to the output file
        """
        self.characters = self._load_characters(characters)
        self.plot_file = plot_file
        self.output_file = output_file
        self.print_mode = print_mode
        self.last_speaker = None
        self.narrator_name = "Narrator"

    def _load_characters(self, character_files: list[str]) -> list[RpyCharacter]:
        """
        Loads character information from the given character files.

        :param character_files: list[str] - A list of file paths to character definition files
        :return: list[RpyCharacter] - A list of RpyCharacter objects created from the character files
        """
        characters = []
        for file in character_files:
            with open(file, "r", encoding="utf-8") as f:
                character_data = f.read()
                character = RpyCharacter.from_json(character_data)
                characters.append(character)
        return characters

    def get_tools(self) -> list[Any]:
        """
        Returns a list of tools that the agent can use to write the script.

        :return: list[tool] - A list of tool functions that the agent can use
        """

        @tool
        def write_dialogue(character_name: str, dialogue: str) -> list[dict[str, Any]]:
            """Writes a line of dialogue for the specified character.
            Args:
                character_name: The name of the character speaking
                dialogue: The dialogue to be spoken by the character
            Returns:
                A list of dictionaries, each containing a "line" key with the line to write,
                a "print" key indicating whether to print the line to the console,
                and a "write" key indicating whether to write the line to the output file.
            Raises:
                ValueError: If the specified character name is not found in the characters list
            """

            if character_name not in [character.name for character in self.characters]:
                raise ValueError(
                    f"Character '{character_name}' not found in characters list."
                )

            out_lines = []

            if character_name == self.narrator_name:
                self.last_speaker = None
                out_lines.append({"line": f"{dialogue}", "print": True, "write": True})
            elif self.last_speaker != character_name:
                self.last_speaker = character_name
                out_lines.append(
                    {"line": f"show {character_name} at bob", "print": False, "write": True}
                )
                out_lines.append(
                    {"line": f'{character_name} "{dialogue}"', "print": True, "write": True}
                )
            else:
                out_lines.append(
                    {"line": f'{character_name} "{dialogue}"', "print": True, "write": True}
                )

            return out_lines

        @tool
        def sprite_action(
            character_name: str,
            sprite_id: str,
            action: str,
            description: str,
            value: int = None,
        ) -> list[dict[str, Any]]:
            """Controls the display of character sprites on screen.
            Args:
                character_name: The name of the character whose sprite is changing
                sprite_id: The ID of the new sprite, often corresponding to a specific emotion or pose
                action: The action to be performed ("show", "hide", "xpos")
                value: An optional relative value for the action (e.g., the new x position for "xpos" action)
                description: An optional description of the action for command line output
            Returns:
                A list of dictionaries, each containing a "line" key with the line to write,
                a "print" key indicating whether to print the line to the console,
                and a "write" key indicating whether to write the line to the output file.
            Raises:
                ValueError: If the specified character name is not found in the characters list, if the specified sprite ID is not found for the character, or if an invalid action is provided
            """

            character = next(
                (
                    character
                    for character in self.characters
                    if character.name == character_name
                ),
                None,
            )
            if not character:
                raise ValueError(
                    f"Character '{character_name}' not found in characters list."
                )

            if sprite_id not in character.sprites:
                """raise ValueError(
                    f"Sprite ID '{sprite_id}' not found for character '{character_name}'."
                )"""
                pass # No sprites yet

            out_lines = []

            match action:
                case "show":
                    out_lines.append(
                        {
                            "line": f"show {character_name} {sprite_id} at bob",
                            "print": False,
                            "write": True
                        }
                    )
                case "hide":
                    out_lines.append(
                        {"line": f"hide {character_name}", "print": False, "write": True}
                    )
                case "xpos":
                    if value is None:
                        raise ValueError("Value must be provided for 'xpos' action.")
                    out_lines.append(
                        {
                            "line": f"show {character_name} {sprite_id} at xpos {value}",
                            "print": False,
                            "write": True
                        }
                    )
                case _:
                    raise ValueError(
                        f"Invalid action '{action}'. Valid actions are 'show', 'hide', and 'xpos'."
                    )

            out_lines.append({"line": f"{description}", "print": True, "write": False})

            return out_lines

        @tool
        def present_choice(options: list[dict], caption: str = "") -> list[dict[str, Any]]:
            """Presents a choice to the player.
            Args:
                options: A list of dictionaries, each containing a "text" key with the option text
                    and a "label" key with the label to jump to if the option is selected
                caption: An optional caption to display above the choices
            Returns:
                A list of dictionaries, each containing a "line" key with the line to write,
                a "print" key indicating whether to print the line to the console,
                and a "write" key indicating whether to write the line to the output file.
            """

            out_lines = [{"line": "menu:\n", "print": False}]
            if caption:
                out_lines.append({"line": f"{caption}", "print": True, "write": True})

            try:
                option_num = 1
                for option in options:
                    out_lines.append(
                        {
                            "line": f'{option_num}. {option["text"]}',
                            "print": True,
                            "write": False
                        }
                    )
                    option_num += 1
                    out_lines.append(
                        {"line": f'    "{option["text"]}":', "print": False, "write": True}
                    )
                    out_lines.append(
                        {
                            "line": f'        jump {option["label"]}',
                            "print": False,
                            "write": True
                        }
                    )
            except KeyError as e:
                raise ValueError(
                    f"Each option must contain 'text' and 'label' keys. Missing key: {e}"
                ) from e

            # TODO: Implement menu in print mode, also set next label.

            return out_lines
        
        @tool
        def write_lines(lines: list[dict[str, Any]]) -> None:
            """
            Writes a list of lines to the output file and optionally prints them to the console.
            Args:
                lines: A list of dictionaries, each containing a "line" key with the line to write,
                    a "print" key indicating whether to print the line to the console,
                    and a "write" key indicating whether to write the line to the output file.
            """
            with open(self.output_file, "a", encoding="utf-8") as f:
                for line in lines:
                    if line["write"]:
                        f.write(line["line"] + "\n")
                    if line["print"]:
                        print(line["line"])

        return [write_dialogue, sprite_action, present_choice, write_lines]