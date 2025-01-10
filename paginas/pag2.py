import plotly.express as px
import pandas as pd
import streamlit as st


# ✅ Acesso global ao DataFrame
if 'df' in st.session_state:
    df = st.session_state.df
else:
    st.error("O DataFrame não foi carregado corretamente.")
    st.stop()  # 🚫 Interrompe a execução se o DataFrame não foi carregado


def formata_numero(valor, prefixo='R$'):
    unidades = ['', 'k', 'mi', 'bi', 'tri']
    
    for i, unidade in enumerate(unidades):
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'.strip()
        valor /= 1000
    return f'{prefixo} {valor:.2f} {unidades[-1]}'.strip()

def formata_total(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


total_pago = df["TOTAL PAGO"].sum()
condenacao_paga = df["Condenação - Pagamentos Efetuados"].sum()
outros_pag = df['Outros Pagamentos'].sum()
deposito = df["Unnamed: 34"].sum()

pagamentos = pd.DataFrame({'Pagamento': ['Valor da Condenação', 'Outros (INSS, Custas e Perícia)'], 
                           'Valor': [condenacao_paga, outros_pag], 
                           'valor_formatado': [formata_numero(condenacao_paga), formata_numero(outros_pag)]})


pie_pag = px.pie(pagamentos, values='Valor', names='Pagamento', hole=0.7,  title='Pagamentos por Condenação', color_discrete_sequence=px.colors.sequential.Blues[-1:-3])
pie_pag.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=30, b=0),  # Removes extra margins
    width=270,  # Set your desired width
    height=270  # Set your desired height
    
    )
pie_pag.update_traces(
    textinfo="none",
    hovertemplate="<b>%{label}</b><br>%{percent}<br>%{customdata}<extra></extra>",
    customdata=pagamentos["valor_formatado"])

df_total_pago = pd.DataFrame({'Pagamento': 'Total Pago', 'Valor': [total_pago]})
pagamentos_reduzido = pagamentos[['Pagamento','Valor']]
pagamentos_show = pd.concat([pagamentos_reduzido, df_total_pago])
pagamentos_show['Valor'] = pagamentos_show['Valor'].apply(lambda x : formata_total(x))

# TABELA E GRÁFICO DE VALORES DEPOSITADOS

outros_dep = deposito - total_pago

df_depositos = pd.DataFrame({'Depósito': ['Pago por Condenação', 'Depósitos Retornáveis'], 
                           'Valor': [total_pago, outros_dep], 
                           'valor formatado': [formata_numero(total_pago), formata_numero(outros_dep)]})

pie_deposito = px.pie(df_depositos, values='Valor', names='Depósito', hole=0.7,  title='Depósitos Judiciais', color_discrete_sequence=px.colors.sequential.Blues[-1:-3])
pie_deposito.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=30, b=0),  # Removes extra margins
    width=270,  # Set your desired width
    height=270  # Set your desired height
    )
pie_deposito.update_traces(
    textinfo="none",
    hovertemplate="<b>%{label}</b><br>%{percent}<br>%{customdata}<extra></extra>",
    customdata=df_depositos["valor formatado"])

df_total_depositado = pd.DataFrame({'Depósito': 'Total Depositado', 'Valor': [deposito]})
depositos_reduzido = df_depositos[['Depósito','Valor']]
depositos_show = pd.concat([depositos_reduzido, df_total_depositado])
depositos_show['Valor'] = depositos_show['Valor'].apply(lambda x : formata_total(x))

# TABELA E GRÁFICO DE RISCO
provavel = df['Provável'].sum()
possivel = df['Possível'].sum()
remoto = df['Remoto'].sum()

df_risco = pd.DataFrame({'Risco': ['Provável', 'Possível', 'Remoto'], 'Valor': [provavel, possivel, remoto]})
df_risco['valor formatado'] = df_risco['Valor'].apply(lambda x : formata_numero(x))
df_risco

pie_risco = px.pie(df_risco, values='Valor', names='Risco', hole=0.7,  title='Risco de Pagamento', color_discrete_sequence=px.colors.sequential.Blues[::-1])
pie_risco.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=30, b=0),  # Removes extra margins
    width=270,  # Set your desired width
    height=270  # Set your desired height
    )
pie_risco.update_traces(
    textinfo="none",
    hovertemplate="<b>%{label}</b><br>%{percent}<br>%{customdata}<extra></extra>",
    customdata=df_risco["valor formatado"])

risco_show = df_risco.loc[:,['Risco', 'Valor']]
risco_show['Valor'] = risco_show['Valor'].apply(lambda x : formata_total(x))