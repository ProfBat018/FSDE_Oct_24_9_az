from pathlib import Path

p = Path("/root/venvs/tf-gpu/bin/activate")
text = p.read_text()
start = text.find("# >>> TF_GPU_LIB_PATHS >>>")
end = text.find("# <<< TF_GPU_LIB_PATHS <<<")
if start == -1 or end == -1:
    raise SystemExit("markers missing")
end = end + len("# <<< TF_GPU_LIB_PATHS <<<")

new = r"""# >>> TF_GPU_LIB_PATHS >>>
_TF_SITE="$VIRTUAL_ENV/lib/python3.12/site-packages"
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
# ensure WSL NVIDIA driver libs are visible
if [ -d /usr/lib/wsl/lib ]; then
  export LD_LIBRARY_PATH="/usr/lib/wsl/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
unset _TF_SITE _TF_NVIDIA_LIBS _d
# <<< TF_GPU_LIB_PATHS <<<"""

p.write_text(text[:start] + new + text[end:])
print("patched ok")
