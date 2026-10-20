from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configurar conexión a base de datos
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        logging.error(f"La variable de entorno '{var_name}' no está definida.")
        sys.exit(1)

DATABASE_URL = get_env_variable('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Configuramos las clases de la base de datos
Base = declarative_base() 

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    edad = Column(Integer, nullable=True)

# Creamos la tabla en la base de datos
Base.metadata.create_all(bind=engine)

# Definimos los modelos Pydantic
class EstudianteCreate(BaseModel):
    nombre: str = Field(min_length=1)
    email: EmailStr
    edad: int = Field(ge=0)

class EstudianteResponse(BaseModel):
    id: int
    nombre: str
    email: str
    edad: int

app = FastAPI(title="CRUD API", version="1.0.0")

# Implementamos los endpoints CRUD
@app.get("/estudiantes", response_model=List[EstudianteResponse])
def listar_estudiantes():
    """Lista todas las entidades"""
    logger.info("Solicitados todos los estudiantes")
    db = SessionLocal()
    try:
        estudiantes = db.query(Estudiante).all()
        return estudiantes
    finally:
        db.close()

@app.get("/estudiantes/{estudiante_id}", response_model=EstudianteResponse)
def obtener_estudiante(estudiante_id: int):
    """Recupera una entidad específica"""
    logger.info(f"Solicitado estudiante con ID {estudiante_id}")
    db = SessionLocal()
    try:
        estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
        if not estudiante:
            logger.warning(f"Estudiante con ID {estudiante_id} no encontrado")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        return estudiante
    finally:
        db.close()

@app.post("/estudiantes", response_model=EstudianteResponse, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: EstudianteCreate):
    """Crea una nueva entidad"""
    logger.info(f"Creando nuevo estudiante: {estudiante.nombre}")
    db = SessionLocal()
    try:
        estudiante_db = Estudiante(**estudiante.model_dump())
        db.add(estudiante_db)
        db.commit()
        db.refresh(estudiante_db)
        return estudiante_db
    finally:
        db.close()

@app.delete("/estudiantes/{estudiante_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(estudiante_id: int):
    """Borra una entidad"""
    logger.info(f"Eliminando estudiante con ID {estudiante_id}")
    db = SessionLocal()
    try:
        estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
        if not estudiante:
            logger.warning(f"Estudiante con ID {estudiante_id} no encontrado")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        db.delete(estudiante)
        db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "CRUD API"}
