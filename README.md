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

## Ejecutar tests unitarios y de integracion
`python manage.py test app`

## Ejecutar tests e2e
`python manage.py test functional_tests`

## Ejecutar analisis de coverage de los test 
`coverage run --source="./app" --omit="./app/migrations/**" manage.py test app `

`coverage report`

## Integrantes:

Baez Gonazalo - Proveedor
Semper, Juan Manuel - Producto
Morullo Manuel  - Mascota
Abregu Candela - Veterinario
González Lurbé, Feliciano - Medicamento

## Docker Baez Gonzalo
Comando utilizado para construir imagen
>> docker build --build-arg VERSION=1.0 -t vetsoft-app:1.0 .

Comando utilizado para crear y ejecutar contenedor
>> docker run -p 8000:8000 --name vetsoft-v0 vetsoft-app:1.0

Comando para utilizar mi imagen
>> docker start vetsoft-v0

## Docker Gonzalez Lurbe Feliciano
Comando utilizado para construir imagen
docker build --build-arg VERSION=1.1 -t vetsoft-app:1.1 .

Comando utilizado para crear y ejecutar contenedor
>> docker run -p 8000:8000 --name vetsoft-v1 vetsoft-app:1.1

Comando para utilizar mi imagen
>> docker start vetsoft-v1

## Docker Semper Juan Manuel
Comando utilizado para construir imagen
>> docker build --build-arg VERSION=1.2 -t vetsoft-app:1.2 .

Comando utilizado para crear y ejecutar contenedor
>> docker run -p 8000:8000 --name vetsoft-v0 vetsoft-app:1.2

Comando para utilizar mi imagen
>> docker start vetsoft-v2

## Docker Abregu Candela
Comando utilizado para construir imagen
>> docker build --build-arg VERSION=1.3 -t vetsoft-app:1.3 .

Comando utilizado para crear y ejecutar contenedor
>> docker run -p 8000:8000 --name vetsoft-v3 vetsoft-app:1.3

Comando para utilizar mi imagen
>> docker start vetsoft-v3

## Docker Morullo Manuel
Comando utilizado para construir imagen
>> docker build --build-arg VERSION=1.4 -t vetsoft-app:1.4 .

Comando utilizado para crear y ejecutar contenedor
>> docker run -p 8000:8000 --name vetsoft-v4 vetsoft-app:1.4

Comando para utilizar mi imagen
>> docker start vetsoft-v4

