
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from app.db import Base
from sqlalchemy.dialects.postgresql import JSONB

class Book(Base):
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    author = Column(String, index=True)
    theme = Column(String)
    rating = Column(Float) #новая колонка для миграции
    publisher = Column(String)
    issuances = relationship("Issuance", back_populates="book")


class Reader(Base):
    __tablename__ = "reader"
    reader_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    passport_number = Column(String, unique=True, index=True)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    mark = Column(Date)
    issuances = relationship("Issuance", back_populates="reader")

class Issuance(Base):
    __tablename__ = "issuance"
    issuance_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    issuance_date = Column(Date)
    date_of_actual_return = Column(Date)
    book_id = Column(Integer, ForeignKey("book.book_id"))
    reader_id = Column(Integer, ForeignKey("reader.reader_id"))
    book = relationship("Book", back_populates="issuances")
    reader = relationship("Reader", back_populates="issuances")
    notes = Column(JSONB) #jsonb колонка