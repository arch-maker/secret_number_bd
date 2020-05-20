import random
from flask import Flask, render_template, request, redirect, url_for, make_response
from model import User, db

app = Flask(__name__)
db.create_all()


@app.route("/")
def index():
    email_address = request.cookies.get("email")

    if email_address:
        user = db.query(User).filter_by(email=email_address).first()

    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    secret_number = random.randint(1, 30)

    user = User(name=name, email=email, secret_number=secret_number)

    db.add(user)
    db.commit()

    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response


@app.route("/result", methods=["POST"])
def result():
    num_user = int(request.form.get("num_user"))

    email_addr = request.cookies.get("email")

    user = db.query(User).filter_by(email=email_addr).first()

    sn = user.secret_number

    if num_user == sn:
        mensaje = "Enhorabuena!! El numero correcto es: " + str(num_user)
        return render_template("result.html", mensaje=mensaje)

        new_secret = random.randint(1, 30)

        user.secret_number = new_secret

        db.add(user)
        db.commit()

    elif num_user > sn:
        mensaje = "Tu numero no es correcto! Intentalo con uno mas pequeño!"
        return render_template("result.html", mensaje=mensaje)

    elif num_user < sn:
        mensaje = "Tu numero no es correcto! Intentalo con uno mas grande!"
        return render_template("result.html", mensaje=mensaje)


if __name__ == '__main__':
    app.run()