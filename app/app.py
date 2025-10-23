"""Aplicación Flask de lista de tareas (To-Do List).

Este módulo define la aplicación web principal que permite gestionar
una lista de tareas: agregar, eliminar y mostrar elementos.
Utiliza funciones definidas en `todo_list.py` para manipular los datos.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from .todo_list import agregar_tarea, eliminar_tarea, obtener_tareas

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  # Necesaria para usar 'flash'


@app.route("/health")
def health():
    """Endpoint para verificar el estado de la aplicación."""
    return "OK", 200


@app.route("/", methods=["GET", "POST"])
def index():
    """Maneja la página principal. Muestra y agrega tareas."""
    if request.method == "POST":
        nueva_tarea = request.form.get("tarea", "").strip()

        if not nueva_tarea:
            flash("⚠️ La tarea no puede estar vacía.")
        else:
            try:
                agregar_tarea(nueva_tarea)
                flash("✅ Tarea agregada correctamente.")
            except ValueError as e:
                flash(f"❌ Error al agregar tarea: {str(e)}")

    try:
        tareas = obtener_tareas()
    except (IOError, ValueError) as e:
        tareas = []
        flash(f"❌ Error al cargar tareas: {str(e)}")

    return render_template("index.html", tareas=tareas)


@app.route("/eliminar/<int:indice>")
def eliminar(indice):
    """Elimina una tarea según su índice."""
    try:
        eliminar_tarea(indice)
        flash("🗑️ Tarea eliminada correctamente.")
    except IndexError:
        flash("⚠️ La tarea seleccionada no existe.")
    except (IOError, ValueError) as e:
        flash(f"❌ Error al eliminar tarea: {str(e)}")

    return redirect(url_for("index"))


if __name__ == "__main__":  # pragma: no cover
    app_port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, port=app_port, host="0.0.0.0")
