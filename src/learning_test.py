import os
from huggingface_hub import InferenceClient
import dotenv

SYSTEM_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

get_weather: Get the current weather in a given location

The way you use the tools is by specifying a json blob.
Specifically, this json should have an `action` key (with the name of the tool to use) and an `action_input` key (with the input to the tool going here).

The only values that should be in the "action" field are:
get_weather: Get the current weather in a given location, args: {"location": {"type": "string"}}
example use :

{{
  "action": "get_weather",
  "action_input": {"location": "New York"}
}}


ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:

$JSON_BLOB (inside markdown cell)

Observation: the result of the action. This Observation is unique, complete, and the source of truth.
(this Thought/Action/Observation can repeat N times, you should take several steps when needed. The $JSON_BLOB must be formatted as markdown and only use a SINGLE action at a time.)

You must always end your output with the following format:

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Now begin! Reminder to ALWAYS use the exact characters `Final Answer:` when you provide a definitive answer. """

class LearningTest:

    def get_weather(_, location):
        return f"the weather in {location} is sunny with low temperatures. \n"

    def run(self):

        dotenv.load_dotenv()
        HF_TOKEN = os.environ.get("HF_TOKEN")

        client = InferenceClient(model="moonshotai/Kimi-K2.5", token=HF_TOKEN)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "What's the weather in London?"},
        ]

        output = client.chat.completions.create(
            messages=messages,
            stream=False,
            max_tokens=150,
            stop=["Observation:"],
            extra_body={'thinking': {'type': 'disabled'}},
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "What's the weather in London ?"},
            {"role": "assistant", "content": output.choices[0].message.content + "Observation:\n" + self.get_weather('London')},
        ]

        output = client.chat.completions.create(
            messages=messages,
            stream=False,
            max_tokens=200,
            extra_body={'thinking': {'type': 'disabled'}},
        )

        print(output.choices[0].message.content)