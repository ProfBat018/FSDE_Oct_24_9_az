"""
CIFAR-10 klassifikatoru — Qt-приложение для модели из практики Модуля 5.

Что делает:
  * показывает в выпадающем списке все модели из папки models/
    (их сохраняет последняя ячейка ноутбука) и загружает выбранную;
  * принимает фото: кнопка, клик по области, drag & drop или Ctrl+V из буфера;
  * готовит фото точно так же, как данные при обучении
    (центральная квадратная обрезка -> 32x32 -> /255);
  * показывает, что «видит» сеть (картинку 32x32 в увеличенном виде),
    и вероятности всех 10 классов.

Модель грузится и считает в отдельном потоке, поэтому окно не зависает.
Запуск:  python app.py
"""

import json
import queue
import sys
import threading
from pathlib import Path

import numpy as np
from PIL import Image
from PySide6.QtCore import QObject, Qt, Signal, Slot
from PySide6.QtGui import QFont, QImage, QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFrame, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy, QVBoxLayout, QWidget,
)

# Тот же порядок классов, что и в ноутбуке (метка 0 = təyyarə, ...)
CLASS_NAMES = ["təyyarə", "avtomobil", "quş", "pişik", "maral",
               "it", "qurbağa", "at", "gəmi", "yük maşını"]

MODELS_DIR = Path(__file__).with_name("models")          # сюда сохраняет ноутбук
DEFAULT_MODEL = Path(__file__).with_name("cifar10_model.keras")   # старый вариант: один файл
IMAGE_FILTER = "Şəkillər (*.png *.jpg *.jpeg *.bmp *.webp)"
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
LOW_CONFIDENCE = 0.5          # ниже этого порога показываем предупреждение
PREVIEW_SIZE = 192            # размер увеличенного превью 32x32 на экране

# Палитра: холодный «учебный» синий, хорошо читается на проекторе
PALETTE = {
    "bg": "#EAEFF5",
    "panel": "#FFFFFF",
    "ink": "#17222E",
    "muted": "#5A6978",
    "accent": "#2B67A8",
    "bar": "#A9BCD3",
    "line": "#D3DCE6",
    "warn": "#B5651D",
}


# ----------------------------------------------------------------------
# Список моделей
# ----------------------------------------------------------------------
def find_models() -> list[tuple[str, str]]:
    """Возвращает [(подпись для списка, путь к файлу)].

    Если есть models/models.json из ноутбука — берём оттуда имена и точность
    (там они уже отсортированы от лучшей к худшей). Иначе просто все .keras в папке.
    """
    found = []
    index_file = MODELS_DIR / "models.json"
    if index_file.exists():
        for m in json.loads(index_file.read_text(encoding="utf-8")):
            path = MODELS_DIR / m["file"]
            if path.exists():
                found.append((f"{m['name']}  —  {m['test_acc'] * 100:.1f}%", str(path)))
    elif MODELS_DIR.is_dir():
        found = [(p.stem, str(p)) for p in sorted(MODELS_DIR.glob("*.keras"))]
    if DEFAULT_MODEL.exists():
        found.append((DEFAULT_MODEL.name, str(DEFAULT_MODEL)))
    return found


# ----------------------------------------------------------------------
# Работа с изображением
# ----------------------------------------------------------------------
def center_crop_square(img: Image.Image) -> Image.Image:
    """Обрезаем по центру до квадрата, чтобы при сжатии до 32x32 не исказить пропорции."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def preprocess(img: Image.Image, size: tuple[int, int]):
    """Та же подготовка, что в ноутбуке: RGB, 32x32, float32 в диапазоне [0, 1]."""
    small = center_crop_square(img.convert("RGB")).resize(
        (size[1], size[0]), Image.Resampling.LANCZOS)   # PIL ждёт (ширина, высота)
    x = np.asarray(small, dtype="float32") / 255.0      # (H, W, 3)
    return x[None, ...], small                          # добавляем ось батча: (1, H, W, 3)


def pil_to_pixmap(img: Image.Image) -> QPixmap:
    arr = np.ascontiguousarray(np.asarray(img.convert("RGB")))
    h, w, _ = arr.shape
    qimg = QImage(arr.data, w, h, 3 * w, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimg.copy())   # copy(): QImage не должен ссылаться на numpy-буфер


def qimage_to_pil(qimg: QImage) -> Image.Image:
    qimg = qimg.convertToFormat(QImage.Format.Format_RGB888)
    w, h, bpl = qimg.width(), qimg.height(), qimg.bytesPerLine()
    buf = np.frombuffer(qimg.constBits(), dtype=np.uint8, count=qimg.sizeInBytes())
    arr = buf.reshape(h, bpl)[:, : w * 3].reshape(h, w, 3)   # убираем выравнивание строк
    return Image.fromarray(arr.copy())


# ----------------------------------------------------------------------
# Модель в отдельном потоке
# ----------------------------------------------------------------------
class Predictor(QObject):
    """Вся работа с TensorFlow — в одном фоновом потоке Python.

    Окно кладёт задачи в очередь, поток выполняет их по одной и
    сообщает результат сигналами Qt (из другого потока они доставляются
    в главный поток через очередь событий, это безопасно).
    """
    model_loaded = Signal(str, int, int)     # имя файла, высота, ширина входа
    model_failed = Signal(str)
    prediction_ready = Signal(object)        # np.ndarray с 10 вероятностями
    prediction_failed = Signal(str)

    def __init__(self):
        super().__init__()
        self.model = None
        self.tasks: queue.Queue = queue.Queue()
        self.worker = threading.Thread(target=self._loop, daemon=True)
        self.worker.start()

    # --- вызываются из окна (главный поток) ---
    def load_model(self, path: str):
        self.tasks.put(("load", path))

    def predict(self, batch):
        self.tasks.put(("predict", batch))

    def stop(self):
        self.tasks.put(("stop", None))

    # --- выполняются в фоновом потоке ---
    def _loop(self):
        while True:
            kind, arg = self.tasks.get()
            if kind == "stop":
                break
            if kind == "load":
                self._load(arg)
            elif kind == "predict":
                self._predict(arg)

    def _load(self, path: str):
        try:
            import keras   # тяжёлый импорт делаем здесь, чтобы окно открылось сразу

            model = keras.models.load_model(path, compile=False)
            shape = model.input_shape
            if isinstance(shape, list):
                shape = shape[0]
            h, w, c = shape[1] or 32, shape[2] or 32, shape[3]
            if c != 3:
                raise ValueError(f"Model {c} kanallı giriş gözləyir, RGB (3) lazımdır.")
            if model.output_shape[-1] != len(CLASS_NAMES):
                raise ValueError(f"Modelin çıxışı {model.output_shape[-1]} sinifdir, 10 lazımdır.")
            self.model = model
            self.model_loaded.emit(Path(path).name, int(h), int(w))
        except Exception as exc:  # noqa: BLE001 — показываем любую ошибку пользователю
            self.model_failed.emit(str(exc))

    def _predict(self, batch):
        try:
            # training=False: Dropout и аугментация выключены, BN берёт moving-статистику
            probs = np.asarray(self.model(batch, training=False))[0].astype("float64")
            # Если последний слой без softmax (логиты), превращаем в вероятности сами
            if probs.min() < 0 or not np.isclose(probs.sum(), 1.0, atol=1e-3):
                e = np.exp(probs - probs.max())
                probs = e / e.sum()
            self.prediction_ready.emit(probs)
        except Exception as exc:  # noqa: BLE001
            self.prediction_failed.emit(str(exc))


# ----------------------------------------------------------------------
# Интерфейс
# ----------------------------------------------------------------------
class DropArea(QLabel):
    """Область с фото: принимает перетаскивание файла и открывает диалог по клику."""
    file_dropped = Signal(str)
    clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("dropArea")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAcceptDrops(True)
        self.setMinimumSize(360, 300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setWordWrap(True)
        self.setText("Şəkli bura sürüşdürün\nvə ya seçmək üçün klikləyin\n\nCtrl+V — buferdən yapışdırmaq")

    def dragEnterEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].toLocalFile().lower().endswith(IMAGE_EXTS):
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.file_dropped.emit(event.mimeData().urls()[0].toLocalFile())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


class MainWindow(QMainWindow):
    request_load = Signal(str)
    request_predict = Signal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CIFAR-10 klassifikatoru")
        self.resize(1040, 680)

        self.image: Image.Image | None = None   # текущее фото
        self.input_size: tuple[int, int] | None = None   # размер входа модели
        self.busy = False
        self.pending = False   # фото сменили, пока модель была занята

        self._build_ui()
        self._start_worker()

        self.model_combo.blockSignals(True)   # заполняем молча, загрузим один раз ниже
        for label, path in find_models():
            self.model_combo.addItem(label, path)
        self.model_combo.blockSignals(False)

        if self.model_combo.count():
            self.load_model(self.model_combo.currentData())
        else:
            self.model_label.setText("Model seçilməyib")
            self.statusBar().showMessage(
                f"“{MODELS_DIR.name}/” qovluğunda model tapılmadı. Notebook-un son xanasını işlədin "
                "və ya “Model seç” düyməsi ilə .keras faylını göstərin.")

    # ---------- построение окна ----------
    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 16, 20, 12)
        outer.setSpacing(14)

        # Верхняя панель: кнопки, список моделей и текущая модель
        top = QHBoxLayout()
        self.open_btn = QPushButton("Şəkil seç")
        self.open_btn.setObjectName("primary")
        self.open_btn.clicked.connect(self.choose_image)
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(260)
        self.model_combo.setToolTip("Proqnoz üçün model")
        self.model_combo.currentIndexChanged.connect(self.on_model_selected)
        self.model_btn = QPushButton("Model seç")
        self.model_btn.clicked.connect(self.choose_model)
        self.model_label = QLabel()
        self.model_label.setObjectName("muted")
        top.addWidget(self.open_btn)
        top.addWidget(self.model_combo)
        top.addWidget(self.model_btn)
        top.addSpacing(8)
        top.addWidget(self.model_label, 1)
        outer.addLayout(top)

        body = QHBoxLayout()
        body.setSpacing(16)
        outer.addLayout(body, 1)

        # Левая колонка: исходное фото
        left = QFrame()
        left.setObjectName("panel")
        lv = QVBoxLayout(left)
        lv.setContentsMargins(14, 14, 14, 14)
        self.drop = DropArea()
        self.drop.file_dropped.connect(self.open_image)
        self.drop.clicked.connect(self.choose_image)
        lv.addWidget(self.drop, 1)
        self.file_label = QLabel(" ")
        self.file_label.setObjectName("muted")
        lv.addWidget(self.file_label)
        body.addWidget(left, 5)

        # Правая колонка: что видит сеть + результат
        right = QFrame()
        right.setObjectName("panel")
        rv = QVBoxLayout(right)
        rv.setContentsMargins(18, 16, 18, 16)
        rv.setSpacing(10)

        head = QHBoxLayout()
        head.setSpacing(18)
        sees_box = QVBoxLayout()
        self.preview = QLabel()
        self.preview.setObjectName("preview")
        self.preview.setFixedSize(PREVIEW_SIZE, PREVIEW_SIZE)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_caption = QLabel("Şəbəkənin gördüyü: 32×32")
        self.preview_caption.setObjectName("muted")
        sees_box.addWidget(self.preview)
        sees_box.addWidget(self.preview_caption)
        head.addLayout(sees_box)

        answer_box = QVBoxLayout()
        answer_box.addStretch(1)
        caption = QLabel("Model deyir:")
        caption.setObjectName("muted")
        self.answer = QLabel("—")
        self.answer.setObjectName("answer")
        self.answer.setWordWrap(True)
        self.confidence = QLabel(" ")
        self.confidence.setObjectName("confidence")
        self.hint = QLabel(" ")
        self.hint.setObjectName("hint")
        self.hint.setWordWrap(True)
        answer_box.addWidget(caption)
        answer_box.addWidget(self.answer)
        answer_box.addWidget(self.confidence)
        answer_box.addWidget(self.hint)
        answer_box.addStretch(1)
        head.addLayout(answer_box, 1)
        rv.addLayout(head)

        line = QFrame()
        line.setObjectName("rule")
        line.setFixedHeight(1)
        rv.addWidget(line)

        # 10 строк вероятностей; при каждом предсказании сортируются по убыванию
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)
        self.rows = []
        for i in range(len(CLASS_NAMES)):
            name = QLabel(CLASS_NAMES[i])
            bar = QProgressBar()
            bar.setRange(0, 1000)
            bar.setValue(0)
            bar.setTextVisible(False)
            bar.setFixedHeight(14)
            pct = QLabel("")
            pct.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            pct.setMinimumWidth(56)
            grid.addWidget(name, i, 0)
            grid.addWidget(bar, i, 1)
            grid.addWidget(pct, i, 2)
            self.rows.append((name, bar, pct))
        grid.setColumnStretch(1, 1)
        rv.addLayout(grid)

        note = QLabel("Model yalnız bu 10 sinfi tanıyır: istənilən şəkli onlardan birinə aid edəcək.")
        note.setObjectName("muted")
        note.setWordWrap(True)
        rv.addWidget(note)
        rv.addStretch(1)
        body.addWidget(right, 6)

        QShortcut(QKeySequence.StandardKey.Open, self, activated=self.choose_image)
        QShortcut(QKeySequence.StandardKey.Paste, self, activated=self.paste_image)

        self._apply_style()

    def _apply_style(self):
        p = PALETTE
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background: {p['bg']}; color: {p['ink']}; font-size: 14px; }}
            QFrame#panel {{ background: {p['panel']}; border: 1px solid {p['line']}; border-radius: 6px; }}
            QFrame#panel QLabel, QFrame#panel QWidget {{ background: transparent; }}
            QFrame#rule {{ background: {p['line']}; }}
            QLabel#muted {{ color: {p['muted']}; font-size: 13px; }}
            QLabel#dropArea {{ border: 2px dashed {p['bar']}; border-radius: 4px;
                               color: {p['muted']}; font-size: 15px; }}
            QLabel#preview {{ border: 1px solid {p['line']}; background: {p['bg']}; }}
            QLabel#answer {{ font-size: 34px; font-weight: 700; color: {p['accent']}; }}
            QLabel#confidence {{ font-size: 16px; color: {p['ink']}; }}
            QLabel#hint {{ font-size: 13px; color: {p['warn']}; }}
            QProgressBar {{ background: {p['bg']}; border: none; border-radius: 3px; }}
            QProgressBar::chunk {{ background: {p['bar']}; border-radius: 3px; }}
            QProgressBar[top="true"]::chunk {{ background: {p['accent']}; }}
            QPushButton {{ background: {p['panel']}; border: 1px solid {p['line']};
                           border-radius: 5px; padding: 7px 16px; }}
            QPushButton:hover {{ border-color: {p['accent']}; }}
            QPushButton:focus {{ border: 2px solid {p['accent']}; }}
            QPushButton#primary {{ background: {p['accent']}; color: white; border: none; font-weight: 600; }}
            QPushButton#primary:hover {{ background: #235890; }}
            QPushButton:disabled {{ color: {p['muted']}; background: {p['bg']}; }}
            QComboBox {{ background: {p['panel']}; border: 1px solid {p['line']};
                         border-radius: 5px; padding: 6px 10px; }}
            QComboBox:hover {{ border-color: {p['accent']}; }}
            QComboBox:disabled {{ color: {p['muted']}; background: {p['bg']}; }}
            QComboBox QAbstractItemView {{ background: {p['panel']};
                                           selection-background-color: {p['accent']};
                                           selection-color: white; }}
            QStatusBar {{ color: {p['muted']}; }}
        """)

    # ---------- фоновый поток ----------
    def _start_worker(self):
        self.predictor = Predictor()
        self.request_load.connect(self.predictor.load_model)
        self.request_predict.connect(self.predictor.predict)
        self.predictor.model_loaded.connect(self.on_model_loaded)
        self.predictor.model_failed.connect(self.on_model_failed)
        self.predictor.prediction_ready.connect(self.on_prediction)
        self.predictor.prediction_failed.connect(self.on_prediction_failed)

    def closeEvent(self, event):
        self.predictor.stop()
        super().closeEvent(event)

    # ---------- модель ----------
    def choose_model(self):
        path, _ = QFileDialog.getOpenFileName(self, "Modeli seçin", str(Path.cwd()),
                                              "Keras modeli (*.keras *.h5)")
        if not path:
            return
        # Файл, выбранный вручную, тоже попадает в список; выбор пункта сам запустит загрузку
        i = self.model_combo.findData(path)
        if i < 0:
            self.model_combo.addItem(Path(path).name, path)
            i = self.model_combo.count() - 1
        if i == self.model_combo.currentIndex():
            self.load_model(path)
        else:
            self.model_combo.setCurrentIndex(i)

    @Slot(int)
    def on_model_selected(self, index):
        if index >= 0:
            self.load_model(self.model_combo.itemData(index))

    def load_model(self, path: str):
        self.input_size = None
        self.set_busy(True)
        self.model_label.setText(f"Model yüklənir: {Path(path).name} …")
        self.statusBar().showMessage("TensorFlow ilk dəfə bir neçə saniyə yüklənir.")
        self.request_load.emit(path)

    @Slot(str, int, int)
    def on_model_loaded(self, name, h, w):
        self.input_size = (h, w)
        self.preview_caption.setText(f"Şəbəkənin gördüyü: {w}×{h}")
        self.model_label.setText(f"Model: {name}")
        self.statusBar().showMessage("Model hazırdır.", 4000)
        self.set_busy(False)
        if self.image is not None:
            self.pending = False
            self.run_prediction()

    @Slot(str)
    def on_model_failed(self, message):
        self.set_busy(False)
        self.model_label.setText("Model yüklənmədi")
        self.statusBar().showMessage(f"Modeli yükləmək olmadı: {message}")

    # ---------- изображение ----------
    def choose_image(self):
        if self.busy:
            return
        path, _ = QFileDialog.getOpenFileName(self, "Şəkli seçin", str(Path.home()), IMAGE_FILTER)
        if path:
            self.open_image(path)

    def open_image(self, path: str):
        try:
            img = Image.open(path)
            img.load()
        except Exception as exc:  # noqa: BLE001
            self.statusBar().showMessage(f"Şəkli açmaq olmadı: {exc}")
            return
        self.set_image(img, Path(path).name)

    def paste_image(self):
        qimg = QApplication.clipboard().image()
        if qimg.isNull():
            self.statusBar().showMessage("Buferdə şəkil yoxdur.", 4000)
            return
        self.set_image(qimage_to_pil(qimg), "buferdən yapışdırılıb")

    def set_image(self, img: Image.Image, title: str):
        self.image = img.convert("RGB")
        w, h = self.image.size
        self.file_label.setText(f"{title}  ({w}×{h})")
        self.show_original()
        if self.busy:
            self.pending = True
        elif self.input_size is not None:
            self.run_prediction()
        else:
            self.statusBar().showMessage("Model hələ hazır deyil — yükləndikdən sonra proqnoz veriləcək.")

    def show_original(self):
        if self.image is None:
            return
        pix = pil_to_pixmap(self.image).scaled(
            self.drop.size() * 0.96, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        self.drop.setPixmap(pix)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.show_original()

    # ---------- предсказание ----------
    def run_prediction(self):
        batch, small = preprocess(self.image, self.input_size)
        # Увеличиваем 32x32 без сглаживания — видно реальные «пиксели», с которыми работает сеть
        self.preview.setPixmap(pil_to_pixmap(small).scaled(
            PREVIEW_SIZE, PREVIEW_SIZE, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation))
        self.set_busy(True)
        self.answer.setText("…")
        self.request_predict.emit(batch)

    @Slot(object)
    def on_prediction(self, probs):
        self.set_busy(False)
        if self.pending:            # пока считали, пользователь выбрал новое фото
            self.pending = False
            self.run_prediction()
            return
        order = np.argsort(probs)[::-1]
        best = int(order[0])
        self.answer.setText(CLASS_NAMES[best])
        self.confidence.setText(f"Əminlik: {probs[best] * 100:.1f}%")
        if probs[best] < LOW_CONFIDENCE:
            second = CLASS_NAMES[int(order[1])]
            self.hint.setText(f"Model əmin deyil — “{second}” variantı da yaxındır.")
        else:
            self.hint.setText(" ")

        for row, cls in enumerate(order):
            name, bar, pct = self.rows[row]
            p = float(probs[cls])
            name.setText(CLASS_NAMES[cls])
            bar.setValue(int(round(p * 1000)))
            pct.setText(f"{p * 100:.1f}%")
            is_top = row == 0
            bar.setProperty("top", is_top)
            bar.style().unpolish(bar)      # перерисовать с учётом нового свойства
            bar.style().polish(bar)
            font = name.font()
            font.setBold(is_top)
            name.setFont(font)

    @Slot(str)
    def on_prediction_failed(self, message):
        self.set_busy(False)
        self.answer.setText("—")
        self.statusBar().showMessage(f"Proqnoz alınmadı: {message}")

    def set_busy(self, busy: bool):
        self.busy = busy
        self.open_btn.setEnabled(not busy)
        self.model_btn.setEnabled(not busy)
        self.model_combo.setEnabled(not busy)
        if busy:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        else:
            while QApplication.overrideCursor() is not None:
                QApplication.restoreOverrideCursor()


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont(app.font().family(), 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
