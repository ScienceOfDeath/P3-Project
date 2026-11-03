#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
HOME_DIR="/ceph/home/student.aau.dk/rr30ub"

TARGET_PATH="${1:-}"
MODEL_PATH="${2:-$HOME_DIR/models/Qwen2.5-Coder-32B-Instruct}"

if [ -z "$TARGET_PATH" ]; then
    echo "Brug: ./submit_4gpu_scenario.sh <CWE-XX/ScenarioY/VariationZ> [MODEL_PATH]" >&2
    exit 1
fi

FULL_TARGET="$REPO_DIR/$TARGET_PATH"
if [ ! -f "$FULL_TARGET/prompt.txt" ]; then
    echo "Fejl: prompt.txt eksisterer ikke på: $FULL_TARGET" >&2
    exit 1
fi

mkdir -p "$HOME_DIR/logs"
JOB_TAG=$(echo "$TARGET_PATH" | tr '/' '_')

sbatch \
    --job-name="4gpu_${JOB_TAG}" \
    --output="$HOME_DIR/logs/4gpu_${JOB_TAG}_%j.out" \
    --error="$HOME_DIR/logs/4gpu_${JOB_TAG}_%j.err" \
    --export=ALL,TARGET_PATH="$TARGET_PATH",MODEL_PATH="$MODEL_PATH" \
    "$SCRIPT_DIR/run_4gpu.sh"