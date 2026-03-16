from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_simple"

DATABASE = "database/landing_page.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def inicio():
    conn = get_db_connection()

    configuracion = conn.execute(
        "SELECT * FROM configuracion_sitio LIMIT 1"
    ).fetchone()

    hero = conn.execute(
        "SELECT * FROM hero LIMIT 1"
    ).fetchone()

    estadisticas = conn.execute(
        "SELECT * FROM estadisticas ORDER BY orden"
    ).fetchall()

    cursos = conn.execute(
        "SELECT * FROM cursos WHERE estado = 1 ORDER BY orden"
    ).fetchall()

    caracteristicas = conn.execute(
        "SELECT * FROM curso_caracteristicas ORDER BY curso_id, orden"
    ).fetchall()

    nosotros = conn.execute(
        "SELECT * FROM nosotros LIMIT 1"
    ).fetchone()

    valores = conn.execute(
        "SELECT * FROM valores ORDER BY orden"
    ).fetchall()

    conn.close()

    caracteristicas_por_curso = {}

    for item in caracteristicas:
        curso_id = item["curso_id"]

        if curso_id not in caracteristicas_por_curso:
            caracteristicas_por_curso[curso_id] = []

        caracteristicas_por_curso[curso_id].append(item["caracteristica"])

    return render_template(
        "index.html",
        configuracion=configuracion,
        hero=hero,
        estadisticas=estadisticas,
        cursos=cursos,
        caracteristicas_por_curso=caracteristicas_por_curso,
        nosotros=nosotros,
        valores=valores
    )


@app.route("/contacto", methods=["POST"])
def contacto():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    mensaje = request.form.get("mensaje")
    print(nombre, email, mensaje)
    if not nombre or not email or not mensaje:
        flash("Por favor, complete todos los campos.")
        return redirect(url_for("inicio"))

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO mensajes_contacto (nombre, email, mensaje) VALUES (?, ?, ?)",
        (nombre, email, mensaje)
    )
    conn.commit()
    conn.close()

    flash("Tu mensaje fue enviado correctamente.")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    ##app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)