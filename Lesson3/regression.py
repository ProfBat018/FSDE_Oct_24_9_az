from sklearn.preprocessing import PolynomialFeatures

# Mənzillər: sahə böyüdükcə qiymət əyri (premium effekt) artır
df_poly = pd.DataFrame({
    "sahe":   [30, 40, 50, 60, 70, 85, 100, 120, 140],
    "qiymet": [55, 70, 90, 115, 145, 190, 250, 340, 460]  # min AZN
})

#region Polynominal learning
# dərəcə = 2 → sahə və sahə² sütunları yaradır
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(df_poly[["sahe"]])

model_poly = LinearRegression()
model_poly.fit(X_poly, df_poly["qiymet"])

#endregion
print("Feature adları:", poly.get_feature_names_out(["sahe"]))
print(f"w_sahe  = {model_poly.coef_[0]:.4f}")
print(f"w_sahe2 = {model_poly.coef_[1]:.4f}")
print(f"b       = {model_poly.intercept_:.2f}")
print(f"\nFormula: qiymət = {model_poly.coef_[0]:.4f}×sahə + {model_poly.coef_[1]:.4f}×sahə² + {model_poly.intercept_:.2f}")

#region base Linear learning 
# Qrafik: düz xətt vs əyri
model_duz = LinearRegression().fit(df_poly[["sahe"]], df_poly["qiymet"])
sahe_grid = pd.DataFrame({"sahe": np.linspace(30, 140, 100)})

#endregion
plt.scatter(df_poly["sahe"], df_poly["qiymet"], s=70, color="black", label="Real mənzillər", zorder=3)
plt.plot(sahe_grid["sahe"], model_duz.predict(sahe_grid), "--", color="gray", label="Simple Linear")
plt.plot(sahe_grid["sahe"], model_poly.predict(poly.transform(sahe_grid)), color="blue", linewidth=2.5, label="Polynomial (dərəcə 2)")
plt.xlabel("Sahə (kv.m)")
plt.ylabel("Qiymət (min AZN)")
plt.title("Mənzil: düz xətt vs Polynomial əyri")
plt.legend()
plt.grid(alpha=0.3)
plt.show()