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

// Verifica della connessione
if ($conn->connect_error) {
    die("Connessione fallita: " . $conn->connect_error);
}
/////////////////////////////////////////////////////////////////////
//Caricamento tabella Contratti Telefonici
//Caricamento tabella Contratti Telefonici
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'loadContracts') {

     $numero_telefono = $_POST['numero_telefono'] ?? ''; 
    $tipo_contratto = $_POST['tipo_contratto'] ?? '';  // Per il tipo di contratto
    $associata_a = $_POST['associata_a'] ?? '';  // Per la SIM associata
    $filtro_attivo = $_POST['filtro_attivo'] ?? false;

       $sql = "SELECT 
                ct.numero, 
                ct.dataAttivazione, 
                ct.tipo, 
                ct.minutiResidui, 
                ct.creditoResiduo,
                sa.codice AS codiceSim
            FROM ContrattoTelefonico ct
            LEFT JOIN SIMAttiva sa ON ct.numero = sa.associataA
            WHERE 1=1";  // Condizione di base che non limita ancora i risultati

if ($filtro_attivo)
{
	// Filtri dinamici
    if (!empty($numero_telefono)) {
        $sql .= " AND ct.numero LIKE '%$numero_telefono%'";  // Filtro per numero telefono
    }

    if (!empty($tipo_contratto)) {
        $sql .= " AND ct.tipo = '$tipo_contratto'";  // Filtro per tipo contratto
    }

    if (!empty($associata_a)) {
        $sql .= " AND sa.codice LIKE '%$associata_a%'";  // Filtro per SIM associata
    }
}

    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $row["numero"] . "</td>";
            echo "<td>" . $row["dataAttivazione"] . "</td>";
            echo "<td>" . ($row["tipo"] ? $row["tipo"] : '') . "</td>";
            echo "<td>" . ($row["creditoResiduo"] ? $row["creditoResiduo"] . "€" : '') . "</td>";
            echo "<td>" . ($row["minutiResidui"] ? $row["minutiResidui"] . "m" : '') . "</td>";
            echo "<td>" . ($row["codiceSim"] ? $row["codiceSim"] : '') . "</td>"; 
            echo "</tr>";
        }
    } else {
        echo "<tr><td colspan='6'>Nessun contratto trovato.</td></tr>";
    }
    exit;
}

//--------------------------------CARICAMENTO TELEFONATE--------------------------------
// Carica le chiamate effettuate
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'loadCalls') {

    // Ottieni il numero di telefono se è stato fornito
    $numero_telefono = $_POST['numero_telefono'] ?? '';

    $sql = "
        SELECT 
            t.id, 
            t.effettuataDa, 
            t.data, 
            t.ora, 
            t.durata, 
            t.costo, 
            CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM SIMDisattiva sd 
                    WHERE sd.eraAssociataA = t.effettuataDa
                ) THEN 1
                ELSE 0
            END AS isDisattivata
        FROM Telefonata t
        WHERE 1=1";

    // Filtro per il numero di telefono se fornito
    if (!empty($numero_telefono)) {
        $sql .= " AND t.effettuataDa LIKE '%$numero_telefono%'";
    }
	
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            // Segno in rosso (rivedere
            $rowClass = $row['isDisattivata'] == 1 ? 'sim-disattivata' : '';

            echo "<tr class='$rowClass'>";
            echo "<td>" . $row["id"] . "</td>";
            echo "<td>" . $row["effettuataDa"] . "</td>";
            echo "<td>" . $row["data"] . "</td>";
            echo "<td>" . $row["ora"] . "</td>";
            echo "<td>" . ($row["durata"] ? $row["durata"] . "m" : '') . "</td>";
            echo "<td>" . ($row["costo"] ? $row["costo"] . "€" : '') . "</td>";
            echo "<td>
                    <button class='action-btn delete-call-btn' data-tooltip='Elimina telefonata' data-id='" . $row['id'] . "'>
                        <i class='fa-solid fa-trash-can'></i>
                    </button>

                <button class='action-btn edit-call-btn' 
                        data-tooltip='Modifica telefonata'
                        onclick='handleEditClick(this)'
                        data-id='" . $row['id'] . "'
                        data-numero='" . $row['effettuataDa'] . "'
                        data-data='" . $row['data'] . "'
                        data-ora='" . $row['ora'] . "'
                        data-durata='" . $row['durata'] . "'
                        data-tipo='" . ($row['tipo'] ?? "-") . "'
                        data-minuti='" . ($row['minutiResidui'] ?? "-") . "'
                        data-credito='" . ($row['creditoResiduo'] ?? "-") . "'>
                    <i class='fas fa-edit'></i>
                </button>

                  </td>";
            echo "</tr>";
        }
    } else {
        echo "<tr><td colspan='6'>Nessuna telefonata trovata.</td></tr>";
    }
    exit;
}



//--------------------------------UPDATE TELEFONATA--------------------------------
if (isset($_POST['action']) && $_POST['action'] === 'editCall') {
    try {
        if (!isset($_POST['id']) || !isset($_POST['numero']) || !isset($_POST['data']) || 
            !isset($_POST['ora']) || !isset($_POST['durata'])) {
            throw new Exception('Dati mancanti per la modifica della chiamata');
        }

        $id = $_POST['id'];
        $numero = $_POST['numero'];
        $data = $_POST['data'];
        $ora = $_POST['ora'];
        $durata = $_POST['durata'];
        $costo = 0;

        $stmt = $conn->prepare("UPDATE Telefonata 
                              SET effettuataDa = ?, 
                                  data = ?, 
                                  ora = ?, 
                                  durata = ?, 
                                  costo = ?
                              WHERE id = ?");
        
        $stmt->bind_param("ssssdi", $numero, $data, $ora, $durata, $costo, $id);
        
        if ($stmt->execute()) {
            echo json_encode([
                'success' => true,
                'message' => 'Chiamata aggiornata con successo'
            ]);
        } else {
            throw new Exception($stmt->error);
        }

    } catch (Exception $e) {
        echo json_encode([
            'success' => false,
            'message' => $e->getMessage()
        ]);
    }
    exit;
}

//--------------------------------OTTENIMENTO DATI TELEFONATA PER MODIFICA--------------------------------
if(isset($_POST['action']) && $_POST['action'] === 'getCallData') {
    $id = mysqli_real_escape_string($conn, $_POST['callId']);
    
    $query = "SELECT c.*, n.tipo_contratto, n.minuti_residui, n.credito_residuo 
              FROM chiamate c 
              LEFT JOIN numeri n ON c.numero = n.numero 
              WHERE c.id = ?";
    
    // Esegui la query con prepared statement
    $stmt = $conn->prepare($query);
    $stmt->bind_param("i", $callId);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($row = $result->fetch_assoc()) {
        // Formatta i dati
        $data = [
            'id' => $row['id'],
            'numero' => $row['numero'],
            'data' => date('Y-m-d', strtotime($row['data'])),
            'ora' => date('H:i', strtotime($row['ora'])),
            'durata' => $row['durata'],
            'tipo_contratto' => $row['tipo_contratto'],
            'minuti_residui' => $row['minuti_residui'],
            'credito_residuo' => $row['credito_residuo']
        ];
        
        echo json_encode($data);
    } else {
        echo json_encode(['error' => 'Chiamata non trovata']);
    }
    exit;
}

// Salva modifiche telefonata
if(isset($_POST['action']) && $_POST['action'] === 'editCall') {
    $id = mysqli_real_escape_string($conn, $_POST['callId']);
    $numero = mysqli_real_escape_string($conn, $_POST['numero']);
    $data = mysqli_real_escape_string($conn, $_POST['data']);
    $ora = mysqli_real_escape_string($conn, $_POST['ora']);
    $durata = mysqli_real_escape_string($conn, $_POST['durata']);
    
    $query = "UPDATE telefonata SET 
              id_numero='$numero', 
              data='$data', 
              ora='$ora', 
              durata='$durata' 
              WHERE id=$id";
              
    if(mysqli_query($conn, $query)) {
        echo 1;
    } else {
        echo 0;
    }
    exit;
}



//////////////////////////////////////////////////////////////
// Gestione caricamento dei numeri dei contratti telefonici non associati ad una sim
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'loadNumber') {

    $sql = "SELECT numero FROM ContrattoTelefonico WHERE numero NOT IN (SELECT associataA FROM SIMAttiva)";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // Opzioni per il menù a tendina
        while ($row = $result->fetch_assoc()) {
            echo '<option value="' . $row['numero'] . '">' . $row['numero'] . '</option>';
        }
    } else {
        echo '<option value="">Nessun contratto disponibile</option>';
    }
    exit;
}

// Gestione inserimento di una nuova SIM
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'addSim') {
    $tipoSIM = $_POST['tipoSIM'];
    $contratto = $_POST['contratto']; // Il contratto selezionato

    // Funzione per generare un codice unico per la SIM
    function generateUniqueCode($conn) {
        do {
            // Genera un codice casuale tra 1 e 100
            $newCode = rand(1, 100);

            // Controlla se il codice esiste in una delle tre tabelle
            $sql_check = "
                SELECT codice FROM SIMAttiva WHERE codice = '$newCode'
                UNION
                SELECT codice FROM SIMDisattiva WHERE codice = '$newCode'
                UNION
                SELECT codice FROM SIMNonAttiva WHERE codice = '$newCode'
            ";
            $result = $conn->query($sql_check);
        } while ($result->num_rows > 0); // Ripeti finché trovi un codice unico

        return $newCode;
    }


    $simCode = generateUniqueCode($conn);

    // Se è stato selezionato un contratto, inserisci la SIM in SIMAttiva e aggiorna ContrattoTelefonico
    if ($contratto) {
        // Aggiorna il contratto con la data di attivazione
        $dataAttivazione = date('Y-m-d'); // Data di attivazione (oggi)
        $updateSql = "UPDATE ContrattoTelefonico SET dataAttivazione = '$dataAttivazione' WHERE numero = '$contratto'";
        $conn->query($updateSql);

        // Inserisci la nuova SIM in SIMAttiva
        $insertSql = "INSERT INTO SIMAttiva (codice, tipoSIM, associataA, dataAttivazione) VALUES ('$simCode', '$tipoSIM', '$contratto', '$dataAttivazione')";
        if ($conn->query($insertSql) === TRUE) {
            echo "SIM aggiunta con successo. Codice: $simCode";
        } else {
            echo "Errore durante l'aggiunta della SIM: " . $conn->error;
        }
    } else {
        // Se nessun contratto è selezionato, inserisci la SIM in SIMNonAttiva
        $insertSql = "INSERT INTO SIMNonAttiva (codice, tipoSIM) VALUES ('$simCode', '$tipoSIM')";
        if ($conn->query($insertSql) === TRUE) {
            echo "SIM aggiunta con successo. Codice: $simCode";
        } else {
            echo "Errore durante l'aggiunta della SIM: " . $conn->error;
        }
    }

    exit;
}
////////////////////////////////////////////////

///////------TEST CHIAMATE------/////

// Carica i numeri di telefono attivi per il menu a tendina delle telefonate
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'loadActiveNumbers') {
    $sql = "SELECT ct.numero, ct.tipo, ct.minutiResidui, ct.creditoResiduo 
            FROM ContrattoTelefonico ct 
            INNER JOIN SIMAttiva sa ON ct.numero = sa.associataA";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            echo '<option value="' . $row['numero'] . '" 
                          data-tipo="' . $row['tipo'] . '"
                          data-minuti="' . $row['minutiResidui'] . '"
                          data-credito="' . $row['creditoResiduo'] . '">' 
                          . $row['numero'] . '</option>';
        }
    } else {
        echo '<option value="">Nessun numero attivo disponibile</option>';
    }
    exit;
}

// Gestione inserimento di una nuova telefonata
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'addCall') {
   error_log("POST data: " . print_r($_POST, true));
    error_log("Inizio funzione addCall");

    $numero = $_POST['numero'];
    $data = $_POST['data'];
    $ora = $_POST['ora'];
    $durata = intval($_POST['durata']);

    error_log("Valori ricevuti: numero=$numero, data=$data, ora=$ora, durata=$durata");


    $conn->begin_transaction();

    try {
        // Recupera il tipo di contratto e i minuti/credito residui
        $stmt = $conn->prepare("SELECT tipo, minutiResidui, creditoResiduo FROM ContrattoTelefonico WHERE numero = ?");
        $stmt->bind_param("s", $numero);
        $stmt->execute();
        $result = $stmt->get_result();
        $contratto = $result->fetch_assoc();

        // Calcola il costo in base al tipo di contratto
        $costo = 0;
        $canProceed = true;
        $errorMessage = "";

        if ($contratto['tipo'] === 'ricarica') {
            $costo = $durata * 0.10; // 10 centesimi al minuto (Aggiorna per vers FINALE)
            if ($contratto['creditoResiduo'] < $costo) {
                $canProceed = false;
                $errorMessage = "Credito insufficiente per effettuare la chiamata";
            }
        } else if ($contratto['tipo'] === 'consumo') { 
      		$costo = $durata * 0.05; // 5 centesimi al minuto per contratti a consumo
            if ($contratto['minutiResidui'] < $durata) {
                $canProceed = false;
                $errorMessage = "Minuti residui insufficienti per effettuare la chiamata";
            }
        }

        if ($canProceed) {
          
            function generateUniqueCallId($conn) {
                do {
                    $newId = rand(1, 1000);
                    $sql_check = "SELECT id FROM Telefonata WHERE id = '$newId'";
                    $result = $conn->query($sql_check);
                } while ($result->num_rows > 0);
                return $newId;
            }

            $callId = generateUniqueCallId($conn);

            // Inserisce telefonata
            $stmt = $conn->prepare("INSERT INTO Telefonata (id, effettuataDa, data, ora, durata, costo) VALUES (?, ?, ?, ?, ?, ?)");
            $stmt->bind_param("isssid", $callId, $numero, $data, $ora, $durata, $costo);
            $stmt->execute();

            // Aggiorna il contratto
            if ($contratto['tipo'] === 'ricarica') {
                $nuovoCredito = $contratto['creditoResiduo'] - $costo;
                $stmt = $conn->prepare("UPDATE ContrattoTelefonico SET creditoResiduo = ? WHERE numero = ?");
                $stmt->bind_param("ds", $nuovoCredito, $numero);
            } else if ($contratto['tipo'] === 'consumo') {
                $nuoviMinuti = $contratto['minutiResidui'] - $durata;
                $stmt = $conn->prepare("UPDATE ContrattoTelefonico SET minutiResidui = ? WHERE numero = ?");
                $stmt->bind_param("is", $nuoviMinuti, $numero);
            }
            $stmt->execute();

            $conn->commit();
            echo json_encode(['success' => true, 'message' => 'Telefonata registrata con successo']);
        } else {
            echo json_encode(['success' => false, 'message' => $errorMessage]);
        }
    } catch (Exception $e) {
        $conn->rollback();
        echo json_encode(['success' => false, 'message' => 'Errore durante la registrazione della telefonata: ' . $e->getMessage()]);
    }
    exit;
}

////////////////////////////////////////////////////////////////////


// Caricamento delle SIM in base alla sezione richiesta
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['section'])) {
    $section = $_POST['section'];
    $sql = "";

    // Costruzione della query SQL in base ai parametri di ricerca
    if ($section == 'sim') {
        $numero_telefono = $_POST['numero_telefono'];
        $tipo_contratto = $_POST['tipo_contratto'];

        $sql = "SELECT codice, tipoSIM, associataA, dataAttivazione, NULL as dataDisattivazione FROM SIMAttiva WHERE 1=1";

        if (!empty($numero_telefono)) {
            $sql .= " AND codice LIKE '%$numero_telefono%'";
        }

        if (!empty($tipo_contratto)) {
            $sql .= " AND tipoSIM = '$tipo_contratto'";
        }

        $sql .= " UNION ALL SELECT codice, tipoSIM, eraAssociataA as associataA, dataAttivazione, dataDisattivazione FROM SIMDisattiva WHERE 1=1";  // mantiene eraAssociataA
        if (!empty($numero_telefono)) {
            $sql .= " AND codice LIKE '%$numero_telefono%'";
        }

        if (!empty($tipo_contratto)) {
            $sql .= " AND tipoSIM = '$tipo_contratto'";
        }

        $sql .= " UNION ALL SELECT codice, tipoSIM, NULL as associataA, NULL as dataAttivazione, NULL as dataDisattivazione FROM SIMNonAttiva WHERE 1=1";

        if (!empty($numero_telefono)) {
            $sql .= " AND codice LIKE '%$numero_telefono%'";
        }

        if (!empty($tipo_contratto)) {
            $sql .= " AND tipoSIM = '$tipo_contratto'";
        }

    } elseif ($section == 'allSIM') {
        // Query per caricare tutte le SIM
        $sql = "
            SELECT codice, tipoSIM, associataA, dataAttivazione, NULL as dataDisattivazione FROM SIMAttiva
            UNION ALL
            SELECT codice, tipoSIM, eraAssociataA as associataA, dataAttivazione, dataDisattivazione FROM SIMDisattiva  -- mantiene eraAssociataA
            UNION ALL
            SELECT codice, tipoSIM, NULL as associataA, NULL as dataAttivazione, NULL as dataDisattivazione FROM SIMNonAttiva
        ";
    }

    // Esecuzione della query e generazione della tabella HTML con i risultati
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            // Inizializza i pulsanti come vuoti
            $actionButtons = '';

            // Determina da quale tabella proviene il record e imposta i pulsanti corrispondenti
            if (!empty($row["associataA"]) && !empty($row["dataAttivazione"]) && empty($row["dataDisattivazione"])) {
                // SIMAttiva: Mostra solo "Disattiva SIM"
                $actionButtons .= "
                    <button class='action-btn delete-btn' data-tooltip='Disattiva SIM' data-id='" . $row['codice'] . "'>
                        <i class='fas fa-ban'></i>
                    </button>
                ";
            } elseif (!empty($row["dataDisattivazione"])) {
                // SIMDisattiva: Mostra solo "Riattiva SIM"
                $actionButtons .= "
                    <button class='action-btn redo-btn' data-tooltip='Riattiva SIM' data-id='" . $row['codice'] . "'>
                        <i class='fas fa-redo'></i>
                    </button>
                ";
            } elseif (empty($row["associataA"]) && empty($row["dataAttivazione"]) && empty($row["dataDisattivazione"])) {
                // SIMNonAttiva: Mostra solo "Attiva SIM"
                $actionButtons .= "
                    <button class='action-btn enable-btn' data-tooltip='Attiva SIM' data-id='" . $row['codice'] . "'>
                        <i class='fas fa-check'></i>
                    </button>
                ";
            }

            // Genera la riga HTML della tabella
            echo "<tr>";
            echo "<td>" . $row["codice"] . "</td>";
            echo "<td>" . $row["tipoSIM"] . "</td>";
            
            // Mostra 'associataA' solo se non è NULL, ma se proviene da SIMDisattiva non la mostriamo
            if (isset($row['associataA']) && $row['associataA'] !== NULL && !empty($row['associataA']) && $row["dataDisattivazione"] === NULL) {
                echo "<td>" . $row["associataA"] . "</td>";
            } else {
                echo "<td></td>";  // Vuota per SIMDisattiva o quando associataA è NULL
            }
            
            echo "<td>" . ($row["dataAttivazione"] ? $row["dataAttivazione"] : '') . "</td>";
            echo "<td>" . ($row["dataDisattivazione"] ? $row["dataDisattivazione"] : '') . "</td>";
            echo "<td>$actionButtons</td>";
            echo "</tr>";
        }
    } else {
        echo "<tr><td colspan='6'>Nessuna SIM trovata.</td></tr>";
    }

    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    $action = $_POST['action'];
    $simId = $_POST['simId'];
    $contratto = $_POST['contratto'] ?? null;

    if ($action === 'activate') {
        // Sposta la SIM da SIMNonAttiva a SIMAttiva
        $stmt = $conn->prepare("INSERT INTO SIMAttiva (codice, tipoSIM, associataA, dataAttivazione)
                                SELECT codice, tipoSIM, ?, NOW() FROM SIMNonAttiva WHERE codice = ?");
        $stmt->bind_param("ss", $contratto, $simId);
        if ($stmt->execute()) {
            $stmt = $conn->prepare("DELETE FROM SIMNonAttiva WHERE codice = ?");
            $stmt->bind_param("s", $simId);
            $stmt->execute();
            echo "SIM attivata con successo.";
        } else {
            echo "Errore durante l'attivazione della SIM.";
        }
    } elseif ($action === 'deactivate') {
        // Sposta la SIM da SIMAttiva a SIMDisattiva
        $stmt = $conn->prepare("INSERT INTO SIMDisattiva (codice, tipoSIM, eraAssociataA, dataAttivazione, dataDisattivazione)
                                SELECT codice, tipoSIM, associataA, dataAttivazione, NOW() FROM SIMAttiva WHERE codice = ?");
        $stmt->bind_param("s", $simId);
        if ($stmt->execute()) {
            $stmt = $conn->prepare("DELETE FROM SIMAttiva WHERE codice = ?");
            $stmt->bind_param("s", $simId);
            $stmt->execute();
            echo "SIM disattivata con successo.";
        } else {
            echo "Errore durante la disattivazione della SIM.";
        }
    } elseif ($action === 'reactivate') {
        // Sposta la SIM da SIMDisattiva a SIMAttiva
        $stmt = $conn->prepare("INSERT INTO SIMAttiva (codice, tipoSIM, associataA, dataAttivazione)
                                SELECT codice, tipoSIM, ?, NOW() FROM SIMDisattiva WHERE codice = ?");
        $stmt->bind_param("ss", $contratto, $simId);
        if ($stmt->execute()) {
            $stmt = $conn->prepare("DELETE FROM SIMDisattiva WHERE codice = ?");
            $stmt->bind_param("s", $simId);
            $stmt->execute();
            echo "SIM riattivata con successo.";
        } else {
            echo "Errore durante la riattivazione della SIM.";
        }
    } else {
        echo "Azione non valida.";
    }
}

// Ottieni la data di oggi nel formato richiesto per MySQL
$dataDisattivazione = date("Y-m-d H:i:s");

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if ($_POST['action'] == 'deleteSim') {
        $associataA = $_POST['associataA'];

      
        $conn->begin_transaction();

        try {
            // Controlla se la SIM esiste nella tabella SIMAttiva
            $stmt = $conn->prepare("SELECT codice, tipoSIM, associataA, dataAttivazione FROM SIMAttiva WHERE associataA = ?");
            $stmt->bind_param("s", $associataA);
            $stmt->execute();
            $result = $stmt->get_result();

            if ($result->num_rows > 0) {
                $row = $result->fetch_assoc();
                $codice = $row['codice'];
                $tipoSIM = $row['tipoSIM'];
                $dataAttivazione = $row['dataAttivazione'];

               	// Inserisci i dati nella tabella SIMDisattiva
                $stmt_insert = $conn->prepare("INSERT INTO SIMDisattiva (codice, tipoSIM, eraAssociataA, dataAttivazione, dataDisattivazione) VALUES (?, ?, ?, ?, ?)");
                $stmt_insert->bind_param("sssss", $codice, $tipoSIM, $associataA, $dataAttivazione, $dataDisattivazione);
                $stmt_insert->execute();

                // Elimina la SIM dalla tabella SIMAttiva
                $stmt_delete = $conn->prepare("DELETE FROM SIMAttiva WHERE associataA = ?");
                $stmt_delete->bind_param("s", $associataA);
                $stmt_delete->execute();

                $conn->commit();

               
                echo json_encode(['success' => true, 'message' => 'SIM eliminata con successo']);
            } else {
                echo json_encode(['success' => false, 'message' => 'SIM non trovata']);
            }
        } catch (Exception $e) {
            // Ritorna in caso di errore
            $conn->rollback();
            echo json_encode(['success' => false, 'message' => 'Errore durante l\'eliminazione della SIM: ' . $e->getMessage()]);
        }

        // Chiudi le dichiarazioni
        $stmt->close();
        if (isset($stmt_insert)) $stmt_insert->close();
        if (isset($stmt_delete)) $stmt_delete->close();
    }
}

if(isset($_POST['action']) && $_POST['action'] === 'deleteCall') {
    $id = mysqli_real_escape_string($conn, $_POST['callId']);
    
    $query = "DELETE FROM Telefonata WHERE id=$id";
    
    if(mysqli_query($conn, $query)) {
        echo 1;
    } else {
        echo 0;
    }
    exit;
}

// Chiusura della connessione al database
$conn->close();
?>
