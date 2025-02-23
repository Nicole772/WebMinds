# Webservice Django - Importazione dati in PostgreSQL

## Descrizione
Questo progetto implementa un webservice basato su Django che importa dati JSON ricevuti da un webservice remoto e li memorizza in un database PostgreSQL locale. Il servizio gestisce informazioni relative a contratti telefonici, SIM attive, SIM disattivate, SIM non attive e telefonate.

## Requisiti
- **Python 3.11+**
- **Django** (`pip install django`)
- **PostgreSQL** (`sudo apt install postgresql` su Linux o [download da qui](https://www.postgresql.org/download/) per Windows/Mac)
- **psycopg2** (`pip install psycopg2`)
- **Git** (per clonare il repository, opzionale)

## Installazione

1. **Clona il repository** (opzionale):
   ```sh
   git clone https://github.com/Nicole772/WebMinds.git
   cd WebMinds/Code/webservice-local
   ```


2. **Installa le dipendenze**:
   ```sh
   pip install django psycopg2
   ```

3. **Configura il database PostgreSQL**:
   - Assicurati che PostgreSQL sia installato e avviato.
   - Accedi a PostgreSQL con:
     ```sh
     psql -U postgres
     ```
   - Crea un database `Telefonia`:
     ```sql
     CREATE DATABASE Telefonia;
     ```
   - Accedi al database con:
     ```sh
     \c Telefonia
     ```
   - Crea le tabelle richieste:
     ```sql
     CREATE TABLE "ContrattoTelefonico" (
       numero VARCHAR(20) PRIMARY KEY,
       "dataAttivazione" DATE NOT NULL,
       tipo VARCHAR(50) NOT NULL,
       "minutiResidui" INT,
       "creditoResiduo" DECIMAL(10,2)
     );

     CREATE TABLE "SIMAttiva" (
       codice VARCHAR(20) PRIMARY KEY,
       "tipoSIM" VARCHAR(20) NOT NULL,
       "associataA" VARCHAR(20) REFERENCES "ContrattoTelefonico"(numero),
       "dataAttivazione" DATE NOT NULL
     );

     CREATE TABLE "SIMDisattiva" (
       codice VARCHAR(20) PRIMARY KEY,
       "tipoSIM" VARCHAR(20) NOT NULL,
       "eraAssociataA" VARCHAR(20),
       "dataAttivazione" DATE NOT NULL,
       "dataDisattivazione" DATE NOT NULL
     );

     CREATE TABLE "SIMNonAttiva" (
       codice VARCHAR(20) PRIMARY KEY,
       "tipoSIM" VARCHAR(20) NOT NULL
     );

     CREATE TABLE "Telefonata" (
       id SERIAL PRIMARY KEY,
       "effettuataDa" VARCHAR(20) NOT NULL REFERENCES "ContrattoTelefonico"(numero),
       data DATE NOT NULL,
       ora TIME NOT NULL,
       durata INT NOT NULL,
       costo DECIMAL(10,2) NOT NULL
     );
     ```

4. **Configurazione di `settings.py`**:
   - Modifica il file `settings.py` per configurare il database PostgreSQL:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'Telefonia',
             'USER': 'postgres',
             'PASSWORD': 'tuapassword',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```
   - Sostituisci `'tuapassword'` con la password effettiva dell'utente PostgreSQL.

## Avvio del server

1. **Esegui le migrazioni del database**:
   ```sh
   python manage.py migrate
   ```

2. **Esegui il server Django**:
   ```sh
   python manage.py runserver
   ```
   Il server sarà disponibile su `http://127.0.0.1:8000/`

3. **Avvia la servlet Java per l'importazione dati**:
   - Accedi a `http://localhost:8080/telefonia/telefonia` per attivare il processo di importazione dati in PostgreSQL.

   - Se la servlet non si avvia, assicurati che il server applicativo (Tomcat o altro) sia in esecuzione.

## Utilizzo del Webservice
### Endpoint principale: `/importa-dati`
- **Metodo:** `POST`
- **Formato:** JSON
- **Descrizione:** Riceve i dati dal webservice remoto e li inserisce in PostgreSQL.

#### Esempio di richiesta JSON:
```json
{
  "data": {
    "ContrattoTelefonico": [
      {
        "numero": "555754489",
        "dataAttivazione": "06/12/2024",
        "tipo": "Ricaricabile",
        "minutiResidui": 100,
        "creditoResiduo": "€10.00"
      }
    ],
    "SIMAttiva": [
      {
        "codice": "12345",
        "tipoSIM": "nano",
        "associataA": "555754489",
        "dataAttivazione": "06/12/2024"
      }
    ]
  }
}
```

#### Risposta JSON di successo:
```json
{
  "status": "success",
  "message": "Dati importati con successo"
}
```

#### Risposta JSON di errore:
```json
{
  "status": "error",
  "message": "Descrizione dell'errore"
}
```

## Test della connessione
Per verificare che il database sia accessibile, visita l'endpoint:
```
http://127.0.0.1:8000/test-connessione/
```
Se la connessione è attiva, riceverai il messaggio:
```
Connessione locale riuscita!
```

## Debug e gestione errori
- **Errori vengono registrati nel file `webservice.log`**
- **Puoi visualizzarli con:**
  ```sh
  cat webservice.log
  ```
- **Esegui query manuali per verificare i dati in PostgreSQL:**
  ```sql
  SELECT * FROM "ContrattoTelefonico";
  SELECT * FROM "SIMDisattiva";
  ```

## Conclusioni
Il webservice permette di importare dati in un database PostgreSQL garantendo consistenza e aggiornamento automatico. Se ci sono problemi, controlla `webservice.log` e verifica che il server PostgreSQL sia avviato e correttamente configurato.

