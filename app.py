from flask import Flask, render_template, request

import math


app = Flask(__name__)


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
        calculo = math.hypot(int(cateto01), int(cateto02))
        return f"""
        A hipotenusa do triângulo equilátero de catetos
        {cateto01} e {cateto02} é : {calculo:.2f}
        """


if __name__ == "__main__":
    app.run(debug=True)
