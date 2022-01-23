# Destacame Buses - Backend
Plataforma para registrar trayectos, choferes, buses, pasajeros y viajes con la opción de reserva de asientos.

### Guía de instalación
Crea un virtual enviroment
```bash
python3 -m venv myvenv
```
Ingresa a myvenv
```bash
cd myvenv/
```
Activa el entorno virtual
```bash
source bin/activate
```
Descarga el repositorio
```bash
git clone https://github.com/MistyBlunch/DestacameBuses.git
```
Ingresa al repositorio (back)
```bash
cd DestacameBuses/back/
```
Instala las dependencias
```bash
pip3 install -r requirements.txt
```
Crea una base datos en PostgreSQL
```bash
CREATE DATABASE agencia_buses;
```
En el archivo settings.py cambia las credenciales de password y user en la configuración de databases
```bash
'USER': '<user>',
'PASSWORD': '<password>',
```
Ejecuta las migraciones
```bash
python3 manage.py migrate
```
Corre el proyecto
```bash
python3 manage.py runserver
```

Made with :heart:
