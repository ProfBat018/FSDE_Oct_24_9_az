#!/usr/bin/env bash
set -euo pipefail

source /root/venvs/tf-gpu/bin/activate

# Register Jupyter kernel
python -m ipykernel install --user --name tf-gpu --display-name "Python (TF GPU)"

# Inject LD_LIBRARY_PATH / PATH into kernel.json so Jupyter sees GPU without sourcing activate
python - <<'PY'
import json
import os
from pathlib import Path

kernel = Path.home() / ".local/share/jupyter/kernels/tf-gpu/kernel.json"
data = json.loads(kernel.read_text())
env = data.setdefault("env", {})
env["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH", "")
env["PATH"] = os.environ.get("PATH", "")
env["TF_CPP_MIN_LOG_LEVEL"] = "1"
kernel.write_text(json.dumps(data, indent=2) + "\n")
print("kernel.json updated:", kernel)
print(json.dumps(data, indent=2))
PY

# Copy Lesson8 into Linux home (fast I/O)
mkdir -p /root/projects
rsync -a --delete \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '.ipynb_checkpoints' \
  /mnt/c/Users/RdpUser/Desktop/FSDE_Oct_24_9_az/Lesson8/ \
  /root/projects/Lesson8/
echo "copied to /root/projects/Lesson8"
ls -la /root/projects/Lesson8 | head
