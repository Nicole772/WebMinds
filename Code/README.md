# 📂 WebMinds - Codice dei Servizi  

Questa directory contiene il codice dei principali servizi che compongono il progetto **WebMinds**, un gestionale per la gestione dei contratti telefonici. Ogni cartella al suo interno corrisponde a un servizio specifico, necessario per il corretto funzionamento del sistema.  

## 📌 Struttura delle Cartelle  

- **`webservice-local/`** - Contiene il codice del webservice basato su Django, che riceve i dati dalla servlet e li memorizza in un database PostgreSQL locale.  
  - 🔗 **[Guida all'installazione](https://github.com/Nicole772/WebMinds/blob/main/Code/webservice-local/README.md)**  

- **`servlet-middleware/`** - Contiene la servlet Java che agisce da intermediario tra il webservice remoto e il webservice locale, gestendo la migrazione dei dati.  
  - 🔗 **[Guida all'installazione](https://github.com/Nicole772/WebMinds/blob/main/Code/servlet-middleware/README.md)**  

- **`webservice-remote/`** *(eventuale, se presente)* - Contiene il webservice remoto in PHP che espone i dati archiviati nel database online.  

## ⚙️ Installazione  

Per installare e configurare correttamente il sistema, seguire l'ordine indicato:  

1️⃣ **Installare il Webservice Locale**  
   - Seguire le istruzioni nel README dedicato:  
     [Guida all'installazione](https://github.com/Nicole772/WebMinds/blob/main/Code/webservice-local/README.md)  

2️⃣ **Installare la Servlet Middleware**  
   - Seguire le istruzioni nel README dedicato:  
     [Guida all'installazione](https://github.com/Nicole772/WebMinds/blob/main/Code/servlet-middleware/README.md)  

Se sono necessarie ulteriori configurazioni, fare riferimento ai README presenti nelle singole cartelle.  

---

