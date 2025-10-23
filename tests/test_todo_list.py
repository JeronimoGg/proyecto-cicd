# tests/test_todo_list.py
import pytest
from app.todo_list import agregar_tarea, eliminar_tarea, obtener_tareas
from unittest.mock import patch, MagicMock

# Fixture para mockear la conexión a la base de datos en memoria
@pytest.fixture
def mock_conexion():
    with patch("app.todo_list.obtener_conexion") as mock:
        # Creamos una conexión SQLite en memoria
        import sqlite3
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

def test_agregar_tarea_valida(mock_conexion):
    # Agregamos una tarea válida
    agregar_tarea("Tarea de prueba")
    tareas = obtener_tareas()
    assert len(tareas) == 1
    assert tareas[0]["descripcion"] == "Tarea de prueba"

def test_agregar_tarea_vacia(mock_conexion):
    # Intentar agregar tarea vacía lanza ValueError
    with pytest.raises(ValueError):
        agregar_tarea("")

def test_eliminar_tarea_existente(mock_conexion):
    # Primero agregamos una tarea
    agregar_tarea("Tarea a eliminar")
    tareas = obtener_tareas()
    tarea_id = tareas[0]["id"]

    # Ahora la eliminamos
    eliminar_tarea(tarea_id)
    tareas = obtener_tareas()
    assert len(tareas) == 0

def test_eliminar_tarea_inexistente(mock_conexion):
    # Intentar eliminar un ID que no existe lanza IndexError
    with pytest.raises(IndexError):
        eliminar_tarea(999)

def test_obtener_tareas(mock_conexion):
    # Agregamos varias tareas
    agregar_tarea("Tarea 1")
    agregar_tarea("Tarea 2")
    tareas = obtener_tareas()
    assert len(tareas) == 2
    assert tareas[0]["descripcion"] == "Tarea 1"
    assert tareas[1]["descripcion"] == "Tarea 2"
