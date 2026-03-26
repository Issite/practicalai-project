from smolagents import tool
from src.rpy_character import RpyCharacter


class ScriptWriter:
    """
    A class that acts as a translation layer between the agent and Ren'py script.
    It provides tools that the agent can use to write Ren'py scripts, and also
    handles the conversion of the agent's output into valid Ren'py script format.
    """

    def __init__(self, characters: list[RpyCharacter], plot_file: str, output_file: str):
        """
        Initializes the ScriptWriter with the given characters, plot file, and output file.
        
        :param characters: list[RpyCharacter] - A list of RpyCharacter instances
        :param plot_file: str - The path to the plot file
        :param output_file: str - The path to the output file
        """
        self.characters = characters
        self.plot_file = plot_file
        self.output_file = output_file
        self.last_speaker = None

    