# Generating a list of 100 vehicle brands
marcas_vehiculos = [
    "Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW", "Mercedes-Benz", "Volkswagen",
    "Audi", "Hyundai", "Kia", "Mazda", "Subaru", "Lexus", "Jeep", "Dodge", "Chrysler", "Cadillac",
    "GMC", "Buick", "Ram", "Volvo", "Porsche", "Jaguar", "Land Rover", "Infiniti", "Lincoln",
    "Acura", "Mitsubishi", "Mini", "Tesla", "Fiat", "Alfa Romeo", "Maserati", "Ferrari", "Lamborghini",
    "Bentley", "Rolls-Royce", "Aston Martin", "McLaren", "Pagani", "Bugatti", "Suzuki", "Peugeot",
    "Renault", "Citroën", "Skoda", "SEAT", "Saab", "Hummer", "Pontiac", "Saturn", "Oldsmobile",
    "Scion", "Genesis", "Smart", "Fisker", "Rivian", "Lucid", "Polestar", "Opel", "Vauxhall",
    "Lancia", "Dacia", "Zotye", "Geely", "Great Wall", "Chery", "BYD", "MG", "Proton", "Perodua",
    "Mahindra", "Tata", "Maruti Suzuki", "Isuzu", "SsangYong", "Holden", "HSV", "Foton", "BAIC",
    "FAW", "Dongfeng", "Haval", "JAC", "Lifan", "Roewe", "Wuling", "Hongqi", "Brilliance", "DFSK",
    "Nio", "XPeng", "VinFast", "GAC", "Changan", "WEY", "Daewoo"
]

marcas_motos = [
    "Kenton", "Yamaha", "Maruti", "Leopard", "Star", "Yamazuky"
]

# Escribir la lista a un TXT file
file_path = 'lista_vehiculos.txt'
with open(file_path, 'w') as file:
    for brand in marcas_vehiculos:
        file.write(brand + '\n')

file_path
