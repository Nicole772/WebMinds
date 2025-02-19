<?php
// Abilita la visualizzazione degli errori per il debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Parametri di connessione al database
$servername = "localhost";
$username = "webmins";
$password = "";
$dbname = "my_webmins";

// Creazione della connessione al database
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die(json_encode(['success' => false, 'error' => 'Connessione al database fallita']));
}

// Imposta gli header per JSON e CORS
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Funzione per ottenere i dati dalle tabelle
function getDatabaseData() {
    global $conn;
    $data = [];
    
    // Query per Telefonata
    $query_telefonata = "SELECT id, effettuataDa, DATE_FORMAT(data, '%d/%m/%Y') as data, 
                         ora, durata, costo FROM Telefonata";
    $result = $conn->query($query_telefonata);
    $data['Telefonata'] = [];
    while($row = $result->fetch_assoc()) {
        $data['Telefonata'][] = $row;
    }
    
    // Query per ContrattoTelefonico
    $query_contratto = "SELECT numero, DATE_FORMAT(dataAttivazione, '%d/%m/%Y') as dataAttivazione, 
                        tipo, minutiResidui, creditoResiduo FROM ContrattoTelefonico";
    $result = $conn->query($query_contratto);
    $data['ContrattoTelefonico'] = [];
    while($row = $result->fetch_assoc()) {
        $data['ContrattoTelefonico'][] = $row;
    }
    
    // Query per SIMAttiva
    $query_sim_attiva = "SELECT codice, tipoSIM, associataA, 
                         DATE_FORMAT(dataAttivazione, '%d/%m/%Y') as dataAttivazione 
                         FROM SIMAttiva";
    $result = $conn->query($query_sim_attiva);
    $data['SIMAttiva'] = [];
    while($row = $result->fetch_assoc()) {
        $data['SIMAttiva'][] = $row;
    }
    
    // Query per SIMDisattiva
    $query_sim_disattiva = "SELECT codice, tipoSIM, eraAssociataA, 
                           DATE_FORMAT(dataAttivazione, '%d/%m/%Y') as dataAttivazione,
                           DATE_FORMAT(dataDisattivazione, '%d/%m/%Y') as dataDisattivazione 
                           FROM SIMDisattiva";
    $result = $conn->query($query_sim_disattiva);
    $data['SIMDisattiva'] = [];
    while($row = $result->fetch_assoc()) {
        $data['SIMDisattiva'][] = $row;
    }
    
    // Query per SIMNonAttiva
    $query_sim_non_attiva = "SELECT codice, tipoSIM FROM SIMNonAttiva";
    $result = $conn->query($query_sim_non_attiva);
    $data['SIMNonAttiva'] = [];
    while($row = $result->fetch_assoc()) {
        $data['SIMNonAttiva'][] = $row;
    }
     
    return $data;
}

function formatData($data) {
    foreach ($data as $tableName => &$records) {
        foreach ($records as &$record) {
            // Formatta i valori monetari con due decimali fissi
            if (isset($record['costo'])) {
                $record['costo'] = '€ ' . number_format((float)$record['costo'], 2, ',', '.');
            }
            if (isset($record['creditoResiduo'])) {
                $record['creditoResiduo'] = '€ ' . number_format((float)$record['creditoResiduo'], 2, ',', '.');
            }
            
            // Formatta la durata in formato mm:ss
            if (isset($record['durata'])) {
                $minuti = floor((int)$record['durata'] / 60);
                $secondi = (int)$record['durata'] % 60;
                $record['durata'] = sprintf("%02d:%02d", $minuti, $secondi);
            }
            
            // Formatta l'ora in formato HH:mm
            if (isset($record['ora'])) {
                $time = DateTime::createFromFormat('H:i:s', $record['ora']);
                if ($time) {
                    $record['ora'] = $time->format('H:i');
                }
            }
        }
    }
    return $data;
}

// Gestione della richiesta
try {
    $result = getDatabaseData();
    $result = formatData($result);
    echo json_encode(['success' => true, 'data' => $result]);
} catch (Exception $e) {
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}


// Chiusura della connessione al database
$conn->close();
?>
