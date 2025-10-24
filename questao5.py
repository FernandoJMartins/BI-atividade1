#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
top_clientes_mens_footwear_germany.py

- Filtra as vendas de calçados masculinos (Men´s Footwear) feitas por clientes
  residentes na Alemanha (ClientePaís == "Germany").
- Agrupa por cliente e soma o valor de vendas (coluna "Vendas").
- Exibe o ranking (default: top 10) e salva um gráfico de barras.
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
OUT_IMG    = BASE_DIR / "top_clientes_mens_footwear_germany.png"
FIGSIZE    = (12, 8)                               # tamanho da figura (polegadas)
TOP_N      = 10                                    # quantos clientes mostrar (None → todos)

# ------------------------------------------------------------
# 2️⃣ LEITURA DOS ARQUIVOS
# ------------------------------------------------------------
vendas         = pd.read_csv(DATA_DIR / "Vendas Globais.csv", sep=",")
fornecedores   = pd.read_csv(DATA_DIR / "Fornecedores.csv")
transportadoras = pd.read_csv(DATA_DIR / "Transportadoras.csv")
vendedores     = pd.read_csv(DATA_DIR / "Vendedores.csv")

# ------------------------------------------------------------
# 3️⃣ TRATAMENTO DE DATA (mantido por consistência)
# ------------------------------------------------------------
vendas["Data"] = pd.to_datetime(vendas["Data"],
                                errors="coerce",
                                dayfirst=True)   # caso a data venha dd/mm/yyyy
vendas["Ano"]  = vendas["Data"].dt.year

# ------------------------------------------------------------
# 4️⃣ FILTRAR O SEGMENTO E O PAÍS DE INTERESSE
# ------------------------------------------------------------
filtro = (
    (vendas["CategoriaNome"] == "Men´s Footwear") &
    (vendas["ClientePaís"] == "Germany")
)

vendas_filtradas = vendas[filtro]

# ------------------------------------------------------------
# 5️⃣ AGRUPAR POR CLIENTE E SOMAR O VALOR DE VENDAS
# ------------------------------------------------------------
cliente_faturamento = (
    vendas_filtradas
    .groupby(["ClienteID", "ClienteNome"], as_index=False)["Vendas"]
    .sum()
    .rename(columns={"Vendas": "TotalVendas"})
)

# Ordena do maior para o menor
cliente_faturamento = cliente_faturamento.sort_values(
    "TotalVendas", ascending=False
)

# Caso queira limitar a quantidade exibida:
if TOP_N:
    cliente_faturamento = cliente_faturamento.head(TOP_N)

print("\n=== Principais clientes (Men´s Footwear – Germany) ===")
print(cliente_faturamento)

# ------------------------------------------------------------
# 6️⃣ GRÁFICO DE BARRAS (horizontal)
# ------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=FIGSIZE)

ax = sns.barplot(
    x="TotalVendas",
    y="ClienteNome",
    data=cliente_faturamento,
    palette="viridis",
    orient="h"
)

ax.set_title(
    "Top Clientes – Calçados Masculinos (Germany)",
    fontsize=16,
    pad=15
)
ax.set_xlabel("Valor de Vendas (US$)", fontsize=14)
ax.set_ylabel("")   # o eixo Y já contém o nome do cliente

# Insere o valor numérico ao final de cada barra
for p in ax.patches:
    largura = p.get_width()
    ax.text(
        largura + max(cliente_faturamento["TotalVendas"]) * 0.005,
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