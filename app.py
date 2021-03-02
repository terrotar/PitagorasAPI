from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


import math


# Criação do app
app = Flask("PitagorasAPI")


# Implementação do Database, Sessão local e modelo de classes
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sql_Pitagoras/sql_app.db"


# Sessão Local
db = SQLAlchemy(app)


# Modelos do Database
class Triangulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cateto01 = db.Column(db.Float, nullable=False)
    cateto02 = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"""
                    Triangulo {self.id} criado com sucesso.
                """


# Usado para criação do Database
db.create_all()


# Endpoints
# Route da Home Page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/calculadora', methods=['GET', 'POST'])
def calculadora():
    if(request.method == 'GET'):
        return render_template('calculadora.html')
    else:
        cateto01 = request.form['cateto01']
        cateto02 = request.form['cateto02']
        calculo = math.hypot(float(cateto01), float(cateto02))
        return f"""
        A hipotenusa do triângulo equilátero de catetos
        {cateto01} e {cateto02} é : {calculo:.2f}
        """


if __name__ == "__main__":
    app.run(debug=True)
