package servlet;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.json.JSONObject;

public class TelefoniaServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private static final String ALTERVISTA_URL = "https://webmins.altervista.org/api/webservice.php";
    private static final String DJANGO_URL = "http://127.0.0.1:8000/api/importa-dati/"; 


    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {

        response.setContentType("application/json; charset=UTF-8");
        PrintWriter out = response.getWriter();

        try {
            // 1. Recupera i dati JSON da Altervista
            String jsonData = getDatiFromAltervista();

            // 2. Log per debugging (opzionale)
            System.out.println("JSON ricevuto da Altervista: " + jsonData);

            // 3. Invia il JSON al webservice Django
            String djangoResponse = inviaDatiADjango(jsonData);

            // 4. Restituisci la risposta di Django
            out.println(djangoResponse);

        } catch (Exception e) {
            // ⚠️ Migliore gestione degli errori: messaggio più chiaro senza stack trace
            out.println("{\"status\": \"error\", \"message\": \"" + e.getMessage().replace("\"", "'") + "\"}");
        }
    }

    /**
     * Recupera il JSON dal webservice remoto ospitato su Altervista.
     * @return Il JSON come stringa.
     * @throws IOException se si verifica un errore nella connessione.
     */
    private String getDatiFromAltervista() throws IOException {
        HttpURLConnection conn = null;

        try {
            URL url = new URL(ALTERVISTA_URL);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);

            int status = conn.getResponseCode();
            if (status != HttpURLConnection.HTTP_OK) {
                throw new IOException("Errore HTTP: " + status);
            }

            // 🔹 Legge il JSON di risposta
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"))) {
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }

        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }

    /**
     * Invia il JSON ricevuto al webservice Django tramite POST.
     * @param jsonData Stringa JSON da inviare.
     * @return Risposta di Django.
     * @throws IOException se si verifica un errore.
     */
    private String inviaDatiADjango(String jsonData) throws IOException {
        HttpURLConnection conn = null;

        try {
            URL url = new URL(DJANGO_URL);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            // 🔹 Scrive i dati nel body della richiesta
            try (OutputStream os = conn.getOutputStream()) {
                os.write(jsonData.getBytes("UTF-8"));
                os.flush();
            }

            // 🔹 Legge la risposta
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"))) {
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                return response.toString();
            }

        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }
}
