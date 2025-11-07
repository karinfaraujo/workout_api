from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/atletas/", response_model=schemas.Atleta)
def create_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(get_db)):
    # checar se já existe cpf
    existing = db.query(models.Atleta).filter(models.Atleta.cpf == atleta.cpf).first()
    if existing:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    return crud.create_atleta(db=db, atleta=atleta) 

@app.get("/atletas/{atleta_id}", response_model=schemas.Atleta)
def read_atleta(atleta_id: int, db: Session = Depends(get_db)):
    db_atleta = crud.get_atleta(db, atleta_id=atleta_id)
    if db_atleta is None:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    return db_atleta

@app.get("/atletas/", response_model=list[schemas.Atleta])
def read_atletas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    atletas = crud.get_atletas(db, skip=skip, limit=limit)
    return atletas