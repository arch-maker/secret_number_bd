import hashlib
import random
import uuid

from flask import Flask, render_template, request, redirect, url_for, make_response
from model import User, db

app = Flask(__name__)
db.create_all()


@app.route("/")
def index():
    token_session = request.cookies.get("token_session")

    if token_session:
        user = db.query(User).filter_by(token_session=token_session).first()

    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")

    hash_pass = hashlib.sha256(password.encode()).hexdigest()

    secret_number = random.randint(1, 30)

    user = User(name=name, email=email, secret_number=secret_number, password=hash_pass)

    db.add(user)
    db.commit()

    if hash_pass != user.password:
        return "Contraseña incorrecta! Introduzca la contraseña correcta!"

    elif hash_pass == user.password:

        token_session = str(uuid.uuid4())

        user.token_session = token_session
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('index')))
        response.set_cookie("token_session", token_session, httponly=True, samesite='Strict')

        return response


@app.route("/result", methods=["POST"])
def result():
    num_user = int(request.form.get("num_user"))

    token_session = request.cookies.get("token_session")

    user = db.query(User).filter_by(token_session=token_session).first()

    if num_user == user.secret_number:

        mensaje = "Enhorabuena!! El numero correcto es: " + str(num_user)

        new_secret = random.randint(1, 30)

        user.secret_number = new_secret

        db.add(user)
        db.commit()

        return render_template("result.html", mensaje=mensaje)

    elif num_user > user.secret_number:
        mensaje = "Tu numero no es correcto! Intentalo con uno mas pequeño!"
        return render_template("result.html", mensaje=mensaje)

    elif num_user < user.secret_number:
        mensaje = "Tu numero no es correcto! Intentalo con uno mas grande!"
        return render_template("result.html", mensaje=mensaje)


if __name__ == '__main__':
    app.run()