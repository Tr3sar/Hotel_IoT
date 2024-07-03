from fastapi import FastAPI, Depends
from app.routers import rooms, clients, cleaning_staff, reservations
from app.routers_simulation import simulation_rooms, simulation_clients, simulation_cleaning_staff, simulation_hotel
from app.database import engine, Base, SessionLocal
from app.storage import Storage

import logging
from colorlog import ColoredFormatter

Base.metadata.create_all(bind=engine)

storage = Storage()

def load_data():
    db = SessionLocal()
    try:
        storage.load_from_db(db)
    finally:
        db.close()

def create_colored_logger(name, color):
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'reset',
            'INFO': color,
            'WARNING': 'yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red'
        },
        style='%'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Remove all handlers associated with the logger to avoid duplication
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)

    return logger

def setup_logging():
    log_colors = {
        'Devices': 'blue',
        'Sensors': 'green',
        'SmartClient': 'yellow',
        'SmartHotel': 'bold_white',
        'SmartRoom': 'purple',
        'SmartServices': 'red',
        'Staff': 'cyan'
    }

    # Create loggers for each category
    create_colored_logger('Devices', log_colors['Devices'])
    create_colored_logger('Sensors', log_colors['Sensors'])
    create_colored_logger('SmartClient', log_colors['SmartClient'])
    create_colored_logger('SmartHotel', log_colors['SmartHotel'])
    create_colored_logger('SmartRoom', log_colors['SmartRoom'])
    create_colored_logger('SmartServices', log_colors['SmartServices'])
    create_colored_logger('Staff', log_colors['Staff'])
    create_colored_logger(__name__, 'bold_white')

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Starting the application")

load_data()


app = FastAPI()

def get_storage():
    return storage

app.include_router(rooms.router, prefix="/rooms", dependencies=[Depends(get_storage)])
app.include_router(clients.router, prefix="/clients", dependencies=[Depends(get_storage)])
app.include_router(cleaning_staff.router, prefix="/cleaning_staff", dependencies=[Depends(get_storage)])
app.include_router(reservations.router, prefix="/reservations", dependencies=[Depends(get_storage)])

app.include_router(simulation_rooms.router, prefix="/simulation/rooms", dependencies=[Depends(get_storage)])
app.include_router(simulation_clients.router, prefix="/simulation/clients", dependencies=[Depends(get_storage)])
app.include_router(simulation_cleaning_staff.router, prefix="/simulation/cleaning_staff", dependencies=[Depends(get_storage)])
app.include_router(simulation_hotel.router, prefix="/simulation/hotel", dependencies=[Depends(get_storage)])