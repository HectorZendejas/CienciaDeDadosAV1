import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Dashboard ReclameAqui - Ibyte",
    layout="wide"
)

# =========================
# CARREGAR DADOS
# =========================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("RECLAMEAQUI_IBYTE_TRATADO.csv")

    # Garantir tipos corretos
    if "DATA" in df.columns:
        df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")

    # Ordenar faixas de texto, se existirem
    if "FAIXA_TEXTO" in df.columns:
        ordem_faixa = [
            "Muito curto",
            "Curto",
            "Médio",
            "Longo",
            "Muito longo",
            "Extenso"
        ]
        df["FAIXA_TEXTO"] = pd.Categorical(
            df["FAIXA_TEXTO"],
            categories=ordem_faixa,
            ordered=True
        )

    return df

df = carregar_dados()

# =========================
# SIDEBAR - FILTROS
# =========================
st.sidebar.title("Filtros")

estados_disponiveis = sorted(df["ESTADO"].dropna().unique()) if "ESTADO" in df.columns else []
status_disponiveis = sorted(df["STATUS"].dropna().unique()) if "STATUS" in df.columns else []
faixas_disponiveis = [
    faixa for faixa in [
        "Muito curto", "Curto", "Médio", "Longo", "Muito longo", "Extenso"
    ] if faixa in df["FAIXA_TEXTO"].dropna().astype(str).unique()
] if "FAIXA_TEXTO" in df.columns else []

estado = st.sidebar.multiselect(
    "Estado",
    options=estados_disponiveis,
    default=estados_disponiveis
)

status = st.sidebar.multiselect(
    "Status",
    options=status_disponiveis,
    default=status_disponiveis
)

faixa_texto = st.sidebar.multiselect(
    "Faixa de tamanho do texto",
    options=faixas_disponiveis,
    default=faixas_disponiveis
)

# =========================
# FILTRAR BASE
# =========================
df_filtrado = df.copy()

if "ESTADO" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin(estado)]

if "STATUS" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["STATUS"].isin(status)]

if "FAIXA_TEXTO" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["FAIXA_TEXTO"].astype(str).isin(faixa_texto)]

# =========================
# TÍTULO
# =========================
st.title("📊 Dashboard ReclameAqui - Ibyte")
st.markdown("Análise exploratória das reclamações da Ibyte com foco em status, localização, categorias e comportamento temporal.")

# =========================
# KPIs
# =========================
total_reclamacoes = len(df_filtrado)

resolvidas = (
    df_filtrado[df_filtrado["STATUS"] == "RESOLVIDO"].shape[0]
    if "STATUS" in df_filtrado.columns else 0
)

nao_resolvidas = (
    df_filtrado[df_filtrado["STATUS"] == "NÃO RESOLVIDO"].shape[0]
    if "STATUS" in df_filtrado.columns else 0
)

perc_resolvidas = (resolvidas / total_reclamacoes * 100) if total_reclamacoes > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total de Reclamações", total_reclamacoes)
k2.metric("Resolvidas", resolvidas)
k3.metric("Não Resolvidas", nao_resolvidas)
k4.metric("% Resolvidas", f"{perc_resolvidas:.1f}%")

# =========================
# INSIGHTS RÁPIDOS
# =========================
with st.expander("Ver insights rápidos"):
    if total_reclamacoes > 0:
        estado_top = (
            df_filtrado["ESTADO"].value_counts().idxmax()
            if "ESTADO" in df_filtrado.columns and not df_filtrado["ESTADO"].dropna().empty
            else "N/A"
        )
        categoria_top = (
            df_filtrado["CATEGORIA_PRINCIPAL"].value_counts().idxmax()
            if "CATEGORIA_PRINCIPAL" in df_filtrado.columns and not df_filtrado["CATEGORIA_PRINCIPAL"].dropna().empty
            else "N/A"
        )
        st.markdown(
            f"""
- A base filtrada possui **{total_reclamacoes} reclamações**.
- O status **RESOLVIDO** representa **{perc_resolvidas:.1f}%** da base filtrada.
- O estado com mais reclamações é **{estado_top}**.
- A categoria principal mais frequente é **{categoria_top}**.
"""
        )
    else:
        st.warning("Nenhum registro encontrado com os filtros atuais.")

# =========================
# GRÁFICOS - LINHA 1
# =========================
col1, col2 = st.columns(2)

with col1:
    if "STATUS" in df_filtrado.columns and not df_filtrado.empty:
        status_df = (
            df_filtrado["STATUS"]
            .value_counts()
            .reset_index()
        )
        status_df.columns = ["STATUS", "QUANTIDADE"]

        fig_status = px.bar(
            status_df,
            x="STATUS",
            y="QUANTIDADE",
            title="Reclamações por Status",
            text="QUANTIDADE"
        )
        fig_status.update_layout(xaxis_title="Status", yaxis_title="Quantidade")
        st.plotly_chart(fig_status, width="stretch")

with col2:
    if "STATUS" in df_filtrado.columns and not df_filtrado.empty:
        status_prop = (
            df_filtrado["STATUS"]
            .value_counts()
            .reset_index()
        )
        status_prop.columns = ["STATUS", "QUANTIDADE"]

        fig_pizza = px.pie(
            status_prop,
            names="STATUS",
            values="QUANTIDADE",
            title="Proporção de Reclamações por Status"
        )
        st.plotly_chart(fig_pizza, width="stretch")

# =========================
# GRÁFICOS - LINHA 2
# =========================
col3, col4 = st.columns(2)

with col3:
    if "CATEGORIA_PRINCIPAL" in df_filtrado.columns and not df_filtrado.empty:
        categoria_df = (
            df_filtrado["CATEGORIA_PRINCIPAL"]
            .value_counts()
            .head(10)
            .sort_values(ascending=True)
            .reset_index()
        )
        categoria_df.columns = ["CATEGORIA_PRINCIPAL", "QUANTIDADE"]

        fig_categoria = px.bar(
            categoria_df,
            x="QUANTIDADE",
            y="CATEGORIA_PRINCIPAL",
            orientation="h",
            title="Top 10 Categorias Principais",
            text="QUANTIDADE"
        )
        fig_categoria.update_layout(
            xaxis_title="Quantidade",
            yaxis_title="Categoria Principal"
        )
        st.plotly_chart(fig_categoria, width="stretch")

with col4:
    if "ESTADO" in df_filtrado.columns and not df_filtrado.empty:
        estado_df = (
            df_filtrado["ESTADO"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        estado_df.columns = ["ESTADO", "QUANTIDADE"]

        fig_estado = px.bar(
            estado_df,
            x="ESTADO",
            y="QUANTIDADE",
            title="Top 10 Estados com Mais Reclamações",
            text="QUANTIDADE"
        )
        fig_estado.update_layout(
            xaxis_title="Estado",
            yaxis_title="Quantidade"
        )
        st.plotly_chart(fig_estado, width="stretch")

# =========================
# MAPA DO BRASIL (CORRIGIDO)
# =========================

st.subheader("🗺️ Mapa do Brasil por Estado")

if "ESTADO" in df_filtrado.columns and not df_filtrado.empty:

    mapa_df = (
        df_filtrado.groupby("ESTADO")
        .size()
        .reset_index(name="QUANTIDADE")
    )

    fig_mapa = px.choropleth(
        mapa_df,
        locations="ESTADO",
        locationmode="geojson-id",  # importante
        color="QUANTIDADE",
        title="Quantidade de Reclamações por Estado",
        color_continuous_scale="Blues"
    )

    fig_mapa.update_geos(
        scope="south america",
        center={"lat": -14, "lon": -55},
        projection_scale=3
    )

    st.plotly_chart(fig_mapa, width="stretch")
# =========================
# SÉRIE TEMPORAL
# =========================
st.subheader("📈 Evolução Temporal")

if "DATA" in df_filtrado.columns and not df_filtrado.empty:
    serie = (
        df_filtrado.groupby("DATA")
        .size()
        .reset_index(name="QUANTIDADE")
        .sort_values("DATA")
    )

    serie["MEDIA_MOVEL_7D"] = serie["QUANTIDADE"].rolling(window=7).mean()

    fig_tempo = px.line(
        serie,
        x="DATA",
        y=["QUANTIDADE", "MEDIA_MOVEL_7D"],
        title="Evolução das Reclamações com Média Móvel de 7 Dias"
    )
    fig_tempo.update_layout(
        xaxis_title="Data",
        yaxis_title="Quantidade",
        legend_title="Série"
    )
    st.plotly_chart(fig_tempo, width="stretch")

# =========================
# BOXPLOT E HISTOGRAMA
# =========================
col5, col6 = st.columns(2)

with col5:
    if all(col in df_filtrado.columns for col in ["STATUS", "TAMANHO_TEXTO"]) and not df_filtrado.empty:
        fig_box = px.box(
            df_filtrado,
            x="STATUS",
            y="TAMANHO_TEXTO",
            title="Tamanho do Texto por Status"
        )
        fig_box.update_layout(
            xaxis_title="Status",
            yaxis_title="Quantidade de caracteres"
        )
        st.plotly_chart(fig_box, width="stretch")

with col6:
    if "TAMANHO_TEXTO" in df_filtrado.columns and not df_filtrado.empty:
        fig_hist = px.histogram(
            df_filtrado,
            x="TAMANHO_TEXTO",
            nbins=30,
            title="Distribuição do Tamanho dos Textos"
        )
        fig_hist.update_layout(
            xaxis_title="Quantidade de caracteres",
            yaxis_title="Frequência"
        )
        st.plotly_chart(fig_hist, width="stretch")

# =========================
# TABELA FINAL
# =========================
st.subheader("📋 Amostra dos Dados Filtrados")

colunas_mostrar = [
    col for col in [
        "ID", "DATA", "ESTADO", "CIDADE", "STATUS",
        "CATEGORIA_PRINCIPAL", "TAMANHO_TEXTO"
    ] if col in df_filtrado.columns
]

st.dataframe(df_filtrado[colunas_mostrar].head(20), width="stretch")

# =========================
# MENSAGEM FINAL
# =========================
st.markdown("---")
st.caption("Dashboard desenvolvido para análise das reclamações da Ibyte com base nos dados do ReclameAqui.")