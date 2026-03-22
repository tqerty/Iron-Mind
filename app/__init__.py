from flask import Flask, render_template, request
from database.security import secure
from database.logic_db import create_table, insert_user


def create_app():
    app = Flask(__name__)
    create_table()

    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/registration")
    def registration():
        return render_template("registration.html")
    
    @app.route("/registr", methods=["POST"])
    def registr():
        name = request.form['name']
        login = request.form['login']
        password = request.form['password']
        password = secure(password)
        insert_user(name, login, password)
        return "Регистрация прошла успешно!"
    
    app.run(debug = True)





