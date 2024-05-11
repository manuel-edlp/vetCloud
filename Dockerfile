# Utilizamos una imagen base adecuada para nuestra aplicación. En este caso, usaremos una imagen de Python.
FROM python:3.10-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos de Python
COPY requirements.txt .

# Instalamos las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente de la aplicación al contenedor
COPY . .

# Exponemos el puerto en el que se ejecuta la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]