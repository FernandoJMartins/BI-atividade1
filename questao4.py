#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
frete_por_transportadora.py

- Calcula a despesa total de frete (coluna "Frete") para cada transportadora.
- Exibe a tabela no terminal.
- Gera um gráfico de barras horizontal e salva como PNG.
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
OUT_IMG    = BASE_DIR / "frete_por_transportadora.png"  # arquivo de saída
FIGSIZE    = (12, 8)                               # tamanho da figura (polegadas)

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
# 4️⃣ CÁLCULO DA DESPESA DE FRETE POR TRANSPORTADORA
# ------------------------------------------------------------
# Agrupa por ID e nome da transportadora e soma o valor de frete
frete_por_transp = (
    vendas.groupby("TransportadoraID")["Frete"].sum().reset_index().sort_values("Frete", ascending=False)
    .merge(transportadoras, on="TransportadoraID", how="left")
)

# Ordena do maior para o menor
frete_por_transp = frete_por_transp.sort_values(
    "Frete", ascending=False
)

print("\n=== Despesa total de frete por transportadora ===")
print(frete_por_transp)

# ------------------------------------------------------------
# 5️⃣ GRÁFICO DE BARRAS (horizontal)
# ------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=FIGSIZE)

ax = sns.barplot(
    x="Frete",
    y="TransportadoraNome",
    data=frete_por_transp,
    palette="crest",
    orient="h"
)

ax.set_title("Despesa de Frete por Transportadora", fontsize=16, pad=15)
ax.set_xlabel("Valor total de Frete (US$)", fontsize=14)
ax.set_ylabel("")   # o eixo Y já contém o nome da transportadora

# Insere o valor numérico ao final de cada barra
for p in ax.patches:
    largura = p.get_width()
    ax.text(
        largura + max(frete_por_transp["Frete"]) * 0.005,
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