import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
n = 200

# Gizli amil: temperatur (°C)
temperatur = rng.normal(25, 6, n)

# Hər ikisi temperaturdan asılıdır, bir-birindən yox
dondurma = 20 * temperatur + rng.normal(0, 60, n)   # gündəlik satış
bogulma = 0.3 * temperatur + rng.normal(0, 2, n)    # boğulma halları

# 1) Kovariasiya və korrelyasiya
kov = np.cov(dondurma, bogulma)[0, 1]
kor = np.corrcoef(dondurma, bogulma)[0, 1]
print(f"Kovariasiya  = {kov:.2f}  (müsbət!)")
print(f"Korrelyasiya = {kor:.2f}  (güclü müsbət!)")

# 2) Sürpriz: temperaturun təsirini hər ikisindən çıxaraq
def qaliq(y, x):
    a, b = np.polyfit(x, y, 1)
    return y - (a * x + b)

d_qaliq = qaliq(dondurma, temperatur)
b_qaliq = qaliq(bogulma, temperatur)
kor_qaliq = np.corrcoef(d_qaliq, b_qaliq)[0, 1]
print(f"Temperaturu çıxandan sonra korrelyasiya = {kor_qaliq:.2f}  (≈ 0)")

# Diaqramlar
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].scatter(dondurma, bogulma, alpha=0.5)
axes[0].set_title(f"Dondurma vs boğulma\nkorrelyasiya = {kor:.2f}")
axes[0].set_xlabel("Dondurma satışı")
axes[0].set_ylabel("Boğulma halları")

sc = axes[1].scatter(dondurma, bogulma, c=temperatur, cmap="coolwarm", alpha=0.7)
axes[1].set_title("Eyni nöqtələr, rəng = temperatur")
axes[1].set_xlabel("Dondurma satışı")
plt.colorbar(sc, ax=axes[1], label="°C")

axes[2].scatter(d_qaliq, b_qaliq, alpha=0.5, color="green")
axes[2].set_title(f"Temperaturu çıxandan sonra\nkorrelyasiya = {kor_qaliq:.2f}")
axes[2].set_xlabel("Dondurma (qalıq)")
axes[2].set_ylabel("Boğulma (qalıq)")

plt.tight_layout()
plt.show()