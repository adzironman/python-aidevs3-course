import json
import os
from pathlib import Path

from openai import OpenAI
from src.tasks.base_task import BaseTask
import json


class Research(BaseTask):
    def __init__(self):
        super().__init__("research")


    sys_prompt = "classify if according to your knowledge observation provided by user is correct or incorrect"

    def to_jsonl_line(self, raw_input: str, correct: bool):
        response = "correct" if correct else "incorrect"
        line = {
            "messages": [
                {"role": "system", "content": "classify if according to your knowledge observation provided by user is correct or incorrect"},
                {"role": "user", "content": f"{raw_input}"},
                {"role": "assistant", "content": response}
            ]
        }
        return json.dumps(line)

    def process(self):
        data_path = Path(os.getcwd()) / "data" / "lab_data"
        print(data_path)

        correct = []   
        incorrect = []

        with open(data_path / "correct.txt", "r") as data:
            for line in data.readlines():
                correct.append(self.to_jsonl_line(line.strip(), True))

        with open(data_path / "incorrect.txt", "r") as data:
            for line in data.readlines():
                incorrect.append(self.to_jsonl_line(line.strip(), False))

        with open(data_path / "data.jsonl", "w") as jl:
            for line in [*correct, *incorrect]:
                jl.write(f"{line}\n")


        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # assert correct
        res = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:validator:AdK3smYc",
            messages=[
                {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content": "94,-14,-46,88"}
            ]
        )

        msg = res.choices[0].message.content
        print(msg)

        # assert incorrect
        res = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:validator:AdK3smYc",
            messages=[
                {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content": "75,-95,67,46"}
            ]
        )

        msg = res.choices[0].message.content
        print(msg)

        # run on actual data

        verify = []
        with open(data_path / "verify.txt", "r") as data:
            for line in data.readlines():
                pair = line.strip().split("=")
                verify.append({"key": pair[0], "value": pair[1]})

        for i, item in enumerate(verify):
            res = client.chat.completions.create(
                model="ft:gpt-4o-mini-2024-07-18:personal:validator:AdK3smYc",
                messages=[
                    {"role": "system", "content": self.sys_prompt},
                    {"role": "user", "content": str(item["value"])}
                ]
            )
            outcome = res.choices[0].message.content
            verify[i]["outcome"] = outcome

        answer = [
                item["key"]
                for item in verify
                if item["outcome"] == "correct"
            ]

        return answer