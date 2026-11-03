#!/bin/bash
set -euo pipefail

BASE_DIR="/ceph/home/student.aau.dk/rr30ub"
REPO_DIR="$BASE_DIR/P3-Project"

# Enforce explicit input
TARGET_PATH="${1:-}"
MODEL_PATH="${2:-$BASE_DIR/models/Qwen2.5-0.5B-Instruct}"

if [ -z "$TARGET_PATH" ]; then
    echo "Usage: ./submit_scenario.sh <CWE-XX/ScenarioY/VariantZ> [MODEL_PATH]" >&2
    exit 1
fi

# Pre-flight check on login node: fail immediately on typos, not inside SLURM
FULL_TARGET="$REPO_DIR/$TARGET_PATH"
if [ ! -f "$FULL_TARGET/prompt.txt" ]; then
    echo "Error: prompt.txt does not exist at: $FULL_TARGET" >&2
    exit 1
fi

# Format safe job name (e.g., eval_CWE-22_S5_V3)
JOB_TAG=$(echo "$TARGET_PATH" | tr '/' '_')

# Submit job with variables strictly scoped to this execution
sbatch \
    --job-name="eval_${JOB_TAG}" \
    --output="$BASE_DIR/logs/${JOB_TAG}_%j.out" \
    --error="$BASE_DIR/logs/${JOB_TAG}_%j.err" \
    --export=ALL,TARGET_PATH="$TARGET_PATH",MODEL_PATH="$MODEL_PATH" \
    "$BASE_DIR/run_single.sh"