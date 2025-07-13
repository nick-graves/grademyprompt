import json
from datasets import Dataset

with open("data.json", "r") as f:
    data = json.load(f)

dataset = Dataset.from_list(data)


def formatting_prompts_func(examples):
    output_text = []
    for i in range(len(examples["input"])):
        input_prompt = examples["input"][i]
        grade = examples["grade"][i]
        reasoning = examples["reasoning"][i]
        rewrite = examples["rewrite"][i]


        text = f'''
        ### Input:
        {input_prompt}
            
        ### Grade:
        {grade}
            
        ### Reasoning:
        {reasoning}

        ### Rewrite:
        {rewrite}
        '''

        output_text.append(text)

    return output_text



print(formatting_prompts_func(dataset))