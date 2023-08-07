from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Mapping
from sqlalchemy.orm import sessionmaker
from typing import Any
from typing import List
import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine.interfaces import ReflectedColumn
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import typing
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Engine
from sqlalchemy import ColumnCollection
import time
import datetime
import os # damit ein back up wieder einlesen aber erst später.

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    userid: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(200))
    
    def __repr__(self) -> str:
        return f"userid(id={self.userid!r}, username={self.username!r}, password_hash={self.password_hash!r})"

class Chats2user(Base):
    __tablename__ = "chats2user"
    chatid: Mapped[int] = mapped_column(primary_key=True)
    userid = Column(Integer, ForeignKey('user.userid'))
    chatname: Mapped[str] = mapped_column(String(30))
    
    def __repr__(self) -> str:
        return f"userid(id={self.userid!r}, chatid={self.chatid!r}, chatname={self.chatname!r})"

global engine 
# später in config
engine = sqlalchemy.create_engine("mysql+pymysql://test:1234@127.0.0.1/gpt4all_socket_server",  echo=True, pool_size=20, max_overflow=0)
if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(engine)
    

def check_user_exist(username):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User).filter(User.username == username).first()
    session.close()
    if result is not None:
        return True
    else:
        return False

def get_hashed_password(username):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User.password_hash).filter(User.username == username).first()
    session.close()
    if result is not None:
        return result[0]

def create_new_user(username, password_hash):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User.password_hash).all()
    if result == None:
        userid = 1
    else:
        userid = len(result)
    new_user = User(userid = userid,username = username,  password_hash = password_hash)
    session.add(new_user)
    session.commit()
    session.close()
    
def get_chats_from_user(username):
    Session = sessionmaker(bind=engine)
    session = Session()
    chats = session.query(Chats2user.chatname).all()
    return chats