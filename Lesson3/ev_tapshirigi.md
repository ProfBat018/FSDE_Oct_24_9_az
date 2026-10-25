# Ev tapşırığı — Regression (Simple / Multiple / Polynomial)

**Modul 3 · Dərs 1**

Bütün lazımi kod nümunələri dərsdəki `ders1_reqressiya_metrics_az.ipynb` faylındadır. Bu tapşırıqda **yeni kod yazın**, dərsdəki hüceyrələri kopyalamayın.

---

## Verilənlər

Bir arıçının gündəlik müşahidə jurnalları. Hər sətir — bir gün.

`data/` qovluğunda 3 CSV faylı var:

| Fayl | Sətir sayı | Feature-lər | Target |
|---|---|---|---|
| `bal_10.csv` | 10 | `cicek_say`, `temperatur`, `rutubet` | `bal_kq` |
| `bal_20.csv` | 20 | `cicek_say`, `temperatur`, `rutubet` | `bal_kq` |
| `bal_50.csv` | 50 | `cicek_say`, `temperatur`, `rutubet` | `bal_kq` |

- `cicek_say` — yaxınlıqda çiçək sayı
- `temperatur` — havanın temperaturu (°C)
- `rutubet` — rütubət (%)
- `bal_kq` — həmin gün toplanan bal (kq)

---

## Tapşırıqlar

### 1. Multiple Linear Regression

Hər üç CSV üçün:

1. Faylı oxuyun.
2. Feature kimi **ən azı 2** sütun seçin (`cicek_say`, `temperatur`, `rutubet` arasından).
3. `LinearRegression` modelini öyrədin.
4. `w` əmsallarını və `b`-ni çap edin.
5. Yeni gün üçün prediction verin: **180 çiçək, 26°C, 55% rütubət** (seçdiyiniz feature-lərə uyğun).

### 2. Polynomial Regression

Hər üç CSV üçün:

1. Eyni feature-lərlə `PolynomialFeatures` (dərəcə 2) tətbiq edin.
2. `LinearRegression` modelini öyrədin.
3. Feature adlarını və əmsalları çap edin.
4. Eyni yeni gün üçün prediction verin.

### 3. Metrics cədvəli

Hər CSV və hər model (Multiple Linear + Polynomial) üçün **MAE**, **MSE**, **R²** hesablayın.

Nəticəni **cədvəl** şəklində göstərin. Məsələn:

| Fayl | Model | MAE | MSE | R² |
|---|---|---|---|---|
| bal_10 | Multiple Linear | … | … | … |
| bal_10 | Polynomial | … | … | … |
| … | … | … | … | … |

### 4. Qısa nəticə (yazılı)

1–2 abzasla cavab verin:

- Hansı model daha yaxşı metric göstərir?
- Sətir sayı (10 / 20 / 50) nəticəyə necə təsir edir?
- Polynomial həmişə daha yaxşıdırmı? Niyə?

---

## Təhvil

- Jupyter Notebook (`.ipynb`)
- Cədvəllər notebook-da görünməlidir
- Sonunda yazılı nəticə olmalıdır
- Hər tapşırıqın MAE, MSE, R^2 təhlili cədvəl ilə göstərilsin

**Son tarix:** dərsdə elan olunacaq.
