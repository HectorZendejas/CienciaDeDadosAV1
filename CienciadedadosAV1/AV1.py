import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# 1. CONFIGURAÇÕES INICIAIS
# =========================

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 200)

sns.set_theme(style="whitegrid")

# Caminho do arquivo
caminho_arquivo = r"C:\Users\hecto\Downloads\CienciadedadosAV1\RECLAMEAQUI_IBYTE.csv"

# =========================
# 2. LEITURA DO DATASET
# =========================

try:
    df = pd.read_csv(caminho_arquivo)
    print("Dataset carregado com sucesso.\n")
except Exception as e:
    print("Erro ao carregar o arquivo:")
    print(e)
    raise

# =========================
# 3. VISÃO GERAL DOS DADOS
# =========================

print("Primeiras 5 linhas:")
print(df.head(), "\n")

print("Informações gerais:")
print(df.info(), "\n")

print("Dimensão do dataset:")
print(f"Linhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}\n")

print("Colunas do dataset:")
print(df.columns.tolist(), "\n")

print("Valores nulos por coluna:")
print(df.isnull().sum(), "\n")

# =========================
# 4. PADRONIZAÇÃO DAS COLUNAS
# =========================

df.columns = (
    df.columns
    .str.strip()
    .str.upper()
    .str.replace(" ", "_", regex=False)
    .str.replace("Ç", "C", regex=False)
    .str.replace("Ã", "A", regex=False)
    .str.replace("Á", "A", regex=False)
    .str.replace("À", "A", regex=False)
    .str.replace("Â", "A", regex=False)
    .str.replace("É", "E", regex=False)
    .str.replace("Ê", "E", regex=False)
    .str.replace("Í", "I", regex=False)
    .str.replace("Ó", "O", regex=False)
    .str.replace("Õ", "O", regex=False)
    .str.replace("Ô", "O", regex=False)
    .str.replace("Ú", "U", regex=False)
)

print("Colunas após padronização:")
print(df.columns.tolist(), "\n")

# =========================
# 5. TRATAMENTO INICIAL
# =========================

# Seleciona colunas de texto sem gerar warning
colunas_textuais = df.select_dtypes(include=["object", "string"]).columns

# Remove espaços extras
for col in colunas_textuais:
    df[col] = df[col].astype(str).str.strip()

# Corrige "nan" string e vazios
df.replace("nan", np.nan, inplace=True)
df.replace("", np.nan, inplace=True)

# Padroniza textos principais em maiúsculo
colunas_para_padronizar = ["TEMA", "LOCAL", "CATEGORIA", "STATUS"]
for col in colunas_para_padronizar:
    if col in df.columns:
        df[col] = df[col].astype(str).str.upper().str.strip()

# =========================
# 6. CONVERSÃO DE TIPOS
# =========================

# Converter TEMPO para data
if "TEMPO" in df.columns:
    df["TEMPO"] = pd.to_datetime(df["TEMPO"], errors="coerce")

# Colunas numéricas
colunas_numericas = [
    "ANO", "MES", "DIA", "DIA_DO_ANO",
    "SEMANA_DO_ANO", "DIA_DA_SEMANA",
    "TRIMETRES", "CASOS"
]

for col in colunas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# 7. CRIAÇÃO DE NOVAS VARIÁVEIS
# =========================

# Separa cidade e estado
if "LOCAL" in df.columns:
    local_split = df["LOCAL"].str.split(" - ", n=1, expand=True)
    if local_split.shape[1] == 2:
        df["CIDADE"] = local_split[0].str.strip()
        df["ESTADO"] = local_split[1].str.strip()
    else:
        df["CIDADE"] = df["LOCAL"]
        df["ESTADO"] = np.nan

# Categoria principal = primeiro nível antes do <->
if "CATEGORIA" in df.columns:
    df["CATEGORIA_PRINCIPAL"] = df["CATEGORIA"].astype(str).str.split("<->").str[0].str.strip()

# Tamanho do texto
if "DESCRICAO" in df.columns:
    df["TAMANHO_TEXTO"] = df["DESCRICAO"].fillna("").astype(str).apply(len)

# Faixa de tamanho do texto
if "TAMANHO_TEXTO" in df.columns:
    df["FAIXA_TEXTO"] = pd.cut(
        df["TAMANHO_TEXTO"],
        bins=[0, 100, 300, 600, 1200, 3000, 10000],
        labels=["Muito curto", "Curto", "Médio", "Longo", "Muito longo", "Extenso"],
        include_lowest=True
    )

# Coluna DATA com base em ANO/MES/DIA
if all(col in df.columns for col in ["ANO", "MES", "DIA"]):
    df["DATA"] = pd.to_datetime(
        df[["ANO", "MES", "DIA"]].rename(
            columns={"ANO": "year", "MES": "month", "DIA": "day"}
        ),
        errors="coerce"
    )

# =========================
# 8. LIMPEZA FINAL
# =========================

df.drop_duplicates(inplace=True)

print("Dimensão após limpeza:")
print(f"Linhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}\n")

# =========================
# 9. ANÁLISE DESCRITIVA
# =========================

print("Resumo estatístico das colunas numéricas:")
print(df.describe(include=[np.number]), "\n")

if "STATUS" in df.columns:
    print("Quantidade por STATUS:")
    print(df["STATUS"].value_counts(dropna=False), "\n")

    print("Proporção por STATUS (%):")
    print((df["STATUS"].value_counts(normalize=True, dropna=False) * 100).round(2), "\n")

if "CATEGORIA" in df.columns:
    print("Top 10 categorias completas:")
    print(df["CATEGORIA"].value_counts(dropna=False).head(10), "\n")

if "CATEGORIA_PRINCIPAL" in df.columns:
    print("Top 10 categorias principais:")
    print(df["CATEGORIA_PRINCIPAL"].value_counts(dropna=False).head(10), "\n")

if "LOCAL" in df.columns:
    print("Top 10 locais:")
    print(df["LOCAL"].value_counts(dropna=False).head(10), "\n")

if "ESTADO" in df.columns:
    print("Quantidade por estado:")
    print(df["ESTADO"].value_counts(dropna=False).head(20), "\n")

# =========================
# 10. GRÁFICOS
# =========================

# 10.1 Barras - Status
if "STATUS" in df.columns:
    plt.figure(figsize=(10, 5))
    df["STATUS"].value_counts().plot(kind="bar")
    plt.title("Quantidade de Reclamações por Status")
    plt.xlabel("Status")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# 10.2 Pizza - Proporção por status
if "STATUS" in df.columns:
    plt.figure(figsize=(8, 8))
    df["STATUS"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Proporção de Reclamações por Status")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

# 10.3 Top categorias principais
if "CATEGORIA_PRINCIPAL" in df.columns:
    plt.figure(figsize=(12, 6))
    df["CATEGORIA_PRINCIPAL"].value_counts().head(10).sort_values().plot(kind="barh")
    plt.title("Top 10 Categorias Principais com Mais Reclamações")
    plt.xlabel("Quantidade")
    plt.ylabel("Categoria Principal")
    plt.tight_layout()
    plt.show()

# 10.4 Top estados
if "ESTADO" in df.columns:
    plt.figure(figsize=(10, 5))
    df["ESTADO"].value_counts().head(10).plot(kind="bar")
    plt.title("Top 10 Estados com Mais Reclamações")
    plt.xlabel("Estado")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

# 10.5 Histograma - tamanho do texto
if "TAMANHO_TEXTO" in df.columns:
    plt.figure(figsize=(10, 5))
    plt.hist(df["TAMANHO_TEXTO"].dropna(), bins=30)
    plt.title("Distribuição do Tamanho dos Textos")
    plt.xlabel("Quantidade de caracteres")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.show()

# 10.6 Boxplot - tamanho do texto por status
if "STATUS" in df.columns and "TAMANHO_TEXTO" in df.columns:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="STATUS", y="TAMANHO_TEXTO")
    plt.title("Tamanho do Texto por Status")
    plt.xlabel("Status")
    plt.ylabel("Quantidade de caracteres")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# 10.7 Série temporal
if "DATA" in df.columns:
    serie_tempo = df.groupby("DATA").size().sort_index()

    plt.figure(figsize=(12, 5))
    plt.plot(serie_tempo.index, serie_tempo.values)
    plt.title("Evolução das Reclamações ao Longo do Tempo")
    plt.xlabel("Data")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.show()

# 10.8 Série temporal com média móvel
if "DATA" in df.columns:
    serie_tempo = df.groupby("DATA").size().sort_index()
    media_movel = serie_tempo.rolling(window=7).mean()

    plt.figure(figsize=(12, 5))
    plt.plot(serie_tempo.index, serie_tempo.values, label="Original")
    plt.plot(media_movel.index, media_movel.values, label="Média móvel 7 dias")
    plt.title("Série Temporal com Tendência")
    plt.xlabel("Data")
    plt.ylabel("Quantidade")
    plt.legend()
    plt.tight_layout()
    plt.show()

# 10.9 Faixa de tamanho do texto
if "FAIXA_TEXTO" in df.columns:
    plt.figure(figsize=(10, 5))
    df["FAIXA_TEXTO"].value_counts().sort_index().plot(kind="bar")
    plt.title("Distribuição por Faixa de Tamanho do Texto")
    plt.xlabel("Faixa")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# =========================
# 11. CRUZAMENTOS IMPORTANTES
# =========================

if "STATUS" in df.columns and "CATEGORIA_PRINCIPAL" in df.columns:
    cruzamento_status_categoria = pd.crosstab(df["CATEGORIA_PRINCIPAL"], df["STATUS"])
    print("Cruzamento: CATEGORIA_PRINCIPAL x STATUS")
    print(cruzamento_status_categoria.head(15), "\n")

if "STATUS" in df.columns and "ESTADO" in df.columns:
    cruzamento_status_estado = pd.crosstab(df["ESTADO"], df["STATUS"])
    print("Cruzamento: ESTADO x STATUS")
    print(cruzamento_status_estado.head(15), "\n")

if "STATUS" in df.columns and "FAIXA_TEXTO" in df.columns:
    cruzamento_status_faixa = pd.crosstab(df["FAIXA_TEXTO"], df["STATUS"])
    print("Cruzamento: FAIXA_TEXTO x STATUS")
    print(cruzamento_status_faixa, "\n")

# =========================
# 12. WORDCLOUD OPCIONAL
# =========================

try:
    from wordcloud import WordCloud, STOPWORDS

    texto_completo = " ".join(df["DESCRICAO"].dropna().astype(str))

    stopwords_pt = set(STOPWORDS)
    stopwords_pt.update([
        "que", "de", "da", "do", "e", "em", "o", "a", "os", "as", "um", "uma",
        "para", "com", "não", "na", "no", "por", "mais", "me", "já", "eu",
        "foi", "ser", "ao", "dos", "das", "se", "como", "mas", "ou", "só",
        "muito", "pela", "pelo", "minha", "meu", "porque", "quando", "onde",
        "ibyte", "loja", "física", "produto", "empresa"
    ])

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        stopwords=stopwords_pt
    ).generate(texto_completo)

    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("WordCloud das Reclamações")
    plt.tight_layout()
    plt.show()

except ModuleNotFoundError:
    print("Biblioteca 'wordcloud' não instalada. Se quiser usar, rode:")
    print("python -m pip install wordcloud\n")

# =========================
# 13. SALVANDO A BASE TRATADA
# =========================

nome_saida = "RECLAMEAQUI_IBYTE_TRATADO.csv"
df.to_csv(nome_saida, index=False, encoding="utf-8-sig")
print(f"Arquivo tratado salvo como: {nome_saida}")