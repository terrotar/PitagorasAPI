from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


import math


# Criacao do app
app = Flask("PitagorasAPI")


# Implementacao do Database, Sessao local e modelo de classes
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sql_Pitagoras/sql_app.db"


# Sessão Local
db = SQLAlchemy(app)


# Modelos do Database
class Triangulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cateto01 = db.Column(db.Float, nullable=False)
    cateto02 = db.Column(db.Float, nullable=False)
    hipotenusa = db.Column(db.Float, nullable=False)

    def hipotenusa(self):
        hipotenusa = math.hypot(float(self.cateto01), float(self.cateto02))
        hipotenusa = round(hipotenusa, 2)
        self.hipotenusa = hipotenusa
        return self.hipotenusa


# Usado para criacao do Database
db.create_all()


# Marshmallow setup
# Criação do Marshmallow
ma = Marshmallow(app)


# Classes Marshmallow
class TrianguloSchema(ma.Schema):
    class Meta:
        fields = ("id", "cateto01", "cateto02", "hipotenusa")


triangulo_schema = TrianguloSchema()
triangulos_schema = TrianguloSchema(many=True)


# Endpoints
# Route Home Page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# Route Calculadora
@app.route('/calculadora', methods=['GET', 'POST'])
def calculadora():
    if(request.method == 'GET'):
        triangulos = Triangulo.query.all()
        api_triangulos = triangulos_schema.dump(triangulos)
        return render_template('calculadora.html',
                               triangulos=api_triangulos)
    else:
        if(request.form['cateto01'] and request.form['cateto02']):
            cateto01 = float(request.form['cateto01'])
            cateto02 = float(request.form['cateto02'])
            triangulo = Triangulo(cateto01=cateto01,
                                  cateto02=cateto02)
            db.session.add(triangulo)
            db.session.commit()
            return render_template('calculadora.html',
                                   triangulos=Triangulo.query.all())
        else:
            return render_template('calculadora.html',
                                   triangulos=Triangulo.query.all(),
                                   error=True)


# Routa funcao deletar todos resultados
@app.route('/calculadora/deletar/todos', methods=['GET'])
def deletar_todos():
    triangulos = Triangulo.query.all()
    for triangulo in triangulos:
        db.session.delete(triangulo)
        db.session.commit()
    return render_template('calculadora.html',
                           triangulos=Triangulo.query.all())


# Route funcao deletar triangulo especifico
@app.route('/calculadora/deletar/<int:triangulo_id>', methods=['GET'])
def deletar_triangulo(triangulo_id):
    triangulo = Triangulo.query.get_or_404(triangulo_id)
    db.session.delete(triangulo)
    db.session.commit()
    return render_template('calculadora.html',
                           triangulos=Triangulo.query.all())


# Route funcao editar triangulo especifico
@app.route('/calculadora/editar/<int:triangulo_id>', methods=['GET', 'POST'])
def editar_triangulo(triangulo_id):
    if(request.method == 'GET'):
        return render_template('editar.html',
                               triangulo_id=triangulo_id)
    else:
        triangulo = Triangulo.query.get_or_404(triangulo_id)
        triangulo.cateto01 = float(request.form['cateto01'])
        triangulo.cateto02 = float(request.form['cateto02'])
        db.session.commit()
        return render_template('calculadora.html',
                               triangulos=Triangulo.query.all())


# Rota resultados formato JSON
@app.route('/calculadora/json', methods=['GET'])
def get_json():
    triangulos = Triangulo.query.all()
    for triangulo in triangulos:
        hipotenusa = int(triangulo.hipotenusa())
        triangulo.hipotenusa = hipotenusa
    db.session.commit()
    resultados = triangulos_schema.dump(triangulos)
    return jsonify(resultados)


if __name__ == "__main__":
    app.run(debug=True)
