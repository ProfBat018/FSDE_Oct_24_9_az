"""Data science dərsinin giriş skripti.

Prezentasiyanın üç bloku üzrə gedir:
1. NumPy massivi, Series, DataFrame, oxuma və yazma, baxış metodları.
2. Təsadüfi kəmiyyət, orta göstəricilər, paylanmalar, kovariasiya və korrelyasiya.
3. matplotlib: fiqur, oxlar və əsas diaqramlar.

Hər bölməni PyCharm-da ayrıca da işlətmək olar.
Skript özü students.csv yaradır, sonra onu geri oxuyur.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "students.csv"
EXCEL_PATH = ROOT / "students.xlsx"
CSV_OUT = ROOT / "students_out.csv"
EXCEL_OUT = ROOT / "students_out.xlsx"

# Eyni toxum hər işə salınanda eyni təsadüfi seçməni verir.
rng = np.random.default_rng(0)


def section(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


def show_figures() -> None:
    """PyCharm-da bütün fiqurları açır. Agg backend-də pəncərə axtarmır."""
    backend = matplotlib_backend()
    if backend.endswith("agg"):
        print(f"\nQrafiklər ekrana verilmədi, backend: {backend}.")
        return
    plt.show()


def matplotlib_backend() -> str:
    return plt.get_backend().lower()


# =============================================================================
# 1. NumPy və pandas
# =============================================================================

section("1. Məlumat və əlamətlər")

# Yaş sütunu həm NumPy massivi, həm də sonra pandas sütunu olacaq.
age = np.array([18, 21, 19, 22])
print("age =", age)


section("1.1. Python siyahısı, C++ massivi, ndarray")

# Siyahı ölçüsünü dəyişə bilir və eyni yerdə fərqli tiplər saxlayır.
# Hər element ayrıca Python obyektinə göstəricidir.
scores_list = [70, 85, 90]
scores_list.append("absent")
print("siyahı:", scores_list)

# ndarray bir dtype saxlayır. Elementlər yaddaşda ardıcıl durur.
# C++ tərəfdəki uyğun model:
#   int scores[3] = {70, 85, 90};
#   scores[i] ünvanı: başlanğıc + i * sizeof(int)
# Python-da sizeof rolunu itemsize oynayır.
scores = np.array([70, 85, 90], dtype=np.int32)
print("scores[1] =", scores[1])
print("dtype =", scores.dtype, " itemsize =", scores.itemsize, " nbytes =", scores.nbytes)

# İkiölçülü massiv C++-dakı int table[3][2] cədvəlinə uyğundur.
# Sətir müşahidə, sütun əlamətdir: yaş və bal.
table = np.array(
    [
        [18, 70],
        [21, 85],
        [19, 90],
    ],
    dtype=np.int32,
)
print("table.shape =", table.shape)
print("birinci sətir =", table[0])
print("bütün ballar, sütun 1 =", table[:, 1])

# Səhv tip massivə düşəndə NumPy onu seçilmiş dtype-a sığışdırmağa çalışır.
# Sətir əlavə etmək üçün yeni massiv yığılır, köhnə bufer uzanmır.
extended = np.append(scores, 60)
print("append yeni massiv qaytarır:", extended)


section("1.2. Əlamət ndarray-də durur")

age = np.array([18, 21, 19, 22])
score = np.array([70, 85, 90, 60])

# Eyni hesab siyahıda Python dövrəsi tələb edir.
total = 0
for value in score.tolist():
    total += value
print("dövrə ilə cəm =", total)

# Massivdə əməliyyat bütün buferə bir dəfədə tətbiq olunur.
print("mean =", score.mean())
print("age + 1 =", age + 1)
print("80 və yuxarı ballar =", score[score >= 80])

# İki əlamət eyni uzunluqda olanda elementlər cüt-cüt toplanır.
print("yaş + bal =", age + score)


section("1.3. Series bir sütundur")

# Standart indeks 0, 1, 2, 3 sırasıdır. Bu RangeIndex adlanır.
age_default = pd.Series([18, 21, 19, 22], name="age")
print(age_default)
print("indeks:", age_default.index.tolist())

# İndeks sətirin adıdır. Mövqe isə 0-dan sayılan yerdir.
age_named = pd.Series(
    [18, 21, 19, 22],
    index=["Aysel", "Murad", "Leyla", "Nigar"],
    name="age",
)
print(age_named)
print("loc Murad =", age_named.loc["Murad"])
print("iloc 1 =", age_named.iloc[1])

# loc dilimi son adı da daxil edir: Murad, Leyla və Nigar.
print(age_named.loc["Murad":"Nigar"])

# Qiymətlər altda ndarray-dir. pandas sütunu bu massivin üzərində durur.
print("to_numpy =", age_named.to_numpy())
print("dtype =", age_named.dtype)


section("1.4. DataFrame cədvəldir")

# Sətir müşahidədir, sütun əlamətdir.
# Hər sütun öz dtype-ı olan Series-dir, indeksləri eynidir.
df = pd.DataFrame(
    {
        "name": ["Aysel", "Murad", "Leyla", "Nigar", "Kamran", "Sevinc", "Elvin", "Aynur"],
        "age": [18, 21, 19, 22, 20, 18, 23, 19],
        "score": [70, 85, 90, 60, 75, 88, 95, 67],
        "hours": [3, 5, 7, 2, 4, 6, 8, 3],
        # Bir boş xana info-da dolu sayın sütundan sütuna dəyişdiyini göstərir.
        "project": [80, 90, 85, np.nan, 70, 88, 92, 75],
    }
)
print(df)
print("shape =", df.shape)
print("dtypes:\n", df.dtypes)

# Bir sütunun seçimi Series qaytarır.
score_column = df["score"]
print("score sütunu Series-dir:", isinstance(score_column, pd.Series))
print(score_column.head(3))

# loc sətiri indeks adı ilə, iloc mövqe ilə götürür.
print("birinci sətir:\n", df.iloc[0])
print("Leyla-nın balı =", df.loc[df["name"] == "Leyla", "score"].iloc[0])

# Şərt bütün sətirlərdən alt cədvəl kəsir.
passed = df[df["score"] >= 80]
print("balı 80 və yuxarı olanlar:\n", passed)


section("1.5. Oxumaq və yazmaq")

# Faylı skriptin yanına yazırıq ki, işçi qovşaqdan asılı qalmasın.
df.to_csv(CSV_PATH, index=False)
print("yazıldı:", CSV_PATH.name)

loaded = pd.read_csv(CSV_PATH)
print("csv-dən oxunan dtypes:\n", loaded.dtypes)
print(loaded.head(3))

# Boş project xanası oxunuşdan sonra NaN qalır.
print("boş project sayı =", int(loaded["project"].isna().sum()))

loaded.to_csv(CSV_OUT, index=False)
print("surət yazıldı:", CSV_OUT.name)

# Excel üçün openpyxl lazımdır. Kitabxana yoxdursa csv nümunəsi yenə işlək qalır.
try:
    loaded.to_excel(EXCEL_PATH, index=False)
    from_excel = pd.read_excel(EXCEL_PATH, sheet_name=0)
    from_excel.to_excel(EXCEL_OUT, index=False)
    print("excel yazıldı və geri oxundu:", EXCEL_PATH.name, "->", from_excel.shape)
except ImportError:
    print("Excel nümunəsi ötürülür: openpyxl qurulmayıb (pip install openpyxl).")


section("1.6. head, tail, sample")

# Üç metod da cədvəlin kiçik hissəsinə baxır.
# Böyük faylda bütün sətirləri ekrana açmağa ehtiyac yoxdur.
print("head, susmaya görə 5:\n", df.head())
print("head(2):\n", df.head(2))
print("tail(2):\n", df.tail(2))

# random_state eyni iki sətri hər dəfə qaytarır, dərsdə nəticə sabit qalır.
print("sample(2):\n", df.sample(2, random_state=0))


section("1.7. info və describe")

# info quruluşu yoxlayır: ad, dtype, dolu xana sayı, yaddaş.
df.info()

# describe ədədi sütunlar üçün say, orta, standart kənarlaşma,
# minimum, kvartillər və maksimum verir. name sütunu bura düşmür.
print(df.describe())

# Dərsin keçidi: cədvəl artıq yoxlanıb, balın ortası statistikaya aparır.
print("score.mean() =", df["score"].mean())


# =============================================================================
# 2. Əsas statistika
# =============================================================================

section("2. Əsas statistika")

# Slaydlardakı seçmə. 85 iki dəfə təkrarlanır ki, modanın bir qiyməti olsun.
score = np.array([70, 85, 90, 85, 60])
print("seçmə =", score)
print("orta =", score.mean())


section("2.1. Təsadüfi kəmiyyət")

# Hər element təsadüfi kəmiyyətin bir müşahidəsidir.
# Sütun bu kəmiyyətin seçməsidir.
# Eyni şəraitdə yeni tələbə gələndə bal dəyişə bilər, kəmiyyətin özü qalır.
print("müşahidə sayı =", score.size)
print("bir müşahidə, mövqe 0 =", score[0])

# Yeni müşahidə seçməyə əlavə olunur, kəmiyyət dəyişmir.
new_draw = np.append(score, 77)
print("yeni müşahidədən sonra =", new_draw)


section("2.2. Ədədi orta")

# Orta: cəm / say. Funksiya həmin nisbəti hesablayır.
manual_mean = score.sum() / score.size
print("əl ilə orta =", manual_mean)
print("score.mean() =", score.mean())
print("np.mean =", np.mean(score))

# Ucqar qiymət ortanı özünə tərəf çəkir.
with_low = np.append(score, 0)
print("0 əlavə olunanda orta =", with_low.mean())


section("2.3. Moda")

# Moda ən tez təkrarlanan qiymətdir. NumPy-də bunun üçün ayrıca funksiya yoxdur.
score_series = pd.Series(score)
print("tək moda:\n", score_series.mode())

# Bir neçə qiymət eyni ən yüksək tezlikdədirsə, mode hamısını qaytarır.
two_modes = pd.Series([70, 70, 90, 90, 60])
print("iki moda:\n", two_modes.mode())


section("2.4. Mediana")

# Tək sayda sıralanmış seçmənin ortasındakı element mediandır.
# 60, 70, 85, 85, 90 içində ortadakı 85-dir.
print("sıra =", np.sort(score))
print("mediana =", np.median(score))

# Cüt sayda mediana iki ortadakı ədədin ortasıdır.
# 60, 70, 85, 90 üçün bu (70 + 85) / 2 olur.
even = np.array([60, 70, 85, 90])
print("cüt seçmənin medianı =", np.median(even))

# Ucqar 0 ortanı 78-dən aşağı salır, mediana ortaya daha az sürüşür.
print("0 ilə orta =", with_low.mean(), " mediana =", np.median(with_low))


section("2.5. Dispersiya")

# Hər qiymətin ortadan fərqi kvadrata yüksəlir və toplanır.
# Seçmə dispersiyasında cəm n - 1-ə bölünür. Bunu ddof=1 seçir.
# ddof yazılmayanda NumPy n-ə bölür.
centered = score - np.mean(score)
sum_sq = np.sum(centered**2)
sample_var = sum_sq / (score.size - 1)
population_var = sum_sq / score.size
print("fərqlər =", centered)
print("kvadratlar cəmi =", sum_sq)
print("seçmə dispersiyası =", sample_var)
print("np.var ddof=1 =", np.var(score, ddof=1))
print("np.var ddof=0 =", np.var(score, ddof=0), " əl ilə =", population_var)


section("2.6. Standart kənarlaşma")

# Standart kənarlaşma dispersiyanın kvadrat köküdür.
# Vahidi balın öz vahidi ilə eyni qalır, dispersiyanın vahidi isə balın kvadratıdır.
sample_std = np.std(score, ddof=1)
print("np.std ddof=1 =", sample_std)
print("kök(dispersiya) =", np.sqrt(sample_var))

# Kiçik kənarlaşma qiymətlərin ortaya yığıldığını göstərir.
tight = np.array([78, 79, 77, 78, 80])
wide = np.array([40, 70, 78, 90, 120])
print("dar seçmə std =", np.std(tight, ddof=1))
print("geniş seçmə std =", np.std(wide, ddof=1))


section("2.7. Bərabər paylanma")

# [0, 10) aralığında hər qiymətin şansı eynidir.
# Böyük seçmənin ortası aralığın ortasına, yəni 5-ə yaxınlaşır.
uniform_small = rng.uniform(0, 10, size=5)
uniform_large = rng.uniform(0, 10, size=10_000)
print("5 qiymət =", uniform_small)
print("min, max, orta =", uniform_large.min(), uniform_large.max(), uniform_large.mean())


section("2.8. Normal paylanma")

# loc mərkəzdir, scale standart kənarlaşmadır.
# Böyük seçmədə orta loc-a, std isə scale-ə yaxınlaşır.
normal_small = rng.normal(loc=78, scale=12, size=5)
normal_large = rng.normal(loc=78, scale=12, size=10_000)
print("5 qiymət =", normal_small)
print("orta =", normal_large.mean(), " std =", normal_large.std(ddof=1))


section("2.9. Puasson paylanması")

# Puasson hadisələrin sayını verir. lam orta hadisə sayıdır.
# Nəticə 0, 1, 2, ... tam ədədləridir.
poisson_small = rng.poisson(lam=3, size=8)
poisson_large = rng.poisson(lam=3, size=10_000)
print("8 qiymət =", poisson_small)
print("unikal qiymətlər =", np.unique(poisson_large))
print("seçmənin ortası =", poisson_large.mean())


section("2.10. Kovariasiya və korrelyasiya")

# Saat artdıqca bal da artır: müsbət əlaqə.
hours = np.array([2, 4, 5, 7, 9], dtype=float)
score_hours = np.array([50, 65, 70, 85, 95], dtype=float)

# Matrisin diaqonalı hər kəmiyyətin öz dispersiyasıdır.
# Diaqonaldan kənar xana cütlüyün kovariasiyasıdır.
cov_matrix = np.cov(hours, score_hours, ddof=1)
corr_matrix = np.corrcoef(hours, score_hours)
print("kovariasiya:\n", cov_matrix)
print("korrelyasiya:\n", corr_matrix)
print("cütlüyün korrelyasiyası =", corr_matrix[0, 1])

# Səhv sayı artdıqca bal düşür: mənfi korrelyasiya.
mistakes = np.array([8, 5, 4, 2, 1], dtype=float)
print("səhv və bal =", np.corrcoef(mistakes, score_hours)[0, 1])

# Əlaqəsiz böyük seçmədə korrelyasiya 0-a yaxın olur.
# Beş elementli təsadüfi cütlükdə isə ədəd təsadüfən iri görünə bilər.
left = rng.normal(size=5_000)
right = rng.normal(size=5_000)
print("əlaqəsiz cütlük, n=5000 =", np.corrcoef(left, right)[0, 1])


# =============================================================================
# 3. matplotlib
# =============================================================================

section("3. matplotlib")

# Fiqur bütün şəkildir. Axes bir koordinat sahəsidir.
# Qrafik sahəyə əlavə olunur. subplots hər ikisini birlikdə qaytarır.
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [70, 85, 90, 60], marker="o")
ax.set_title("score")
ax.set_xlabel("nömrə")
ax.set_ylabel("bal")

# Bir fiqurda iki ox: solda xətt, sağda həmin nöqtələrin sütunları.
fig_two, axes = plt.subplots(1, 2, figsize=(8, 3))
axes[0].plot([1, 2, 3, 4], [70, 85, 90, 60], marker="o")
axes[0].set_title("xətt")
axes[1].bar([1, 2, 3, 4], [70, 85, 90, 60])
axes[1].set_title("sütun")
fig_two.suptitle("Bir Figure, iki Axes")


section("3.1. Funksiyanın qrafiki")

# x nöqtə massividir, y həmin nöqtələrdə funksiyanın qiymətidir.
# plot nöqtələri xətlə birləşdirir. Nöqtə çox olduqca əyri hamar görünür.
x = np.linspace(-3, 3, 200)
y = x**2
fig_fn, ax_fn = plt.subplots()
ax_fn.plot(x, y, label="y = x²")
ax_fn.plot(x, 2 * x + 3, label="y = 2x + 3")
ax_fn.set_xlabel("x")
ax_fn.set_ylabel("y")
ax_fn.legend()
ax_fn.set_title("Funksiyaların qrafiki")


section("3.2. Histoqram")

# Histoqram qiymətləri intervallara bölür və hər intervalın sayını göstərir.
# bins interval sayıdır. Şaquli xətt seçmənin ortasını göstərir.
normal_sample = rng.normal(loc=78, scale=12, size=500)
fig_hist, ax_hist = plt.subplots()
ax_hist.hist(normal_sample, bins=20)
ax_hist.axvline(normal_sample.mean(), color="black", linestyle="--", label="orta")
ax_hist.set_title("Normal seçmənin histoqramı")
ax_hist.set_xlabel("qiymət")
ax_hist.set_ylabel("say")
ax_hist.legend()

# Üç paylanma yan-yana: bərabər, normal, Puasson.
uniform_sample = rng.uniform(0, 10, size=500)
poisson_sample = rng.poisson(lam=3, size=500)
fig_dist, dist_axes = plt.subplots(1, 3, figsize=(10, 3))
dist_axes[0].hist(uniform_sample, bins=15)
dist_axes[0].set_title("Bərabər")
dist_axes[1].hist(normal_sample, bins=15)
dist_axes[1].set_title("Normal")
dist_axes[2].hist(poisson_sample, bins=range(0, 12))
dist_axes[2].set_title("Puasson")
fig_dist.suptitle("Paylanmaların histoqramı")


section("3.3. Dairəvi diaqram")

# Dilimin bucağı hissənin bütündəki payıdır. autopct faizi yazır.
labels = ["A", "B", "C"]
sizes = [12, 7, 5]
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90)
ax_pie.set_title("Qiymət qruplarının payı")


section("3.4. Box-plot")

# Qutu birinci kvartildən üçüncü kvartilə qədərdir.
# Ortadakı xətt mediandır. Bığlardan kənar nöqtələr ayrıca düşür.
# describe həmin kvartilləri ədədlə verir.
box_score = np.array([70, 85, 90, 85, 60, 100, 40])
print("box seçməsinin describe-u:\n", pd.Series(box_score).describe())

fig_box, ax_box = plt.subplots()
ax_box.boxplot(box_score, tick_labels=["score"])
ax_box.set_title("Balın box-plot diaqramı")
ax_box.set_ylabel("bal")


section("3.5. Nöqtəli diaqram")

# Hər nöqtə bir tələbədir. Üfüqi ox saat, şaquli ox baldır.
# Nöqtələr yuxarı-sağa gedəndə korrelyasiya müsbətdir.
print("saat və bal korrelyasiyası =", np.corrcoef(hours, score_hours)[0, 1])
fig_sc, ax_sc = plt.subplots()
ax_sc.scatter(hours, score_hours)
ax_sc.set_xlabel("hours")
ax_sc.set_ylabel("score")
ax_sc.set_title("Saat və bal")


section("3.6. Sütun diaqramı")

# Hər sütun bir tələbənin balıdır. Hündürlük ədədi göstərir.
names = ["Aysel", "Murad", "Leyla", "Nigar"]
bar_score = [70, 85, 90, 60]
fig_bar, ax_bar = plt.subplots()
bars = ax_bar.bar(names, bar_score)
ax_bar.bar_label(bars)
ax_bar.set_ylabel("bal")
ax_bar.set_title("Tələbələrin balı")
ax_bar.set_ylim(0, 100)

print("\nQrafik pəncərələri açılır. Hamısını bağlayandan sonra skript bitir.")
show_figures()
