#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
eu_sales_by_country.py

- Soma o valor bruto de vendas (coluna "Vendas") para cada país europeu.
- Exporta a tabela para CSV (eu_sales_by_country.csv).
- Opcionalmente gera um gráfico de barras (eu_sales_by_country.png).
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------
# 1️⃣ CONFIGURAÇÕES
# ------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).parent
DATA_DIR = BASE_DIR / "csv"
OUT_CSV = BASE_DIR / "eu_sales_by_country.csv"
OUT_IMG = BASE_DIR / "eu_sales_by_country.png"
FIGSIZE = (12, 8)

# Lista de países reconhecidos como europeus (inclui UE + EFTA + alguns vizinhos)
EUROPEAN_COUNTRIES = {
    "France", "Germany", "United Kingdom", "Italy", "Spain",
    "Netherlands", "Belgium", "Switzerland", "Portugal", "Ireland",
    "Austria", "Poland", "Denmark", "Sweden", "Norway", "Finland",
    "Greece", "Czech Republic", "Hungary", "Romania", "Bulgaria",
    "Croatia", "Slovakia", "Lithuania", "Latvia", "Estonia",
    "Luxembourg", "Malta", "Cyprus"
}

# ------------------------------------------------------------
# 2️⃣ LEITURA DOS DADOS
# ------------------------------------------------------------
vendas = pd.read_csv(DATA_DIR / "Vendas Globais.csv", sep=",")

# ------------------------------------------------------------
# 3️⃣ FILTRAR SOMENTE PAÍSES EUROPEUS
# ------------------------------------------------------------
vendas_eu = vendas[vendas["ClientePaís"].isin(EUROPEAN_COUNTRIES)]

# ------------------------------------------------------------
# 4️⃣ AGRUPAR POR PAÍS E SOMAR O VALOR DE VENDAS
# ------------------------------------------------------------
sales_by_country = (
    vendas_eu
    .groupby("ClientePaís", as_index=False)["Vendas"]
    .sum()
    .rename(columns={"Vendas": "TotalVendas"})
    .sort_values("TotalVendas", ascending=False)
)

# Salva a tabela em CSV (útil para auditoria ou uso posterior)
sales_by_country.to_csv(OUT_CSV, index=False, float_format="%.2f")
print(f"Tabela salva em: {OUT_CSV}")

# ------------------------------------------------------------
# 5️⃣ GRÁFICO DE BARRAS (horizontal)
# ------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=FIGSIZE)

ax = sns.barplot(
    x="TotalVendas",
    y="ClientePaís",
    data=sales_by_country,
    palette="viridis",
    orient="h"
)

ax.set_title("Vendas Totais por País – Europa", fontsize=16, pad=15)
ax.set_xlabel("Valor de Vendas (US$)", fontsize=14)
ax.set_ylabel("")   # o eixo Y já contém o nome do país

# Insere o valor numérico ao final de cada barra
for p in ax.patches:
    largura = p.get_width()
    ax.text(
        largura + max(sales_by_country["TotalVendas"]) * 0.005,
        p.get_y() + p.get_height() / 2,
        f"${largura:,.2f}",
        ha="left",
        va="center",
        fontsize=11,
        color="#333333"
    )

plt.tight_layout()
plt.savefig(OUT_IMG, dpi=300, bbox_inches="tight")
print(f"Gráfico salvo em: {OUT_IMG}")

# Se quiser visualizar imediatamente (janela interativa), descomente:
# plt.show()