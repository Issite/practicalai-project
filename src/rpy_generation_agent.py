from smolagents import ToolCallingAgent, InferenceClientModel, GradioUI
from src.script_writer import ScriptWriter


class RpyGenerationAgent:
    def run(self):
        print("RRpyGenerationAgent is running.")

        script_writer = ScriptWriter(
            ["data/stories/trial/alice.md", "data/stories/trial/bob.md"],
            "data/stories/trial/plot.md",
            "output/script.rpy",
            print_mode="both"
        )

        model = InferenceClientModel(
            max_tokens=8192,
            temperature=0.9,
            model_id="google/gemma-4-26B-A4B-it",
            custom_role_conversions=None,
        )

        agent = ToolCallingAgent(
            model=model,
            tools=script_writer.get_tools(),
            max_steps=8,
            verbosity_level=1,
            planning_interval=None,
            name=None,
            description=None,
        )

        GradioUI(agent).launch()