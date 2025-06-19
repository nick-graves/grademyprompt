from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
import json
from transformers import TrainingArguments
from trl import SFTTrainer


model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-Instruct-bnb-4bit",
    max_seq_length = 2048,
    dtype = torch.float16,
    load_in_4bit = True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r                       = 64,
    lora_alpha              = 16,
    lora_dropout            = 0.05,
    bias                    = "none",
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    use_gradient_checkpointing = True,
    random_state            = 42,
    max_seq_length          = 2048,
)

'''
with open("data.json", "r") as f:
    data = json.load(f)

dataset = Dataset.from_list(data)
'''
dataset = load_dataset('json', data_files='data.json')

'''
def formatting_func(example):
    output = example["rewrite"] if example["rewrite"] != "N/A" else example["input"]

    prompt = f"""### Instruction:
Revise the following prompt to make it better for AI. Then explain the reasoning and assign a grade from 0–100 based on prompt quality.

### Input:
{example['input']}

### Response:
**Rewritten Prompt**:
{output}

**Reasoning**:
{example['reasoning']}

**Grade**:
{example['grade']}"""

    return prompt
'''
def formatting_prompts_func(example):
    input_prompt = example["input"]
    grade        = example["grade"]
    reasoning    = example["reasoning"]
    rewrite      = example["rewrite"]

    text = f"""### Input:
{input_prompt}

### Grade:
{grade}

### Reasoning:
{reasoning}

### Rewrite:
{rewrite}"""

    return [text]



training_args = TrainingArguments(
    output_dir = "./llama3-8b-qlora-finetuned",
    per_device_train_batch_size = 1,
    gradient_accumulation_steps = 8,
    warmup_steps = 10,
    max_steps = 100,
    learning_rate = 2e-4,
    fp16 = True,
    logging_steps = 10,
    save_steps = 100,
    save_total_limit = 2,
    optim = "paged_adamw_8bit",
    lr_scheduler_type = "cosine",
    report_to = "none",
)

trainer = SFTTrainer(
    model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    formatting_func = formatting_prompts_func,
    dataset_text_field = None,
    args = training_args,
    max_seq_length = 2048,
)


trainer.train()
trainer.save_model("./llama3-8b-qlora-finetuned")
tokenizer.save_pretrained("./llama3-8b-qlora-finetuned")