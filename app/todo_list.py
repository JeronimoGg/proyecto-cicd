"""Módulo de lógica de negocio para la lista de tareas (To-Do List)."""

from .database import obtener_conexion, inicializar_bd


def agregar_tarea(tarea):
    """Agrega una nueva tarea a la base de datos."""
    if not tarea:
        raise ValueError("La tarea no puede estar vacía.")

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tareas (descripcion) VALUES (?);", (tarea,))
        conn.commit()


def eliminar_tarea(indice):
    """Elimina una tarea por su ID."""
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?;", (indice,))
        if cursor.rowcount == 0:
            raise IndexError("No existe una tarea con ese ID.")
        conn.commit()


def obtener_tareas():
    """Obtiene todas las tareas registradas en la base de datos."""
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, descripcion FROM tareas;")
        tareas = cursor.fetchall()
    return [{"id": fila[0], "descripcion": fila[1]} for fila in tareas]


# Inicializar la base de datos si no existe
inicializar_bd()
