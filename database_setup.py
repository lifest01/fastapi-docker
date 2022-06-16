from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class SecretData(Base):
    __tablename__ = 'secret_data'
    id = Column(Integer, primary_key=True)
    encrypted_text = Column(String(250), nullable=False)
    decrypted_text = Column(String(250))
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'{self.__tablename__}'


engine = create_engine('sqlite:///database.db')

Base.metadata.create_all(engine)
