# Proyecto Docker Compose con FastAPI y Base de Datos

API CRUD desarrollada con FastAPI y Docker Compose, utilizando PostgreSQL como base de datos.

## Requisitos Previos

- Docker instalado
- Docker Compose instalado

## Instalación y Ejecución

### 1. Construir y ejecutar los contenedores

```bash
docker compose up --build
```

Este comando construirá la imagen de la aplicación y levantará ambos contenedores (aplicación y base de datos).

### 2. Verificar que los servicios están corriendo

```bash
docker compose ps
```

### 3. Ver los logs

```bash
# Ver todos los logs
docker compose logs

# Ver logs de un servicio específico
docker compose logs app
docker compose logs db
```

### 4. Detener los contenedores

```bash
docker compose down
```

### 5. Detener y eliminar volúmenes (elimina los datos)

```bash
docker compose down -v
```

## Endpoints de la API

Una vez que la aplicación esté corriendo, estará disponible en `http://localhost:8080`

| Método | Ruta | Descripción | Respuestas posibles |
|---|---|---|---|
| `GET` | `/estudiantes` | Lista todos los estudiantes | 200 |
| `GET` | `/estudiantes/{id}` | Obtiene un estudiante | 200; 404 si no existe |
| `POST` | `/estudiantes` | Crea un estudiante | 201; 409 si el email ya existe; 422 si un campo no es válido |
| `DELETE` | `/estudiantes/{id}` | Borra un estudiante | 204; 404 si no existe |

Las rutas con `{id}` devuelven 422 si el `id` no es un número entero.

Cuerpo de `POST /estudiantes`:

```json
{"nombre": "Ana", "email": "ana@example.com", "edad": 21}
```

- `nombre`: texto de al menos 1 carácter.
- `email`: dirección de correo válida. No puede repetirse.
- `edad`: entero mayor o igual que 0.

Cada petición que pasa la validación escribe una línea `INFO` en el log, y los 404 y 409 escriben además una línea `WARNING`. Para consultar el log, ejecuta `docker compose logs app`.

## Documentación Interactiva

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

## Estructura del Proyecto

- `docker-compose.yml`: Configuración de servicios y red
- `Dockerfile`: Configuración de la imagen de la aplicación
- `main.py`: Código de la aplicación FastAPI
- `requirements.txt`: Dependencias de Python

## Notas

- Los datos de la base de datos persisten en un volumen de Docker
- Los contenedores se comunican a través de una red personalizada
- El puerto 8080 está expuesto al host para acceder a la API
