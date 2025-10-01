import os, json
from flask import Flask, jsonify

app = Flask(__name__)

# Path file JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SNACK_FILE = os.path.join(BASE_DIR, "snack.json")
DRINK_FILE = os.path.join(BASE_DIR, "drink.json")

# --- Helper ---
def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return "SELAMAT DATANG DI PRODUK UMKM MAKMUR JAYA"


@app.route("/produk/snack", methods=["GET"])
def snack_all():
    data = load_data(SNACK_FILE)
    return jsonify(data)

@app.route("/produk/snack/<int:id>", methods=["GET"])
def snack_id(id):
    data = load_data(SNACK_FILE)
    for s in data:
        if s["id"] == id:
            return jsonify(s)
    return jsonify({"error": "Snack tidak ditemukan"}), 404


@app.route("/produk/drink", methods=["GET"])
def drink_all():
    data = load_data(DRINK_FILE)
    return jsonify(data)

@app.route("/produk/drink/<int:id>", methods=["GET"])
def drink_id(id):
    data = load_data(DRINK_FILE)
    for d in data:
        if d["id"] == id:
            return jsonify(d)
    return jsonify({"error": "Drink tidak ditemukan"}), 404

if __name__ == "__main__":
    app.run(debug=True)
