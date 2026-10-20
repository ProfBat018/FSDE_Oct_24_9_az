# Dərs mühitinin qurulması

Dərs notebook-u: `data_science_dersi.ipynb`.

Python 3.15 və altı paket lazımdır: NumPy, pandas, matplotlib, openpyxl, ipykernel və Jupyter Notebook. Aşağıda işlək mühitdəki addımlar və versiyalar var.

## 1. Python 3.15 quraşdırın

**Python 3.15** quraşdırıcısını [python.org/downloads](https://www.python.org/downloads/) ünvanından yükləyin və quraşdırın.

macOS-da quraşdırmadan sonra yeni Terminal pəncərəsi açın və versiyanı yoxlayın:

```bash
python3 --version
```

Nəticə `Python 3.15.0` və ya 3.15 xəttindən daha yeni versiya olmalıdır. Əmr `python3` adlanır.

Windows-da quraşdırıcıda **Add python.exe to PATH** qutusunu işarələyin. Yeni PowerShell pəncərəsində yoxlama:

```powershell
py --version
```

## 2. Dərs qovluğunu açın

Dərs materiallarını açın və `data_science_dersi.ipynb` faylının olduğu qovluğa keçin.

macOS və Linux:

```bash
cd dərs/qovluğunun/yolu
```

Windows PowerShell:

```powershell
cd dərs\qovluğunun\yolu
```

## 3. Virtual mühit yaradın

Mühit notebook-un yanındakı `.venv` qovluğundadır. Bu qovluğu başqasına köçürmək lazım deyil: hər kəs öz mühitini yaradır.

macOS və Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Sətrin əvvəlində `(.venv)` görünəcək. Bundan sonra paketlər bu mühitin içinə qurulur.

Növbəti dəfə mühiti yenidən yaratmaq lazım deyil. `source` və ya `Activate.ps1` əmrini yenidən işlətmək kifayətdir. Çıxış: `deactivate`.

## 4. Paketləri quraşdırın

Aktiv mühitdən bir əmrlə. Siyahı və versiyalar `requirements.txt` faylındadır.

```bash
python -m pip install -r requirements.txt
```

Windows-da `python` əvəzinə belə yazmaq olar:

```powershell
py -m pip install -r requirements.txt
```

Nə qurulur:

| Paket | Versiya | Nə üçün |
|---|---|---|
| numpy | 2.5.4 | massivlər |
| pandas | 3.0.6 | Series və DataFrame |
| matplotlib | 3.11.2 | qrafiklər |
| openpyxl | 3.1.5 | Excel oxumaq və yazmaq |
| ipykernel | 7.4.0 | notebook xanalarını işə salmaq |
| notebook | 7.6.3 | Jupyter Notebook |

Yoxlama:

```bash
python -c "import numpy, pandas, matplotlib, openpyxl, ipykernel; print('ok')"
```

Cavabda `ok` sətri olmalıdır.

## 5. Kernel-i Cursor-a qoşun

Mühiti Jupyter kernel-i kimi qeyd edin:

```bash
python -m ipykernel install --user --name step --display-name "Python 3.15 (STEP)"
```

Cursor-da `data_science_dersi.ipynb` faylını açın. Sağ yuxarı küncdə **Select Kernel** düyməsini basın və **Python 3.15 (STEP)** seçin.

Xana soldakı düymə ilə və ya **Shift+Enter** ilə işə düşür. Kod olan hər xananın öz verilənləri var, onun üçün əvvəlki xanaları işə salmaq lazım deyil.

## 6. Jupyter Notebook ilə işə salmaq

Aktiv mühitdən, dərs qovluğunda:

```bash
jupyter notebook
```

Brauzerdə `data_science_dersi.ipynb` faylını açın. Kernel eynidir: **Python 3.15 (STEP)**.
