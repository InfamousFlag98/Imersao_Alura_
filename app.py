import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análise de Dados - Imersão Alura",
    page_icon=":bar_chart:",
    layout="wide",
)

df= pd.read_csv('https://raw.githubusercontent.com/InfamousFlag98/Imersao_Alura_/refs/heads/main/dados-imersao-limpo.csv')
#Barra Lateral
st.sidebar.header("Filtros")

# Filtro por Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("ano", anos_disponiveis, default=anos_disponiveis)

# Filtro por Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

#Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# Filtro do Dataframe
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

#Main Content
st.title("Análise de Dados - Imersão Alura")
st.markdown("Explorando os dados salariais na area de dados e tecnologia nos ultimos anos. Use os filtros à esquerda para personalizar a visualização.")
st.subheader('Metricas Gerais(Salário anual em USD)')

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_minimo = df_filtrado['usd'].min()
    salario_maximo = df_filtrado['usd'].max()
    cargo_frequente = df_filtrado['cargo'].mode()[0]
    total_registros = df_filtrado.shape[0]
    st.write(f"Total de Registros: {total_registros}")
    st.write(f"Salário Médio: ${salario_medio:,.2f}")
    st.write(f"Salário Mínimo: ${salario_minimo:,.2f}")
    st.write(f"Salário Máximo: ${salario_maximo:,.2f}")
    st.write(f"Cargo mais frequente: {cargo_frequente}")
else:
    salario_medio, salario_minimo, salario_maximo, cargo_frequente, total_registros = 0, 0, 0, "", 0


col1, col2, col3, col4, col5 = st.columns(5)
col3.metric("Total de Registros", f"{total_registros}")
col1.metric("Salário Médio (USD)", f"${salario_medio:,.2f}")
col5.metric("Salário Mínimo (USD)", f"${salario_minimo:,.2f}")
col2.metric("Salário Máximo (USD)", f"${salario_maximo:,.2f}")
col4.metric("Cargo mais frequente", f"{cargo_frequente}")

st.markdown("---")

st.subheader("Gráficos de Análise")

col1_graf1, col2_graf2 = st.columns(2)

with col1_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().sort_values(ascending=False).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            title='Top 10 Cargos por Salário Médio',
            labels={'usd': 'Salário Médio Anual (USD)', 'cargo': 'Cargo'}
            )
        grafico_cargos.update_layout(title_x=0.1,yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir no grafico de cargos.")
with col2_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title='Distribuição de Salários Anuais',
            labels={'usd': 'Faixa Salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir no gráfico de distribuição salarial.")

st.markdown("---")
st.subheader("Análises Adicionais Pt.1")

if not df_filtrado.empty:
    remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
    remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
    grafico_remoto = px.pie(
        remoto_contagem,
        names='tipo_trabalho',
        values='quantidade',
        title='Proporção dos tipos de trabalho',
        hole=0.5
    )
    grafico_remoto.update_traces(textinfo='percent+label')
    grafico_remoto.update_layout(title_x=0.1)
    st.plotly_chart(grafico_remoto, use_container_width=True)
else:
    st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

st.markdown("---")
st.subheader("Análises Adicionais Pt.2")

if not df_filtrado.empty:
    df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
    media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
    grafico_paises = px.choropleth(media_ds_pais,
        locations='residencia_iso3',
        color='usd',
        color_continuous_scale='rdylgn',
        title='Salário médio de Cientista de Dados por país',
        labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
    grafico_paises.update_layout(title_x=0.1)
    st.plotly_chart(grafico_paises, use_container_width=True)
else:
    st.warning("Nenhum dado para exibir no gráfico de países.")

st.subheader('Dados Detalhados')
st.dataframe(df_filtrado)