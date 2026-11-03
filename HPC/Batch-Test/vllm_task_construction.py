import os
import sys
import argparse
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

def load_code_context(task_dir: str) -> str:
    valid_extensions = (".py", ".html", ".js", ".json", ".sql", ".sh", ".c", ".cpp", ".h")
    code_blocks = []

    for root, dirs, files in os.walk(task_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("venv", "env", "__pycache__", "node_modules")]
        
        for file in sorted(files):
            if file in ("prompt.txt", "solution.txt") or file.startswith("."):
                continue
            if file.endswith(valid_extensions):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, task_dir)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="replace") as sf:
                        code_blocks.append(f"\n--- FILE: {rel_path} ---\n{sf.read()}\n")
                except OSError as err:
                    print(f"Advarsel: Kunne ikke læse {filepath}: {err}", file=sys.stderr)

    return "".join(code_blocks)

def main():
    if len(sys.argv) < 3:
        print(f"Brug: python {sys.argv[0]} <task_dir> <model_path> [output_file]", file=sys.stderr)
        sys.exit(1)

    task_dir = os.path.abspath(sys.argv[1])
    model_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(task_dir, "solution.txt")

    prompt_path = os.path.join(task_dir, "prompt.txt")
    if not os.path.isfile(prompt_path):
        print(f"Fejl: prompt.txt mangler i {task_dir}", file=sys.stderr)
        sys.exit(1)

    with open(prompt_path, "r", encoding="utf-8", errors="replace") as f:
        prompt_content = f.read()

    context = load_code_context(task_dir)
    full_prompt = f"{prompt_content}\n\nProject Files:\n{context}" if context else prompt_content

    # Formater prompten med chat template
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    messages = [{"role": "user", "content": full_prompt}]
    formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # Initialiser vLLM med Tensor Parallelism = 4
    llm = LLM(
        model=model_path,
        tensor_parallel_size=4,
        trust_remote_code=True,
        gpu_memory_utilization=0.90,
        max_model_len=16384
    )

    # Deterministisk evaluering (greedy)
    sampling_params = SamplingParams(
        temperature=0.0,
        max_tokens=4096
    )

    outputs = llm.generate([formatted_prompt], sampling_params)
    solution = outputs[0].outputs[0].text

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write(solution)

if __name__ == "__main__":
    main()