﻿# Aplicación de Gestión de Vehículos

Esta es una aplicación de gestión de vehículos desarrollada utilizando Flask y SQLite, y actualmente servida con Waitress para el Instituto Nacional de Estadística del Paraguay. La aplicación permite administrar información relacionada con vehículos de manera sencilla y eficiente, y se encuentra en desarrollo una versión móvil con HTML y CSS separados.

## Características

- **Gestión de vehículos:** Crear, modificar, listar y eliminar vehículos en la base de datos.
- **Filtrado avanzado:** Filtrado de registros utilizando sentencias SQL.
- **Paginación con AJAX:** Navegación fluida entre páginas de resultados sin recargar la página.
- **Interfaz moderna:** Uso de Bootstrap para el diseño de tablas y modales.
- **Alertas dinámicas:** SweetAlert2 para mostrar mensajes de error, información y éxito.
- **Contacto directo:** Funcionalidad para escribir directamente al WhatsApp del contacto desde la tabla de vehículos.
- **Registro de eventos:** Registro de logs en `access.log` de las solicitudes HTML (GET, POST, DELETE, UPDATE, OPTIONS, etc.) recibidas en el servidor.
- **Animaciones CSS:** Animaciones suaves para mejorar la experiencia del usuario.
- **Restricciones JavaScript:** Validaciones que impiden la entrada de números en campos donde solo se esperan letras (e.g., "propietario") y capitalización automática en el campo "chapa".
- **Versión móvil en desarrollo:** Una versión optimizada para dispositivos móviles está en desarrollo, con HTML y CSS separados.

## Requisitos

Antes de iniciar con la instalación, asegúrate de tener instalado lo siguiente:

- Python 3.8 o superior
- Flask 2.x
- SQLite
- Waitress

Las dependencias adicionales están listadas en el archivo `requirements.txt`.

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. **Crear un entorno virtual e instalar dependencias:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurar el entorno de desarrollo o producción:**

   Para ejecutar el entorno de desarrollo, descomenta la configuración del entorno de desarrollo en `app.py` y comenta la configuración del entorno de producción. El entorno de desarrollo utiliza el puerto 5000, mientras que el entorno de producción utiliza el puerto 8080.

   ```python
   # Configuración para desarrollo
   # app.run(debug=True, port=5000)

   # Configuración para producción
   # waitress.serve(app, host="0.0.0.0", port=8080)
   ```

4. **Ejecutar el servidor:**

   Para el entorno de desarrollo y producción:

   ```bash
   python app.py
   ```

5. **Poblar la base de datos (opcional):**

   Si deseas poblar la base de datos con datos ficticios para pruebas, puedes ejecutar el siguiente comando:

   ```bash
   python poblar.py
   ```

## Uso

- Accede a la aplicación desde tu navegador utilizando la URL `http://127.0.0.1:5000` para el entorno de desarrollo o `http://127.0.0.1:8080` para el entorno de producción.
- Navega por las diferentes secciones para agregar, modificar, listar o eliminar vehículos.
- Utiliza el filtrado avanzado para buscar vehículos específicos.
- Escribe directamente al WhatsApp del contacto desde la tabla de vehículos.

## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una rama nueva para tu funcionalidad o corrección de errores (`git checkout -b nombre-rama`).
3. Realiza tus cambios y haz commit (`git commit -am 'Descripción de cambios'`).
4. Haz push a la rama (`git push origin nombre-rama`).
5. Crea un Pull Request en GitHub.

## Limitaciones

- **Autenticación:** Actualmente, la aplicación no cuenta con un sistema de autenticación implementado. Esta característica será añadida en futuras versiones.

## Contacto

Si tienes alguna pregunta o sugerencia, puedes contactar al desarrollador principal:

- **Nombre:** Marcelo Aguayo
- **Email:** marcelo.adrian2011@fpuna.edu.py
- **GitHub:** [Marceeaax](https://github.com/Marceeaax)
