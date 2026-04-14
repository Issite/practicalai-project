from smolagents import CodeAgent, InferenceClientModel, GradioUI
from src.script_writer import ScriptWriter
from src.document_reader import DocumentReader


class RpyGenerationAgent:
    def run(self):
        print("RpyGenerationAgent is running.")

        script_writer = ScriptWriter(
            ["data/stories/trial/alice.json", "data/stories/trial/bob.json"],
            "data/stories/trial/plot.json",
            "output/script.rpy",
            print_mode="both"
        )

        document_reader = DocumentReader("data/stories/trial")

        model = InferenceClientModel(
            max_tokens=8192,
            temperature=1,
            model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
            custom_role_conversions=None,
        )

        agent = CodeAgent(
            model=model,
            code_block_tags=("```python", "```"),
            tools=script_writer.get_tools() + document_reader.get_tools(),
            max_steps=8,
            verbosity_level=2,
            planning_interval=None,
            name=None,
            description=None,
        )

        # Dev deploymment. I need to build my own user-focused front-end
        GradioUI(agent).launch()