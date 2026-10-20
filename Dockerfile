# Crear Dockerfile para la aplicación FastAPI
FROM python:3.11-slim

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos requirements.txt e instalamos dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la aplicación
COPY main.py .

# Cambiamos el ownership y usuario
RUN chown -R appuser:appuser /app
USER appuser

# Exponemos el puerto 8080
EXPOSE 8080

# Ejecutamos aplicación con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
