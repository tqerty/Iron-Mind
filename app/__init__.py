from flask import Flask, render_template, request, session
from database.security import secure, check_password
from database.logic_db import create_tables, insert_user, check_user, get_hash, get_name
from .checking import check_data
import hashlib
from app import ai
from app.ai import load_messages


def create_app():
    app = Flask(__name__)
    create_tables()
    app.secret_key = hashlib.md5(b"salt").hexdigest()
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
            hash = get_hash(login)
            if hash != None and check_password(password, hash):
                session['login'] = login
                info = load_messages(login)
                return render_template('page.html', name=get_name(login), info=info)
            else:
                return render_template('errors.html', problem = 'Логин и пароль не нашлись')
        else:
            if 'login' in session:
                return render_template('page.html', name=get_name(session['login']), info=load_messages(session['login']))
            else:
                return 'У вас нет доступа, авторизуйтесь'

    @app.route('/error')
    def erors():
        return render_template('errors.html')
    
    @app.route('/response', methods=['POST'])
    async def response():
        if 'login' not in session:
            return 'У вас нет доступа, авторизуйтесь', 401
        re = request.form['responsible']
        login = session['login']
        await ai.gpt_io(re, login)
        return render_template(
            'page.html',
            name=get_name(login),
            info=load_messages(login)
        )

    
    @app.route('/exit', methods = ['POST'])
    def exit():
        del session['login']
        return render_template('index.html')
    return app 





