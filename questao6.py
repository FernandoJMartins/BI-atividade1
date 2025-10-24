#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
descontos_vendedores_usa.py

- Filtra as vendas realizadas nos Estados Unidos (ClientePaís == "USA").
- Agrupa por vendedor (VendedorID / VendedorNome) e soma o valor de desconto.
- Exibe a tabela (default: top 10) e gera um gráfico de barras horizontal.
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------
# 1️⃣ CONFIGURAÇÕES INICIAIS
# ------------------------------------------------------------
BASE_DIR   = pathlib.Path(__file__).parent
DATA_DIR   = BASE_DIR / "csv"
OUT_IMG    = BASE_DIR / "descontos_vendedores_usa.png"
FIGSIZE    = (12, 8)
TOP_N      = 10

# ------------------------------------------------------------
# 2️⃣ LEITURA DOS ARQUIVOS
# ------------------------------------------------------------
vendas          = pd.read_csv(DATA_DIR / "Vendas Globais.csv", sep=",")
fornecedores    = pd.read_csv(DATA_DIR / "Fornecedores.csv")
transportadoras = pd.read_csv(DATA_DIR / "Transportadoras.csv")
vendedores      = pd.read_csv(DATA_DIR / "Vendedores.csv")

# ------------------------------------------------------------
# 3️⃣ TRATAMENTO DE DATA
# ------------------------------------------------------------
vendas["Data"] = pd.to_datetime(vendas["Data"], errors="coerce", dayfirst=True)
vendas["Ano"]  = vendas["Data"].dt.year

# ------------------------------------------------------------
# 4️⃣ FILTRAR SOMENTE VENDAS NOS EUA
# ------------------------------------------------------------
vendas_usa = vendas[vendas["ClientePaís"].str.lower().str.contains("usa|united states|eua", na=False)]

# ------------------------------------------------------------
# 5️⃣ AGRUPAR POR VENDEDOR E SOMAR O DESCONTO
# ------------------------------------------------------------
# Agrupa apenas por ID (ainda não tem o nome)
desconto_por_vendedor = (
    vendas_usa
    .groupby("VendedorID", as_index=False)["Desconto"]
    .sum()
    .rename(columns={"Desconto": "TotalDesconto"})
)

# Junta com os nomes dos vendedores
desconto_por_vendedor = desconto_por_vendedor.merge(
    vendedores[["VendedorID", "VendedorNome"]],
    on="VendedorID",
    how="left"
)

# Ordena do maior para o menor
desconto_por_vendedor = desconto_por_vendedor.sort_values("TotalDesconto", ascending=False)

# Limita ao TOP_N
if TOP_N:
    desconto_por_vendedor = desconto_por_vendedor.head(TOP_N)

print("\n=== Vendedores que mais dão descontos (EUA) ===")
print(desconto_por_vendedor)

# ------------------------------------------------------------
# 6️⃣ GRÁFICO DE BARRAS (horizontal)
# ------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=FIGSIZE)

ax = sns.barplot(
    x="TotalDesconto",
    y="VendedorNome",
    data=desconto_por_vendedor,
    palette="rocket",
    orient="h"
)

ax.set_title("Vendedores que Mais Concedem Desconto – EUA", fontsize=16, pad=15)
ax.set_xlabel("Valor total de desconto (US$)", fontsize=14)
ax.set_ylabel("")

# Insere o valor numérico ao final de cada barra
for p in ax.patches:
    largura = p.get_width()
    ax.text(
        largura + max(desconto_por_vendedor["TotalDesconto"]) * 0.005,
        p.get_y() + p.get_height() / 2,
        f"${largura:,.2f}",
        ha="left",
        va="center",
        fontsize=12,
        color="#333333"
    )

plt.tight_layout()
plt.savefig(OUT_IMG, dpi=300, bbox_inches="tight")
print(f"\n✅ Gráfico salvo em: {OUT_IMG}")

# plt.show()  # descomente se quiser abrir o gráfico
