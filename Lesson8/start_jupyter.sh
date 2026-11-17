#!/usr/bin/env bash
# Launch Jupyter Lab with TF GPU kernel env
set -euo pipefail
source /root/venvs/tf-gpu/bin/activate
cd /root/projects/Lesson8
exec jupyter lab --no-browser --ip=127.0.0.1 --port=8888
