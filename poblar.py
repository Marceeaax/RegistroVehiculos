import json
from app import app, db, Vehiculo

def populate_db():
    with open('vehiculos.json') as f:
        data = json.load(f)
    
    for item in data:
        vehiculo = Vehiculo(
            chapa=item['chapa'],
            propietario=item['propietario'],
            modelo=item['modelo'],
            color=item['color'],
            area=item['area'],
            contacto=item['contacto']
        )
        db.session.add(vehiculo)
    
    db.session.commit()
    print("Datos insertados correctamente!")

if __name__ == '__main__':
    with app.app_context():
        populate_db()
