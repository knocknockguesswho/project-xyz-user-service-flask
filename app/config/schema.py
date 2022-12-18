import datetime
from sqlalchemy import Column, Integer, VARCHAR, DateTime, BINARY, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import config
from utils import _TIME_FORMAT_, get_age


Base = declarative_base()


class Users(Base):
    """TODO: 
    - create email validation
    - more research for char length of every columns, especially for `avatar`
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
    username = Column(VARCHAR(32), unique=True)
    password = Column(BINARY(80))
    birth_date = Column(DateTime)
    email = Column(VARCHAR(50), unique=True)
    avatar = Column(VARCHAR(512))
    country_code = Column(VARCHAR(2))
    # created_at would return UTC date string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, first_name: str, last_name: str, birth_date: str, email: str, username: str, password: bytes, avatar: str, country_code: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar
        self.birth_date = birth_date
        self.country_code = country_code

    def get_item(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': get_age(self.birth_date),
            'email': self.email,
            'avatar': self.avatar,
            'country_code': self.country_code,
            'created_at': self.created_at.strftime(_TIME_FORMAT_)
        }


# class Sessions(Base):
#   __tablename__ = 'sessions'


engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(
    config['DB_USER'], config['DB_PASSWORD'], config['DB_HOST'], config['DB_NAME']))
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
