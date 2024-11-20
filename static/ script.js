// Funzione per caricare i seminari
function loadSeminari() {
    fetch('/seminari')
        .then(response => response.json())
        .then(seminari => {
            let html = '<h2>Semiari Disponibili</h2>';
            seminari.forEach(seminario => {
                html += `<p>${seminario.nome} - ${seminario.data} - ${seminario.luogo}</p>`;
            });
            document.getElementById('seminari').innerHTML = html;
        });
}

// Funzione per caricare i docenti
function loadDocenti() {
    fetch('/docenti')
        .then(response => response.json())
        .then(docenti => {
            let html = '<h2>Docenti Registrati</h2>';
            docenti.forEach(docente => {
                html += `<p>${docente.nome} ${docente.cognome}</p>`;
            });
            document.getElementById('docenti').innerHTML = html;
        });
}

// Funzione per caricare le prenotazioni
function loadPrenotazioni() {
    fetch('/prenotazioni')
        .then(response => response.json())
        .then(prenotazioni => {
            let html = '<h2>Prenotazioni</h2>';
            prenotazioni.forEach(prenotazione => {
                html += `<p>Seminario: ${prenotazione.seminario} - Pren
