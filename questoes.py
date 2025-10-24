#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
top10_clientes_grafico.py

- Lê os quatro CSVs que você enviou
- Calcula o total de vendas por cliente
- Exibe os 10 maiores clientes em um gráfico de barras
- Salva o gráfico como PNG (top10_clientes.png)
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns          # deixa o visual mais bonito (não obrigatório)

# ------------------------------------------------------------
# 1️⃣ CONFIGURAÇÕES INICIAIS
# ------------------------------------------------------------
BASE_DIR   = pathlib.Path(__file__).parent          # pasta onde o script está
DATA_DIR   = BASE_DIR / "csv"                       # sub‑pasta onde estão os CSVs
OUT_IMG    = BASE_DIR / "top10_clientes.png"        # arquivo de saída
FIGSIZE    = (12, 8)                               # tamanho da figura (polegadas)

# ------------------------------------------------------------
# 2️⃣ LEITURA DOS ARQUIVOS
# ------------------------------------------------------------
vendas         = pd.read_csv(DATA_DIR / "Vendas Globais.csv", sep=",")
fornecedores   = pd.read_csv(DATA_DIR / "Fornecedores.csv")
transportadoras = pd.read_csv(DATA_DIR / "Transportadoras.csv")
vendedores     = pd.read_csv(DATA_DIR / "Vendedores.csv")

# ------------------------------------------------------------
# 3️⃣ TRATAMENTO DE DATA
# ------------------------------------------------------------
vendas["Data"] = pd.to_datetime(vendas["Data"],
                                errors="coerce",
                                dayfirst=True)   # caso a data venha dd/mm/yyyy
vendas["Ano"]  = vendas["Data"].dt.year

# ------------------------------------------------------------
# 4️⃣ CÁLCULO DO TOP 10 CLIENTES
# ------------------------------------------------------------
cliente_faturamento = (
    vendas
    .groupby(["ClienteID", "ClienteNome"], as_index=False)["Vendas"]
    .sum()
    .rename(columns={"Vendas": "TotalVendas"})
)

top_10 = (
    cliente_faturamento
    .sort_values("TotalVendas", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

print("\n=== Top 10 clientes (valor total de vendas) ===")
print(top_10)

# ------------------------------------------------------------
# 5️⃣ PREPARAÇÃO DO DATAFRAME PARA O GRÁFICO
# ------------------------------------------------------------
# Cria um rótulo único para ficar legível no eixo Y
top_10["Rótulo"] = top_10.apply(
    lambda r: f"{r['ClienteNome']} (ID:{r['ClienteID']})", axis=1
)

# ------------------------------------------------------------
# 6️⃣ GERAÇÃO DO GRÁFICO DE BARRAS (horizontal)
# ------------------------------------------------------------
sns.set_style("whitegrid")               # estilo leve
plt.figure(figsize=FIGSIZE)

ax = sns.barplot(
    x="TotalVendas",
    y="Rótulo",
    data=top_10,
    palette="viridis",
    orient="h"
)

ax.set_title("Top 10 Clientes – Valor Total de Vendas", fontsize=16, pad=15)
ax.set_xlabel("Valor de Vendas (US$)", fontsize=14)
ax.set_ylabel("")                         # já temos o label nas barras

# Adiciona o valor numérico ao final de cada barra
for p in ax.patches:
    largura = p.get_width()
    ax.text(
        largura + max(top_10["TotalVendas"]) * 0.005,   # deslocamento sutil
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