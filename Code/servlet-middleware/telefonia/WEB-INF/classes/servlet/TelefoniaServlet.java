package servlet;

import java.io.*;
import java.sql.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.*;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONException;

public class TelefoniaServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private static final String DB_URL = "jdbc:postgresql://localhost:5432/telefonia";
    private static final String DB_USER = "postgres";
    private static final String DB_PASSWORD = "tua_password";

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        
        try {
            // 1. Ottieni dati da Altervista
            String jsonData = getDatiFromAltervista();
            
            // 2. Connessione al database
            Class.forName("org.postgresql.Driver");
            Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
            
            // 3. Parsing e inserimento dati
            JSONObject dati = new JSONObject(jsonData);
            inserisciDati(conn, dati);
            
            // 4. Risposta
            out.println("{\"status\": \"success\", \"message\": \"Dati importati correttamente\"}");
            
        } catch (Exception e) {
            out.println("{\"status\": \"error\", \"message\": \"" + e.getMessage() + "\"}");
        }
    }

    private String getDatiFromAltervista() throws IOException {
        URL url = new URL("http://tuodominio.altervista.org/script.php");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        
        BufferedReader reader = new BufferedReader(
            new InputStreamReader(conn.getInputStream()));
        StringBuilder response = new StringBuilder();
        String line;
        
        while ((line = reader.readLine()) != null) {
            response.append(line);
        }
        reader.close();
        
        return response.toString();
    }

    private void inserisciDati(Connection conn, JSONObject dati) throws SQLException, JSONException {
        // Verifica se l'oggetto dati contiene l'array "telefonate"
        if (!dati.has("telefonate")) {
            throw new JSONException("Il campo 'telefonate' non è presente nei dati");
        }
    
        // Inserimento telefonate con gestione più robusta
        JSONArray telefonate = dati.getJSONArray("telefonate");
        for (int i = 0; i < telefonate.length(); i++) {
            JSONObject tel = telefonate.getJSONObject(i);
            
            // Validazione dei dati richiesti
            if (!tel.has("id") || !tel.has("effettuataDa") || !tel.has("data") || 
                !tel.has("ora") || !tel.has("durata") || !tel.has("costo")) {
                throw new JSONException("Dati mancanti nella telefonata #" + i);
            }
    
            PreparedStatement pstmt = conn.prepareStatement(
                "INSERT INTO telefonata (id, effettuatada, data, ora, durata, costo) " +
                "VALUES (?, ?, ?, ?, ?, ?) " +
                "ON CONFLICT (id) DO UPDATE SET " +
                "effettuatada = EXCLUDED.effettuatada, " +
                "data = EXCLUDED.data, " +
                "ora = EXCLUDED.ora, " +
                "durata = EXCLUDED.durata, " +
                "costo = EXCLUDED.costo"
            );
            
            pstmt.setInt(1, tel.getInt("id"));
            pstmt.setString(2, tel.getString("effettuataDa"));
            pstmt.setInt(1, tel.getInt("id"));
            pstmt.setString(2, tel.getString("effettuataDa"));
            pstmt.setDate(3, Date.valueOf(tel.getString("data")));
            pstmt.setTime(4, Time.valueOf(tel.getString("ora")));
            pstmt.setInt(5, tel.getInt("durata"));
            pstmt.setDouble(6, tel.getDouble("costo"));
            
            pstmt.executeUpdate();
            pstmt.close();
        }
    }
}