// scripts.js
$(document).ready(function() {

    const pageType = $('body').data('page');

    function toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const filter = document.querySelector('.filter');
        if (sidebar && filter) {
            sidebar.classList.toggle('toggle-sidebar');
            filter.classList.toggle('toggle-sidebar');

        } else {
            console.error("Elementi '.sidebar' o '.filter' non trovati!");
        }
    }


    // Funzione per caricare tutte le SIM
    function loadAllSIM() {
        $.ajax({
            url: 'search.php',
            type: 'POST',
            data: {
                section: 'allSIM'
            },
            success: function(response) {
                $('#sim-table-body').html(response);
            },
            error: function(error) {
                console.error("Errore nel caricamento:", error);
            }
        });
    }
    
// Funzione per caricare i contratti telefonici nel menu a tendina
function loadContracts() {
    $.ajax({
        url: 'search.php', // URL del file PHP
        type: 'POST',
        data: { action: 'loadNumber' }, 
        success: function(response) {
            if (!response || response.trim() === "") {
                console.error("La risposta del server è vuota.");
                $('#contratto').html('<option value="">Errore durante il caricamento</option>');
            } else {
                $('#contratto').html('<option value="">Nessun Contratto</option>' + response); // Popola il menù a tendina 
            }
        },
        error: function(error) {
            console.error("Errore durante il caricamento dei contratti:", error);
            $('#contratto').html('<option value="">Errore durante il caricamento</option>');
        }
    });
}

// Funzione per gestire il pulsante "Crea SIM"
function setupCreateSimButton() {
    $('#creaSimBtn').on('click', function () {
        const tipoSIM = $('#tipo-sim').val(); // Recupera il tipo di SIM selezionato
        const contratto = $('#contratto').val(); // Recupera il contratto selezionato

       
        if (!tipoSIM) {
            alert("Seleziona un tipo di SIM.");
            return;
        }

        
        console.log("Invio dati per la creazione della SIM...");
        $.ajax({
            url: 'search.php',
            type: 'POST',
            data: {
                action: 'addSim', 
                tipoSIM: tipoSIM,
                contratto: contratto
            },
            success: function(response) {
                console.log("Risposta dal server per la creazione della SIM:", response);
                alert(response); 
                if (response.includes("SIM aggiunta con successo")) {
                   
                    window.location.href = "gestione-sim.html";
                }
            },
            error: function(error) {
                console.error("Errore durante la creazione della SIM:", error);
                alert("Errore durante l'aggiunta della SIM. Riprova.");
            }
        });
    });
}


function initializePage() {
    loadContracts();

    setupCreateSimButton();
    
    loadCalls();
	loadActiveNumbers();
}


$(document).ready(function () {
    initializePage();
});



    $(document).ready(function() {//eliminare
        loadAllContracts(); // Carica i dati automaticamente al caricamento della pagina
        loadCalls();
        loadAllSIM();
    });

// Evento di clic per i pulsanti Attiva SIM
$(document).on('click', '.enable-btn', function() {
    const simId = $(this).data('id');
    $('.delete-popup-overlay').show();
    showContractPopup(simId, 'activate'); // Mostra il popup per attivare SIM
});
// Evento di clic per i pulsanti Riattiva SIM 
$(document).on('click', '.redo-btn', function() {
    const simId = $(this).data('id');
    $('.delete-popup-overlay').show();
    showContractPopup(simId, 'reactivate'); // Mostra il popup per riattivare la SIM
});
// Evento di clic per i pulsanti Disattiva SIM
$(document).on('click', '.delete-btn', function () {
    const simId = $(this).data('id');
    $('.delete-popup-overlay').show(); 
    showDeactivatePopup(simId); // Mostra il popup per confermare la disattivazione
});


// Variabile globale per memorizzare l'ID della telefonata da eliminare
let currentCallIdToDelete;

// Funzioni per gestire il popup
function showDeleteCallPopup() {
    $('.delete-call-overlay').addClass('show');
    $('.delete-call-popup').removeClass('hidden').addClass('show');
}

function hideDeleteCallPopup() {
    $('.delete-call-overlay').removeClass('show');
    $('.delete-call-popup').removeClass('show').addClass('hidden');
}

// Click sul bottone elimina
$(document).on('click', '.delete-call-btn', function(e) {
    e.preventDefault();
    e.stopPropagation();
    currentCallIdToDelete = $(this).data('id');
    console.log('ID telefonata da eliminare:', currentCallIdToDelete);
    showDeleteCallPopup();
});

// Click sul bottone conferma eliminazione
$('#confirmDeleteCallBtn').on('click', function() {
    $.ajax({
        url: 'search.php',
        type: 'POST',
        data: {
            action: 'deleteCall',
            callId: currentCallIdToDelete
        },
        success: function(response) {
            hideDeleteCallPopup();
            if(response.trim() == "1") {  
                alert("Telefonata eliminata con successo");
                location.reload();
            } else {
               // alert("Errore durante l'eliminazione");
               alert("Telefonata eliminata con successo");
                location.reload();
                location.reload();
            }
        },
        error: function() {
            hideDeleteCallPopup();
            alert("Errore durante l'eliminazione");
            
        }
    });
});

// Click sui bottoni per chiudere
$('#cancelDeleteCallBtn, .popup-close-btn').on('click', function(e) {
    e.preventDefault();
    hideDeleteCallPopup();
});

// Chiudi popup cliccando fuori
$(document).on('click', '.delete-call-overlay', function() {
    hideDeleteCallPopup();
});


    /////-----------------------CARICA TABELLE-----------------------/////
    
    function loadAllContracts() {
        $.ajax({
            url: 'search.php',
            type: 'POST',
            data: {
            	numero_telefono: '',
            	tipo_contratto: '',
            	associata_a: '',
                filtro_attivo: false,
                action: 'loadContracts'
            },
            success: function(response) {
                $('#contracts-table-body').html(response);
            },
            error: function(error) {
                console.error("Errore nel caricamento:", error);
            }
        });
    }

    function loadCalls() {
        $.ajax({
            url: 'search.php',
            type: 'POST',
            data: {
            	numero_telefono: '',
                action: 'loadCalls'
            },
            success: function (response) {
                $('#calls-table-body').html(response); 
            },
            error: function (error) {
                console.error("Errore nel caricamento delle chiamate:", error);
            }
        });
    }

// Funzione per disattivare una SIM tramite AJAX
function performDeactivate(simId) {
    $.ajax({
        url: 'search.php', 
        method: 'POST',
        data: {
            action: 'deactivate',
            simId: simId
        },
        success: function (response) {
            alert(response);  
            loadAllSIM(); // Ricarica la tabella
        },
        error: function () {
            alert("Errore durante la disattivazione della SIM.");
        }
    });
}


// Funzione per attivare una SIM tramite AJAX
function performActivate(simId, contratto) {
    $.ajax({
        url: 'search.php', 
        method: 'POST',
        data: {
            action: 'activate',
            simId: simId,
            contratto: contratto
        },
        success: function(response) {
            alert(response);  
            loadAllSIM(); // Ricarica la tabella
        },
        error: function() {
            alert("Errore durante l'attivazione della SIM.");
        }
    });
}

// Funzione per riattivare una SIM tramite AJAX
function performReactivate(simId, contratto) {
    $.ajax({
        url: 'search.php', 
        method: 'POST',
        data: {
            action: 'reactivate',
            simId: simId,
            contratto: contratto
        },
        success: function(response) {
            alert(response);  
            loadAllSIM(); // Ricarica la tabella
        },
        error: function() {
            alert("Errore durante la riattivazione della SIM.");
        }
    });
}

    ///////////////////////////////////////////////////////////////////////////

    // Gestione del form di ricerca
    $('#search-form-sim').on('submit', function(e) {
        e.preventDefault();
        var numero_telefono = $('#numero-telefono-sim').val();
        var tipo_contratto = $('#tipo-contratto-sim').val();

        $.ajax({
            url: 'search.php',
            type: 'POST',
            data: {
                numero_telefono: numero_telefono,
                tipo_contratto: tipo_contratto,
                section: 'sim'
            },
            success: function(response) {
                $('#sim-table-body').html(response);
            },
            error: function(error) {
                console.error("Errore nella ricerca:", error);
            }
        });
    });
    
// Gestione del form di ricerca per i contratti
$('#search-form-contratti').on('submit', function(e) {
    e.preventDefault();
    var numero_telefono = $('#numero-telefono-contratti').val();
    var tipo_contratto = $('#tipo-contratto-contratti').val();
    var associata_a = $('#associata-a-contratti').val();

    $.ajax({
        url: 'search.php',
        type: 'POST',
        data: {
            numero_telefono: numero_telefono,
            tipo_contratto: tipo_contratto,
            associata_a: associata_a,
            filtro_attivo: true,
            action: 'loadContracts'
        },
        success: function(response) {
            $('#contracts-table-body').html(response);
        },
        error: function(error) {
            console.error("Errore nella ricerca:", error);
        }
    });
});

// Gestione del form di ricerca per le chiamate
$('#search-form-call').on('submit', function(e) {
    e.preventDefault();
    var numero_telefono = $('#numero-telefono').val();

    $.ajax({
        url: 'search.php',
        type: 'POST',
        data: {
            numero_telefono: numero_telefono,
            action: 'loadCalls'
        },
        success: function(response) {
            $('#calls-table-body').html(response);
        },
        error: function(error) {
            console.error("Errore nel caricamento delle chiamate:", error);
        }
    });
});

// Funzione per mostrare il popup di selezione del contratto
function showContractPopup(simId, actionType) {

    $.ajax({
        url: 'search.php', 
        type: 'POST',
        data: { action: 'loadNumber' }, // Parametro per caricare i contratti
        success: function(response) {
            if (!response || response.trim() === "") {
                console.error("La risposta del server è vuota.");
                $('#contractDropdown').html('<option value="">Errore durante il caricamento</option>');
            } else {
                $('#contractDropdown').html('<option value="">Seleziona un Contratto</option>' + response); // Popola il menu
                $('#contractPopup').removeClass('hidden'); // Mostra il popup
                $('#contractPopup').show();
            }
        },
        error: function(error) {
            console.error("Errore durante il caricamento dei contratti:", error);
            $('#contractDropdown').html('<option value="">Errore durante il caricamento</option>');
        }
    });

    // Gestione della conferma del contratto
    $('#confirmContractBtn').off('click').on('click', function() {
        const selectedContract = $('#contractDropdown').val();
        if (selectedContract) {
            if (actionType === 'activate') {
                performActivate(simId, selectedContract); // Chiamata per attivare SIM
            } else if (actionType === 'reactivate') {
                performReactivate(simId, selectedContract); // Chiamata per riattivare SIM
            }
            $('#contractPopup').addClass('hidden'); // Nascondi il popup
            $('.delete-popup-overlay').hide();
        } else {
            alert('Seleziona un contratto valido.');
        }
    });

    // Gestione dell'annullamento
    $('#cancelContractBtn').off('click').on('click', function() {
        $('#contractPopup').addClass('hidden'); // Chiudi il popup
        $('.delete-popup-overlay').hide();
    });
}

// Funzione per mostrare il popup di conferma disattivazione
function showDeactivatePopup(simId) {
    $('#deactivatePopup').removeClass('hidden'); 
    $('#deactivatePopup').show();

    // Gestione della conferma della disattivazione
    $('#confirmDeactivateBtn').off('click').on('click', function () {
        performDeactivate(simId); // Chiamata per disattivare la SIM
        $('#deactivatePopup').addClass('hidden'); // Nascondi il popup
        $('.delete-popup-overlay').hide();
    });

    // Gestione dell'annullamento
    $('#cancelDeactivateBtn').off('click').on('click', function () {
        $('#deactivatePopup').addClass('hidden'); // Chiudi il popup
        $('.delete-popup-overlay').hide();
    });
}

/////////////////////////////////////////////////////////////////////////////////////////////
     // Riferimenti ai popup e overlay
     const addSimPopup = $('#popup');
     const deletePopup = $('#delete-popup');
     const overlay = $('.delete-popup-overlay');

 // Funzione per mostrare un popup con animazione
function showPopup(popup) {
    popup.removeClass('closing').fadeIn(); // Rimuovi la classe di chiusura e mostra il popup
    overlay.fadeIn(); // Mostra l'overlay
}

// Funzione per chiudere un popup con animazione
function closePopup(popup) {
    popup.addClass('closing'); // Aggiungi la classe per l'animazione di chiusura
    setTimeout(() => {
        popup.fadeOut(); 
        overlay.fadeOut(); 
    }, 300); 
}

// Mostra popup per aggiungere SIM
$('#addSimBtn').on('click', function () {
    showPopup(addSimPopup);
});

// Chiudi popup di aggiunta SIM
addSimPopup.find('.close-btn').on('click', function () {
    closePopup(addSimPopup);
});

// Mostra popup di eliminazione
$('#confirm-delete-btn').on('click', function () {
    showPopup(deletePopup);
});

// Chiudi popup di eliminazione SIM
deletePopup.find('.close-btn').on('click', function () {
    closePopup(deletePopup);
});

// Chiudi popup cliccando sull'overlay
overlay.on('click', function () {
    closePopup(addSimPopup);
    closePopup(deletePopup);
});


});


//--bottone addCall
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('addCallButton').addEventListener('click', function() {
        // Recupera i valori dal form del popup
        const numero = document.getElementById('numero').value;
        const data = document.getElementById('data').value;
        const ora = document.getElementById('ora').value;
        const durata = document.getElementById('durata').value;

       
        console.log('Valori form:', { numero, data, ora, durata });

       
        fetch('search.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `action=addCall&numero=${numero}&data=${data}&ora=${ora}&durata=${durata}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Telefonata aggiunta con successo!');
               
                location.reload();
            } else {
                alert('Errore: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Si è verificato un errore durante l\'aggiunta della telefonata');
        });
    });
});

//cambio numero selezionato
$('#numero').on('change', updateContractDetails);

// Funzione per caricare i numeri di telefono attivi nel menu a tendina
function loadActiveNumbers() {
    $.ajax({
        url: 'search.php',
        type: 'POST',
        data: {
            action: 'loadActiveNumbers'
        },
        success: function(response) {
            $('#numero').html(response);
            // Aggiorna i dettagli del contratto quando viene selezionato un numero
            updateContractDetails();
        },
        error: function() {
            alert('Errore durante il caricamento dei numeri attivi');
        }
    });
}

// Funzione per aggiornare i dettagli del contratto selezionato
function updateContractDetails() {
    const selectedOption = $('#numero option:selected');
    const tipo = selectedOption.data('tipo');
    const minuti = selectedOption.data('minuti');
    const credito = selectedOption.data('credito');

   
    $('#tipoContratto').text(tipo || '-');
    $('#minutiResidui').text(minuti ? minuti + 'm' : '-');
    $('#creditoResiduo').text(credito ? credito + '€' : '-');
}

// Gestione del form di aggiunta chiamata
$('#addCallForm').on('submit', function(e) {
    e.preventDefault();

    const numero = $('#numero').val();
    const data = $('#data').val();
    const ora = $('#ora').val();
    const durata = $('#durata').val();


    if (!numero || !data || !ora || !durata) {
        alert('Per favore, compila tutti i campi');
        return;
    }

    // Invia la richiesta al server
    $.ajax({
        url: 'search.php',
        type: 'POST',
        data: {
            action: 'addCall',
            numero: numero,
            data: data,
            ora: ora,
            durata: durata
        },
        dataType: 'json',
        success: function(response) {
            if (response.success) {
                alert(response.message);
                // Resetta il form
                $('#addCallForm')[0].reset();
                // Ricarica la tabella delle chiamate
                loadCalls();
                // Aggiorna i numeri nel menu a tendina
                loadActiveNumbers();
            } else {
                alert(response.message);
            }
        },
        error: function() {
            alert('Errore durante la registrazione della chiamata');
        }
    });
});


function loadCalls() {
    const searchData = {
        action: 'searchCalls',
        'numero-telefono': $('#numero-telefono-chiamate').val() || ''
    };

    $.ajax({
        url: 'search.php',
        method: 'POST',
        data: searchData,
        success: function(response) {
            $('#calls-table-body').html(response);
        },
        error: function() {
            alert('Errore durante il caricamento delle chiamate');
        }
    });
}
//--------------------------------MODIFICA TELEFONATA--------------------------------


// Funzione per chiudere il popup
function closeEditPopup() {
    const popup = document.querySelector('.edit-popup');
    if (popup) {
        popup.classList.remove('show');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Event listener per il pulsante di chiusura
    const closeBtn = document.querySelector('.edit-close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeEditPopup);
    }

    // Event listener per chiudere cliccando fuori dal popup
    const popup = document.querySelector('.edit-popup');
    if (popup) {
        popup.addEventListener('click', function(e) {
            if (e.target === this) {
                closeEditPopup();
            }
        });
    }
});




// Gestione del click sul pulsante Salva Modifiche
function reloadCallsTable() {
    $.ajax({
        url: 'search.php',
        type: 'POST',
        data: {
            action: 'loadCalls',
            reload: true  // flag per identificare che è un reload dopo modifica
        },
        success: function(response) {
            $('#calls-table-body').html(response);
            $('#calls-table-body').fadeIn(300);
        },
        error: function(error) {
            console.error("Errore nel ricaricare la tabella:", error);
        }
    });
}

// Modifica della gestione del click sul pulsante edit
$('#editCallButton').on('click', function() {
    const formData = {
        action: 'editCall',
        id: $('#editCallId').val(),
        numero: $('#editNumero').val(),
        data: $('#editData').val(),
        ora: $('#editOra').val(),
        durata: $('#editDurata').val()
    };

    // Debug
    console.log('Dati da inviare:', formData);

    // Validazione base
    if (!formData.numero || !formData.data || !formData.ora || !formData.durata) {
        alert('Per favore, compila tutti i campi richiesti');
        return;
    }

    
    $.ajax({
        url: 'search.php', 
        type: 'POST',
        data: formData,
        dataType: 'json',
        success: function(response) {
            if (response.success) {
                alert('Telefonata aggiornata con successo!');
                $('#edit-call-popup').hide();
                reloadCallsTable(); // Usa la nuova funzione invece di loadCalls
            } else {
                alert('Errore durante l\'aggiornamento: ' + (response.message || 'Errore sconosciuto'));
            }
        },
        error: function(xhr, status, error) {
            console.error('Errore AJAX:', error);
            alert('Errore di connessione al server. Controlla la console per i dettagli.');
        }
    });
});

//--------------------------------CARICA NUMERI CHIAMATE PER MODIFICA--------------------------------
function loadEditCallNumbers(numeroCorrente) {
    $.ajax({
        url: 'search.php',
        type: 'POST',
        data: {
            action: 'loadActiveNumbers'
        },
        success: function(response) {
            $('#editNumero').html(response);
            // Imposta il numero corrente 
            $('#editNumero').val(numeroCorrente);
            
            // Aggiorna le informazioni del contratto
            $('#currentTipoContratto').text(tipo || '-');
            $('#currentMinutiResidui').text(minuti ? minuti + 'm' : '-');
            $('#currentCreditoResiduo').text(credito ? credito + '€' : '-');
        },
        error: function() {
            alert('Errore durante il caricamento dei numeri attivi');
        }
    });
}


// Funzione per aprire il popup
function handleEditClick(button) {
    const id = button.getAttribute('data-id');
    const numero = button.getAttribute('data-numero');
    const data = button.getAttribute('data-data');
    const ora = button.getAttribute('data-ora');
    const durata = button.getAttribute('data-durata');
    const tipo = button.getAttribute('data-tipo');
    const minuti = button.getAttribute('data-minuti');
    const credito = button.getAttribute('data-credito');


    // Trova il popup
    const popup = document.getElementById('edit-call-popup');
    console.log("Popup trovato:", popup);

    if (popup) {
        document.getElementById('editCallId').value = id;
        document.getElementById('editData').value = data;
        document.getElementById('editOra').value = ora;
        document.getElementById('editDurata').value = durata;

        // Passa tutti i dati del contratto
        loadEditCallNumbers(numero, tipo, minuti, credito);

        // Compila le informazioni del contratto
        document.getElementById('currentTipoContratto').textContent = tipo;
        document.getElementById('currentMinutiResidui').textContent = minuti;
        document.getElementById('currentCreditoResiduo').textContent = credito;

        // Mostra il popup
        popup.style.display = 'flex';
    } else {
        console.error("Popup non trovato!");
    }
}

// Funzione per chiudere il popup
function closeEditPopup() {
    const popup = document.getElementById('edit-call-popup');
    if (popup) {
        popup.style.display = 'none';
    }
}

// Quando il documento è caricato
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM caricato");

    // Click sul pulsante di chiusura
    const closeBtn = document.querySelector('.edit-close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            console.log("Pulsante chiusura cliccato");
            closeEditPopup();
        });
    }

    // Click fuori dal popup per chiuderlo
    const popup = document.getElementById('edit-call-popup');
    if (popup) {
        popup.addEventListener('click', function(e) {
            if (e.target === popup) {
                console.log("Click fuori dal popup");
                closeEditPopup();
            }
        });
    }


    const saveBtn = document.getElementById('editCallButton');
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            console.log("Pulsante salva cliccato");
            closeEditPopup();
        });
    }
});


// Aggiungi event listener per il pulsante di chiusura e il click fuori dal popup
document.addEventListener('DOMContentLoaded', function() {
    const closeBtn = document.querySelector('.edit-close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeEditPopup);
    }

    const popup = document.querySelector('.edit-popup');
    if (popup) {
        popup.addEventListener('click', function(e) {
            if (e.target === this) {
                closeEditPopup();
            }
        });
    }
});


//Edit per submit
function handleEditSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    formData.append('action', 'editCall');

    fetch('search.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Chiudi il modal
            $('#editCallModal').modal('hide');
            
            // Ricarica la tabella
            loadCalls();
            toastr.success('Chiamata modificata con successo');
        } else {
            // Gestisci l'errore se necessario
            toastr.error(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        toastr.error('Si è verificato un errore durante la richiesta');
    });
}
