import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapa = db.Column(db.String(10), nullable=False, unique=True)
    propietario = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(15), nullable=False)

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    per_page = 10
    vehiculos = Vehiculo.query.paginate(page=page, per_page=per_page, error_out=False)
    total_pages = vehiculos.pages
    return render_template('index.html', vehiculos=vehiculos.items, pages=range(1, total_pages + 1), current_page=page)

@app.route('/agregar', methods=['POST'])
def agregar():
    chapa = request.form['chapa']
    propietario = request.form['propietario']
    modelo = request.form['modelo']
    color = request.form['color']
    area = request.form['area']
    contacto = request.form['contacto']
    nuevo_vehiculo = Vehiculo(chapa=chapa, propietario=propietario, modelo=modelo, color=color, area=area, contacto=contacto)
    db.session.add(nuevo_vehiculo)
    db.session.commit()
    return jsonify(success=True)

@app.route('/vehiculo/<int:id>', methods=['GET'])
def obtener_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    return jsonify(id=vehiculo.id, chapa=vehiculo.chapa, propietario=vehiculo.propietario, modelo=vehiculo.modelo, color=vehiculo.color, area=vehiculo.area, contacto=vehiculo.contacto)

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    vehiculo.chapa = request.form['chapa']
    vehiculo.propietario = request.form['propietario']
    vehiculo.modelo = request.form['modelo']
    vehiculo.color = request.form['color']
    vehiculo.area = request.form['area']
    vehiculo.contacto = request.form['contacto']
    db.session.commit()
    return jsonify(success=True)

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
