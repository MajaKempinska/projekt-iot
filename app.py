from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("czesc.html")

@app.route("/maja")
def o_mai():
    return render_template("maja.html")

@app.route("/asia")
def o_asi():
    return render_template("asia.html")

@app.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    if request.method == "POST":
        imie = request.form.get("imie")
        email = request.form.get("email")
        wiadomosc = request.form.get("wiadomosc")
        print(f"Nowa wiadomość od {imie} ({email}): {wiadomosc}")
        return render_template("podziekowanie.html", imie=imie, email=email)
    return render_template("kontakt.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)