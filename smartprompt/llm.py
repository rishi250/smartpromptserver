from pathlib import Path

from dotenv import load_dotenv
from litellm import completion

dotenv_path = Path("/Users/rishi/smartpromptserver/.env") # add the path to your env file here
load_dotenv(dotenv_path=dotenv_path)

class RunLLm:
    """Run prompts against LLM."""
    def __init__(self, model: str):
        self.model = model

    def completion(self, prompt: str) -> dict:
        """Given a prompt, return a completion from the language model."""
        response = completion(
            model=self.model,
            messages=[{"content": prompt, "role": "assistant"}],
        )
        llm_response = {}
        llm_response["output"] = response.choices[0].message.content
        return llm_response
