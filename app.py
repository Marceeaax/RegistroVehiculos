import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapa = db.Column(db.String(10), nullable=False, unique=True)
    propietario = db.Column(db.String(30), nullable=False)
    modelo = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    area = db.Column(db.String(15), nullable=False)
    contacto = db.Column(db.String(15), nullable=False)
    observacion = db.Column(db.String(30), nullable=True)

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    page = request.args.get('page', page, type=int)
    per_page = 7
    filters = []
    chapa = request.args.get('chapa')
    propietario = request.args.get('propietario')
    modelo = request.args.get('modelo')
    color = request.args.get('color')
    area = request.args.get('area')
    
    if chapa:
        filters.append(Vehiculo.chapa.like(f'%{chapa}%'))
    if propietario:
        filters.append(Vehiculo.propietario.like(f'%{propietario}%'))
    if modelo:
        filters.append(Vehiculo.modelo.like(f'%{modelo}%'))
    if color:
        filters.append(Vehiculo.color.like(f'%{color}%'))
    if area:
        filters.append(Vehiculo.area.like(f'%{area}%'))
    
    vehiculos = Vehiculo.query.filter(*filters).paginate(page=page, per_page=per_page, error_out=False)
    total_pages = vehiculos.pages

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'vehiculos': [
                {
                    'id': v.id,
                    'chapa': v.chapa,
                    'propietario': v.propietario,
                    'modelo': v.modelo,
                    'color': v.color,
                    'area': v.area,
                    'contacto': v.contacto,
                    'observacion': v.observacion
                } for v in vehiculos.items
            ],
            'pages': total_pages,
            'current_page': page
        })

    return render_template('index.html', vehiculos=vehiculos.items, pages=range(1, total_pages + 1), current_page=page)

@app.route('/agregar', methods=['POST'])
def agregar():
    chapa = request.form['chapa']
    propietario = request.form['propietario']
    modelo = request.form['modelo']
    modelo = re.sub(r'\b[a-z]', lambda match: match.group().upper(), modelo)
    color = request.form['color']
    color = color.capitalize()
    area = request.form['area']
    contacto = request.form['contacto']
    observacion = request.form['observacion']
    nuevo_vehiculo = Vehiculo(chapa=chapa, propietario=propietario, modelo=modelo, color=color, area=area, contacto=contacto, observacion=observacion)
    
    try:
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        return jsonify(success=True)
    except IntegrityError:
        db.session.rollback()
        return jsonify(success=False, error='La chapa ya existe. Por favor, ingresa una chapa diferente.'), 400

@app.route('/vehiculo/<int:id>', methods=['GET'])
def obtener_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    return jsonify(id=vehiculo.id, chapa=vehiculo.chapa, propietario=vehiculo.propietario, modelo=vehiculo.modelo, color=vehiculo.color, area=vehiculo.area, contacto=vehiculo.contacto, observacion=vehiculo.observacion)

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    vehiculo.chapa = request.form['chapa']
    vehiculo.propietario = request.form['propietario']
    vehiculo.modelo = request.form['modelo']
    vehiculo.color = request.form['color']
    vehiculo.area = request.form['area']
    vehiculo.contacto = request.form['contacto']
    vehiculo.observacion = request.form['observacion']
    try:
        db.session.commit()
        return jsonify(success=True)
    except IntegrityError:
        db.session.rollback()
        return jsonify(success=False, error='La chapa ya existe. Por favor, ingresa una chapa diferente.'), 400

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
