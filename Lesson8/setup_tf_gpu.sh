#!/usr/bin/env bash
set -euo pipefail

VENV=/root/venvs/tf-gpu
ACT="$VENV/bin/activate"
SITE="$VENV/lib/python3.12/site-packages"

if ! grep -q "TF_GPU_LIB_PATHS" "$ACT"; then
  cat >> "$ACT" << 'EOF'

# >>> TF_GPU_LIB_PATHS >>>
_TF_SITE="$(dirname "$(dirname "$(dirname "${BASH_SOURCE[0]}")")")/lib/python3.12/site-packages"
_TF_NVIDIA_LIBS=""
for _d in "$_TF_SITE"/nvidia/*/lib; do
  [ -d "$_d" ] && _TF_NVIDIA_LIBS="${_TF_NVIDIA_LIBS:+$_TF_NVIDIA_LIBS:}$_d"
done
if [ -n "$_TF_NVIDIA_LIBS" ]; then
  export LD_LIBRARY_PATH="${_TF_NVIDIA_LIBS}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
if [ -d "$_TF_SITE/nvidia/cuda_nvcc/bin" ]; then
  export PATH="$_TF_SITE/nvidia/cuda_nvcc/bin${PATH:+:$PATH}"
fi
unset _TF_SITE _TF_NVIDIA_LIBS _d
# <<< TF_GPU_LIB_PATHS <<<
EOF
fi

# shellcheck disable=SC1090
source "$ACT"
echo "ptxas: $(command -v ptxas || echo missing)"

python - <<'PY'
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"
import tensorflow as tf
print("TF", tf.__version__)
print("cuda", tf.test.is_built_with_cuda())
print("GPU", tf.config.list_physical_devices("GPU"))
print("ALL", tf.config.list_physical_devices())
PY
