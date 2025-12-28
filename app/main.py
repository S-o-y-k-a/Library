from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal, Base, engine
from app.models import Book as BookModel, Reader as ReaderModel, Issuance as IssuanceModel
from app.schemas import BookCreate, Book, ReaderCreate, Reader, IssuanceCreate, Issuance

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = BookModel(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/", response_model=list[Book])
def read_books(db: Session = Depends(get_db)):
    return db.query(BookModel).all()

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted"}

@app.post("/readers/", response_model=Reader)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    new_reader = ReaderModel(**reader.dict())
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)
    return new_reader

@app.get("/readers/", response_model=list[Reader])
def read_readers(db: Session = Depends(get_db)):
    return db.query(ReaderModel).all()

@app.get("/readers/{reader_id}", response_model=Reader)
def read_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = db.query(ReaderModel).filter(ReaderModel.reader_id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@app.put("/readers/{reader_id}", response_model=Reader)
def update_reader(reader_id: int, reader: ReaderCreate, db: Session = Depends(get_db)):
    db_reader = db.query(ReaderModel).filter(ReaderModel.reader_id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    for key, value in reader.dict().items():
        setattr(db_reader, key, value)
    db.commit()
    db.refresh(db_reader)
    return db_reader

@app.delete("/readers/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = db.query(ReaderModel).filter(ReaderModel.reader_id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    db.delete(db_reader)
    db.commit()
    return {"detail": "Reader deleted"}

@app.post("/issuances/", response_model=Issuance)
def create_issuance(issuance: IssuanceCreate, db: Session = Depends(get_db)):
    new_issuance = IssuanceModel(**issuance.dict())
    db.add(new_issuance)
    db.commit()
    db.refresh(new_issuance)
    return new_issuance

@app.get("/issuances/", response_model=list[Issuance])
def read_issuances(db: Session = Depends(get_db)):
    return db.query(IssuanceModel).all()

@app.get("/issuances/{issuance_id}", response_model=Issuance)
def read_issuance(issuance_id: int, db: Session = Depends(get_db)):
    issuance = db.query(IssuanceModel).filter(IssuanceModel.issuance_id == issuance_id).first()
    if not issuance:
        raise HTTPException(status_code=404, detail="Issuance not found")
    return issuance

@app.put("/issuances/{issuance_id}", response_model=Issuance)
def update_issuance(issuance_id: int, issuance: IssuanceCreate, db: Session = Depends(get_db)):
    db_issuance = db.query(IssuanceModel).filter(IssuanceModel.issuance_id == issuance_id).first()
    if not db_issuance:
        raise HTTPException(status_code=404, detail="Issuance not found")
    for key, value in issuance.dict().items():
        setattr(db_issuance, key, value)
    db.commit()
    db.refresh(db_issuance)
    return db_issuance

@app.delete("/issuances/{issuance_id}")
def delete_issuance(issuance_id: int, db: Session = Depends(get_db)):
    db_issuance = db.query(IssuanceModel).filter(IssuanceModel.issuance_id == issuance_id).first()
    if not db_issuance:
        raise HTTPException(status_code=404, detail="Issuance not found")
    db.delete(db_issuance)
    db.commit()
    return {"detail": "Issuance deleted"}