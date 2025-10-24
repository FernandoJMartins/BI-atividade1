
import pandas as pd
import re
import matplotlib.pyplot as plt

# -----------------------------
# Ler CSVs
# -----------------------------
vendas = pd.read_csv("csv/Vendas Globais.csv", sep=",")
fornecedores = pd.read_csv('csv/Fornecedores.csv')
transportadoras = pd.read_csv('csv/Transportadoras.csv')
vendedores = pd.read_csv('csv/Vendedores.csv')


# -----------------------------
# Converter datas
# -----------------------------
vendas["Data"] = pd.to_datetime(vendas["Data"], errors="coerce", dayfirst=True)
vendas["Ano"] = vendas["Data"].dt.year

# =====================================================
# PERGUNTAS + GRÁFICOS
# =====================================================

# 2️⃣ Verificar os nomes das colunas (ajuste caso haja espaços extras)
print(vendas.columns.tolist())

# 3️⃣ Agrupar por cliente e somar o valor bruto de vendas
cliente_faturamento = (
    vendas
    .groupby(['ClienteID', 'ClienteNome'], as_index=False)['Vendas']
    .sum()
    .rename(columns={'Vendas': 'TotalVendas'})
)

# 4️⃣ Ordenar do maior para o menor
top_10_clientes = (
    cliente_faturamento
    .sort_values('TotalVendas', ascending=False)
    .head(10)
    .reset_index(drop=True)
)

# 5️⃣ Exibir o resultado
print(top_10_clientes)