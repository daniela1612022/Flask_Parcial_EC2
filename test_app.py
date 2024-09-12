import pytest
from app import app  # Importa directamente la instancia de `app` del archivo app.py
import mysql.connector
from mysql.connector import Error

# Simulación de conexión a la base de datos para evitar interacción real en pruebas
def conectar_base_de_datos_mock():
    return None  # Simulamos que la conexión no es exitosa para las pruebas (ajústalo según tu necesidad)

# Configuración del cliente de pruebas
@pytest.fixture
def client(monkeypatch):
    # Parchar la función de conexión a la base de datos para las pruebas
    monkeypatch.setattr('app.conectar_base_de_datos', conectar_base_de_datos_mock)
    
    app.config['TESTING'] = True
    app.config['DEBUG'] = False

    # Crear el cliente de pruebas
    with app.test_client() as client:
        yield client


# Prueba para la ruta de inicio
def test_home_route(client):
    """Prueba para la ruta de inicio"""
    response = client.get('/')
    assert response.status_code == 200
    assert "Servidor Flask está corriendo" in response.get_data(as_text=True)  # Cambiado a cadena de texto


# Prueba para la creación de un usuario usando POST
def test_register_user(client):
    """Prueba para registrar un usuario"""
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'date_of_birth': '1990-01-01',
        'password': 'password123'
    }
    response = client.post('/register', json=data)
    assert response.status_code == 500  # Ya que estamos simulando un fallo de conexión a la base de datos


# Prueba para obtener usuarios con GET (simulado)
def test_get_users(client):
    """Prueba para obtener usuarios"""
    response = client.get('/users')
    assert response.status_code == 500  # Ya que estamos simulando un fallo de conexión a la base de datos


# Prueba para manejar un recurso que no existe (404)
def test_404_error(client):
    """Prueba para el manejo de errores 404"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
