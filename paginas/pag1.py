import plotly.express as px
import pandas as pd
import streamlit as st


# ✅ Acesso global ao DataFrame
if 'df' in st.session_state:
    df = st.session_state.df
else:
    st.error("O DataFrame não foi carregado corretamente.")
    st.stop()  # 🚫 Interrompe a execução se o DataFrame não foi carregado


def formata_numero(valor, prefixo=''):
    unidades = ['', 'k', 'mi', 'bi', 'tri']
    
    for i, unidade in enumerate(unidades):
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'.strip()
        valor /= 1000
    return f'{prefixo} {valor:.2f} {unidades[-1]}'.strip()

## Variáveis para os cards

processos = len(df)
valor_total = formata_numero(df['Valor Pedido Inicial Atualizado 31/03/2022'].sum(), 'R$')
processos_novos = len(df[df['Ano em que entrou no Relatório']==2022])
valores_novos = formata_numero(df[df['Ano em que entrou no Relatório']==2022]['Valor Pedido Inicial Atualizado 31/03/2022'].sum(), 'R$')

## PÁGINA 1 

# GRÁFICO DE BARRAS 1

# Contar a quantidade de ocorrências por ano
counts = df["Fecha  de Inicio del Juicio"].value_counts().reset_index()
counts.columns = ["Ano", "Quantidade"]
counts = counts.sort_values("Ano")  # Ordena os anos

# Criar o gráfico de barras com Plotly Express
barras_anos = px.bar(
    counts,
    x="Ano",
    y="Quantidade",
    title="Processos Ajuizados por Ano",
    text="Quantidade",  # Exibir os valores no topo das barras
    color_discrete_sequence=px.colors.sequential.Blues[::-1]
)

# Atualizar o layout para melhorar a aparência
barras_anos.update_layout(
    xaxis=dict(tickmode="linear",),  # Garante que todos os anos sejam exibidos no eixo x
    yaxis=dict(showgrid=False),
    xaxis_title=None,
    yaxis_title=None,
    margin=dict(l=0, r=0, t=60, b=0),
)

barras_anos.update_yaxes(showticklabels=False)

barras_anos.update_traces(hovertemplate="<b>%{label}</b><br>%{value}<extra></extra> processos")

# PIE CHART DE JULGAMENTO DOS PROCESSOS

df['Sentença / Acórdão / Acordo'] = df['Sentença / Acórdão / Acordo'].map({'SIm':'Sim', 'Não':'Não', "Sim":'Sim'})

sentenca = df['Sentença / Acórdão / Acordo'].value_counts().reset_index()

julgamento = px.pie(sentenca, values=sentenca['count'],
       names=sentenca['Sentença / Acórdão / Acordo'],
       hole=0.7,
       color_discrete_sequence=px.colors.sequential.Blues[::-1],
       title="Sentença, Acórdão ou Acordo"
       )

julgamento.update_layout(
    margin=dict(l=25, r=25, t=25, b=0,),
    showlegend=False)

julgamento.update_traces(hovertemplate="<b>%{label}</b><br>%{value}<extra></extra>")

#PIE CHART DE LIQUIDAÇÃO DOS PROCESSOS

df['Liquidação Inicial'] = df['Liquidação Inicial']. map({'Sim':'Sim', 'Não':'Não', 'Sim (Braz)':'Sim'})

liquidacao = df['Liquidação Inicial'].value_counts().reset_index()

liquidacao = px.pie(liquidacao,
       values=liquidacao['count'],
       names=liquidacao['Liquidação Inicial'],
       hole=0.7,
       color_discrete_sequence=px.colors.sequential.Blues[::-1],
       title="Liquidação Inicial"
       )

liquidacao.update_layout(
    margin=dict(l=25, r=25, t=25, b=0),
    showlegend=False)

liquidacao.update_traces(hovertemplate="<b>%{label}</b><br>%{value}<extra></extra>")

# GRÁFICO DE LINHAS DE ENTRADA DE PROCESSOS NO RELATÓRIO

meses = df[['Ano em que entrou no Relatório','Trimestre em que entrou no Relatório','Mês de Entrada para constar no Relatório']]
meses = meses.rename(columns={'Ano em que entrou no Relatório':'ano', 'Trimestre em que entrou no Relatório':'trimestre', 'Mês de Entrada para constar no Relatório':'mes'})
mes_map = {
    'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
    'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
    'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
}

tri_map = {
    '1º Trimestre':1, '2º Trimestre':2, '3º Trimestre':3, '4º Trimestre':4
}

meses['mes_num'] = meses['mes'].map(mes_map)
meses['trimestre'] = meses['trimestre'].map(tri_map)
meses['data'] = pd.to_datetime(meses['ano'].astype(str) + '-' + meses['mes_num'].astype(str) + '-01')

entradas_mensais = meses.groupby('data').size().reset_index(name='entradas')

linhas = px.bar(
    entradas_mensais,
    x='data',
    y='entradas',
    title='Entrada de Processos no Relatório por Mês',
    labels={'data': 'Data', 'entradas': 'Quantidade de Entradas'},
    color_discrete_sequence=px.colors.sequential.Blues[-2:]
)

linhas.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',  # Fundo do gráfico
    },
    xaxis_title=None,
    yaxis_title=None,
    margin=dict(l=0, r=0, t=25, b=0)
)

linhas.update_traces(hovertemplate="<b>%{label}</b><br>%{value}<extra></extra> processos")