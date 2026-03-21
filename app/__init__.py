from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/registration")
    def registration():
        return render_template("registration.html")

        
    app.run(debug = True)





