import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import plotly.graph_objects as go

st.set_page_config(page_title='Dashboard do Projeto Integrador', page_icon='📊', layout='wide')

cores = ['#118DFF', '#102790']
df = pd.read_excel('base_dados.xlsx')
df.columns = df.columns.str.strip()

df = df[pd.to_numeric(df['Ano'], errors='coerce').notnull()]
df['Ano'] = df['Ano'].astype(int)
df = df[df['Ano'].isin([2019, 2020, 2021, 2022])]

def Home():
    st.title("Projeto Integrador")    

    modelo_mascara = ' PFF2 S/Válvula'
    total_mascaras = '+950 milhões'
    componentes_mascara = '3'
    periodo_dados = 'Período de 2019 à 2022 '

    st.markdown("### Visão Geral")

    col1, col2, col3= st.columns(3)

    with col1:
        st.metric(label="Máscara modelo", value=modelo_mascara)
    with col2:
        st.metric(label="Total das Máscaras", value=total_mascaras)
    with col3:
        st.metric(label="Componentes", value=componentes_mascara)

    # with col4:
    #     st.metric(label="Temáticas", value=periodo_dados)

    st.text(periodo_dados)

    st.markdown("---")
    

    unidades_por_ano = df.groupby('Ano')['Unidades'].sum().reset_index()
    unidades_por_ano['Unidades Formatadas'] = unidades_por_ano['Unidades'].apply(lambda x: f'{int(x):,}'.replace(',', '.'))

    fig_ano = px.bar(
        unidades_por_ano,
        x='Ano',
        y='Unidades',
        title='Total de Unidades de Máscaras por Ano',
        color_discrete_sequence=cores,
        text='Unidades Formatadas'
    )
    fig_ano.update_traces(textposition='outside')
    fig_ano.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis=dict(tickmode='linear'))

    emissao_por_ano = df.groupby('Ano')['TOTAL Ton CO2e'].sum().reset_index()
    emissao_por_ano['Ano'] = emissao_por_ano['Ano'].astype(str)

    total_geral = emissao_por_ano['TOTAL Ton CO2e'].sum()
    emissao_por_ano.loc[len(emissao_por_ano.index)] = ['Total', total_geral]

    medidas = ["relative"] * (len(emissao_por_ano) - 1) + ["total"]

    fig_emissao = go.Figure(go.Waterfall(
        name="Emissão",
        orientation="v",
        x=emissao_por_ano['Ano'],
        y=emissao_por_ano['TOTAL Ton CO2e'],
        measure=medidas,
        text=[f"{v:,.2f}".replace(",", ".") for v in emissao_por_ano['TOTAL Ton CO2e']],
        textposition="outside",
        increasing={"marker": {"color": cores[0]}},
        decreasing={"marker": {"color": cores[1]}},
        totals={"marker": {"color": "#102790"}}
    ))

    fig_emissao.update_layout(
        title="TOTAL Ton CO2e",
        waterfallgap=0.3,
        xaxis=dict(
            title="Ano",
            type="category"
        ),
        yaxis_title="Toneladas de CO2e",
    )

    st.plotly_chart(fig_ano, use_container_width=True)
    st.plotly_chart(fig_emissao, use_container_width=True)

def Menu():
    with st.sidebar:
        selecionado = option_menu(
            menu_title='Menu',
            options=['Projeto Limpa Brasil'],
            icons=['house'],
            default_index=0
        )
    return selecionado

escolha = Menu()
if escolha == 'Projeto Limpa Brasil':
    Home()
