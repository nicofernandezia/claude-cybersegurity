"""Tienda de ejemplo CON FALLOS DE SEGURIDAD PUESTOS A PROPÓSITO.

Sirve para probar la skill modo-atacante. No la uses como base de nada real.
La clave de abajo es inventada y no funciona.
"""
import json
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
OPENAI_API_KEY = "sk-proj-FAKE0000000000000000000000000000demo"  # clave inventada para la demo
db = sqlite3.connect("tienda.db", check_same_thread=False)


def llamar_modelo(prompt: str) -> str:
    """Simula la llamada a un modelo de IA (aquí iría la petición real con OPENAI_API_KEY)."""
    return '{"accion": "responder", "texto": "Hola"}'


@app.post("/login")
def login():
    email, password = request.json["email"], request.json["password"]
    fila = db.execute("SELECT id FROM usuarios WHERE email = ? AND password = ?", (email, password)).fetchone()
    return jsonify(ok=bool(fila), usuario=fila[0] if fila else None)


@app.get("/buscar")
def buscar():
    q = request.args.get("q", "")
    filas = db.execute(f"SELECT id, producto FROM pedidos WHERE producto LIKE '%{q}%'").fetchall()
    return jsonify(filas)


@app.get("/pedido/<int:pedido_id>")
def ver_pedido(pedido_id):
    fila = db.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,)).fetchone()
    return jsonify(fila)


@app.post("/webhook/whatsapp")
def webhook_whatsapp():
    msg = request.json
    cliente = db.execute("SELECT nombre, telefono, dni FROM clientes WHERE telefono = ?", (msg["from"],)).fetchone()
    prompt = (
        "Eres el asistente de la tienda. Puedes responder o cancelar pedidos.\n"
        f"Datos del cliente: {cliente}\n"
        f"Mensaje del cliente: {msg['text']}\n"
        'Responde en JSON: {"accion": "responder"|"cancelar", "pedido": id, "texto": "..."}'
    )
    respuesta = json.loads(llamar_modelo(prompt))
    if respuesta["accion"] == "cancelar":
        db.execute(f"UPDATE pedidos SET estado = 'cancelado' WHERE id = {respuesta['pedido']}")
        db.commit()
    db.execute("INSERT INTO mensajes (telefono, texto) VALUES (?, ?)", (msg["from"], msg["text"]))
    return jsonify(respuesta)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
