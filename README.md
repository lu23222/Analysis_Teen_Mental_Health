# Analysis_Teen_Mental_Health
Un'applicazione web interattiva sviluppata con Streamlit per eseguire un'analisi esplorativa dei dati (EDA) approfondita e calcolare statistiche descrittive. Questo strumento fornisce un'interfaccia intuitiva per analizzare dati tabulari, visualizzare le distribuzioni ed esplorare le relazioni tra le variabili senza dover scrivere codice.

Attualmente, il progetto è configurato per analizzare un dataset di esempio (Teen_Mental_Health_Dataset.csv), caricando le prime 150 righe, ma può essere facilmente adattato a qualsiasi file CSV personalizzato.


🌟 Funzionalità
L'applicazione è suddivisa in quattro sezioni analitiche principali:


	Visualizzatore Dati Interattivo: Un dataframe espandibile e modificabile che permette all'utente di visualizzare e alterare i dati caricati in tempo reale.

	Sintesi Statistica: Calcola e mostra indicatori statistici completi per una variabile selezionata, tra cui:


	Tendenza Centrale: Media, Mediana, Moda.

	Dispersione: Varianza, Deviazione Standard, Scarto Medio Assoluto, Ampiezza del campo di variazione, Coefficiente di Variazione (CV).

	Forma: Asimmetria (Skewness) e Curtosi (con interpretazioni testuali).

	Posizione e Intervalli: Quartili (Q1, Q3), Scarto Interquartile (IQR), limiti per la ricerca degli Outlier e intervalli basati sulla disuguaglianza di Chebyshev.

	Analisi Univariata: Visualizza la distribuzione di una singola variabile attraverso:


	Istogrammi (Frequenza assoluta, relativa e cumulativa).

	Grafici di Densità (KDE).

	Box Plot.

	Grafici a torta basati su intervalli di classe (bin) definiti dall'utente.

	Analisi Bivariata: Esplora la relazione tra due variabili selezionate:


	Coefficiente di Correlazione di Pearson (r) con interpretazione automatica.

	Diagrammi a dispersione (Scatter Plot) e Grafici a linee.

	Modelli di Regressione Lineare (Scatter plot con la retta di regressione stimata e la sua equazione matematica).

	Tabelle di Frequenza: Genera tabelle strutturate che mostrano le frequenze assolute, relative e cumulative basate su intervalli di classe dinamici.

🛠️ Tecnologie Utilizzate
	Python 3.x

	Streamlit: Per la creazione dell'interfaccia web interattiva.

	Pandas & NumPy: Per la manipolazione dei dati e i calcoli matematici.

	Matplotlib & Seaborn: Per la generazione di grafici statistici di alta qualità.

🚀 Installazione e Configurazione
Per eseguire questo progetto in locale sul tuo computer, segui questi passaggi:


	Clona la repository:


Bash
git clone https://github.com/TuoNomeUtente/NomeDelTuoProgetto.git
cd NomeDelTuoProgetto
	Crea un ambiente virtuale:


Bash
python -m venv venv
source venv/bin/activate  # Su Windows usa: venv\Scripts\activate
	Installa le dipendenze richieste:
Assicurati di avere un file requirements.txt, oppure installa le librerie direttamente con:


Bash
pip install streamlit pandas numpy matplotlib seaborn
	Aggiungi il dataset:
Assicurati che il file Teen_Mental_Health_Dataset.csv si trovi nella cartella principale (root) del progetto.

	Avvia l'applicazione Streamlit:


Bash
streamlit run app.py
(Sostituisci app.py con il nome effettivo del tuo script Python).

📊 Utilizzo
	Apri l'URL localhost fornito dal terminale nel tuo browser web.

	Usa il Pannello di Controllo in alto per selezionare le variabili che desideri analizzare.

	Regola lo Slider per modificare il numero di classi (intervalli) per gli istogrammi e le tabelle di frequenza.

	Naviga attraverso le Schede (Tabs) per passare dalla sintesi statistica ai grafici univariati, bivariati e ai dati di frequenza.
