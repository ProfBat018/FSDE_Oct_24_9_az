"""Smoke-test: notebook-like CNN training on GPU (synthetic CIFAR-shaped data)."""
import os
import time

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

import tensorflow as tf
import numpy as np
import keras
from keras import layers

print("TensorFlow:", tf.__version__)
print("Keras:", keras.__version__)
gpus = tf.config.list_physical_devices("GPU")
print("GPU:", gpus)
assert gpus, "GPU not found"

for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Synthetic CIFAR-10 shaped batch (avoids slow toronto.edu download in WSL)
n = 2048
x_train = np.random.rand(n, 32, 32, 3).astype("float32")
y_train = np.random.randint(0, 10, size=(n, 1))
print("train:", x_train.shape)

model = keras.Sequential(
    [
        layers.Input(shape=(32, 32, 3)),
        layers.Conv2D(32, 3, activation="relu"),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        layers.Dense(10),
    ]
)
model.compile(
    optimizer="adam",
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)

t0 = time.perf_counter()
hist = model.fit(
    x_train,
    y_train,
    epochs=1,
    batch_size=64,
    validation_split=0.1,
    verbose=2,
)
dt = time.perf_counter() - t0
print(f"fit wall time: {dt:.2f}s")

a = tf.random.normal([256, 32, 32, 3])
logits = model(a, training=False)
print("logits device:", logits.device)
assert "GPU" in logits.device, logits.device
print("SMOKE OK: training on GPU")
