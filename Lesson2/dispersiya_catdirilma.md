# Dispersiya: çatdırılma nümunəsi

Gəlin real həyatdan nümunə götürək: iki çatdırılma xidmətinin **sifarişi çatdırma müddəti**.

## Məlumatlar

Hər xidmətdən 7 dəfə sifariş verilib. Çatdırılma müddəti (dəqiqə ilə):

- **A xidməti:** 28, 30, 29, 31, 30, 32, 30
- **B xidməti:** 15, 45, 20, 40, 30, 50, 10

## Addım 1. Ortanı hesablayırıq

**A xidməti:** (28 + 30 + 29 + 31 + 30 + 32 + 30) / 7 = 210 / 7 = **30 dəqiqə**

**B xidməti:** (15 + 45 + 20 + 40 + 30 + 50 + 10) / 7 = 210 / 7 = **30 dəqiqə**

Orta eynidir. Yalnız ortaya baxsaq, xidmətlər bərabər görünür, amma praktikada bu, tamamilə belə deyil.

## Addım 2. Dispersiyanı hesablayırıq

**A xidməti:**

| Müddət | 30-dan kənarlaşma | Kvadrat |
|---|---|---|
| 28 | −2 | 4 |
| 30 | 0 | 0 |
| 29 | −1 | 1 |
| 31 | 1 | 1 |
| 30 | 0 | 0 |
| 32 | 2 | 4 |
| 30 | 0 | 0 |
| **Cəm** | | **10** |

s² = 10 / (7 − 1) = 10 / 6 ≈ **1,67 dəq²**

**B xidməti:**

| Müddət | 30-dan kənarlaşma | Kvadrat |
|---|---|---|
| 15 | −15 | 225 |
| 45 | 15 | 225 |
| 20 | −10 | 100 |
| 40 | 10 | 100 |
| 30 | 0 | 0 |
| 50 | 20 | 400 |
| 10 | −20 | 400 |
| **Cəm** | | **1450** |

s² = 1450 / 6 ≈ **241,67 dəq²**

## Addım 3. Standart kənarlaşma

Dispersiya «dəqiqə kvadratı» ilə ölçüldüyü üçün onu şərh etmək çətindir. Ona görə kvadrat kök alırıq:

- A xidməti: σ = √1,67 ≈ **1,3 dəqiqə**
- B xidməti: σ = √241,67 ≈ **15,5 dəqiqə**

## Praktikada bunun mənası

| | Orta | Standart kənarlaşma | Nə gözləmək olar |
|---|---|---|---|
| A xidməti | 30 dəq | 1,3 dəq | Demək olar ki, həmişə 28-32 dəqiqəyə gətirəcək |
| B xidməti | 30 dəq | 15,5 dəq | Həm 10, həm də 50 dəqiqə ola bilər |

A xidməti **proqnozlaşdırıla biləndir**: yeməyin 30-cu dəqiqədə gələcəyinə arxayın planlaşdırmaq olar. B xidməti isə **proqnozlaşdırıla bilməyəndir**: orta hesabla eyni 30 dəqiqədir, amma sifarişi 10 dəqiqəyə də ala bilərsiniz, 50 dəqiqə gözləyib görüşə gecikə də bilərsiniz.

B xidmətinin dispersiyası 145 dəfə böyükdür (241,67 / 1,67) və məhz bu, onun qeyri-sabitliyini göstərir. Orta isə bu fərqi **gizlədir**.

## Digər real nümunələr

- **Maliyyə:** orta illik gəliri 10% olan iki səhm. Birinin dispersiyası kiçikdir (sabit artım), digərinin böyükdür (bir ildə +40%, digərində −20%). İkincisi daha risklidir. Maliyyədə gəlirliliyin standart kənarlaşmasına **volatillik** deyilir.
- **İstehsalat:** dəzgah uzunluğu 10 mm olan detallar hazırlayır. Təkcə orta (10 mm) yox, kiçik dispersiya da vacibdir, əks halda çoxlu detal brak olacaq.
- **Hava:** iki şəhərdə orta temperatur +15°C-dir. Sahil şəhərində temperatur +12 ilə +18 arasında dəyişir, kontinental şəhərdə isə −10-dan +40-a qədər. İkincinin dispersiyası xeyli böyükdür.
- **Data Science:** modelin keyfiyyət metrikası çarpaz validasiya zamanı. Fold-lar üzrə dəqiqlik 0,90; 0,91; 0,89-dursa, model stabildir. 0,95; 0,70; 0,98-dirsə, dispersiya böyükdür və nəticəyə etibar etmək olmaz.

## Python ilə yoxlama

```python
import numpy as np

a = [28, 30, 29, 31, 30, 32, 30]
b = [15, 45, 20, 40, 30, 50, 10]

print(np.var(a, ddof=1), np.std(a, ddof=1))  # 1.67  1.29
print(np.var(b, ddof=1), np.std(b, ddof=1))  # 241.67  15.54
```

**Əsas nəticə:** orta göstərir ki, məlumatlar **harada** yerləşir, dispersiya isə göstərir ki, ona tipik dəyər kimi **nə qədər etibar etmək olar**. Dispersiya olmadan mənzərə həmişə natamam olur.
