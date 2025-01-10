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

## PÁGINA 3

## Variáveis para Tabelas (cidades_df)

valores = df.groupby('Lotação')['Valor Pedido Inicial Atualizado 31/03/2022'].sum().sort_values(ascending=False)
valores = pd.DataFrame(valores).reset_index()
valores = valores.rename(columns={'Valor Pedido Inicial Atualizado 31/03/2022':'Valor'})
cidades = pd.DataFrame(df['Lotação'].value_counts()).reset_index()
cidades_df = cidades.merge(valores).rename(columns={'count':'Processos'})
cidades_df = (
    cidades_df
    .style
    .background_gradient(subset=['Valor'], cmap='Blues')  # Gradiente na coluna Valor
    .background_gradient(subset=['Processos'], cmap='Blues')  # Gradiente na coluna Processos
)
cidades_df.format({'Valor': lambda val: formata_numero(val, "R$")})

# GRÁFICOS TREEMAP (LOTAÇÃO E ÁREA)

# Corrigindo o valor incorreto na coluna 'Lotação'
df['Lotação'] = df['Lotação'].replace('Riberão Preto', 'Ribeirão Preto')

lot_area_contagem = df.groupby(['Lotação', 'Área']).size().reset_index(name='Contagem')

# Exibindo o resultado
count_lot = df.groupby(['Lotação']).size().reset_index(name="Contagem").sort_values(by='Contagem', ascending=False)

# Exibindo o resultado
count_area = df.groupby(['Área']).size().reset_index(name="Contagem").sort_values(by='Contagem', ascending=False)

# Calcula a contagem total por Lotação
lotacao_totais = lot_area_contagem.groupby('Lotação')['Contagem'].sum().reset_index()
lotacao_totais.columns = ['Lotação', 'Total_Contagem']

# Mescla o total de contagem por lotação de volta ao DataFrame principal
lot_area_contagem = lot_area_contagem.merge(lotacao_totais, on='Lotação')

# Cria o gráfico de treemap, usando 'Total_Contagem' para definir a cor
fig_map = px.treemap(
    lot_area_contagem,
    path=[px.Constant('Reclamantes'), 'Lotação', 'Área'],
    values='Contagem',
    color='Total_Contagem',  # Usa o total de contagem para aplicar a escala
    color_continuous_scale='Blues',
    title = "Ditribuição dos Processos por Lotação e Área"
)

fig_map.update_traces(
    hovertemplate=' <b>%{parent}</b><br> %{label}<br> %{value}<extra></extra>'
)

# Atualizando o layout para remover a barra de cor e ajustar o tamanho
fig_map.update_layout(
    coloraxis_showscale=False,  # Remove a barra de cor
    autosize=True,               # Habilita o redimensionamento automático
    margin=dict(t=30, l=5, r=0, b=20)  # Margens reduzidas
)

# ÁREAS DA EMPRESA

area = pd.DataFrame(df.groupby('Área')['Área'].count())
area_v = pd.DataFrame(df.groupby('Área')['Valor Pedido Inicial Atualizado 31/03/2022'].sum())
area = area.rename(columns={'Área':'Processos'}).reset_index()
area_v = area_v.rename(columns={'Área':'Valores'}).reset_index()
area = area.merge(area_v).rename(columns={'Valor Pedido Inicial Atualizado 31/03/2022':'Valor'})
area = area.sort_values(by='Processos', ascending=False)
area_cor = (
    area
    .style
    .background_gradient(subset=['Valor'], cmap='Blues')  # Gradiente na coluna Valor
    .background_gradient(subset=['Processos'], cmap='Blues')  # Gradiente na coluna Processos
)
area_cor = area_cor.format({'Valor': lambda val: formata_numero(val, "R$")})

area_pie = area.copy()
area_pie["valor formatado"] = [formata_numero(val, "R$") for val in area["Valor"]]

pie_processos = px.pie(area_pie, values='Processos', names='Área', hole=0.7, title='Processos por Área', color_discrete_sequence=px.colors.sequential.Blues[::-1])
pie_processos.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=30, b=15),  # Removes extra margins
    width=270,  # Set your desired width
    height=270  # Set your desired height
    )
pie_processos.update_traces(
    textinfo="none",
    hovertemplate="<b>%{label}</b><br>%{percent}<br>%{value}<extra></extra> processos")

pie_valor = px.pie(area_pie, values='Valor', names='Área', hole=0.7, title='Valores por Área', color_discrete_sequence=px.colors.sequential.Blues[::-1])
pie_valor.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=30, b=15),  # Removes extra margins
    width=270,  # Set your desired width
    height=270  # Set your desired height
    )
pie_valor.update_traces(
    textinfo="none",
    hovertemplate="<b>%{label}</b><br>%{percent}<br>%{customdata}<extra></extra>",
    customdata=area_pie["valor formatado"])


periodo = df.groupby('Área')[['Período de Empresa', 'Valor Pedido Inicial Atualizado 31/03/2022']].median().reset_index().sort_values(by='Período de Empresa')
periodo = periodo.rename(columns={'Valor Pedido Inicial Atualizado 31/03/2022':'Inicial Média'})
periodo['valor formatado'] = periodo['Inicial Média'].apply(lambda x : formata_numero(x, "R$"))

bar_periodo = px.bar(periodo, 
                     x='Área', 
                     y='Período de Empresa', 
                     title="Período de Empresa por Área",
                     color_discrete_sequence=px.colors.sequential.Blues[::-1]
                     )
bar_periodo.update_layout(margin=dict(l=0, r=0, t=50, b=0))
bar_periodo.update_traces(hovertemplate="<b>%{label}</b><br>%{value}<extra></extra> anos")

bar_inicial = px.bar(periodo, 
                     x='Área', 
                     y='Inicial Média',
                     title="Pedido Inicial Médio por Área",
                     color_discrete_sequence=px.colors.sequential.Blues[::-1]
                     )
bar_inicial.update_layout(margin=dict(l=0, r=0, t=50, b=0))
bar_inicial.update_traces(
    hovertemplate="<b>%{label}</b><br>%{customdata}<extra></extra>",
    customdata=periodo["valor formatado"])