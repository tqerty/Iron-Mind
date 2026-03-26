from flask import Flask, render_template, request, session
from database.security import secure
from database.logic_db import create_table, insert_user, check_user, check_l_p, get_name
from .checking import check_data
import hashlib

def create_app():
    app = Flask(__name__)
    create_table()
    app.secret_key = f'{hashlib.md5('salt'.encode())}'
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
        if check_data(name, login, password) == True:
            return render_template('errors.html', problem = 'Проверьте, пожалуйста, длину вашего логина (4 символа и более), длину пароля (8 символов и более) и ваше имя (не должен быть пустым)')
        elif check_user(login):
            return render_template('errors.html', problem = 'Логин занят')
        password = secure(password)
        insert_user(name, login, password)
        return "Регистрация прошла успешно!"
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.route('/admit', methods = ['GET', 'POST'])
    def admit():
        return render_template('admit.html')

    @app.route('/autorization', methods=['GET','POST'])
    def autorization():
        if request.method == 'POST':
            
            login = request.form['login']
            password = request.form['password']
            password = secure(password)
            if check_l_p(login, password) == True:
                session['login'] = login
                return render_template('page.html', name=get_name(session['login']))
            else:
                return render_template('errors.html', problem = 'Логин и пароль не нашлись')
        else:
            if 'login' in session:
                return render_template('page.html', name=get_name(session['login']))
            else:
                return 'У вас нет доступа, авторизуйтесь'

    @app.route('/error')
    def erors():
        return render_template('errors.html')
    return app 





