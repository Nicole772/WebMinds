# WebMinds: Gestionale per Contratti Telefonici

Benvenuti al repository del progetto **WebMinds**, un gestionale web per la gestione dei contratti telefonici, sviluppato come progetto per il corso di **Programmazione Web 2023-2024**. Questo sistema offre un'interfaccia per la gestione di dati relativi a telefonate, contratti, SIM attive, disattivate e non attive, utilizzando operazioni CRUD complete e funzionalità di ricerca avanzata.

## Descrizione del Progetto

Il progetto si basa sul database **Telefoni (Ex 2)** e implementa le seguenti caratteristiche:

- **CRUD completo**: Operazioni di Creazione, Lettura, Aggiornamento e Eliminazione per la tabella **Telefonata**.
- **Sistema di ricerca**: Filtri dinamici per esplorare i dati delle tabelle del database.
- **Interfaccia Utente**: Progettata secondo il template **Interfaccia 5**, include header, footer, navigazione e aree dedicate per filtri e risultati.
- **Palette Magenta**: Scelta dal docente come tema principale dell'interfaccia.
- **Connessione a PHPMyAdmin**: Il sito è collegato al database ospitato su Altervista per la gestione dei dati.

## Database: Contratti Telefonici

Il database rappresenta un sistema per un operatore di telefonia mobile, strutturato come segue:

- **Contratti Telefonici**: Suddivisi in contratti a ricarica (con credito residuo) e contratti a consumo (con minuti residui).
- **SIM**: Classificate come attive, disattivate o mai attivate, con tracciamento delle associazioni ai contratti.
- **Telefonate**: Ogni telefonata è identificata da un ID univoco e registra data, ora, durata e costo.

### Schema delle Tabelle
- **Telefonata**: Contiene i dettagli delle telefonate effettuate.
- **ContrattoTelefonico**: Gestisce i contratti attivi e passati.
- **SIMAttiva, SIMDisattiva, SIMNonAttiva**: Tieni traccia dello stato delle SIM.

## Funzionalità del Sito

1. **Visualizzazione dei dati**: Tutte le tabelle del database possono essere consultate attraverso interfacce grafiche intuitive.
2. **Ricerca avanzata**: I dati sono filtrabili in base a criteri specifici per ogni tabella.
3. **Collegamenti tra dati**: Dove rilevante, i dati tra le tabelle sono linkati (ad esempio, SIM associate a contratti).
4. **CRUD completo sulla tabella Telefonata**:
    - Creazione di nuove telefonate.
    - Modifica di dati esistenti.
    - Eliminazione di telefonate.
    - Visualizzazione dettagliata delle telefonate.

## Tecnologie Utilizzate

- **Frontend**: HTML, CSS, JavaScript (con focus su usabilità e palette magenta).
- **Backend**: PHP per la gestione della logica applicativa e delle connessioni al database.
- **Database**: MySQL ospitato su Altervista, accessibile tramite PHPMyAdmin.

## Esecuzione del Progetto

Il progetto è già ospitato online e accessibile tramite il seguente link:

🔗 **[WebMinds - Gestionale per Contratti Telefonici](https://webmins.altervista.org/)**

Visita il sito per esplorare tutte le funzionalità del gestionale, tra cui:
- Visualizzazione dei dati relativi a contratti, telefonate e SIM.
- Ricerca avanzata e filtraggio dei dati.
- Operazioni CRUD sulla tabella "Telefonata".
