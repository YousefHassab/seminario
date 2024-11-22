from flask import Flask, jsonify, request, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configurazione del database
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='mysql-2ba23f1f-iisgalvanimi-dbaa.j.aivencloud.com',  # Modifica con il tuo host
            user='avnadmin',       # Modifica con il tuo utente
            password='AVNS_b9uUZMqcvZOz-7cHDDp',  # Modifica con la tua password
            database='politecnico',  # Modifica con il tuo database
            port = 16366
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Errore connessione al database: {e}")
        return None

# Endpoint per la home della SPA
@app.route('/')
def index():
    return render_template('homepage.html')

# Endpoint per visualizzare docenti
@app.route('/docenti', methods=['GET'])
def get_docenti():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM DOCENTE')
        docenti = cursor.fetchall()
        conn.close()
        return jsonify(docenti)
    return jsonify({"error": "Database connection failed"}), 500

@app.route('/seminari', methods=['GET'])
def get_seminari():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM SEMINARIO')
        docenti = cursor.fetchall()
        conn.close()
        return jsonify(docenti)

    return jsonify({"error": "Database connection failed"}), 500

# 3. Endpoint /prenotazioni: visualizza le prenotazioni per seminario
@app.route('/prenotazioni', methods=['GET'])
def get_prenotazioni():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM PRENOTAZIONE inner join SEMINARIO on PRENOTAZIONE.seminario_id=SEMINARIO.id ')
        docenti = cursor.fetchall()
        conn.close()
        return jsonify(docenti)
    return jsonify({"error": "Database connection failed"}), 500

# 4. Endpoint /signup: registrazione di un docente
@app.route('/signup', methods=['POST'])
def signup_docente():
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    
    try:
        connection =  get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO DOCENTE (nome, email) VALUES (%s, %s)", (nome, email))
        connection.commit()
        return jsonify({"message": "Docente registrato con successo!"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()


# 5. Endpoint /insert: inserimento di un seminario
@app.route('/insert', methods=['POST'])
def insert_seminario():
    data = request.get_json()
    titolo = data['titolo']
    data_seminario = data['data']
    max_partecipanti = data['max_partecipanti']
    
    try:
        connection =  get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO seminari (titolo, data, max_partecipanti) 
            VALUES (%s, %s, %s)
        """, (titolo, data_seminario, max_partecipanti))
        connection.commit()
        return jsonify({"message": "Seminario inserito con successo!"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

            
# 6. Endpoint /book: prenotazione di uno studente a un seminario
@app.route('/book', methods=['POST'])
def book_seminario():
    data = request.get_json()
    id_seminario = data['id_seminario']
    nome_studente = data['nome_studente']
    email_studente = data['email_studente']
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Controlla se ci sono ancora posti disponibili
        cursor.execute("SELECT max_partecipanti, iscritti FROM seminari WHERE id = %s", (id_seminario,))
        seminario = cursor.fetchone()
        
        if seminario['iscritti'] < seminario['max_partecipanti']:
            # Prenotazione
            cursor.execute("""
                INSERT INTO prenotazioni (id_seminario, nome_studente, email_studente) 
                VALUES (%s, %s, %s)
            """, (id_seminario, nome_studente, email_studente))
            cursor.execute("UPDATE seminari SET iscritti = iscritti + 1 WHERE id = %s", (id_seminario,))
            connection.commit()
            return jsonify({"message": "Prenotazione effettuata con successo!"}), 201
        else:
            return jsonify({"error": "Non ci sono più posti disponibili per questo seminario!"}), 400
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)

