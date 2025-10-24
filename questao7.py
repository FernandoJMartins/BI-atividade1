#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fornecedores_maior_margem_womens.py

- Filtra as vendas do segmento "Womens wear".
- Soma a margem bruta por fornecedor.
- Exibe o ranking (default: top 10) e salva um gráfico de barras.
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
OUT_IMG    = BASE_DIR / "fornecedores_maior_margem_womens.png"
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
# 4️⃣ FILTRAR O SEGMENTO "Womens wear"
# ------------------------------------------------------------
vendas_women = vendas[vendas["CategoriaNome"].str.lower().str.contains(
    "women|womens|vestuário feminino|vestuario feminino", na=False
)]

# ------------------------------------------------------------
# 5️⃣ AGRUPAR POR FORNECEDOR E SOMAR A MARGEM BRUTA
# ------------------------------------------------------------
# 1. Calcula a margem total por ID
margem_por_fornecedor = (
    vendas_women
    .groupby("FornecedorID", as_index=False)["Margem Bruta"]
    .sum()
    .rename(columns={"Margem Bruta": "TotalMargem"})
)

# 2. Faz o merge com o nome do fornecedor
margem_por_fornecedor = margem_por_fornecedor.merge(
    fornecedores[["FornecedorID", "FornecedorNome"]],
    on="FornecedorID",
    how="left"
)

# 3. Ordena e limita
margem_por_fornecedor = margem_por_fornecedor.sort_values("TotalMargem", ascending=False)
if TOP_N:
    margem_por_fornecedor = margem_por_fornecedor.head(TOP_N)

print("\n=== Fornecedores com maior margem (segmento Womens wear) ===")
print(margem_por_fornecedor)

# ------------------------------------------------------------
# 6️⃣ GRÁFICO DE BARRAS (horizontal)
# ------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=FIGSIZE)

ax = sns.barplot(
    x="TotalMargem",
    y="FornecedorNome",
    data=margem_por_fornecedor,
    palette="mako",
    orient="h"
)

ax.set_title("Top Fornecedores – Margem Bruta (Womens wear)", fontsize=16, pad=15)
ax.set_xlabel("Margem Bruta total (US$)", fontsize=14)
ax.set_ylabel("")

# Insere o valor numérico no final da barra
for p in ax.patches:
    largura = p.get_width()
    ax.text(
        largura + max(margem_por_fornecedor["TotalMargem"]) * 0.005,
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
