import os
from huggingface_hub import InferenceClient
import dotenv

class LearningTest:
    def run(self):

        dotenv.load_dotenv()
        HF_TOKEN = os.environ.get("HF_TOKEN")
        print("HF_TOKEN:", HF_TOKEN)

        client = InferenceClient(model="moonshotai/Kimi-K2.5", token=HF_TOKEN)
        output = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "The capital of France is"},
            ],
            stream=False,
            max_tokens=1024,
            extra_body={'thinking': {'type': 'disabled'}},
        )
        print(output.choices[0].message.content)
