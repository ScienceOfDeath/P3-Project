import os
import sys
import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_code_context(task_dir: str) -> str:
    """Recursively collects project context while safely ignoring binary,

    metadata, prompt, and output artifacts.
    """
    valid_extensions = (".py", ".html", ".js", ".json", ".sql", ".sh", ".c", ".cpp", ".h")
    code_blocks = []

    for root, dirs, files in os.walk(task_dir):
        # Prevent traversal into VCS, environments, and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("venv", "env", "__pycache__", "node_modules")]
        
        for file in sorted(files):
            # Exclude non-source files, inputs, and previous solution artifacts
            if file in ("prompt.txt", "solution.txt") or file.startswith("."):
                continue
            
            if file.endswith(valid_extensions):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, task_dir)
                try:
                    # Enforce strict UTF-8 with fallback replacement to avoid UnicodeDecodeError crashes
                    with open(filepath, "r", encoding="utf-8", errors="replace") as sf:
                        code_blocks.append(f"\n--- FILE: {rel_path} ---\n{sf.read()}\n")
                except OSError as err:
                    print(f"Warning: Could not read {filepath}: {err}", file=sys.stderr)

    return "".join(code_blocks)

def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <task_dir> <model_path> [output_file]", file=sys.stderr)
        sys.exit(1)

    task_dir = os.path.abspath(sys.argv[1])
    model_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(task_dir, "solution.txt")

    prompt_path = os.path.join(task_dir, "prompt.txt")
    if not os.path.isfile(prompt_path):
        print(f"Error: Prompt file missing at {prompt_path}", file=sys.stderr)
        sys.exit(1)

    with open(prompt_path, "r", encoding="utf-8", errors="replace") as f:
        prompt_content = f.read()

    context = load_code_context(task_dir)
    full_prompt = f"{prompt_content}\n\nProject Files:\n{context}" if context else prompt_content

    # local_files_only enforces offline reliability; prevents network lockups on offline compute nodes
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype="auto",
        device_map="auto",
        local_files_only=True
    )

    # Set pad token fallback for causal models without default padding configurations
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    # Single-pass tokenization directly to the model's mapped device
    messages = [{"role": "user", "content": full_prompt}]
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    prompt_length = input_ids.shape[1]

    # Run inference without autograd memory retention
    with torch.inference_mode():
        generated_ids = model.generate(
            input_ids,
            max_new_tokens=10240,
            pad_token_id=tokenizer.pad_token_id,
            do_sample=False  # Deterministic decoding for benchmark consistency
        )

    # Direct 2D tensor slice past prompt token boundary
    response_tokens = generated_ids[0][prompt_length:]
    response = tokenizer.decode(response_tokens, skip_special_tokens=True)

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write(response)

if __name__ == "__main__":
    main()