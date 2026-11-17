import os
import time

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "0")

import tensorflow as tf

print("TF", tf.__version__)
print("built_with_cuda", tf.test.is_built_with_cuda())
gpus = tf.config.list_physical_devices("GPU")
print("GPU", gpus)

for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

N = 4096


def bench(device: str) -> float:
    with tf.device(device):
        a = tf.random.normal([N, N])
        b = tf.random.normal([N, N])
        # warmup
        c = tf.matmul(a, b)
        _ = c.numpy()
        t0 = time.perf_counter()
        c = tf.matmul(a, b)
        _ = c.numpy()
        return time.perf_counter() - t0


cpu_t = bench("/CPU:0")
print(f"CPU matmul {N}x{N}: {cpu_t:.4f}s")

if gpus:
    gpu_t = bench("/GPU:0")
    print(f"GPU matmul {N}x{N}: {gpu_t:.4f}s on /GPU:0")
    print(f"speedup: {cpu_t / gpu_t:.1f}x")
else:
    raise SystemExit("GPU not visible")
