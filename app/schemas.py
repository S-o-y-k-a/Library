from pydantic import BaseModel
from datetime import date

class BookIn(BaseModel):
    name: str
    author: str
    theme: str
    publisher: str


class BookOut(BookIn):
    book_id: int

    class Config:
        orm_mode = True


class ReaderIn(BaseModel):
    passport_number: str
    name: str
    address: str
    phone_number: str
    mark: date

class ReaderOut(ReaderIn):
    reader_id: int

    class Config:
        orm_mode = True


class IssuanceIn(BaseModel):
    issuance_date: date
    date_of_actual_return: date
    book_id: int
    reader_id: int

class IssuanceOut(IssuanceIn):
    issuance_id: int

    class Config:
        orm_mode = True