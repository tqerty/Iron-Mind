from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/registration")
    def registration():
        return render_template("registration.html")
    
    @app.route("/registr", methods=['GET', 'POST'])
    def registr():
        result = request.form['name']
        return "Регистрация прошла успешно!"      
    app.run(debug = True)





