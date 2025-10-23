# tests/test_app_routes.py
import pytest
from app.app import app
from unittest.mock import patch, MagicMock
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Fixture para mockear la conexión a la DB
@pytest.fixture
def mock_db():
    with patch("app.todo_list.obtener_conexion") as mock:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL
            );
        """)
        conn.commit()
        mock.return_value.__enter__.return_value = conn
        yield conn
        conn.close()

def test_index_get(client, mock_db):
    response = client.get('/')
    assert response.status_code == 200
    assert b'To-Do List' in response.data

def test_index_post_agregar_tarea_valida(client, mock_db):
    response = client.post('/', data={'tarea': 'Tarea de prueba'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tarea agregada correctamente' in response.data
    # Verificar que la tarea realmente está en la DB
    cursor = mock_db.cursor()
    cursor.execute("SELECT descripcion FROM tareas")
    tareas = cursor.fetchall()
    assert tareas[0][0] == 'Tarea de prueba'

def test_index_post_agregar_tarea_vacia(client, mock_db):
    response = client.post('/', data={'tarea': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert b'La tarea no puede estar vac\xc3\xada' in response.data

def test_eliminar_tarea_existente(client, mock_db):
    # Insertar tarea manualmente
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO tareas (descripcion) VALUES (?)", ("Tarea a eliminar",))
    mock_db.commit()
    tarea_id = cursor.lastrowid

    response = client.get(f'/eliminar/{tarea_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Tarea eliminada correctamente' in response.data

    # Verificar que ya no está en la DB
    cursor.execute("SELECT * FROM tareas WHERE id=?", (tarea_id,))
    assert cursor.fetchone() is None

def test_eliminar_tarea_inexistente(client, mock_db):
    response = client.get('/eliminar/999', follow_redirects=True)
    assert response.status_code == 200
    assert b'La tarea seleccionada no existe' in response.data
