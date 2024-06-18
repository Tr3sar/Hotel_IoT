from fastapi import FastAPI, Depends
from app.routers import rooms, services, clients, cleaning_staff, reservations
from app.database import engine, Base, SessionLocal
from app.storage import Storage

import logging
from colorlog import ColoredFormatter

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar el almacenamiento de forma global
storage = Storage()

# Cargar los datos desde la base de datos al almacenamiento en memoria
def load_data():
    db = SessionLocal()
    try:
        storage.load_from_db(db)
    finally:
        db.close()

def setup_logging():
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

load_data()  # Llamar a la función para cargar los datos al iniciar la aplicación

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI()

# Hacer que el almacenamiento se comparta entre todas las solicitudes
def get_storage():
    return storage

app.include_router(rooms.router, prefix="/rooms", dependencies=[Depends(get_storage)])
app.include_router(services.router, prefix="/services", dependencies=[Depends(get_storage)])
app.include_router(clients.router, prefix="/clients", dependencies=[Depends(get_storage)])
app.include_router(cleaning_staff.router, prefix="/cleaning_staff", dependencies=[Depends(get_storage)])
app.include_router(reservations.router, prefix="/reservations", dependencies=[Depends(get_storage)])
