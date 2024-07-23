import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False)
    propietario = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_salida = db.Column(db.DateTime, nullable=True)

@app.route('/')
def index():
    vehiculos = Vehiculo.query.all()
    return render_template('index.html', vehiculos=vehiculos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        placa = request.form['placa']
        propietario = request.form['propietario']
        modelo = request.form['modelo']
        fecha_ingreso = datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%dT%H:%M')
        nuevo_vehiculo = Vehiculo(placa=placa, propietario=propietario, modelo=modelo, fecha_ingreso=fecha_ingreso)
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    if request.method == 'POST':
        vehiculo.placa = request.form['placa']
        vehiculo.propietario = request.form['propietario']
        vehiculo.modelo = request.form['modelo']
        vehiculo.fecha_ingreso = datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%dT%H:%M')
        if request.form['fecha_salida']:
            vehiculo.fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%dT%H:%M')
        else:
            vehiculo.fecha_salida = None
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', vehiculo=vehiculo)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    db.session.delete(vehiculo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('vehiculos.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
