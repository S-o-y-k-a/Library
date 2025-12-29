from app.db import SessionLocal
from app.models import Issuance
import random

db = SessionLocal()

r = ["ok", "fantastic", "bad plot", "great plot", "great characters", "bad characters", "eww"]

for issuance in db.query(Issuance).all():
    issuance.notes = {
        "rating": random.uniform(0.0, 10.0),
        "review": f"{r[random.randint(0, 6)]}"
    }

db.commit()
db.close()