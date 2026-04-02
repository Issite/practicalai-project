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
        characters: list[RpyCharacter],
        plot_file: str,
        output_file: str,
        print_mode: str = "both"
    ):
        """
        Initializes the ScriptWriter with the given characters, plot file, and output file.

        :param characters: list[RpyCharacter] - A list of RpyCharacter instances
        :param plot_file: str - The path to the plot file
        :param output_file: str - The path to the output file
        """
        self.characters = characters
        self.plot_file = plot_file
        self.output_file = output_file
        self.print_mode = print_mode
        self.last_speaker = None
        self.narrator_name = "Narrator"

    def _write_lines(self, lines: list[dict]) -> None:
        """
        Writes a list of lines to the output file and optionally prints them to the console.

        :param lines: list[dict] - A list of dictionaries, each containing a "line" key with the line to write,
        a "print" key indicating whether to print the line to the console,
        and a "write" key indicating whether to write the line to the output file.
        """
        with open(self.output_file, "a", encoding="utf-8") as f:
            for line in lines:
                if line["write"]:
                    f.write(line["line"] + "\n")
                if line["print"]:
                    print(line["line"])

    @tool
    def write_dialogue(self, character_name: str, dialogue: str) -> None:
        """
        Writes a line of dialogue for the specified character.

        :param character_name: str - The name of the character speaking
        :param dialogue: str - The dialogue to be spoken by the character
        :raises ValueError: If the specified character name is not found in the characters list
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
            out_lines.append({"line": f"show {character_name} at bob", "print": False, "write": True})
            out_lines.append({"line": f'{character_name} "{dialogue}"', "print": True, "write": True})
        else:
            out_lines.append({"line": f'{character_name} "{dialogue}"', "print": True, "write": True})

        self._write_lines(out_lines)

    @tool
    def sprite_action(
        self,
        character_name: str,
        sprite_id: str,
        action: str,
        description: str,
        value: int = None,
    ) -> None:
        """
        Controls the display of character sprites on screen.

        :param character_name: str - The name of the character whose sprite is changing
        :param sprite_id: str - The ID of the new sprite, often corresponding to a specific emotion or pose
        :param action: str - The action to be performed ("show", "hide", "xpos")
        :param value: int - An optional relative value for the action (e.g., the new x position for "xpos" action)
        :param description: str - An optional description of the action for command line output
        :raises ValueError: If the specified character name is not found in the characters list, if the specified sprite ID is not found for the character, or if an invalid action is provided
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
            raise ValueError(
                f"Sprite ID '{sprite_id}' not found for character '{character_name}'."
            )

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
                out_lines.append({"line": f"hide {character_name}", "print": False, "write": True})
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

        self._write_lines(out_lines)


    @tool
    def present_choice(self, options: list[dict], caption: str = "") -> None:
        """
        Presents a choice to the player.

        :param options: list[dict] - A list of dictionaries, each containing a "text" key with the option text
        and a "label" key with the label to jump to if the option is selected
        :param caption: str - An optional caption to display above the choices
        """

        out_lines = [{"line": "menu:\n", "print": False}]
        if caption:
            out_lines.append({"line": f"{caption}", "print": True})

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
                    {
                        "line": f'    "{option["text"]}":',
                        "print": False,
                        "write": True
                    }
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
        
        self._write_lines(out_lines)