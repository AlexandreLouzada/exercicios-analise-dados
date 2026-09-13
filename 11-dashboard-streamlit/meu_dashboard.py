import streamlit as st
import pandas as pd


@st.cache_data
def carregar_dados():
    """Lê o CSV uma única vez — @st.cache_data evita releitura a cada interação."""
    df = pd.read_csv("vendas.csv", parse_dates=["data"])
    return df


# ---------- Fase 1: Título principal ----------
st.title("Dashboard de Vendas")

# ---------- Fase 2: Filtros no painel lateral ----------
df = carregar_dados()

st.sidebar.title("Filtros")
lista_categorias = df["categoria"].unique().tolist()
categorias_sel = st.sidebar.multiselect(
    "Selecione as Categorias",
    options=lista_categorias,
    default=lista_categorias,
)

# Regra de ouro: filtrar o DataFrame pelo valor dos widgets
df_filtrado = df[df["categoria"].isin(categorias_sel)]

# ---------- Fase 3: Métricas em destaque ----------
col1, col2 = st.columns([1, 1])

with col1:
    receita_total = df_filtrado["receita"].sum()
    st.metric(label="Receita Total", value=f"R$ {receita_total:,.2f}")

with col2:
    total_pedidos = len(df_filtrado)
    st.metric(label="Total de Pedidos", value=f"{total_pedidos:,}")

# ---------- Fase 3: Abas de navegação ----------
aba1, aba2 = st.tabs(["Evolução Mensal", "Tabela de Dados"])

with aba1:
    # Agrupar por mês antes de plotar para um gráfico legível
    receita_mensal = (
        df_filtrado.set_index("data")["receita"]
        .resample("ME")
        .sum()
        .rename("receita")
    )
    st.area_chart(receita_mensal)

with aba2:
    st.dataframe(df_filtrado, use_container_width=True)

    # Botão de exportação do recorte filtrado
    csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar recorte em CSV",
        data=csv_bytes,
        file_name="recorte_vendas.csv",
        mime="text/csv",
    )

# ---------- Fase 4: Executar localmente ----------
# Rodar local:  streamlit run meu_dashboard.py
# Publicar (Streamlit Community Cloud):
#   1. Suba meu_dashboard.py + vendas.csv + requirements.txt para um repositório no GitHub
#   2. No share.streamlit.io, conecte sua conta GitHub e selecione o repositório
#   3. Aponte o arquivo principal (meu_dashboard.py) e clique em Deploy