


# 📌 INSTALLAZIONE E AVVIO DELLA SERVLET


---

## ✅ **REQUISITI**
Il software è stato progettato per funzionare su un sistema con i seguenti programmi già installati:
- **PostgreSQL**
- **Java (JDK 8+)**
- **Python**
- **Apache Tomcat 9.0+**

---

## 1️⃣ **CONFIGURARE LE VARIABILI D'AMBIENTE**
Prima di avviare la servlet, è necessario configurare le variabili d’ambiente per la connessione a **PostgreSQL**.

### 🔹 **Windows (Prompt dei comandi)**
Aprire **cmd** ed eseguire:
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
⚠️ **Nota**: Su Linux/macOS, queste variabili vanno rieseguite ad ogni riavvio.  
Per renderle permanenti, aggiungerle a `~/.bashrc` o `~/.zshrc`.

---

## 2️⃣ **POSIZIONARE IL PROGETTO NELLA CARTELLA DI TOMCAT**
Spostare l’intera cartella del progetto `telefonia/` in **`webapps/`** di Tomcat:

### 🔹 **Windows**
```sh
C:\Program Files\Apache Software Foundation\Tomcat 9.0\webapps\telefonia\
```

### 🔹 **Linux/macOS**
```sh
mv telefonia/ /usr/local/tomcat/webapps/
```

---

## 3️⃣ **COMPILARE LA SERVLET**

Aprire un terminale nella cartella del progetto e compilare la servlet utilizzando il comando appropriato per il proprio sistema operativo. 

### 🔹 **Windows (cmd)**
Su Windows, utilizzare il comando seguente, assicurandosi che la codifica sia impostata su UTF-8 per evitare problemi con caratteri speciali:
```sh
javac -encoding UTF-8 -cp "WEB-INF/lib/*;." -d WEB-INF/classes src/servlet/TelefoniaServlet.java
```

### 🔹 **Linux/macOS**
Su macOS e Linux, il separatore di classpath è `:` anziché `;`. Il comando corretto è:
```sh
javac -encoding UTF-8 -cp "WEB-INF/lib/*:." -d WEB-INF/classes src/servlet/TelefoniaServlet.java
```

Se si utilizza Tomcat installato tramite Homebrew su macOS, potrebbe essere necessario specificare manualmente il percorso della libreria `servlet-api.jar`, come nell'esempio seguente:
```sh
javac -encoding UTF-8 -cp "/opt/homebrew/Cellar/tomcat/11.0.4/libexec/lib/servlet-api.jar:/Library/Java/JavaVirtualMachines/openjdk.jdk/Contents/Home/lib/*:." -d ../WEB-INF/classes/ servlet/TelefoniaServlet.java
```

Se la compilazione è riuscita, il file `TelefoniaServlet.class` sarà generato in:
```sh
WEB-INF/classes/servlet/TelefoniaServlet.class
```


---
## 🚨 **IMPORT NECESSARI PER TOMCAT 10+**
Se si utilizza **Tomcat 10 o superiore**, è necessario aggiornare gli import nella servlet per usare il package `jakarta.servlet` anziché `javax.servlet`. Ecco gli import corretti:

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
```


---

## 4️⃣ **AVVIARE TOMCAT**
Aprire un terminale e navigare nella cartella di **Tomcat**:

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

## 5️⃣ **TESTARE LA SERVLET**
Aprire un browser e digitare:
```
http://localhost:8080/telefonia/telefonia
```
Se la servlet funziona correttamente, si otterrà una risposta simile:
```json
{"status": "success", "message": "Dati importati correttamente"}
```

Se ci sono errori, controllare i log di Tomcat:
- **Windows**: `C:\Program Files\Apache Software Foundation\Tomcat 9.0\logs\`
- **Linux/macOS**: `/var/log/tomcat9/`

---

🔹 Risoluzione problemi

Errore: ClassNotFoundException: org.postgresql.Driver

🔹 Soluzione: Assicurarsi che il driver PostgreSQL (postgresql.jar) sia presente in WEB-INF/lib/.

Errore: 404 Not Found

🔹 Soluzione: Verificare che la servlet sia mappata correttamente in web.xml.

📌 Note importanti

Se PostgreSQL ha credenziali diverse, aggiornare le variabili d’ambiente.

Tomcat e PostgreSQL devono essere attivi prima di eseguire la servlet.

In caso di problemi, consultare i log di sistema per diagnosticare errori specifici.




