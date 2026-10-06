import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Analisi Statistica", layout="wide")

sns.set_style('whitegrid')
sns.set_context('talk', font_scale=0.9)
colori_azzurro_arancione = ['#3498db', '#e67e22', '#85c1e9', '#f39c12', '#2980b9']
sns.set_palette(sns.color_palette(colori_azzurro_arancione))

st.markdown("<h1 style='text-align: center; color: #2980b9; font-family: \"Comic Sans MS\", cursive;'>Analisi Statistica</h1>", unsafe_allow_html=True)
st.divider()

df = pd.read_csv("Teen_Mental_Health_Dataset.csv",nrows=150)

with st.expander("Dataset", expanded=False):
    edited_df = st.data_editor(df, use_container_width=True)

#Pannello di Controllo 
numeric_cols = edited_df.select_dtypes(include='number').columns.tolist()

col1, col2, col3, col4 = st.columns(4)
with col1:
    col = st.selectbox("Variabile Univariata", numeric_cols, help="Colonna per istogrammi, boxplot e indici singoli")
with col2:
    num_bins = st.slider("Numero di Classi (Intervalli)", min_value=3, max_value=10, value=5)
with col3:
    col_x = st.selectbox("Asse X (Bivariata)", numeric_cols, index=0)
with col4:
    col_y = st.selectbox("Asse Y (Bivariata)", numeric_cols, index=1 if len(numeric_cols)>1 else 0)

st.divider()

#Calcoli
mediaCampionaria = edited_df[col].mean()
medianaCampionaria = edited_df[col].median()
modaCampionaria = edited_df[col].mode().tolist()
devStandard = edited_df[col].std()
varCampionaria = edited_df[col].var()
amp = edited_df[col].max() - edited_df[col].min()
coeff = devStandard / mediaCampionaria if mediaCampionaria != 0 else 0
skew = edited_df[col].skew() 
kurt = edited_df[col].kurt()
q1 = edited_df[col].quantile(0.25)
q3 = edited_df[col].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
k = 2 
chebyshev_lower = mediaCampionaria - k * devStandard
chebyshev_upper = mediaCampionaria + k * devStandard

def scartoMedioAssoluto(col_series):
    return (col_series - mediaCampionaria).abs().mean()


interpret_cv = "Bassa variabilità relativa" if coeff <= 0.2 else "Variabilità moderata" if coeff <= 0.5 else "Alta variabilità relativa"
interpret_skew = "Asimmetria positiva" if skew >= 0 else "Asimmetria negativa"
interpret_kurt = "Distribuzione leptocurtica (eccesso al centro)" if kurt > 0 else "Distribuzione platicurtica (carenza al centro)" if kurt < 0 else "Distribuzione normocurtica"

corr = edited_df[[col_x, col_y]].corr().iloc[0,1]
interpret_corr = "Bassa correlazione" if abs(corr) <= 0.3 else "Correlazione moderata" if abs(corr) <= 0.8 else "Alta correlazione"
interpret_corr += " e diretta (positiva)" if corr > 0 else " e inversa (negativa)" if corr < 0 else " e nulla"

class_intervals = pd.cut(edited_df[col], bins=num_bins)
edited_df['classi_'+col] = class_intervals

tab_stat, tab_univ, tab_biv, tab_freq = st.tabs([
    "Sintesi Statistica", 
    "Analisi Univariata", 
    "Analisi Bivariata", 
    "Tabelle di Frequenza"
])

#TAB 1: SINTESI STATISTICA
with tab_stat:
    st.markdown(f"### Indici principali per la variabile: **{col}**")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Media", f"{mediaCampionaria:.2f}")
    m2.metric("Mediana", f"{medianaCampionaria:.2f}")
    m3.metric("Dev. Standard", f"{devStandard:.2f}")
    m4.metric("IQR", f"{iqr:.2f}") #scarto interquantile, serve per il boxplot
    
    #per avere piu spazio
    st.markdown("<br>", unsafe_allow_html=True)
    
    dettaglio1, dettaglio2 = st.columns(2)
    
    with dettaglio1:
        with st.expander("Indici di Posizione e Forma", expanded=True):
            st.markdown(rf"**Media:** $\overline{{x}} = {mediaCampionaria:.4f}$")
            st.markdown(rf"**Mediana:** ${medianaCampionaria:.4f}$")
            st.markdown(f"**Moda:** {modaCampionaria}")
            st.markdown(f"**Asimmetria (Skewness):** {skew:.4f} → _{interpret_skew}_")
            st.markdown(f"**Curtosi:** {kurt:.4f} → _{interpret_kurt}_")

        with st.expander("Quartili e Intervalli", expanded=True):
            st.markdown(rf"**1° Quartile (Q1):** ${q1:.4f}$ | **3° Quartile (Q3):** ${q3:.4f}$")
            st.markdown(rf"**IQR:** ${iqr:.4f}$")
            st.markdown(rf"**Intervallo basato su IQR:** $[{lower_bound:.2f}, \; {upper_bound:.2f}]$")
            st.markdown(rf"**Disuguaglianza Chebyshev ($k={k}$):** $[{chebyshev_lower:.2f}, \; {chebyshev_upper:.2f}]$")

    with dettaglio2:
        with st.expander("Indici di Variabilità", expanded=True):
            st.markdown(rf"**Varianza ($s^2$):** ${varCampionaria:.4f}$")
            st.markdown(rf"**Dev. Standard ($s$):** ${devStandard:.4f}$")
            st.markdown(rf"**Scarto Medio Assoluto:** ${scartoMedioAssoluto(edited_df[col]):.4f}$")
            st.markdown(rf"**Ampiezza:** ${amp:.4f}$")
            st.markdown(rf"**Coeff. Variazione (CV):** ${coeff:.4f}$ → _{interpret_cv}_")
            
        with st.expander("Riepilogo Tabellare (Dataframe)", expanded=False):
            descrittivi = pd.DataFrame({
                "Valore": [mediaCampionaria, medianaCampionaria, devStandard, varCampionaria, 
                           scartoMedioAssoluto(edited_df[col]), amp, coeff, skew, kurt, q1, q3, iqr]
            }, index=["Media", "Mediana", "Deviazione standard", "Varianza", "Scarto medio assoluto",
                      "Ampiezza campo variazione", "Coefficiente di variazione", "Asimmetria (skewness)", 
                      "Curtosi", "Q1", "Q3", "IQR"])
            st.dataframe(descrittivi.style.background_gradient(cmap="Blues"), use_container_width=True)

#TAB 2: ANALISI UNIVARIATA
with tab_univ:
    st.markdown(f"### Visualizzazione della distribuzione: **{col}**")
    
    # Prima riga di grafici
    g1, g2 = st.columns(2)
    with g1:
        st.write("**Istogramma (Frequenza Assoluta)**")
        fig, ax = plt.subplots(figsize=(6,4)) 
        sns.histplot(edited_df[col], bins=num_bins, color="#3498db")
        st.pyplot(fig)
        
        st.write("**Densità (KDE plot)**")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.kdeplot(data=edited_df[col].dropna(), color='#e67e22', fill=True, ax=ax)
        st.pyplot(fig)

    with g2:
        st.write("**Istogramma (Freq. Assoluta Cumulativa)**")
        fig, ax = plt.subplots(figsize=(6,4)) 
        sns.histplot(edited_df[col], bins=num_bins, color="#85c1e9", cumulative=True)
        st.pyplot(fig)
        
        st.write("**Box Plot**")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.boxplot(y=edited_df[col].dropna(), color="#f39c12", ax=ax)
        st.pyplot(fig)

    # Seconda riga
    g3, g4 = st.columns(2)
    with g3:
        st.write("**Istogramma (Frequenza Relativa)**")
        fig, ax = plt.subplots(figsize=(6,4)) 
        sns.histplot(edited_df[col], bins=num_bins, color="#3498db", stat="probability")
        st.pyplot(fig)

    with g4:
        st.write("**Grafico a torta (Distribuzione in classi)**")
        fig, ax = plt.subplots(figsize=(6,4)) 
        class_counts = edited_df['classi_'+col].value_counts()
        ax.pie(class_counts, autopct='%1.1f%%', 
               startangle=90, colors=colori_azzurro_arancione, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
        st.pyplot(fig)

#TAB 3: ANALISI BIVARIATA
with tab_biv:
    st.markdown(f"### Relazione tra **{col_x}** (X) e **{col_y}** (Y)")
    
    st.info(rf"**Correlazione di Pearson ($r$):** {corr:.4f} → {interpret_corr}")
    
    b1, b2 = st.columns(2)
    with b1:
        st.write("**Diagramma a dispersione (Scatter Plot)**")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.scatterplot(x=edited_df[col_x], y=edited_df[col_y], color='#2980b9', s=60, ax=ax)
        st.pyplot(fig)#funzione per la stampa
        
        st.write("**Grafico a linee**")
        fig, ax = plt.subplots(figsize=(6,4)) 
        sns.lineplot(data=edited_df, x=col_x, y=col_y, color="#e67e22")
        st.pyplot(fig)

    with b2:
        st.write("**Retta di regressione stimata**")
        x_vals = edited_df[col_x].dropna()
        y_vals = edited_df[col_y].dropna()
        
        valid_idx = x_vals.index.intersection(y_vals.index)
        if len(valid_idx) > 1:
            slope, intercept = np.polyfit(x_vals[valid_idx], y_vals[valid_idx], 1)
            st.latex(f"\\hat{{y}} = {intercept:.2f} + {slope:.2f} \\cdot x")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.regplot(data=edited_df, x=col_x, y=col_y, color="#3498db", scatter_kws={'alpha':0.5})
        st.pyplot(fig)

#TAB 4: TABELLE DI FREQUENZA
with tab_freq:
    st.markdown(f"### Tabella delle Frequenze per: **{col}**")
    st.write(f"Dati raggruppati in {num_bins} classi.")
    
    freq_assoluta = class_intervals.value_counts().sort_index()
    freq_relat = freq_assoluta / freq_assoluta.sum()
    
    freq_table = pd.DataFrame({
        "Freq. Assoluta": freq_assoluta,
        "Freq. Relativa": freq_relat.round(3),
        "Freq. Assoluta Cumulativa": freq_assoluta.cumsum(),
        "Freq. Relativa Cumulativa": freq_relat.cumsum().round(3)
    })
    
    st.dataframe(freq_table.style.highlight_max(subset=['Freq. Assoluta'], color='#f39c12'), use_container_width=True)