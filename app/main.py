
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import SessionLocal, Base, engine
from app.models import Book, Reader, Issuance
from app.schemas import BookIn, BookOut, ReaderIn, ReaderOut, IssuanceIn, IssuanceOut
import random
from typing import List
from sqlalchemy import asc

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/books/", response_model=BookOut)
def create_book(book: BookIn, db: Session = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books/", response_model=List[BookOut])
def read_books(sort_by: str = "book_id", db: Session = Depends(get_db)
):
    sorts = {
        "book_id": Book.book_id,
        "name": Book.name,
        "author": Book.author,
        "theme": Book.theme,
        "rating": Book.rating,
        "publisher": Book.publisher
    }

    if sort_by not in sorts:
        raise HTTPException(
            status_code=400,
            detail="Wrong sort_by"
        )

    s = sorts[sort_by]
    query = db.query(Book).order_by(asc(s))

    return query.all()


@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookIn, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Such a book doesn't exist in database")

    for key, value in book.dict().items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Such a book doesn't exist in database")

    db.delete(db_book)
    db.commit()


@app.post("/readers/", response_model=ReaderOut)
def create_reader(reader: ReaderIn, db: Session = Depends(get_db)):
    new_reader = Reader(**reader.dict())
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)
    return new_reader


@app.get("/readers/", response_model=List[ReaderOut])
def read_readers(sort_by: str = "reader_id", db: Session = Depends(get_db)):

    sorts = {
        "reader_id": Reader.reader_id,
        "passport_number": Reader.passport_number,
        "address": Reader.address,
        "phone_number": Reader.phone_number,
        "name": Reader.name,
        "mark": Reader.mark
    }

    if sort_by not in sorts:
        raise HTTPException(
            status_code=400,
            detail="Wrong sort_by"
        )

    s = sorts[sort_by]
    query = db.query(Reader).order_by(asc(s))

    return query.all()


@app.put("/readers/{reader_id}", response_model=ReaderOut)
def update_reader(reader_id: int, reader: ReaderIn, db: Session = Depends(get_db)):
    db_reader = db.query(Reader).filter(Reader.reader_id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Such a reader doesn't exist in database")

    for key, value in reader.dict().items():
        setattr(db_reader, key, value)

    db.commit()
    db.refresh(db_reader)
    return db_reader


@app.delete("/readers/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = db.query(Reader).filter(Reader.reader_id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Such a reader doesn't exist in database")

    db.delete(db_reader)
    db.commit()



@app.post("/issuances/", response_model=IssuanceOut)
def create_issuance(issuance: IssuanceIn, db: Session = Depends(get_db)):
    new_issuance = Issuance(**issuance.dict())
    db.add(new_issuance)
    db.commit()
    db.refresh(new_issuance)
    return new_issuance


@app.get("/issuances/", response_model=List[IssuanceOut])
def read_issuances(sort_by: str = "issuance_id", db: Session = Depends(get_db)):
    sorts = {
        "issuance_id": Issuance.issuance_id,
        "issuance_date": Issuance.issuance_date,
        "date_of_actual_return": Issuance.date_of_actual_return,
    }

    if sort_by not in sorts:
        raise HTTPException(
            status_code=400,
            detail="Wrong sort_by"
        )

    s = sorts[sort_by]
    query = db.query(Issuance).order_by(asc(s))

    return query.all()


@app.put("/issuances/{issuance_id}", response_model=IssuanceOut)
def update_issuance(issuance_id: int, issuance: IssuanceIn, db: Session = Depends(get_db)):
    db_issuance = db.query(Issuance).filter(Issuance.issuance_id == issuance_id).first()
    if not db_issuance:
        raise HTTPException(status_code=404, detail="Such an issuance doesn't exist in database")

    for key, value in issuance.dict().items():
        setattr(db_issuance, key, value)

    db.commit()
    db.refresh(db_issuance)
    return db_issuance


@app.delete("/issuances/{issuance_id}")
def delete_issuance(issuance_id: int, db: Session = Depends(get_db)):
    db_issuance = db.query(Issuance).filter(Issuance.issuance_id == issuance_id).first()
    if not db_issuance:
        raise HTTPException(status_code=404, detail="Such anissuance doesn't exist in database")

    db.delete(db_issuance)
    db.commit()


#сложные запросы

#select all books with given author and theme
@app.get("/books/search_author_and_theme/", response_model=List[BookOut])
def search_books(author: str = None, theme: str = None, db: Session = Depends(get_db)):
    query = db.query(Book)

    if author:
        query = query.filter(Book.author == author)
    if theme:
        query = query.filter(Book.theme == theme)

    books = query.all()
    if not books:
        raise HTTPException(status_code=404, detail="Books not found")

    return books


#join (вывести все выдачи с указанием читателя)
@app.get("/issuances_with_readers/")
def get_issuances_with_readers(db: Session = Depends(get_db)):
    res = (
        db.query(Issuance, Reader)
        .join(Reader, Issuance.reader_id == Reader.reader_id)
        .all()
    )

    output = []
    for issuance, reader in res:
        output.append({
            "issuance_id": issuance.issuance_id,
            "issuance_date": str(issuance.issuance_date),
            "date_of_actual_return": str(issuance.date_of_actual_return)
            if issuance.date_of_actual_return else None,
            "book_id": issuance.book_id,
            "reader_id": reader.reader_id,
            "reader_name": reader.name,
            "reader_passport": reader.passport_number
        })

    return output


#update (make rating = random float from 0 to 10 of all the books with even primary key) 
#Сложно придумать что-то более осмысленное, когда данные в таблице рандомные...
@app.put("/books/update_even_rating/")
def update_even_book_rating(db: Session = Depends(get_db)):
    updated_count = (
        db.query(Book)
        .filter(Book.book_id % 2 == 0)
        .update({"rating": random.uniform(0.0, 10.0)})
    )

    db.commit()
    return {"count_of_updated_books": updated_count}


#group by (сгруппировать книги по округленному рейтингу)
#рейтинг появился после миграции а значит он не нулл только в тех строчках, которые мы апдейтнули предыдущим запросом
@app.get("/books/group_by_rounded_rating/")
def group_books_by_rounded_rating(db: Session = Depends(get_db)):
    res = (
        db.query(
            func.floor(Book.rating).label("rounded_rating"),
            func.count(Book.book_id).label("book_count")
        )
        .filter(Book.rating != None)
        .group_by(func.floor(Book.rating))
        .all()
    )

    return [
        {"rounded_rating": int(rating), "book_count": count}
        for rating, count in res
    ]