"""Módulo de manejo de base de datos SQLite para la aplicación To-Do List."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tareas.db")


def obtener_conexion():
    """Devuelve una conexión a la base de datos."""
    return sqlite3.connect(DB_PATH)


def inicializar_bd():
    """Crea la tabla de tareas si no existe."""
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL
            );
            """
        )
        conn.commit()


if __name__ == "__main__":
    inicializar_bd()
    print("Base de datos inicializada correctamente.")
