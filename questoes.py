import pandas as p

# Carregar os dados dos CSVs
fornecedores = p.read_csv('csv/Fornecedores.csv')
transportadoras = p.read_csv('csv/Transportadoras.csv')
vendas_globais = p.read_csv('csv/Vendas Globais.csv')
vendedores = p.read_csv('csv/Vendedores.csv')


print("\nQuem são os meus 10 maiores clientes, em termos de vendas ($)?:")

dezMaioresClientes = vendas_globais.groupby(
    [
        "ClienteID",
        "ClienteNome"
    ]) ["Vendas"].sum().nlargest(10).to_frame()

print(dezMaioresClientes)

print("\nQuais os três maiores países, em termos de vendas ($)?:")

tresMaioresPaises = vendas_globais.groupby(
    [
        "ClientePaísID",
        "ClientePaís"
    ]) ["Vendas"].sum().nlargest(3).to_frame()

print(tresMaioresPaises)

print("\nQuais as categorias de produtos que geram maior faturamento (vendas $) no Brasil?")

brasil_vendas = vendas_globais[vendas_globais["ClientePaís"] == "Brazil"]
categProd = brasil_vendas.groupby(
    [
        "CategoriaID",
        "CategoriaNome"
    ]
)["Vendas"].sum().nlargest(5).to_frame()

print(categProd)

print("\nQual a despesa com frete envolvendo cada transportadora?")

# Merge para obter nomes das transportadoras e calcular despesa com frete
frete_por_transportadora = vendas_globais.merge(
    transportadoras, 
    on='TransportadoraID'
).groupby(
    ['TransportadoraID', 'TransportadoraNome']
)['Frete'].sum().to_frame()

print(frete_por_transportadora)

print("\nQuais são os principais clientes (vendas $) do segmento 'Calçados Masculinos' (Men ́s Footwear) na Alemanha?")

# Filtrar vendas da Alemanha e categoria Men's Footwear
alemanha_mens_footwear = vendas_globais[
    (vendas_globais["ClientePaís"] == "Germany") & 
    (vendas_globais["CategoriaNome"] == "Men´s Footwear")
]

principaisClientesCalcadosAlemanha = alemanha_mens_footwear.groupby(
    [
        "ClienteID",
        "ClienteNome"
    ]
)["Vendas"].sum().nlargest(5).to_frame()

print(principaisClientesCalcadosAlemanha)

print("\nQuais os vendedores que mais dão descontos nos Estados Unidos?")

# Filtrar vendas dos Estados Unidos
USA = vendas_globais[vendas_globais["ClientePaís"] == "USA"]

# Merge com vendedores para obter nomes e calcular descontos
vendedoresMaiorDesconto = USA.merge(
    vendedores, 
    on='VendedorID'
).groupby(
    ['VendedorID', 'VendedorNome']
)['Desconto'].sum().to_frame().sort_values(
    "Desconto",
    ascending=False
)

print(vendedoresMaiorDesconto)



print("\nQuais os fornecedores que dão a maior margem de lucro ($) no segmento de 'Vestuário Feminino' (Womens wear)?")

# Filtrar vendas do segmento Womens wear
womensWear = vendas_globais[vendas_globais["CategoriaNome"] == "Womens wear"]

# Merge com fornecedores para obter nomes e calcular margem de lucro
fornecedoresMaiorMargemLucro = womensWear.merge(
    fornecedores, 
    on='FornecedorID'
).groupby(
    ['FornecedorID', 'FornecedorNome']
)['Margem Bruta'].sum().nlargest(5).to_frame()

print(fornecedoresMaiorMargemLucro)

print("\nQuanto que foi vendido ($) no ano de 2009? Analisando as vendas anuais entre 2009 e 2012, podemos concluir que o faturamento vem crescendo, se mantendo estável ou decaindo?")

# Converter coluna Data para datetime e extrair ano
vendas_globais['Data'] = p.to_datetime(vendas_globais['Data'], format='%d/%m/%Y')
vendas_globais['Ano'] = vendas_globais['Data'].dt.year

# Vendas em 2009
vendas_2009 = vendas_globais[vendas_globais['Ano'] == 2009]['Vendas'].sum()
print(f"Vendas em 2009: ${vendas_2009:,.2f}")

# Análise das vendas anuais entre 2009-2012
vendas_anuais = vendas_globais[
    (vendas_globais['Ano'] >= 2009) & (vendas_globais['Ano'] <= 2012)
].groupby('Ano')['Vendas'].sum().to_frame()

print("\nVendas anuais (2009-2012):")
print(vendas_anuais)

# Análise de crescimento
crescimento = vendas_anuais.pct_change() * 100
print("\nCrescimento anual (%):")
print(crescimento.dropna())

# Conclusão sobre tendência
vendas_inicial = vendas_anuais.iloc[0]['Vendas']
vendas_final = vendas_anuais.iloc[-1]['Vendas']
if vendas_final > vendas_inicial * 1.05:
    tendencia = "CRESCENDO"
elif vendas_final < vendas_inicial * 0.95:
    tendencia = "DECAINDO"
else:
    tendencia = "ESTÁVEL"

print(f"\nConclusão: O faturamento está {tendencia} no período 2009-2012")


print("\n9. Quais são os principais clientes (vendas $) do segmento "+
      "\"Calçados Masculinos\" (Men´s Footwear) no ano de 2013. Para quais "
      +"cidades houve venda e quanto?")

# Verificar se 2013 existe nos dados
anos_disponiveis = vendas_globais['Ano'].dropna().unique()
print(f"Anos disponíveis: {sorted(anos_disponiveis)}")

if 2013 in anos_disponiveis:
    # Usar a coluna Ano já criada na questão 8
    principais_clientes_2013 = vendas_globais[
        (vendas_globais["Ano"] == 2013) 
        & (vendas_globais["CategoriaNome"] == "Men´s Footwear")
    ].groupby(
        [
            "ClienteID", "ClienteNome", "ClienteCidade"
        ]
    )[
        "Vendas"
    ].sum().reset_index().sort_values(
        "Vendas",
        ascending=False
    ).head(10)
    
    print("Principais clientes Men's Footwear 2013:")
    print(principais_clientes_2013)
else:
    print("Não há dados para Men's Footwear em 2013.")

print("\nNa Europa, quanto que se vende ($) para cada país?")


europa = [ "Denmark", "Finland","Austria", "Belgium", "France", "Netherlands",
    "Germany", "Ireland", "Italy", "Norway", "Portugal", "Spain", "Switzerland",
    "Sweden", "UK"]


eurVendas = vendas_globais[
    vendas_globais["ClientePaís"].isin(europa)
]

vendasEur = eurVendas.groupby("ClientePaís",)["Vendas"].sum().reset_index().sort_values("Vendas", ascending=False)

print(vendasEur)