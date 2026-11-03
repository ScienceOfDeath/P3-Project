#!/bin/bash
#SBATCH --job-name=flask-dynamic
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH --output=solver_%j.out
#SBATCH --error=solver_%j.err

export SINGULARITY_TMPDIR=$TMPDIR
export APPTAINER_TMPDIR=$TMPDIR

MODEL_NAME="${MODEL_NAME:-Qwen/Qwen2.5-0.5B-Instruct}"
# Example: "CWE-22/Scenario5/Variant3"
TARGET_PATH="${TARGET_PATH:-CWE-22/Scenario5/Variant3}"

BASE_DIR="/ceph/home/student.aau.dk/rr30ub/.local/tmp"
cd "$BASE_DIR"

# Create isolated run directory
RUN_DIR="$BASE_DIR/workspace_runtime"
rm -rf "$RUN_DIR"
mkdir -p "$RUN_DIR"
cd "$RUN_DIR"

# Dynamically sparse-checkout only the requested variant
git init
git remote add origin https://github.com/ScienceOfDeath/P3-Project.git
git sparse-checkout init --cone
git sparse-checkout set "$TARGET_PATH"
git pull origin main

# Locate the actual task folder containing prompt.txt
CURRENT_TASK="$RUN_DIR/$TARGET_PATH"

if [ ! -f "$CURRENT_TASK/prompt.txt" ]; then
    echo "Error: prompt.txt not found in pulled path $TARGET_PATH"
    exit 1
fi

# Ensure container and dependencies exist
if [ ! -f "$BASE_DIR/pytorch26.sif" ]; then
    singularity pull "$BASE_DIR/pytorch26.sif" docker://pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
fi
singularity exec --nv "$BASE_DIR/pytorch26.sif" pip install --user transformers accelerate

# Execute solver script using the isolated dynamic path[cite: 1, 2]
singularity exec --nv "$BASE_DIR/pytorch26.sif" python3 "$BASE_DIR/task_construction.py" "$CURRENT_TASK" "$MODEL_NAME"