import json
import uuid

from smartprompt.llm import RunLLm


class LabelMaker:
    def __init__(self, RunLLm: RunLLm, num_relevant_labels=5, label_length: int = 125):
        self.label_length = label_length
        self.num_relevant_labels = num_relevant_labels
        self.RunLLm = RunLLm

    def create_label(self, user_prompt_response: dict) -> tuple[str, str]:
        """Given a prompt-response pair, create a label for it."""
        prompt = f"""
                    You are an agent responsible for creating labels for context:
                    Read the following prompt and the subsequent response: \n
                    Prompt: {user_prompt_response["prompt"]} \n
                    Response: {user_prompt_response["response"]}\n
                    \n
                    Create a a label for the following prompt response pair.
                    It should be is no more than {self.label_length} characters long.
                    The purpose of this label is to make retrieval of \
                    the prompt-response easy, \
                    so it can be use as context for future prompts.
                """
        label = self.RunLLm.completion(prompt)["output"].strip()
        label_id = str(uuid.uuid4().int)
        return (label_id, label)

    def find_relevant_labels(self, label_list: dict, user_prompt: str) -> list:
        """Given a list of labels and a user prompt, find the most relevant labels."""

        prompt = f"""
        Read the following prompt: \n
        {user_prompt} \n
        
        Go through the labels for the prompt-response history given below.\n
        Select the {self.num_relevant_labels} most relevant labels \
        to use as context. \n\n
        """

        for label_id in label_list:
            prompt = (
                prompt
                + f"""
            label_id :{label_id}\n
            label : {label_list[label_id]}\n\n
            """
            )

        prompt = (
            prompt
            + """
        Return these as a list of the requested length for the most relevant labels of the following JSON format \
        in order of importance: \n
        [{{
            label_id: <most important label id>
            label: <most important label>
            
        }},
        {{
            label_id: <second most important label id>
            label: <second most important label>
            
        }},
        ]
        \n
        Add as many items as the number of most relevant labels requested.
        Your response should consist of only the requested list of JSON.
        """
        )

        response = self.RunLLm.completion(prompt)["output"].strip()
        print(response)
        response_list = json.loads(response)

        labels_jsons = [json.loads(json.dumps(item)) for item in response_list]

        return labels_jsons
