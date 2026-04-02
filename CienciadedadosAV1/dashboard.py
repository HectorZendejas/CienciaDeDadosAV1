import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from br_geojson import COORDENADAS_ESTADOS

try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

try:
    import nltk
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

import re
import warnings

# Silenciar avisos de libraries (nltk/wordcloud, depreciações visualmente indesejadas)
warnings.filterwarnings("ignore")

# Garantir stopwords (pode falhar se offline)
if NLTK_AVAILABLE:
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)

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

    # Calcular tamanho de texto se ainda não existir
    if "DESCRICAO" in df.columns and "TAMANHO_TEXTO" not in df.columns:
        df["TAMANHO_TEXTO"] = df["DESCRICAO"].astype(str).str.len()

    # Classificar faixas de texto se já existir ou criar (com base em TAMANHO_TEXTO)
    if "TAMANHO_TEXTO" in df.columns and "FAIXA_TEXTO" not in df.columns:
        bins = [0, 50, 100, 250, 500, 1000, float("inf")]
        labels = ["Muito curto", "Curto", "Médio", "Longo", "Muito longo", "Extenso"]
        df["FAIXA_TEXTO"] = pd.cut(df["TAMANHO_TEXTO"], bins=bins, labels=labels, right=False)

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

estado_nao_informado = "NÃO INFORMADO"
estado_options = estados_disponiveis.copy()
if "ESTADO" in df.columns and df["ESTADO"].isna().any():
    estado_options = estados_disponiveis + [estado_nao_informado]

estado = st.sidebar.multiselect(
    "Estado",
    options=estado_options,
    default=estado_options
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
    if estado_nao_informado in estado:
        estados_selecionados = [e for e in estado if e != estado_nao_informado]
        if estados_selecionados:
            df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin(estados_selecionados) | df_filtrado["ESTADO"].isna()]
        else:
            df_filtrado = df_filtrado[df_filtrado["ESTADO"].isna()]
    else:
        df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin(estado)]

if "STATUS" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["STATUS"].isin(status)]

if "FAIXA_TEXTO" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["FAIXA_TEXTO"].astype(str).isin(faixa_texto)]

# =========================
# TÍTULO
# =========================
st.title(" Dashboard ReclameAqui - Ibyte")
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
# ANÁLISE GEOGRÁFICA AVANÇADA
# =========================
st.subheader(" Análise Geográfica Avançada: Distribuição por Estado")

if "ESTADO" in df_filtrado.columns and "ANO" in df_filtrado.columns and not df_filtrado.empty:
    anos_disponiveis = sorted(df_filtrado["ANO"].dropna().unique())
    
    if len(anos_disponiveis) > 0:
        ano_selecionado = st.slider(
            "Selecione o ano para análise geográfica",
            min_value=int(min(anos_disponiveis)),
            max_value=int(max(anos_disponiveis)),
            value=int(max(anos_disponiveis))
        )
        
        df_ano = df_filtrado[df_filtrado["ANO"] == ano_selecionado].copy()
        
        if not df_ano.empty:
            # Agrupar por estado
            reclamacoes_por_estado = (
                df_ano.groupby("ESTADO")
                .size()
                .reset_index(name="QUANTIDADE")
            )
            
            # Adicionar coordenadas
            reclamacoes_por_estado['LAT'] = reclamacoes_por_estado['ESTADO'].apply(
                lambda x: COORDENADAS_ESTADOS.get(x, (0, 0))[1]
            )
            reclamacoes_por_estado['LON'] = reclamacoes_por_estado['ESTADO'].apply(
                lambda x: COORDENADAS_ESTADOS.get(x, (0, 0))[0]
            )
            
            # Remover estados sem coordenadas
            reclamacoes_por_estado = reclamacoes_por_estado[
                (reclamacoes_por_estado['LAT'] != 0) | (reclamacoes_por_estado['LON'] != 0)
            ]
            
            if not reclamacoes_por_estado.empty:
                # Criar heatmap com scatter_mapbox
                fig_heat = px.scatter_geo(
                    reclamacoes_por_estado,
                    lat='LAT',
                    lon='LON',
                    size='QUANTIDADE',
                    color='QUANTIDADE',
                    hover_name='ESTADO',
                    hover_data={'QUANTIDADE': True, 'LAT': False, 'LON': False},
                    color_continuous_scale='Reds',
                    size_max=60,
                    title=f"Heatmap de Reclamações por Estado - {int(ano_selecionado)}",
                    labels={'QUANTIDADE': 'Reclamações'}
                )
                
                fig_heat.update_geos(
                    scope='south america',
                    projection_type='natural earth',
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    showcountries=True,
                    countrycolor='lightgray',
                    showcoastlines=True,
                    coastlinecolor='darkgray',
                    center=dict(lat=-10, lon=-55)
                )
                
                fig_heat.update_layout(
                    height=700,
                    coloraxis_colorbar=dict(title="Qtd.<br>Reclamações")
                )
                
                st.plotly_chart(fig_heat, use_container_width=True)
                
                # Abas complementares
                tab1, tab2 = st.tabs(["Tabela de Estados", "Ranking por Reclamações"])
                
                with tab1:
                    st.markdown(f"**Reclamações por Estado - Ano {int(ano_selecionado)}**")
                    tabela = reclamacoes_por_estado[['ESTADO', 'QUANTIDADE']].sort_values('QUANTIDADE', ascending=False)
                    st.dataframe(tabela, use_container_width=True)
                
                with tab2:
                    ranking = reclamacoes_por_estado.sort_values('QUANTIDADE', ascending=True)
                    fig_rank = px.bar(
                        ranking,
                        y='ESTADO',
                        x='QUANTIDADE',
                        orientation='h',
                        color='QUANTIDADE',
                        color_continuous_scale='Reds',
                        title=f"Ranking de Estados - Ano {int(ano_selecionado)}",
                        labels={'QUANTIDADE': 'Qtd. de Reclamações', 'ESTADO': 'Estado'}
                    )
                    fig_rank.update_layout(height=600)
                    st.plotly_chart(fig_rank, use_container_width=True)
            else:
                st.warning("Nenhum estado com dados válidos para este ano.")
        else:
            st.info(f"Nenhum dado disponível para o ano {int(ano_selecionado)}.")
    else:
        st.info("Nenhum ano disponível nos dados filtrados.")
else:
    st.info("Dados insuficientes para análise geográfica.")

# =========================
st.subheader(" Evolução Temporal")

if "DATA" in df_filtrado.columns and not df_filtrado.empty:
    serie = (
        df_filtrado
        .set_index("DATA")
        .resample("W-MON")
        .size()
        .reset_index(name="QUANTIDADE")
        .sort_values("DATA")
    )

    serie["MEDIA_MOVEL_4S"] = serie["QUANTIDADE"].rolling(window=4, min_periods=1).mean()

    fig_tempo = px.line(
        serie,
        x="DATA",
        y=["QUANTIDADE", "MEDIA_MOVEL_4S"],
        title="Evolução das Reclamações com Média Móvel de 7 Dias"
    )
    fig_tempo.update_layout(
        xaxis_title="Semana (início)",
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
# WORDCLOUD / MINERAÇÃO DE TEXTO
# =========================
st.subheader("WordCloud de Termos em DESCRICAO")

if WORDCLOUD_AVAILABLE and "DESCRICAO" in df_filtrado.columns and not df_filtrado.empty:
    texto_completo = " ".join(df_filtrado["DESCRICAO"].dropna().astype(str).tolist())
    texto_limpo = re.sub(r"[^\w\s]", " ", texto_completo, flags=re.UNICODE).lower()

    if NLTK_AVAILABLE:
        stopwords_pt = set(stopwords.words("portuguese"))
    else:
        stopwords_pt = {"o", "a", "e", "os", "as", "de", "do", "da", "em", "para", "com", "sem", "por", "que"}

    stopwords_pt.update(["https", "http", "www", "você", "usuario", "ibye", "ibyte", "não", "nao"])

    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        stopwords=stopwords_pt,
        max_words=150
    ).generate(texto_limpo)

    st.image(wordcloud.to_array(), width=1200)
else:
    # Se não há wordcloud ou descrição, mantém dashboard limpo sem avisos amarelos
    pass

# =========================
# TREEMAP HIERÁRQUICO
# =========================
st.subheader("Treemap: Status x Categorias (Hierárquico)")

if "STATUS" in df_filtrado.columns and "CATEGORIA_PRINCIPAL" in df_filtrado.columns and not df_filtrado.empty:
    treemap_data = (
        df_filtrado
        .dropna(subset=["STATUS", "CATEGORIA_PRINCIPAL"])
        .groupby(["STATUS", "CATEGORIA_PRINCIPAL"], as_index=False)
        .size()
        .rename(columns={"size": "QUANTIDADE"})
    )

    if not treemap_data.empty:
        fig_treemap = px.treemap(
            treemap_data,
            path=["STATUS", "CATEGORIA_PRINCIPAL"],
            values="QUANTIDADE",
            color="QUANTIDADE",
            color_continuous_scale="RdYlGn_r",
            title="Distribuição Hierárquica: Status → Categorias → Volume de Reclamações"
        )
        fig_treemap.update_layout(height=700)
        st.plotly_chart(fig_treemap, use_container_width=True)
    else:
        st.info("Nenhum dado válido para treemap (Status/Categoria).")
else:
    st.info("Dados insuficientes para gerar treemap.")

# =========================
# CRUZAMENTO DE DADOS
# =========================

st.subheader("Cruzamento de Dados")

col7, col8 = st.columns(2)

# STATUS x CATEGORIA
with col7:
    cruz = pd.crosstab(
        df_filtrado["CATEGORIA_PRINCIPAL"],
        df_filtrado["STATUS"]
    ).head(10)

    fig = px.imshow(
        cruz,
        text_auto=True,
        title="Categoria x Status"
    )

    st.plotly_chart(fig, width="stretch")

# STATUS x ESTADO
with col8:
    cruz2 = pd.crosstab(
        df_filtrado["ESTADO"],
        df_filtrado["STATUS"]
    ).head(10)

    fig2 = px.imshow(
        cruz2,
        text_auto=True,
        title="Estado x Status"
    )

    st.plotly_chart(fig2, width="stretch")

# =========================
# TABELA FINAL
# =========================
st.subheader(" Amostra dos Dados Filtrados")

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