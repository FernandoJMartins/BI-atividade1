# 📘 README – Análise de Clientes (Top 10 Maiores Clientes por Vendas)

## 💬 Conversa Original (LLM)

### **Pergunta:**
> Preciso que você leia os arquivos CSV. Por enquanto, faça apenas isso, armazene os dados na sua memória.

### **Resposta:**
Posso ler os arquivos CSV que você enviar e armazenar os dados na memória da sessão para usarmos depois.  
Por favor, faça o upload dos arquivos CSV que deseja analisar.

---

### **Arquivos Enviados:**
| Arquivo | Descrição breve |
|----------|----------------|
| **Transportadoras.csv** | Lista de transportadoras (TransportadoraID, TransportadoraNome) |
| **Fornecedores.csv** | Lista de fornecedores (FornecedorID, FornecedorNome) |
| **Vendedores.csv** | Lista de vendedores (VendedorID, VendedorNome) |
| **Vendas Globais.csv** | Transações de vendas detalhadas (pedido, produto, cliente, data, valores, descontos, frete, etc.) |

---

### **Pergunta:**
> Quem são os meus 10 maiores clientes, em termos de vendas ($)?

---

## ⚙️ Solução proposta (via Python + Pandas)

A maneira mais direta de encontrar os 10 maiores clientes por valor de vendas é:

1. Ler o arquivo **Vendas Globais.csv**.  
2. Agrupar por **ClienteID** e **ClienteNome**.  
3. Somar o campo **Vendas**.  
4. Ordenar em ordem decrescente.  
5. Selecionar os 10 primeiros.

---

### 🧩 Exemplo de código em Python

```python
import pandas as pd

# 1️⃣ Carregar os arquivos CSV
transportadoras = pd.read_csv('Transportadoras.csv')
fornecedores    = pd.read_csv('Fornecedores.csv')
vendedores      = pd.read_csv('Vendedores.csv')
vendas          = pd.read_csv('Vendas Globais.csv', sep=',')

# 2️⃣ Verificar as colunas (ajuste se houver espaços)
print(vendas.columns.tolist())

# 3️⃣ Agrupar por cliente e somar o valor total das vendas
cliente_faturamento = (
    vendas
    .groupby(['ClienteID', 'ClienteNome'], as_index=False)['Vendas']
    .sum()
    .rename(columns={'Vendas': 'TotalVendas'})
)

# 4️⃣ Ordenar do maior para o menor e pegar o Top 10
top_10_clientes = (
    cliente_faturamento
    .sort_values('TotalVendas', ascending=False)
    .head(10)
    .reset_index(drop=True)
)

# 5️⃣ Exibir resultado
print(top_10_clientes)
```

---

### 🧠 O que o código faz

| Etapa | Descrição |
|-------|------------|
| **Leitura** | Carrega os CSVs em DataFrames. |
| **GroupBy** | Agrupa por `ClienteID` e `ClienteNome`. |
| **Sum()** | Soma a coluna `Vendas`. |
| **Sort** | Ordena do maior para o menor total. |
| **Head(10)** | Seleciona apenas os 10 primeiros. |

---

### 📊 Exemplo de saída esperada (dados ilustrativos)

| ClienteID | ClienteNome | TotalVendas |
|------------|--------------|-------------|
| 41 | Elle Fashion & Design | 1 234 567 |
| 84 | Art et Fashion | 1 102 345 |
| 33 | La Abrigo Mortal | 987 654 |
| ... | ... | ... |
| 19 | Th Fashing | 543 210 |

---

## 🔍 Dicas de uso

- **Dashboard BI** – Copie o DataFrame `top_10_clientes` para o Power BI, Tableau, ou Google Data Studio.  
- **Time Comercial** – Liste os top 10 clientes e use para priorizar campanhas ou ofertas.  
- **Análises adicionais** – Adicione margem bruta, lucro líquido ou volume de pedidos.

### Exemplo: incluir margem bruta

```python
cliente_margem = (
    vendas
    .groupby(['ClienteID','ClienteNome'], as_index=False)['Margem Bruta']
    .sum()
    .rename(columns={'Margem Bruta':'TotalMargem'})
)

# Combina com faturamento
top_10 = top_10_clientes.merge(cliente_margem, on=['ClienteID','ClienteNome'])
print(top_10)
```

---

## 🧾 Alternativa via Excel

Se preferir não usar Python:

1. Abra **Vendas Globais.csv** no Excel.  
2. Vá em **Inserir → Tabela Dinâmica**.  
3. Linhas → `ClienteNome`  
4. Valores → `Vendas` (usar “Somar”).  
5. Ordene a soma de forma decrescente e mantenha os 10 primeiros.

---

## 🎯 Possíveis extensões

- Comparar **Top 10 Clientes** entre diferentes anos.  
- Descobrir **categorias** mais compradas pelos top clientes.  
- Calcular **rentabilidade** considerando custos, descontos e frete.  
- Integrar com fornecedores e vendedores para entender correlações.

---

## ⚠️ Observação sobre o resultado no Lumo

> O sistema “Lumo” apenas exibiu um gráfico **mockado** (modelo genérico), sem processar o código real.  
> Para um usuário comum, isso **não resolve o problema**.  
> Para um programador, o código fornecido acima é **completo e funcional**, pronto para uso local com Python + Pandas.
