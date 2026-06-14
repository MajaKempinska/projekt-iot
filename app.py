import os
from flask import Flask, render_template, request

# pyodbc jest tylko w kontenerze (chmura). Lokalnie moze go nie byc -
# wtedy aplikacja dziala bez bazy (do podgladu stron), zamiast sie wywalac.
try:
    import pyodbc
    PYODBC_OK = True
except ModuleNotFoundError:
    PYODBC_OK = False

app = Flask(__name__)

def get_connection():
    conn_str = os.environ.get("SQL_CONNECTION")
    return pyodbc.connect(conn_str)

def init_db():
    if not PYODBC_OK:
        print("pyodbc niedostepny (tryb lokalny) - pomijam tworzenie tabeli")
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='wiadomosci' AND xtype='U')
            CREATE TABLE wiadomosci (
                id INT IDENTITY(1,1) PRIMARY KEY,
                imie NVARCHAR(100),
                email NVARCHAR(200),
                wiadomosc NVARCHAR(MAX),
                data DATETIME DEFAULT GETDATE()
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Blad inicjalizacji bazy: {e}")

@app.route("/")
def hello():
    return render_template("czesc.html")

@app.route("/maja")
def o_mai():
    return render_template("maja.html")

@app.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    if request.method == "POST":
        imie = request.form.get("imie")
        email = request.form.get("email")
        wiadomosc = request.form.get("wiadomosc")
        if PYODBC_OK:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO wiadomosci (imie, email, wiadomosc) VALUES (?, ?, ?)",
                    imie, email, wiadomosc
                )
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Blad zapisu do bazy: {e}")
        else:
            print(f"(tryb lokalny) wiadomosc od {imie} ({email}): {wiadomosc}")
        return render_template("podziekowanie.html", imie=imie, email=email)
    return render_template("kontakt.html")

@app.route("/wiadomosci")
def wiadomosci():
    lista = []
    if PYODBC_OK:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT imie, email, wiadomosc, data FROM wiadomosci ORDER BY data DESC")
            lista = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"Blad odczytu z bazy: {e}")
    return render_template("wiadomosci.html", wiadomosci=lista)

# Utworzenie tabeli przy starcie aplikacji (dziala tez pod gunicorn w chmurze)
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)