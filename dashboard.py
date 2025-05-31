import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Dashboard do Projeto Integrador', page_icon='📊', layout='wide')

cores = ['#118DFF', '#102790']
df = pd.read_excel('planilha_base.xlsx')
df.columns = df.columns.str.strip()

def Home():
    st.title("Projeto Integrador")

    unidades_por_ano = df.groupby('Ano')['Unidades'].sum().reset_index()

    fig_ano = px.bar(
        unidades_por_ano,
        x='Ano',
        y='Unidades',
        title='Total de Unidades de Máscaras por Ano',
        color_discrete_sequence=cores,
        text='Unidades'
    )
    st.plotly_chart(fig_ano, use_container_width=True)

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