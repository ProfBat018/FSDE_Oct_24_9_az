import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

MODEL_PATH = Path(__file__).parent / "mnist_cnn.pt"
MEAN, STD = 0.1307, 0.3081
CANVAS_SIZE = 280
PEN_WIDTH = 22


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = self.dropout(torch.relu(self.fc1(x)))
        return self.fc2(x)


def preprocess(pixels):
    """280×280 canvas (0..255) → MNIST-like 28×28 image (0..1). None if the canvas is empty."""
    ys, xs = np.nonzero(pixels > 30)
    if len(xs) == 0:
        return None

    # 1. crop the bounding box around the digit
    crop = pixels[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    crop = torch.from_numpy(crop).float()[None, None] / 255   # (1, 1, h, w)

    # 2. fit into 20×20, keeping the aspect ratio
    h, w = crop.shape[-2:]
    scale = 20 / max(h, w)
    new_h, new_w = max(1, round(h * scale)), max(1, round(w * scale))
    small = F.interpolate(crop, size=(new_h, new_w), mode="bilinear", antialias=True)[0, 0]

    # 3. place it in the center of a 28×28 image
    img = torch.zeros(28, 28)
    top, left = (28 - new_h) // 2, (28 - new_w) // 2
    img[top:top + new_h, left:left + new_w] = small

    # 4. shift the center of mass to the image center
    rows = torch.arange(28).float()
    total = img.sum()
    cy = (img.sum(dim=1) * rows).sum() / total
    cx = (img.sum(dim=0) * rows).sum() / total
    shift = (round(14 - cy.item()), round(14 - cx.item()))
    return torch.roll(img, shifts=shift, dims=(0, 1))


class Canvas(QWidget):
    """Black canvas, we draw in white on it, just like MNIST."""

    def __init__(self, on_change):
        super().__init__()
        self.on_change = on_change
        self.setFixedSize(CANVAS_SIZE, CANVAS_SIZE)
        self.image = QImage(CANVAS_SIZE, CANVAS_SIZE, QImage.Format.Format_Grayscale8)
        self.last_point = None
        self.clear()

    def clear(self):
        self.image.fill(Qt.GlobalColor.black)
        self.update()
        self.on_change()

    def pixels(self):
        """Canvas → (280, 280) numpy array with values 0..255."""
        bpl = self.image.bytesPerLine()
        data = np.frombuffer(self.image.constBits(), dtype=np.uint8)
        return data.reshape(CANVAS_SIZE, bpl)[:, :CANVAS_SIZE].copy()

    def draw_line(self, start: QPoint, end: QPoint):
        painter = QPainter(self.image)
        pen = QPen(QColor("white"), PEN_WIDTH, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawLine(start, end)
        painter.end()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = event.position().toPoint()
            self.draw_line(self.last_point, self.last_point)
            self.on_change()

    def mouseMoveEvent(self, event):
        if self.last_point is not None:
            point = event.position().toPoint()
            self.draw_line(self.last_point, point)
            self.last_point = point
            self.on_change()

    def mouseReleaseEvent(self, event):
        self.last_point = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)


class MainWindow(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("MNIST: rəqəm çək")

        # right side: answer, probabilities, what the network sees
        self.answer = QLabel("?")
        self.answer.setFont(QFont("Helvetica", 64, QFont.Weight.Bold))
        self.answer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bars = []
        bars_layout = QGridLayout()
        for digit in range(10):
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setFormat("%p%")
            bars_layout.addWidget(QLabel(str(digit)), digit, 0)
            bars_layout.addWidget(bar, digit, 1)
            self.bars.append(bar)

        self.preview = QLabel()
        self.preview.setFixedSize(112, 112)
        self.preview.setStyleSheet("background: black; border: 1px solid gray;")

        clear_button = QPushButton("Təmizlə (C)")
        clear_button.clicked.connect(lambda: self.canvas.clear())

        right = QVBoxLayout()
        right.addWidget(self.answer)
        right.addLayout(bars_layout)
        right.addWidget(QLabel("Şəbəkə nə görür (28×28):"))
        right.addWidget(self.preview)
        right.addStretch()

        left = QVBoxLayout()
        left.addWidget(QLabel("Mausun sol düyməsi ilə çək:"))
        self.canvas = Canvas(self.predict)
        left.addWidget(self.canvas)
        left.addWidget(clear_button)
        left.addStretch()

        layout = QHBoxLayout(self)
        layout.addLayout(left)
        layout.addLayout(right)

        self.predict()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_C, Qt.Key.Key_Space, Qt.Key.Key_Escape):
            self.canvas.clear()

    def predict(self):
        if not hasattr(self, "canvas"):
            return
        img = preprocess(self.canvas.pixels())

        if img is None:
            self.answer.setText("?")
            for bar in self.bars:
                bar.setValue(0)
            self.preview.clear()
            return

        x = ((img - MEAN) / STD)[None, None]           # (1, 1, 28, 28)
        with torch.no_grad():
            probs = torch.softmax(self.model(x), dim=1)[0]

        best = probs.argmax().item()
        self.answer.setText(str(best))
        for digit, bar in enumerate(self.bars):
            bar.setValue(round(probs[digit].item() * 100))

        # show the 28×28 image scaled up 4×
        gray = (img * 255).byte().numpy().copy()
        qimg = QImage(gray.data, 28, 28, 28, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg.copy()).scaled(112, 112, Qt.AspectRatioMode.KeepAspectRatio,
                                                       Qt.TransformationMode.FastTransformation)
        self.preview.setPixmap(pixmap)


def main():
    app = QApplication(sys.argv)

    if not MODEL_PATH.exists():
        QMessageBox.critical(None, "Model tapılmadı",
                             f"{MODEL_PATH.name} faylı tapılmadı.\nƏvvəlcə modeli torch_mnist.ipynb notebook-unda öyrədin.")
        sys.exit(1)

    model = Net()
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()

    window = MainWindow(model)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
