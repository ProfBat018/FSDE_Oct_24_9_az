#!/usr/bin/env bash
set -euo pipefail

WIN_ARC="/mnt/c/Users/RdpUser/.keras/datasets/cifar-10-batches-py-target_archive"
WIN_DIR="/mnt/c/Users/RdpUser/.keras/datasets/cifar-10-batches-py-target/cifar-10-batches-py"
DEST="/root/.keras/datasets"
EXPECTED="6d958be074577803d12ecdefd02955f39262c83c16fe9348329d7fe0b5c001ce"

mkdir -p "$DEST/cifar-10-batches-py-target"

echo "1) Put archive where Keras 3 expects it:"
echo "   $DEST/cifar-10-batches-py-target_archive"
cp -f "$WIN_ARC" "$DEST/cifar-10-batches-py-target_archive"

HASH="$(sha256sum "$DEST/cifar-10-batches-py-target_archive" | awk '{print $1}')"
echo "sha256=$HASH"
[ "$HASH" = "$EXPECTED" ] || { echo "HASH MISMATCH"; exit 1; }

echo "2) Put extracted batches:"
rm -rf "$DEST/cifar-10-batches-py-target/cifar-10-batches-py"
mkdir -p "$DEST/cifar-10-batches-py-target"
cp -a "$WIN_DIR" "$DEST/cifar-10-batches-py-target/cifar-10-batches-py"

# Also keep legacy name for older code paths
cp -f "$WIN_ARC" "$DEST/cifar-10-batches-py.tar.gz"

echo "3) Cache layout:"
ls -lh "$DEST"
ls -lh "$DEST/cifar-10-batches-py-target/cifar-10-batches-py"

source /root/venvs/tf-gpu/bin/activate
python - <<'PY'
import os
import time
from pathlib import Path

# Simulate exact notebook call
import keras
from keras.utils import get_file

print("HOME=", os.environ.get("HOME"))
print("calling get_file exactly like cifar10.load_data ...")
t0 = time.perf_counter()
path = get_file(
    fname="cifar-10-batches-py-target",
    origin="https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz",
    extract=True,
    file_hash="6d958be074577803d12ecdefd02955f39262c83c16fe9348329d7fe0b5c001ce",
)
dt = time.perf_counter() - t0
print("get_file path:", path)
print("get_file seconds:", round(dt, 3))
print("inner exists:", Path(path, "cifar-10-batches-py", "data_batch_1").exists())

t0 = time.perf_counter()
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
print("load_data seconds:", round(time.perf_counter() - t0, 3))
print("shapes:", x_train.shape, x_test.shape)
if dt > 5:
    raise SystemExit("Still looks like network download (>5s for get_file)")
print("OK: cache hit, no download")
PY
