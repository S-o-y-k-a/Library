from pydantic import BaseModel
from typing import Optional
from datetime import date

class BookBase(BaseModel):
    name: str
    author: str
    theme: Optional[str] = None
    publisher: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    book_id: int

    class Config:
        orm_mode = True


class ReaderBase(BaseModel):
    passport_number: str
    name: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    mark: Optional[date] = None

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    reader_id: int

    class Config:
        orm_mode = True


class IssuanceBase(BaseModel):
    issuance_date: date
    date_of_actual_return: Optional[date] = None
    book_id: int
    reader_id: int

class IssuanceCreate(IssuanceBase):
    pass

class Issuance(IssuanceBase):
    issuance_id: int

    class Config:
        orm_mode = True