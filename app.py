from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS para permitir solicitudes desde el frontend
CORS(app)

# Configuración de la base de datos MySQL
def conectar_base_de_datos():
    try:
        conexion = mysql.connector.connect(
            host='3.83.48.233',  # IP pública de tu instancia EC2 de MySQL
            user='dani',                          # Usuario MySQL
            password='Dani_1612',                      # Contraseña MySQL
            database='mi_base_de_datos'            # Base de datos que creaste
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print("Error al conectar a MySQL:", e)
        return None

# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conexion = conectar_base_de_datos()

    if conexion:
        cursor = conexion.cursor()
        query = "INSERT INTO user (first_name, last_name, date_of_birth, password) VALUES (%s, %s, %s, %s)"
        valores = (data['first_name'], data['last_name'], data['date_of_birth'], data['password'])
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({"message": "Usuario registrado con éxito"}), 201
    else:
        return jsonify({"message": "Error al conectar a la base de datos"}), 500

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    conexion = conectar_base_de_datos()
    
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT first_name, last_name, date_of_birth FROM user"
        cursor.execute(query)
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(usuarios), 200
    else:
        return jsonify({"message": "Error al conectar a la base de datos"}), 500

# Ruta de prueba para verificar que el servidor Flask funciona
@app.route('/')
def home():
    return "Servidor Flask está corriendo"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

