#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <model_name> [--dry-run]"
    echo "Example: $0 Qwen2.5-Coder-32B-Instruct --dry-run"
    exit 1
fi

MODEL="$1"
DRY_RUN="${2:-}"
REPO_DIR="./P3-Project"

if [[ ! -x "./submit.sh" ]]; then
    echo "Error: ./submit.sh not found or not executable in $(pwd)." >&2
    exit 1
fi

if [[ ! -d "$REPO_DIR" ]]; then
    echo "Error: Repository directory ${REPO_DIR} not found in $(pwd)." >&2
    exit 1
fi

CWES=(
    "CWE-22"
    "CWE-306"
    "CWE-352"
    "CWE-502"
    "CWE-79"
    "CWE-89"
    "CWE-94"
)

for cwe in "${CWES[@]}"; do
    for scenario in {1..3}; do
        for variation in {1..3}; do
            rel_target="${cwe}/Scenario${scenario}/Variation${variation}"
            full_target="${REPO_DIR}/${rel_target}"

            if [[ -d "$full_target" ]]; then
                if [[ "$DRY_RUN" == "--dry-run" ]]; then
                    echo "[DRY-RUN] ./submit.sh -a -g 4 ${rel_target} -m models/${MODEL}"
                else
                    echo "[SUBMIT] ./submit.sh -a -g 4 ${rel_target} -m models/${MODEL}"
                    ./submit.sh -a -g 4 "${rel_target}" -m "models/${MODEL}"
                fi
            else
                echo "[SKIP] Missing directory: ${full_target}" >&2
            fi
        done
    done
done