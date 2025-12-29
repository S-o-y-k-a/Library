from pydantic import BaseModel
from datetime import date
from typing import Optional
from typing import Dict
from typing import Any

class BookIn(BaseModel):
    name: str
    author: str
    theme: str
    publisher: str
    rating: Optional[float] = None


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
    notes: Dict[str, Any]

class IssuanceOut(IssuanceIn):
    issuance_id: int

    class Config:
        orm_mode = True