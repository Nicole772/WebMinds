---
title: Installazione e avvio della servlet "TelefoniaServlet"
description: Guida all'installazione e avvio del progetto su Tomcat con PostgreSQL.

requisiti:
  - PostgreSQL
  - Java
  - Python
  - Tomcat

passaggi:

  1. Impostare le variabili d'ambiente:
    windows:
      - Aprire il Prompt dei comandi (cmd) e digitare:
        - setx DB_URL "jdbc:postgresql://localhost:5432/telefonia"
        - setx DB_USER "postgres"
        - setx DB_PASSWORD "password_del_prof"
      - Riavviare il terminale per applicare le modifiche.

    linux_mac:
      - Aprire il terminale e digitare:
        - export DB_URL="jdbc:postgresql://localhost:5432/telefonia"
        - export DB_USER="postgres"
        - export DB_PASSWORD="password_del_prof"
      - Per rendere permanenti le variabili, aggiungerle a ~/.bashrc o ~/.zshrc.

  2. Posizionare il progetto nella cartella Tomcat:
    windows:
      - Spostare la cartella del progetto "telefonia/" in:
        "C:\Program Files\Apache Software Foundation\Tomcat 9.0\webapps\telefonia\"
    linux_mac:
      - Spostare la cartella del progetto in:
        "/usr/local/tomcat/webapps/telefonia/"

  3. Compilare la servlet:
    windows:
      - Aprire un terminale nella cartella del progetto e digitare:
        javac -cp "WEB-INF/lib/*;." -d WEB-INF/classes src/servlet/TelefoniaServlet.java
    linux_mac:
      - Usare ":" invece di ";":
        javac -cp "WEB-INF/lib/*:." -d WEB-INF/classes src/servlet/TelefoniaServlet.java

  4. Avviare Tomcat:
    windows:
      - Aprire il terminale e navigare nella cartella di Tomcat:
        cd "C:\Program Files\Apache Software Foundation\Tomcat 9.0\bin"
      - Avviare Tomcat:
        startup.bat
    linux_mac:
      - Aprire il terminale e navigare nella cartella di Tomcat:
        cd /usr/local/tomcat/bin
      - Avviare Tomcat:
        ./startup.sh

  5. Testare la servlet:
    - Aprire un browser e andare su:
      http://localhost:8080/telefonia/telefonia
    - Se tutto funziona correttamente, la risposta sarà:
      {"status": "success", "message": "Dati importati correttamente"}
    - Se ci sono errori, controllare i log di Tomcat:
      windows:
        "C:\Program Files\Apache Software Foundation\Tomcat 9.0\logs\"
      linux_mac:
        "/var/log/tomcat9/"

note:
  - Se PostgreSQL ha un nome utente o una password diversa, modificare le variabili d'ambiente.
  - La servlet deve essere eseguita con PostgreSQL e Tomcat attivi.
  - Assicurarsi che il webservice su Altervista sia attivo all'URL:
    http://tuonome.altervista.org/api/webservice.php


