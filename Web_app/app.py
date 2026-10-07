from flask import Flask, jsonify, request, render_template, send_file
import sqlite3
from pathlib import Path

app = Flask(__name__)

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "database" / "chicago_crime.db"
GRAPHS = ROOT / "Graphs"

def connect():
    if not DB.exists():
        raise FileNotFoundError(f"Database not found: {DB}")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def columns():
    with connect() as con:
        return [r["name"] for r in con.execute(
            "PRAGMA table_info(chicago_crime)"
        ).fetchall()]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def status():
    try:
        with connect() as con:
            total = con.execute("SELECT COUNT(*) FROM chicago_crime").fetchone()[0]
        return jsonify(connected=True, records=total)
    except Exception as e:
        return jsonify(connected=False, error=str(e)), 500

@app.route("/api/crimes", methods=["GET"])
def get_crimes():
    try:
        limit = min(int(request.args.get("limit", 50)), 500)
        search = request.args.get("search", "").strip()
        cols = columns()
        wanted = ["id","case_number","date","block","primary_type",
                  "description","arrest","domestic","district_code",
                  "community_code"]
        selected = [c for c in wanted if c in cols]
        sql = f"SELECT {', '.join(selected)} FROM chicago_crime"
        params = []
        if search and "case_number" in cols:
            sql += " WHERE case_number LIKE ?"
            params.append(f"%{search}%")
        if "id" in cols:
            sql += " ORDER BY id DESC"
        sql += " LIMIT ?"
        params.append(limit)
        with connect() as con:
            rows = con.execute(sql, params).fetchall()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/api/crimes/<int:crime_id>", methods=["GET"])
def get_crime(crime_id):
    try:
        with connect() as con:
            row = con.execute(
                "SELECT * FROM chicago_crime WHERE id=?", (crime_id,)
            ).fetchone()
        return (jsonify(dict(row)) if row
                else (jsonify(error="Record not found"), 404))
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/api/crimes", methods=["POST"])
def create_crime():
    try:
        data = request.get_json(silent=True) or {}
        valid = set(columns())
        data = {k:v for k,v in data.items() if k in valid and k != "id"}
        if not data:
            return jsonify(error="No valid fields supplied"), 400
        fields = ", ".join(data)
        marks = ", ".join("?" for _ in data)
        with connect() as con:
            cur = con.execute(
                f"INSERT INTO chicago_crime ({fields}) VALUES ({marks})",
                list(data.values()))
            con.commit()
        return jsonify(message="Record created", id=cur.lastrowid), 201
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/api/crimes/<int:crime_id>", methods=["PUT"])
def update_crime(crime_id):
    try:
        data = request.get_json(silent=True) or {}
        valid = set(columns())
        data = {k:v for k,v in data.items() if k in valid and k != "id"}
        if not data:
            return jsonify(error="No valid fields supplied"), 400
        assignments = ", ".join(f"{k}=?" for k in data)
        with connect() as con:
            cur = con.execute(
                f"UPDATE chicago_crime SET {assignments} WHERE id=?",
                list(data.values()) + [crime_id])
            con.commit()
        if not cur.rowcount:
            return jsonify(error="Record not found"), 404
        return jsonify(message="Record updated")
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/api/crimes/<int:crime_id>", methods=["DELETE"])
def delete_crime(crime_id):
    try:
        with connect() as con:
            cur = con.execute(
                "DELETE FROM chicago_crime WHERE id=?", (crime_id,))
            con.commit()
        if not cur.rowcount:
            return jsonify(error="Record not found"), 404
        return jsonify(message="Record deleted")
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/graphs/<path:name>")
def graph(name):
    path = GRAPHS / name
    if not path.is_file():
        return jsonify(error="Graph not found"), 404
    return send_file(path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
