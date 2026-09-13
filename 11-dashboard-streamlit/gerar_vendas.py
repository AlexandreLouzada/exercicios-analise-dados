import pandas as pd
import numpy as np

np.random.seed(7)
n = 720
datas = pd.date_range(start="2025-01-01", periods=n, freq="h").normalize()

produtos = {
    "Eletrônicos": ["Smartphone", "Notebook", "Fone", "Smart TV"],
    "Vestuário": ["Camiseta", "Jeans", "Tênis", "Jaqueta"],
    "Casa": ["Sofá", "Mesa", "Luminária", "Cortina"],
    "Livros": ["Ficção", "Negócios", "Infantil", "Técnico"],
}
categorias = list(produtos.keys())

linhas = []
for i in range(600):
    cat = np.random.choice(categorias)
    prod = np.random.choice(produtos[cat])
    qtd = np.random.randint(1, 8)
    precos_base = {"Smartphone": 1500, "Notebook": 3200, "Fone": 180, "Smart TV": 2200,
                   "Camiseta": 50, "Jeans": 120, "Tênis": 250, "Jaqueta": 300,
                   "Sofá": 1800, "Mesa": 700, "Luminária": 150, "Cortina": 200,
                   "Ficção": 45, "Negócios": 60, "Infantil": 35, "Técnico": 90}
    valor = precos_base[prod] * qtd * np.random.uniform(0.9, 1.15)
    linhas.append({
        "data": pd.Timestamp("2025-01-01") + pd.to_timedelta(np.random.randint(0, 330), unit="D"),
        "categoria": cat,
        "produto": prod,
        "quantidade": qtd,
        "receita": round(valor, 2),
    })

df = pd.DataFrame(linhas).sort_values("data").reset_index(drop=True)
df.to_csv("vendas.csv", index=False, encoding="utf-8")
print(df.shape)
print(df.head(3).to_string())
print(df["categoria"].value_counts().to_dict())
print(df["data"].min(), df["data"].max())