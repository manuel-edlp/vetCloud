# VetCloud

Aplicación web de gestión de veterinaria para el trabajo integrador de Software Cloud. UTN-FRLP. 2024.

## Características

Permite el registro y gestión de proveedores, clientes, veterinarios, mascotas, productos y medicamentos.

Integración con IA de Azure: Utilizamos Azure Cognitive Services para mejorar la experiencia del usuario:

Extracción de Texto Inteligente: La aplicación puede extraer automáticamente texto de las etiquetas de los medicamentos, utilizando tecnología OCR (Reconocimiento Óptico de Caracteres), y autocompletar la descripción del producto.

Recomendaciones de Categorías: Al subir imágenes de productos, la IA de Azure analiza la imagen y sugiere categorías apropiadas para el producto, facilitando la organización y clasificación de los inventarios.

## Tecnologías
Tecnología Cloud: Azure

Motor de Base de Datos: PostgreSQL

FrameWork: Django

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

# Créditos y Agradecimientos

## Colaboradores Actuales
Morullo Manuel - Desarrollador principal y encargado del proyecto.

## Colaboradores Anteriores
Baez Gonzalo

Semper Juan Manuel

Abregu Candela

Gonzalez Lurbe Feliciano
