# 📌 INSTALLAZIONE E AVVIO DELLA SERVLET

## ✅ **Introduzione**
Questo documento fornisce istruzioni dettagliate su come installare e avviare la servlet Java per la gestione della migrazione dei dati. Il servizio si occupa di recuperare i dati dal webservice remoto, processarli e inserirli in un database PostgreSQL locale.

## ✅ **Requisiti**
Prima di procedere, assicurarsi di avere installato:
- **PostgreSQL**
- **Java (JDK 8+)**
- **Python**
- **Apache Tomcat 9.0+**

Se uno di questi componenti non è installato, seguire la documentazione ufficiale per l'installazione.

---

## 1️⃣ **Configurare le variabili d'ambiente**
Prima di avviare la servlet, configurare le variabili d’ambiente per la connessione a **PostgreSQL**.

### 🔹 **Windows (Prompt dei comandi)**
```sh
setx DB_URL "jdbc:postgresql://localhost:5432/telefonia"
setx DB_USER "postgres"
setx DB_PASSWORD "password"
```
Chiudere e riaprire il terminale per applicare le modifiche.

### 🔹 **Linux/macOS (Terminale)**
```sh
export DB_URL="jdbc:postgresql://localhost:5432/telefonia"
export DB_USER="postgres"
export DB_PASSWORD="password"
```
⚠️ **Nota**: Per rendere le variabili permanenti, aggiungerle a `~/.bashrc` o `~/.zshrc`.

---

## 2️⃣ **Posizionare il progetto nella cartella di Tomcat**
Spostare la cartella `telefonia/` in **`webapps/`** di Tomcat:

### 🔹 **Windows**
```sh
move telefonia "C:\Program Files\Apache Software Foundation\Tomcat 9.0\webapps\"
```

### 🔹 **Linux/macOS**
```sh
mv telefonia/ /usr/local/tomcat/webapps/
```

---

## 3️⃣ **Compilare la servlet**

Aprire un terminale nella cartella del progetto e compilare la servlet.

### 🔹 **Windows (cmd)**
```sh
javac -encoding UTF-8 -cp "WEB-INF/lib/*;." -d WEB-INF/classes src/servlet/TelefoniaServlet.java
```

### 🔹 **Linux/macOS**
```sh
javac -encoding UTF-8 -cp "WEB-INF/lib/*:." -d WEB-INF/classes src/servlet/TelefoniaServlet.java
```

Se si utilizza Tomcat installato tramite Homebrew su macOS:
```sh
javac -encoding UTF-8 -cp "/opt/homebrew/Cellar/tomcat/11.0.4/libexec/lib/servlet-api.jar:/Library/Java/JavaVirtualMachines/openjdk.jdk/Contents/Home/lib/*:." -d ../WEB-INF/classes/ servlet/TelefoniaServlet.java
```

Se la compilazione è riuscita, il file `TelefoniaServlet.class` sarà generato in:
```sh
WEB-INF/classes/servlet/TelefoniaServlet.class
```

---

## 🚨 **Import necessari per Tomcat 10+**
Se si utilizza **Tomcat 10 o superiore**, aggiornare gli import nella servlet per usare `jakarta.servlet` anziché `javax.servlet`.
```java
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
```

---

## 4️⃣ **Avviare Tomcat**
Aprire un terminale e avviare Tomcat:

### 🔹 **Windows**
```sh
cd "C:\Program Files\Apache Software Foundation\Tomcat 9.0\bin"
startup.bat
```

### 🔹 **Linux/macOS**
```sh
cd /usr/local/tomcat/bin
./startup.sh
```

---

## 5️⃣ **Testare la servlet**
Aprire un browser e digitare:
```
http://localhost:8080/telefonia/telefonia
```
Se la servlet funziona correttamente, si otterrà:
```json
{"status": "success", "message": "Dati importati correttamente"}
```

Se ci sono errori, controllare i log di Tomcat:
- **Windows**: `C:\Program Files\Apache Software Foundation\Tomcat 9.0\logs\`
- **Linux/macOS**: `/var/log/tomcat9/`

---

## 🔹 **Risoluzione problemi**
### Errore: `ClassNotFoundException: org.postgresql.Driver`
🔹 **Soluzione**: Assicurarsi che il driver PostgreSQL (`postgresql.jar`) sia presente in `WEB-INF/lib/`.

### Errore: `404 Not Found`
🔹 **Soluzione**: Verificare che la servlet sia mappata correttamente in `web.xml`.

---

## 📌 **Note importanti**
- Se **PostgreSQL ha credenziali diverse**, aggiornare le variabili d’ambiente.
- **Tomcat e PostgreSQL devono essere attivi** prima di eseguire la servlet.
- In caso di problemi, consultare i log di sistema per diagnosticare errori specifici.

