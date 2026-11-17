#!/usr/bin/env bash
set -euo pipefail
DIR=/mnt/c/Users/RdpUser/Desktop/FSDE_Oct_24_9_az/Lesson8
sed -i 's/\r$//' "$DIR/patch_activate.py" "$DIR/tf_gpu_verify.py" "$DIR/run_gpu_setup.sh"
python3 "$DIR/patch_activate.py"
# shellcheck disable=SC1091
source /root/venvs/tf-gpu/bin/activate
echo "ptxas=$(command -v ptxas || true)"
python - <<'PY'
import os
ld = os.environ.get("LD_LIBRARY_PATH", "")
print("LD_LIBRARY_PATH length:", len(ld))
print("LD_LIBRARY_PATH start:", ld[:200])
PY
python "$DIR/tf_gpu_verify.py"
