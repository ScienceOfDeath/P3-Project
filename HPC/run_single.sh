#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00

set -euo pipefail

# Ensure essential variables were passed from the wrapper
: "${TARGET_PATH:?Error: TARGET_PATH environment variable not set}"
: "${MODEL_PATH:?Error: MODEL_PATH environment variable not set}"

BASE_DIR="/ceph/home/student.aau.dk/rr30ub"
REPO_DIR="$BASE_DIR/P3-Project"
SIF_IMAGE="$BASE_DIR/pytorch_llm.sif"
SCRIPT_PATH="$BASE_DIR/task_construction.py"

SOURCE_TASK="$REPO_DIR/$TARGET_PATH"

# 1. Isolate to local scratch storage
JOB_SCRATCH="${TMPDIR:-/tmp}/job_${SLURM_JOB_ID}"
mkdir -p "$JOB_SCRATCH/task"
trap 'rm -rf "$JOB_SCRATCH"' EXIT

cp -r "$SOURCE_TASK/." "$JOB_SCRATCH/task/"

# 2. Execute within Singularity container
singularity exec --nv \
    -B "$BASE_DIR:$BASE_DIR" \
    -B "$JOB_SCRATCH:$JOB_SCRATCH" \
    "$SIF_IMAGE" \
    python3 "$SCRIPT_PATH" "$JOB_SCRATCH/task" "$MODEL_PATH"

# 3. Write back solution file
cp "$JOB_SCRATCH/task/solution.txt" "$SOURCE_TASK/solution.txt"