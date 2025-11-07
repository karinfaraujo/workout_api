from sqlalchemy.orm import Session
from . import models, schemas

def get_atleta(db: Session, atleta_id: int):
    return db.query(models.Atleta).filter(models.Atleta.id == atleta_id).first()

def get_atleta(db: Session,skip: int = 0, limit: int = 100):
    return db.query(models.Atleta).offset(skip).limit(limit).all()

def create_atleta(db: Session, atleta: schemas.AtletaCreate):
    db_atleta = models.Atleta(nome=atleta.nome, cpf=atleta.cpf)
    db.add(db_atleta)
    db.commit()
    db.refresh(db_atleta)
    return db_atleta