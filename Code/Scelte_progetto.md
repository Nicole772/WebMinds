# Scelte di Progetto

## Architettura del Sistema
Il sistema è composto da tre componenti principali:
1. **Servlet Java** (eseguita su Apache Tomcat) che richiama il webservice remoto e invia i dati al webservice locale.
2. **Webservice locale Django** che riceve i dati dalla servlet, li elabora e li memorizza in PostgreSQL.
3. **Database PostgreSQL** per garantire persistenza, coerenza e integrità dei dati.

## Scelte Tecnologiche

### **1. Webservice Remoto e Acquisizione Dati**
- La servlet Java è stata scelta per effettuare la richiesta HTTP al webservice remoto su AlterVista.
- I dati vengono recuperati in formato JSON e successivamente inviati al webservice locale.
- Per la comunicazione, si utilizza `HttpURLConnection`, in grado di gestire richieste e risposte HTTP in modo efficiente.

### **2. Webservice Locale con Django**
- **Django** è stato scelto per la sua robustezza e semplicità nella gestione delle API REST.
- L’endpoint `/api/importa-dati/` riceve i dati JSON dalla servlet, li valida e li elabora.
- Il framework Django permette un’agevole gestione delle query e delle operazioni di aggiornamento/inserimento nel database PostgreSQL.

### **3. Database PostgreSQL**
- PostgreSQL è stato selezionato per la sua affidabilità nella gestione di transazioni e integrità referenziale.
- Le tabelle `ContrattoTelefonico`, `SIMAttiva`, `SIMDisattiva`, `SIMNonAttiva` e `Telefonata` vengono aggiornate utilizzando `ON CONFLICT` per evitare duplicati e garantire la coerenza.
- L'uso di vincoli `FOREIGN KEY` garantisce relazioni coerenti tra i dati.

## Gestione degli Aggiornamenti e dell'Integrità dei Dati
- I dati provenienti dal webservice remoto vengono elaborati con logiche di **upsert**, ovvero aggiornamento in caso di esistenza del record o inserimento se non presente.
- Ogni entità è stata progettata per minimizzare ridondanze e garantire un accesso rapido alle informazioni.
- Per evitare problemi di connessione o interruzioni, sono stati implementati **timeout sulle query SQL** e **log degli errori**.

## Considerazioni Finali
L’architettura scelta permette:
- **Scalabilità**: Il sistema può essere esteso facilmente aggiungendo nuove API o modificando le regole di business.
- **Affidabilità**: L’uso di PostgreSQL assicura transazioni sicure e consistenti.
- **Modularità**: I componenti (servlet, webservice locale, database) sono indipendenti, semplificando manutenzione e aggiornamenti futuri.

Queste scelte garantiscono un sistema efficiente, robusto e facilmente adattabile a esigenze future.

