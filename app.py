import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------
# GERANDO BASE DE DADOS FICTÍCIA
# ------------------------------
np.random.seed(42)
clientes = [f"Cliente {i}" for i in range(1, 11)]
datas = pd.date_range("2024-01-01", periods=12, freq="M")

dados = []
for cliente in clientes:
    ticket_medio = np.random.randint(500, 2000)
    for data in datas:
        economia = np.random.randint(1000, 10000)
        perc_economia = round(np.random.uniform(5, 30), 2)
        dados.append([cliente, data, ticket_medio, economia, perc_economia])

df = pd.DataFrame(dados, columns=["Cliente", "Data", "Ticket Médio", "Economia", "% Economia"])

# ------------------------------
# STREAMLIT APP
# ------------------------------
st.set_page_config(page_title="Dashboard de Clientes", layout="wide")

st.title("📊 Dashboard Interativo - Clientes & Economia")
st.markdown("Este é um BI interativo fictício com dados de clientes, ticket médio, economia e curva de tendência.")

# Filtros
clientes_sel = st.multiselect("Selecione os clientes:", df["Cliente"].unique(), default=df["Cliente"].unique())

df_filtrado = df[df["Cliente"].isin(clientes_sel)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("💰 Economia Total", f"R$ {df_filtrado['Economia'].sum():,.0f}")
col2.metric("🎟️ Ticket Médio", f"R$ {df_filtrado['Ticket Médio'].mean():,.2f}")
col3.metric("📉 % Economia Média", f"{df_filtrado['% Economia'].mean():.2f}%")

# Gráfico de tendência
st.subheader("📈 Curva de Tendência - Economia ao longo do tempo")
fig1 = px.line(df_filtrado, x="Data", y="Economia", color="Cliente", markers=True, title="Economia Mensal por Cliente")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de barras
st.subheader("📊 Ticket Médio por Cliente")
df_ticket = df_filtrado.groupby("Cliente")[["Ticket Médio"]].mean().reset_index()
fig2 = px.bar(df_ticket, x="Cliente", y="Ticket Médio", title="Ticket Médio por Cliente", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)

# Tabela de detalhes
st.subheader("📋 Dados Detalhados")
st.dataframe(df_filtrado, use_container_width=True)
