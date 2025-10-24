#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
top3_paises_grafico.py

Gera um gráfico de barras com os 3 países que mais contribuíram
para o faturamento total (coluna "Vendas") a partir do arquivo
"Vendas Globais.csv".
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns          # deixa o visual mais agradável (opcional)

# ------------------------------------------------------------
# 1️⃣ CONFIGURAÇÕES INICIAIS
# ------------------------------------------------------------
BASE_DIR   = pathlib.Path(__file__).parent          # pasta onde o script está
DATA_DIR   = BASE_DIR / "csv"                       # sub‑pasta onde ficam os CSVs
OUT_IMG    = BASE_DIR / "top3_paises.png"           # arquivo de saída
FIGSIZE    = (10, 6)                               # tamanho da figura (polegadas)

# ------------------------------------------------------------
# 2️⃣ LEITURA DOS ARQUIVOS
# ------------------------------------------------------------
vendas         = pd.read_csv(DATA_DIR / "Vendas Globais.csv", sep=",")
fornecedores   = pd.read_csv(DATA_DIR / "Fornecedores.csv")
transportadoras = pd.read_csv(DATA_DIR / "Transportadoras.csv")
vendedores     = pd.read_csv(DATA_DIR / "Vendedores.csv")

# ------------------------------------------------------------
# 3️⃣ TRATAMENTO DE DATA (mantido para consistência)
# ------------------------------------------------------------
vendas["Data"] = pd.to_datetime(vendas["Data"],
                                errors="coerce",
                                dayfirst=True)   # caso a data venha dd/mm/yyyy
vendas["Ano"]  = vendas["Data"].dt.year

# ------------------------------------------------------------
# 4️⃣ CÁLCULO DO TOP 3 PAÍSES
# ------------------------------------------------------------
# Agrupa por nome do país (coluna ClientePaís) e soma o valor de vendas
pais_faturamento = (
    vendas
    .groupby("ClientePaís", as_index=False)["Vendas"]
    .sum()
    .rename(columns={"Vendas": "TotalVendas"})
)

# Ordena do maior para o menor e pega apenas os 3 primeiros
top_3 = (
    pais_faturamento
    .sort_values("TotalVendas", ascending=False)
    .head(3)
    .reset_index(drop=True)
)

print("\n=== Top 3 países (valor total de vendas) ===")
print(top_3)

# ------------------------------------------------------------
# 5️⃣ GERAÇÃO DO GRÁFICO DE BARRAS (horizontal)
# ------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=FIGSIZE)

ax = sns.barplot(
    x="TotalVendas",
    y="ClientePaís",
    data=top_3,
    palette="rocket",
    orient="h"
)

ax.set_title("Top 3 Países – Valor Total de Vendas", fontsize=16, pad=15)
ax.set_xlabel("Valor de Vendas (US$)", fontsize=14)
ax.set_ylabel("")   # o eixo Y já contém o nome do país

# Insere o valor numérico ao final de cada barra
for p in ax.patches:
    largura = p.get_width()
    ax.text(
        largura + max(top_3["TotalVendas"]) * 0.005,   # deslocamento sutil
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

# Se quiser abrir a janela interativa (útil durante desenvolvimento),
# descomente a linha abaixo:
# plt.show()