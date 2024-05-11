# Vetsoft

Aplicación web para veterinarias utilizada en la cursada 2024 de Ingeniería y Calidad de Software. UTN-FRLP

## Dependencias

- python 3
- Django
- sqlite
- playwright
- ruff

## Instalar dependencias

`pip install -r requirements.txt`

## Iniciar la Base de Datos

`python manage.py migrate`

## Iniciar app

`python manage.py runserver`

## Integrantes:

Baez Gonazalo - Proveedor
Semper, Juan Manuel - Producto
Morullo Manuel  - Mascota
Abregu Candela - Veterinario
González Lurbé, Feliciano - Medicamento

## Docker Baez Gonzalo
Comando utilizado para crear el contenedor
>> docker build --build-arg VERSION=1.0 -t vetsoft-app:1.0 .

Comando utilizado para crear la imagen 
>> docker run -p 8000:8000 --name vetsoft-v0 vetsoft-app:1.0

Comando para utilizar mi imagen
>> docker start vetsoft-v0

## Docker Gonzalez Lurbe Feliciano

## Docker Semper Juan Manuel

## Docker Abregu Candela

## Docker Morullo Manuel