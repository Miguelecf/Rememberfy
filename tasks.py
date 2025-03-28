import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Time, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear la base y el motor de la base de datos
Base = declarative_base()
engine = create_engine("sqlite:///rememberfy.db")
Session = sessionmaker(bind=engine)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    hour = Column(Time, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(150))
    created_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=True)


# Crear todas las tablas
Base.metadata.create_all(engine)


def print_tasks():
    session = Session()
    tasks = session.query(Task).all()
    for task in tasks:
        print(f"ID: {task.id}")
        print(f"Título: {task.title}")
        print(f"Hora: {task.hour}")
        print(f"Fecha: {task.date}")
        print(f"Descripción: {task.description}")
        print("-------------------")
    session.close()


def save_task(task):
    session = Session()
    session.add(task)
    session.commit()
    session.close()


def add_task(title, hour, date, description, user_id):
    session = Session()

    try:
        hour = datetime.datetime.strptime(hour, "%H:%M").time()
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError(
            "Exception en add_task: Formato de hora o fecha inválido. Use el formato HH:MM y dd/mm/aaaa."
        )

    task = Task(
        title=title,
        hour=hour,
        date=date,
        description=description,
        user_id=user_id,
        created_at=datetime.datetime.now(),
    )
    save_task(task)

def get_tasks(user_id):
    session = Session()
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    session.close()
    return tasks

def delete_tasks(user_id):
    session = Session()
    session.query(Task).filter(Task.user_id == user_id).delete()
    session.commit()
    session.close()

