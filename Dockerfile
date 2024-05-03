# Utilizamos una imagen base adecuada para nuestra aplicación. En este caso, usaremos una imagen de Python.
FROM python:3.9-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos de Python
COPY requirements.txt .

# Instalamos las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente de la aplicación al contenedor
COPY . .

# Se recomienda configurar el archivo .dockerignore para evitar la inclusión de archivos innecesarios en la imagen
# Se ignora .git, archivos de pruebas, archivos temporales, etc.

# Creamos un archivo .env-example que servirá como plantilla para configurar las variables de entorno
# En este ejemplo, asumimos que las variables de entorno necesarias están documentadas en .env-example

# Se debería configurar el archivo .env en cada entorno de despliegue con las variables de entorno específicas

# Exponemos el puerto en el que se ejecuta la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
