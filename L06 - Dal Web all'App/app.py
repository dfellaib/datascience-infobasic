"""
Mondiale 2026 Dashboard
Questa app legge il CSV generato dal notebook Colab e lo mostra in modo interattivo.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Mondiale 2026", page_icon="⚽", layout="wide")
st.title("⚽ Mondiale 2026 — Dashboard")
st.caption("Dati estratti da Wikipedia e analizzati su Colab")

# --- CARICA IL CSV (generato dal notebook Colab) ---
df = pd.read_csv("L06 - Dal Web all'App/mondiale_2026_gironi.csv")

# --- SIDEBAR: FILTRI ---
st.sidebar.header("Filtri")

# Filtro gironi
selected_groups = st.sidebar.multiselect(
    "Seleziona gironi",
    options=sorted(df['Group'].unique()),
    default=sorted(df['Group'].unique())
)

# Filtro punti minimi
min_pts = st.sidebar.slider("Punti minimi", 0, int(df['Pts'].max()), 0)

# Applica filtri
filtered = df[(df['Group'].isin(selected_groups)) & (df['Pts'] >= min_pts)]

# --- METRICHE ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Squadre", len(filtered))
col2.metric("Gol totali", int(filtered['GF'].sum()))
col3.metric("Media gol/squadra", f"{filtered['GF'].mean():.1f}")
col4.metric("Media punti", f"{filtered['Pts'].mean():.1f}")

# --- TABELLA ---
st.subheader("Classifica gironi")
st.dataframe(
    filtered[['Team', 'Group', 'Pld', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']]
    .sort_values(['Group', 'Pts'], ascending=[True, False]),
    use_container_width=True,
    hide_index=True
)

# --- GRAFICI ---
st.subheader("Grafici")
tab1, tab2, tab3 = st.tabs(["Top Goleador", "Attacco vs Difesa", "Punti per girone"])

with tab1:
    top = filtered.sort_values('GF', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top['Team'], top['GF'], color='steelblue')
    ax.set_xlabel('Gol fatti')
    ax.set_title('Top 10 squadre per gol fatti')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(filtered['GF'], filtered['GA'], s=80, alpha=0.7, color='darkorange')
    for _, row in filtered.iterrows():
        ax.annotate(row['Team'], (row['GF'], row['GA']),
                     fontsize=7, alpha=0.7, xytext=(5, 5), textcoords='offset points')
    ax.set_xlabel('Gol fatti')
    ax.set_ylabel('Gol subiti')
    ax.set_title('Attacco vs Difesa')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

with tab3:
    avg_pts = filtered.groupby('Group')['Pts'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_pts.plot(kind='bar', color='green', alpha=0.8, ax=ax)
    ax.set_xlabel('Girone')
    ax.set_ylabel('Punti medi')
    ax.set_title('Punti medi per girone')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    st.pyplot(fig)
