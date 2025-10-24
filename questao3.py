#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
categorias_brasil.py

- Filtra as vendas realizadas no Brasil;
- Agrupa por categoria de produto;
- Calcula o faturamento total (coluna "Vendas");
- Exibe as categorias em ordem decrescente;
- Salva um gráfico de barras (PNG) com o ranking.
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
OUT_IMG    = BASE_DIR / "categorias_brasil.png"    # arquivo de saída (gráfico)
FIGSIZE    = (12, 8)                               # tamanho da figura (polegadas)

# ------------------------------------------------------------
# 2️⃣ LEITURA DO CSV DE VENDAS
# ------------------------------------------------------------
vendas = pd.read_csv(DATA_DIR / "Vendas Globais.csv", sep=",")

# ------------------------------------------------------------
# 3️⃣ TRATAMENTO DE DATA (mantido por consistência)
# ------------------------------------------------------------
vendas["Data"] = pd.to_datetime(vendas["Data"],
                                errors="coerce",
                                dayfirst=True)   # caso a data venha dd/mm/yyyy
vendas["Ano"]  = vendas["Data"].dt.year

# ------------------------------------------------------------
# 4️⃣ FILTRAR SOMENTE REGISTROS DO BRASIL
# ------------------------------------------------------------
vendas_br = vendas[vendas["ClientePaís"] == "Brazil"]

# ------------------------------------------------------------
# 5️⃣ AGRUPAR POR CATEGORIA E SOMAR O FATURAMENTO
# ------------------------------------------------------------
categoria_faturamento = (
    vendas_br
    .groupby("CategoriaNome", as_index=False)["Vendas"]
    .sum()
    .rename(columns={"Vendas": "TotalVendas"})
)

# Ordena do maior para o menor
categoria_faturamento = categoria_faturamento.sort_values(
    "TotalVendas", ascending=False
)

print("\n=== Faturamento por categoria (Brasil) ===")
print(categoria_faturamento)

# ------------------------------------------------------------
# 6️⃣ GRÁFICO DE BARRAS (horizontal) – TOP N (todos ou limitados)
# ------------------------------------------------------------
# Caso queira mostrar apenas as N primeiras categorias, ajuste aqui:
TOP_N = None                     # None → mostra todas; ou coloque um número, ex.: 10
if TOP_N:
    plot_df = categoria_faturamento.head(TOP_N)
else:
    plot_df = categoria_faturamento

sns.set_style("whitegrid")
plt.figure(figsize=FIGSIZE)

ax = sns.barplot(
    x="TotalVendas",
    y="CategoriaNome",
    data=plot_df,
    palette="magma",
    orient="h"
)

ax.set_title("Faturamento por Categoria – Brasil", fontsize=16, pad=15)
ax.set_xlabel("Valor de Vendas (US$)", fontsize=14)
ax.set_ylabel("")   # o eixo Y já traz o nome da categoria

# Insere o valor numérico ao final de cada barra
for p in ax.patches:
    largura = p.get_width()
    ax.text(
        largura + max(plot_df["TotalVendas"]) * 0.005,
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