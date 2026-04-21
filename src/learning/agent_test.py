from smolagents import CodeAgent, InferenceClientModel, GradioUI, load_tool, tool
import datetime
import pytz
import yaml


@tool
def dialogue_tool(name: str, dialogue: str) -> str:
    """A tool that continues the dialogue by appending a message to the script
    Args:
        name: the name of the character saying the message
        dialogue: the final answer that the character is saying. This should be a concise answer to the question, and should not include any reasoning steps or tool calls. It should be the final output of the agent.
    """
    print(f"DEBUG: {name} says: {dialogue}")
    return dialogue


@tool
def sprite_tool(name: str, sprite_id: str, action: str, value: int = None) -> str:
    """A tool that displays, hides, moves, and otherwise manipulates sprites on the screen
    Args:
        name: the name of the character whose sprite will be affected
        sprite_id: an identifier for which sprite variation to affect (e.g. "happy", "shocked", "neutral")
        action: the action that the sprite should take (e.g. "show", "hide", "xpos")
        value: when moving, how far across the screen should the sprite be placed (relative from 0 to 1.0)
    """
    print(f"DEBUG: {name} sprite {sprite_id} action: {action} value: {value}")
    return f"{sprite_id} {name} {action}s {value}"


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


class AgentTest:
    def run(self):
        model = InferenceClientModel(
            max_tokens=2096,
            temperature=0.5,
            model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
            custom_role_conversions=None,
        )

        """
        with open("resources/agent_test/prompts.yaml", 'r') as stream:
            prompt_templates = yaml.safe_load(stream)
        """

        # We're creating our CodeAgent
        agent = CodeAgent(
            model=model,
            tools=[final_answer, get_current_time_in_timezone],
            max_steps=6,
            verbosity_level=1,
            planning_interval=None,
            name=None,
            description=None,
            # prompt_templates=prompt_templates
        )

        GradioUI(agent).launch()
