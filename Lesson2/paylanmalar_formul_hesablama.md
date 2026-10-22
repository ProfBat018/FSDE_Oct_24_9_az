# Paylanmalar, kovariasiya və korrelyasiya: düsturlar və hesablamalarla nümunələr

## 1. Bərabər paylanma

**Vəziyyət:** avtobus hər 10 dəqiqədən bir gəlir, siz isə təsadüfi bir anda dayanacağa çatırsınız. Gözləmə müddəti X [a; b] = [0; 10] parçasında bərabər paylanıb.

### Düsturlar

| Nə | Düstur |
|---|---|
| Sıxlıq | $f(x) = \dfrac{1}{b-a}$, [a; b] parçasında |
| [c; d] aralığına düşmə ehtimalı | $P(c \le X \le d) = \dfrac{d-c}{b-a}$ |
| Orta (riyazi gözlənti) | $E(X) = \dfrac{a+b}{2}$ |
| Dispersiya | $Var(X) = \dfrac{(b-a)^2}{12}$ |

### Hesablamalar

- Sıxlıq: f(x) = 1 / (10 − 0) = **0,1**
- 7 dəqiqədən çox gözləmək: P(X > 7) = (10 − 7) / 10 = **0,3**
- 3 ilə 8 dəqiqə arasında gözləmək: P(3 ≤ X ≤ 8) = (8 − 3) / 10 = **0,5**
- Orta: E(X) = (0 + 10) / 2 = **5 dəqiqə**
- Dispersiya: Var(X) = 10² / 12 = 100 / 12 ≈ **8,33**
- Standart kənarlaşma: σ = √8,33 ≈ **2,89 dəqiqə**

### Zər (diskret analoq)

Qiymətlər 1...6, hər birinin ehtimalı 1/6.

- E(X) = (1 + 2 + 3 + 4 + 5 + 6) / 6 = 21 / 6 = **3,5**
- E(X²) = (1 + 4 + 9 + 16 + 25 + 36) / 6 = 91 / 6 ≈ 15,17
- Var(X) = E(X²) − (E(X))² = 15,17 − 12,25 ≈ **2,92**

## 2. Normal paylanma

**Vəziyyət:** yetkin kişilərin boyu normal paylanıb: μ = 175 sm, σ = 7 sm. Belə yazılır: X ~ N(175; 7²).

### Düsturlar

Sıxlıq:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\, e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

Standartlaşdırma (istənilən normal paylanmanı standart N(0; 1) paylanmasına çevirir):

$$z = \frac{x - \mu}{\sigma}$$

Sonra ehtimal cədvəldən və ya Φ(z) = P(Z ≤ z) funksiyasından götürülür.

### Hesablamalar

**Sual 1. Kişilərin neçə faizinin boyu 189 sm-dən yüksəkdir?**

z = (189 − 175) / 7 = **2**

P(X > 189) = 1 − Φ(2) = 1 − 0,9772 = **0,0228** (təxminən 2,3%)

**Sual 2. Kişilərin neçə faizinin boyu 160 sm-dən aşağıdır?**

z = (160 − 175) / 7 ≈ −2,14

P(X < 160) = Φ(−2,14) ≈ **0,0162** (təxminən 1,6%)

**Sual 3. Kişilərin neçə faizinin boyu 168 ilə 182 sm arasındadır?**

z₁ = (168 − 175) / 7 = −1
z₂ = (182 − 175) / 7 = 1

P = Φ(1) − Φ(−1) = 0,8413 − 0,1587 = **0,6827** (təxminən 68%)

**Sual 4. Ən hündür 10% içərisinə düşmək üçün boy nə qədər olmalıdır?**

Üst 10% üçün z = 1,28 lazımdır (cədvəldən, Φ(1,28) ≈ 0,90).

x = μ + z · σ = 175 + 1,28 · 7 ≈ **184 sm**

### Üç siqma qaydası

| Aralıq | Hesab | Məlumatların payı |
|---|---|---|
| μ ± σ | 168 ... 182 | **68,27%** |
| μ ± 2σ | 161 ... 189 | **95,45%** |
| μ ± 3σ | 154 ... 196 | **99,73%** |

### Şəkər paketi

X ~ N(1000; 5²). Paketlərin neçə faizinin çəkisi 990 q-dan azdır?

z = (990 − 1000) / 5 = −2, P(X < 990) = Φ(−2) = **0,0228** (paketlərin təxminən 2,3%-i əskik çəkilir).

## 3. Puasson paylanması

**Vəziyyət:** dəstək xidmətinə orta hesabla saatda 4 zəng daxil olur. Zənglərin sayı X ~ Poisson(λ = 4).

### Düsturlar

$$P(X = k) = \frac{\lambda^k \, e^{-\lambda}}{k!}$$

$$E(X) = Var(X) = \lambda$$

Lazım olan qiymət: e⁻⁴ ≈ 0,018316.

### Hesablamalar

**Heç bir zəng yoxdur (k = 0):**

P(X = 0) = 4⁰ · e⁻⁴ / 0! = 1 · 0,018316 / 1 ≈ **0,0183** (1,8%)

**Düz 1 zəng:**

P(X = 1) = 4¹ · e⁻⁴ / 1! = 4 · 0,018316 ≈ **0,0733**

**Düz 2 zəng:**

P(X = 2) = 4² · e⁻⁴ / 2! = 16 · 0,018316 / 2 ≈ **0,1465**

**Düz 3 zəng:**

P(X = 3) = 4³ · e⁻⁴ / 3! = 64 · 0,018316 / 6 ≈ **0,1954**

**Düz 4 zəng:**

P(X = 4) = 4⁴ · e⁻⁴ / 4! = 256 · 0,018316 / 24 ≈ **0,1954**

3 və 4 qiymətləri eyni ehtimal verir, bunlar ən ehtimallı nəticələrdir.

**Ən azı bir zəng:**

P(X ≥ 1) = 1 − P(X = 0) = 1 − 0,0183 = **0,9817** (təxminən 98%)

**İkidən çox olmayan zəng:**

P(X ≤ 2) = 0,0183 + 0,0733 + 0,1465 = **0,2381** (təxminən 24%)

### Xülasə

| k | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| P(X = k) | 0,0183 | 0,0733 | 0,1465 | 0,1954 | 0,1954 |

### Zaman müddətinin dəyişməsi

İntensivlik zamana mütənasib olaraq dəyişir. 30 dəqiqə üçün λ = 4 · 0,5 = **2**.

P(yarım saatda heç bir zəng yoxdur) = e⁻² = **0,1353** (13,5%)

## 4. Kovariasiya və korrelyasiya

**Vəziyyət:** 5 tələbə, x - hazırlıq saatları, y - imtahan balları.

| Tələbə | x | y |
|---|---|---|
| 1 | 1 | 50 |
| 2 | 2 | 55 |
| 3 | 3 | 65 |
| 4 | 4 | 70 |
| 5 | 5 | 80 |

### Düsturlar

Seçmə kovariasiyası:

$$Cov(X,Y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})$$

Pirson korrelyasiya əmsalı:

$$r = \frac{Cov(X,Y)}{\sigma_X \cdot \sigma_Y}$$

### Addım 1. Ortalar

x̄ = (1 + 2 + 3 + 4 + 5) / 5 = **3**
ȳ = (50 + 55 + 65 + 70 + 80) / 5 = 320 / 5 = **64**

### Addım 2. Kənarlaşmalar və onların hasilləri

| x | y | x − x̄ | y − ȳ | (x − x̄)(y − ȳ) | (x − x̄)² | (y − ȳ)² |
|---|---|---|---|---|---|---|
| 1 | 50 | −2 | −14 | 28 | 4 | 196 |
| 2 | 55 | −1 | −9 | 9 | 1 | 81 |
| 3 | 65 | 0 | 1 | 0 | 0 | 1 |
| 4 | 70 | 1 | 6 | 6 | 1 | 36 |
| 5 | 80 | 2 | 16 | 32 | 4 | 256 |
| **Cəm** | | | | **75** | **10** | **570** |

### Addım 3. Kovariasiya

Cov(X, Y) = 75 / (5 − 1) = **18,75**

Müsbətdir: x artdıqda y də artır.

### Addım 4. Standart kənarlaşmalar

σₓ = √(10 / 4) = √2,5 ≈ **1,581**
σᵧ = √(570 / 4) = √142,5 ≈ **11,937**

### Addım 5. Korrelyasiya

r = 18,75 / (1,581 · 11,937) = 18,75 / 18,875 ≈ **0,993**

Çox güclü müsbət əlaqə, demək olar ki, ideal düz xətt.

### Niyə korrelyasiya kovariasiyadan yaxşıdır

Saatları dəqiqəyə çevirək: x-i 60-a vururuq.

- Kovariasiya: 18,75 · 60 = **1125** (əlaqə eyni qalsa da, ədəd 60 dəfə dəyişdi)
- Korrelyasiya: **0,993** (dəyişmədi)

Kovariasiyanı müxtəlif məsələlər arasında müqayisə etmək olmaz, korrelyasiyanı isə olar, çünki o həmişə −1 ilə +1 aralığındadır.

### Tələ: güclü əlaqə zamanı sıfır korrelyasiya

x = −2, −1, 0, 1, 2 və y = x² = 4, 1, 0, 1, 4 götürək. Əlaqə dəqiqdir, y tamamilə x ilə müəyyən olunur.

- x̄ = 0, ȳ = (4 + 1 + 0 + 1 + 4) / 5 = 2
- (x − x̄)(y − ȳ) hasilləri: (−2)(2) + (−1)(−1) + (0)(−2) + (1)(−1) + (2)(2) = −4 + 1 + 0 − 1 + 4 = **0**
- Cov = 0, deməli **r = 0**

Pirson korrelyasiyası yalnız xətti əlaqəni tutur, ona görə burada «heç nə yoxdur» göstərir.

## Python ilə yoxlama

```python
import numpy as np
from scipy import stats

# 1. Bərabər paylanma
print(stats.uniform.cdf(8, 0, 10) - stats.uniform.cdf(3, 0, 10))  # 0.5
print(stats.uniform.var(0, 10))                                    # 8.33

# 2. Normal paylanma
print(1 - stats.norm.cdf(189, loc=175, scale=7))   # 0.0228
print(stats.norm.cdf(160, loc=175, scale=7))       # 0.0161
print(stats.norm.cdf(182, 175, 7) - stats.norm.cdf(168, 175, 7))  # 0.6827
print(stats.norm.ppf(0.90, loc=175, scale=7))      # 183.97

# 3. Puasson
for k in range(5):
    print(k, stats.poisson.pmf(k, mu=4))           # 0.0183 0.0733 0.1465 0.1954 0.1954
print(1 - stats.poisson.pmf(0, mu=4))              # 0.9817
print(stats.poisson.cdf(2, mu=4))                  # 0.2381

# 4. Kovariasiya və korrelyasiya
x = [1, 2, 3, 4, 5]
y = [50, 55, 65, 70, 80]
print(np.cov(x, y)[0, 1])        # 18.75
print(np.corrcoef(x, y)[0, 1])   # 0.9934

x2 = np.array([-2, -1, 0, 1, 2])
print(np.corrcoef(x2, x2**2)[0, 1])   # 0.0
```

Python-da kiçik fərq (160 sm-dən aşağı boy sualında 0,0162 əvəzinə 0,0161) onunla bağlıdır ki, cədvəllə işləmək üçün z-i −2,14-ə yuvarlaqlaşdırmışıq, Python isə dəqiq −2,1429 qiymətindən istifadə edir.
