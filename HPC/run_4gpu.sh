#!/bin/bash
#SBATCH --partition=l4
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=00:30:00

set -euo pipefail

: "${TARGET_PATH:?Fejl: TARGET_PATH er ikke sat}"
: "${MODEL_PATH:?Fejl: MODEL_PATH er ikke sat}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
HOME_DIR="/ceph/home/student.aau.dk/rr30ub"

SIF_IMAGE="$HOME_DIR/vllm.sif"
SCRIPT_PATH="$SCRIPT_DIR/vllm_task_construction.py"
SOURCE_TASK="$REPO_DIR/$TARGET_PATH"

# Node-lokal isolation i scratch
JOB_SCRATCH="${TMPDIR:-/tmp}/job_${SLURM_JOB_ID}"
mkdir -p "$JOB_SCRATCH/task"
trap 'rm -rf "$JOB_SCRATCH"' EXIT

cp -r "$SOURCE_TASK/." "$JOB_SCRATCH/task/"

# Kør over de 4 allokerede L4 GPU'er
singularity exec --nv \
    -B "$HOME_DIR:$HOME_DIR" \
    -B "$JOB_SCRATCH:$JOB_SCRATCH" \
    "$SIF_IMAGE" \
    python3 "$SCRIPT_PATH" "$JOB_SCRATCH/task" "$MODEL_PATH"

cp "$JOB_SCRATCH/task/solution.txt" "$SOURCE_TASK/solution.txt"