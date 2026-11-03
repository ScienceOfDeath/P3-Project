import os
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

task_dir = sys.argv[1]
model_name = sys.argv[2]

# Load prompt
prompt_path = os.path.join(task_dir, "prompt.txt")
with open(prompt_path, "r") as f:
    prompt = f.read()

# Load project source files using clean relative paths
code_context = ""
for root, _, files in os.walk(task_dir):
    for file in files:
        if file.endswith((".py", ".html", ".js", ".json")):
            if file == "prompt.txt":
                continue
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, task_dir)
            with open(filepath, "r") as sf:
                code_context += f"\n--- FILE: {rel_path} ---\n{sf.read()}\n"

full_prompt = f"{prompt}\n\nProject Files:\n{code_context}"

# Initialize Model & Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

messages = [{"role": "user", "content": full_prompt}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
model_inputs = tokenizer([text], return_tensors="pt").to("cuda")

generated_ids = model.generate(**model_inputs, max_new_tokens=1024)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

# Write isolated solution
output_path = os.path.join(task_dir, "solution.txt")
with open(output_path, "w") as out_f:
    out_f.write(response)