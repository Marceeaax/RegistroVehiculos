import unicodedata
import os
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func

# Variable global para las áreas
areas = [
    "Encuestas (DED)", "Informatica", "Codificacion", "Logistica",
    "Cartografia", "Talentos Humanos (DTH)", "Segmentacion", "Movilidad",
    "Pre-Critica", "Viaticos", "Direccion Administrativa", "Transporte",
    "DESD", "DEE", "Digitacion", "Combustibles", "Central", "Servicios", "Reclutamiento", "EPH",
    "Patrimonio", "Central", "DEH", "Informatica T1"
]

# Función para eliminar acentos de una cadena de texto
def eliminar_acentos(input_str):
    if isinstance(input_str, str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return input_str

# Función para normalizar las columnas de la base de datos reemplazando caracteres acentuados
def normalizar_columna(column):
    column = func.replace(column, 'á', 'a')
    column = func.replace(column, 'Á', 'A')
    column = func.replace(column, 'é', 'e')
    column = func.replace(column, 'É', 'E')
    column = func.replace(column, 'í', 'i')
    column = func.replace(column, 'Í', 'I')
    column = func.replace(column, 'ó', 'o')
    column = func.replace(column, 'Ó', 'O')
    column = func.replace(column, 'ú', 'u')
    column = func.replace(column, 'Ú', 'U')
    column = func.replace(column, 'ñ', 'n')
    column = func.replace(column, 'Ñ', 'N')
    column = func.lower(column)
    return column

# Función para detectar si el usuario está utilizando un dispositivo móvil
def es_movil(user_agent):
    navegadores_moviles = ["iphone", "android", "blackberry", "nokia", "opera mini", "windows mobile", "windows phone", "iemobile"]
    user_agent = user_agent.lower()
    return any(navegador_movil in user_agent for navegador_movil in navegadores_moviles)

# Función para detectar el sistema operativo del usuario
def obtener_sistema_operativo(user_agent):
    user_agent = user_agent.lower()
    if 'windows' in user_agent:
        return 'Windows'
    elif 'android' in user_agent:
        return 'Android'
    elif 'iphone' in user_agent or 'ipad' in user_agent:
        return 'iOS'
    elif 'mac' in user_agent:
        return 'MacOS'
    elif 'linux' in user_agent:
        return 'Linux'
    else:
        return 'Otro'

def formatear_numero(numero):
    if numero.startswith('0'):
        numero = numero[1:]  # Eliminar el primer dígito si es '0'
    return '595' + numero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo Vehiculo
class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapa = db.Column(db.String(7), nullable=False, unique=True)
    propietario = db.Column(db.String(30), nullable=False)
    modelo = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    area = db.Column(db.String(15), nullable=False)
    contacto = db.Column(db.String(15), nullable=False)
    observacion = db.Column(db.String(30), nullable=True)
    # moto = db.Column(db.Boolean, default=False) Falta implementar condicionales 

# Middleware para registrar las IPs
class LogIPMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        ip = environ.get('REMOTE_ADDR')
        method = environ.get('REQUEST_METHOD')
        path = environ.get('PATH_INFO')
        user_agent = environ.get('HTTP_USER_AGENT', '')
        os_type = obtener_sistema_operativo(user_agent)
        now = datetime.now().strftime('%H:%M %d/%m/%Y')
        log_message = f'IP "{ip}" realizó una solicitud {method} a la ruta {path} usando {os_type} a las {now}'
        
        # Imprimir en la consola
        print(log_message)
        
        # Registrar en un archivo de texto
        with open("access.log", "a") as log_file:
            log_file.write(log_message + "\n")
        
        return self.app(environ, start_response)

app.wsgi_app = LogIPMiddleware(app.wsgi_app)

# Ruta para la página principal
@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    user_agent = request.headers.get('User-Agent')
    template = 'index_mobile.html' if es_movil(user_agent) else 'index.html'

    page = request.args.get('page', page, type=int)
    per_page = 7
    filters = []
    chapa = request.args.get('chapa')
    propietario = request.args.get('propietario')
    modelo = request.args.get('modelo')
    color = request.args.get('color')
    area = request.args.get('area')
    
    if chapa:
        chapa = eliminar_acentos(chapa).lower()
        filters.append(normalizar_columna(Vehiculo.chapa).like(f'%{chapa}%'))
    if propietario:
        propietario = eliminar_acentos(propietario).lower()
        filters.append(normalizar_columna(Vehiculo.propietario).like(f'%{propietario}%'))
    if modelo:
        modelo = eliminar_acentos(modelo).lower()
        filters.append(normalizar_columna(Vehiculo.modelo).like(f'%{modelo}%'))
    if color:
        color = eliminar_acentos(color).lower()
        filters.append(normalizar_columna(Vehiculo.color).like(f'%{color}%'))
    if area:
        area = eliminar_acentos(area).lower()
        filters.append(normalizar_columna(Vehiculo.area).like(f'%{area}%'))
    
    vehiculos = Vehiculo.query.filter(*filters).paginate(page=page, per_page=per_page, error_out=False)
    total_pages = vehiculos.pages

    pages = get_display_pages(page, total_pages)

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
                    'observacion': v.observacion,
                    'whatsapp': formatear_numero(v.contacto)
                } for v in vehiculos.items
            ],
            'pages': total_pages,
            'current_page': page,
            'display_pages': pages
        })

    return render_template(template, vehiculos=vehiculos.items, pages=pages, current_page=page, areas=areas)

def get_display_pages(current_page, total_pages, delta=2):
    pages = []
    for i in range(max(1, current_page - delta), min(total_pages + 1, current_page + delta + 1)):
        pages.append(i)
    if 1 not in pages:
        pages.insert(0, 1)
    if total_pages not in pages:
        pages.append(total_pages)
    return pages

# Ruta para agregar un nuevo vehículo
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

# Ruta para obtener la información de un vehículo específico
@app.route('/vehiculo/<int:id>', methods=['GET'])
def obtener_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    return jsonify(id=vehiculo.id, chapa=vehiculo.chapa, propietario=vehiculo.propietario, modelo=vehiculo.modelo, color=vehiculo.color, area=vehiculo.area, contacto=vehiculo.contacto, observacion=vehiculo.observacion)

# Ruta para editar la información de un vehículo existente
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

# Ruta para eliminar un vehículo
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
    
    # ENTORNO DE PRODUCCIÓN (HACER PIP INSTALL WAITRESS)
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
    
    """ # ENTORNO DE DESARROLLO
    app.run(debug=True) """
