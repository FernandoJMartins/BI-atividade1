#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
analise_mens_footwear_2013.py

- Filtra as vendas do segmento "Men´s Footwear".
- Limita ao ano 2013.
- Exibe:
    • Ranking de clientes (valor total de vendas)
    • Total vendido por cidade
- Caso não exista nenhum registro, informa que o conjunto está vazio.
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns          # opcional, melhora o visual

# ------------------------------------------------------------
# 1️⃣ CONFIGURAÇÕES
# ------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).parent          # pasta onde o script está
DATA_DIR = BASE_DIR / "csv"                       # sub‑pasta com os CSVs
ANO_DE_INTERESSE = 2013                           # ano a analisar
SEGMENTO = "Men´s Footwear"                       # segmento desejado
TOP_N_CLIENTES = 10                               # quantos clientes mostrar (None → todos)

# ------------------------------------------------------------
# 2️⃣ LEITURA DOS ARQUIVOS
# ------------------------------------------------------------
vendas = pd.read_csv(DATA_DIR / "Vendas Globais.csv", sep=",")
# (os demais CSVs não são necessários para esta análise, mas podem ser lidos se quiser)

# ------------------------------------------------------------
# 3️⃣ CONVERSÃO DE DATA e extração do ano
# ------------------------------------------------------------
vendas["Data"] = pd.to_datetime(vendas["Data"],
                                errors="coerce",
                                dayfirst=True)   # aceita formatos dd/mm/yyyy ou yyyy-mm-dd
vendas["Ano"] = vendas["Data"].dt.year

# ------------------------------------------------------------
# 4️⃣ FILTRAR POR ANO e POR SEGMENTO
# ------------------------------------------------------------
mask = (vendas["Ano"] == ANO_DE_INTERESSE) & (vendas["CategoriaNome"] == SEGMENTO)
dados_filtrados = vendas.loc[mask]

if dados_filtrados.empty:
    print(f"\n⚠️  Não foram encontrados registros de '{SEGMENTO}' no ano {ANO_DE_INTERESSE}.")
    exit(0)

# ------------------------------------------------------------
# 5️⃣ RANKING DE CLIENTES (valor total de vendas)
# ------------------------------------------------------------
clientes = (
    dados_filtrados
    .groupby(["ClienteID", "ClienteNome"], as_index=False)["Vendas"]
    .sum()
    .rename(columns={"Vendas": "TotalVendas"})
    .sort_values("TotalVendas", ascending=False)
)

if TOP_N_CLIENTES:
    clientes = clientes.head(TOP_N_CLIENTES)

print("\n🏆 Top clientes (valor total de vendas) →")
print(clientes)

# ------------------------------------------------------------
# 6️⃣ TOTAL POR CIDADE
# ------------------------------------------------------------
cidades = (
    dados_filtrados
    .groupby(["ClienteCidade"], as_index=False)["Vendas"]
    .sum()
    .rename(columns={"Vendas": "TotalVendas"})
    .sort_values("TotalVendas", ascending=False)
)

print("\n📍 Vendas por cidade →")
print(cidades)

# ------------------------------------------------------------
# 7️⃣ (Opcional) GRÁFICOS – CLIENTES + CIDADES
# ------------------------------------------------------------
sns.set_style("whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# ----- Gráfico 1 – Top clientes -----
sns.barplot(
    x="TotalVendas",
    y="ClienteNome",
    data=clientes,
    palette="viridis",
    orient="h",
    ax=axes[0]
)
axes[0].set_title(f"Top {len(clientes)} clientes – {SEGMENTO} ({ANO_DE_INTERESSE})")
axes[0].set_xlabel("Valor de Vendas (US$)")
axes[0].set_ylabel("")

# ----- Gráfico 2 – Vendas por cidade -----
sns.barplot(
    x="TotalVendas",
    y="ClienteCidade",
    data=cidades,
    palette="mako",
    orient="h",
    ax=axes[1]
)
axes[1].set_title(f"Vendas por cidade – {SEGMENTO} ({ANO_DE_INTERESSE})")
axes[1].set_xlabel("Valor de Vendas (US$)")
axes[1].set_ylabel("")

plt.tight_layout()
plt.show()