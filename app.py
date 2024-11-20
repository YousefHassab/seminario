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
            password='',  # Modifica con la tua password
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

if __name__ == '__main__':
    app.run(debug=True)
