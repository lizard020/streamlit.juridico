import streamlit as st

from readcsv import load_data

# Carrega o DataFrame apenas uma vez
if 'df' not in st.session_state:
    st.session_state.df = load_data()

from paginas.pag1 import barras_anos, linhas, julgamento, liquidacao, processos, valor_total, processos_novos, valores_novos
from paginas.pag2 import pie_pag, pagamentos_show, pie_risco, risco_show, pie_deposito, depositos_show
from paginas.pag3 import fig_map, bar_periodo, bar_inicial, pie_processos, pie_valor, area_cor, cidades_df

df = st.session_state.df

## App

st.set_page_config(layout = 'wide')

st.title('Relatório Jurídico 2022')

## Visualização no Streamlit
aba1, aba2, aba3, aba4 = st.tabs(['Home', 'Financeiro', 'Reclamantes', 'Base de Dados'])

with aba1:
    # CSS para centralizar completamente tudo no st.metric
    st.markdown(
        """
        <style>
        /* Centralizar o container inteiro do st.metric */
        div[data-testid="stMetric"] {
            display: flex;
            flex-direction: column;
            align-items: center; /* Centraliza horizontalmente */
            justify-content: center; /* Centraliza verticalmente */
        }

        /* Centralizar especificamente o label */
        div[data-testid="stMetricLabel"] {
            text-align: center; /* Alinha o texto ao centro */
        }

        /* Centralizar o valor */
        div[data-testid="stMetricValue"] {
            text-align: center; /* Alinha o valor ao centro */
        }

        /* Centralizar o delta */
        div[data-testid="stMetricDelta"] {
            text-align: center; /* Alinha o delta ao centro */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Quantidade de processos', processos, border=True)
    with col2:
        st.metric('Valor total demandado', valor_total, border=True)
    with col3:
        st.metric('Quantidade de processos novos (2022)', processos_novos, border=True)
    with col4:
        st.metric('Valor total demandado em 2022', valores_novos, border=True)

    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        st.plotly_chart(barras_anos)

    with col2:
        st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
        st.plotly_chart(julgamento, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
        st.plotly_chart(liquidacao, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.plotly_chart(linhas)

with aba2:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
        st.plotly_chart(pie_risco, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.dataframe(risco_show, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
        st.plotly_chart(pie_pag, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.dataframe(pagamentos_show, hide_index=True, use_container_width=True)

    with col3:
        st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
        st.plotly_chart(pie_deposito, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.dataframe(depositos_show, hide_index=True, use_container_width=True)

with aba3:
    st.write('')

    col1, col2 = st.columns([1,2])

    with col1:
        st.dataframe(cidades_df, hide_index=True, use_container_width=True)

    with col2:
        st.plotly_chart(fig_map)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
        st.plotly_chart(pie_processos, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
        st.plotly_chart(pie_valor, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.dataframe(area_cor, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(bar_periodo)

    with col2:
        st.plotly_chart(bar_inicial)

with aba4:
    st.dataframe(df.iloc[:,1:])