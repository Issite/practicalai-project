from smolagents import CodeAgent, InferenceClientModel, GradioUI
from src.script_writer import ScriptWriter


class RpyGenerationAgent:
    def run(self):
        print("RpyGenerationAgent is running.")

        script_writer = ScriptWriter(
            ["data/stories/trial/alice.json", "data/stories/trial/bob.json"],
            "data/stories/trial/plot.json",
            "output/script.rpy",
            print_mode="both"
        )

        model = InferenceClientModel(
            max_tokens=8192,
            temperature=1,
            model_id="google/gemma-4-26B-A4B-it",
            custom_role_conversions=None,
        )

        agent = CodeAgent(
            model=model,
            code_block_tags=("```python", "```"),
            tools=script_writer.get_tools(),
            max_steps=8,
            verbosity_level=2,
            planning_interval=None,
            name=None,
            description=None,
        )

        GradioUI(agent).launch()