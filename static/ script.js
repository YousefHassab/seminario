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
        async function loadPrenotazioni() {
            const response = await fetch('http://localhost:5000/prenotazioni');
            const prenotazioni = await response.json();
            
            let html = '<h2>Prenotazioni</h2><ul>';
            prenotazioni.forEach(prenotazione => {
                html += `<li>${prenotazione.titolo} - ${prenotazione.numero_studenti} studenti prenotati</li>`;
            });
            html += '</ul>';
            
            document.getElementById('prenotazioni-container').innerHTML = html;
        }

        

        
