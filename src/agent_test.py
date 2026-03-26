from smolagents import CodeAgent, InferenceClientModel, GradioUI, load_tool, tool
import datetime
import pytz
import yaml


@tool
def final_answer(name:str, dialogue:str)-> str:
    """A tool that does nothing yet 
    Args:
        name: the name of the character saying the answer
        dialogue: the final answer that the character is saying. This should be a concise answer to the question, and should not include any reasoning steps or tool calls. It should be the final output of the agent.
    """
    print(f"DEBUG: {name} says: {dialogue}")
    return dialogue

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
            model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
            custom_role_conversions=None,
        )

        with open("resources/agent_test/prompts.yaml", 'r') as stream:
            prompt_templates = yaml.safe_load(stream)
            
        # We're creating our CodeAgent
        agent = CodeAgent(
            model=model,
            tools=[final_answer, get_current_time_in_timezone], # add your tools here (don't remove final_answer)
            max_steps=6,
            verbosity_level=1,
            planning_interval=None,
            name=None,
            description=None,
            # prompt_templates=prompt_templates
        )

        GradioUI(agent).launch()