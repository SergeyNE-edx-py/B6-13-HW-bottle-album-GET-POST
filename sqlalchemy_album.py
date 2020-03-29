# Написать веб-сервер, который принимает GET-запросы по пути /album/<artist> и отвечает списком всех альбомов артиста artist. Если артист artist не зарегистрирован в музыкальной коллекции, то есть в базе данных отсутствуют соответствующие записи, сервер возвращает 404 ошибку. Для формирования поиска альбомов использовать следующий файл базы данных SQLite.

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к БД, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(session, artist, album=None):
    """
    Находит все альбомы в БД по заданному артисту
    """
    if album == None:
        result = session.query(Album).filter(Album.artist == artist).all()
    else:
        result = session.query(Album).filter(Album.artist == artist, Album.album == album).first() # !не "and", a ","

    return result    

def add(session, album):
    """
    Добавляет альбом в БД по заданному артисту
    """
    session.add(album)
    session.commit()

    return