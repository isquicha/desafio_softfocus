from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from src.extensions.database import db

STRING_BASE_LENGTH = 200


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(STRING_BASE_LENGTH), unique=True, nullable=False)
    name = Column(String(STRING_BASE_LENGTH))
    password = Column(String(512), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class ProdutorRural(db.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String(STRING_BASE_LENGTH), nullable=False)
    email = Column(String(STRING_BASE_LENGTH), nullable=False)
    cpf = Column(String(9), nullable=False, unique=True)

    def __repr__(self) -> str:
        return "<ProdutorRural %r>" % self.nome


class Lavoura(db.Model):
    id = Column(Integer, primary_key=True)
    latitude = Column(Float(precision=32), nullable=False)
    longitude = Column(Float(precision=32), nullable=False)
    tipo = Column(String(STRING_BASE_LENGTH), nullable=False)

    def __repr__(self) -> str:
        return "<Lavoura %r>" % self.id


class Perda(db.Model):
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)

    # ? 1 - CHUVA EXCESSIVA
    # ? 2 - GEADA
    # ? 3 - GRANIZO
    # ? 4 - SECA
    # ? 5 - VENDAVAL
    # ? 6 - RAIO
    evento = Column(Integer, nullable=False)

    produtor_rural_id = Column(
        Integer, ForeignKey("produtor_rural.id"), nullable=False
    )
    produtor_rural = db.relationship(
        "ProdutorRural", backref=db.backref("perdas", lazy=True)
    )
    lavoura_id = Column(Integer, ForeignKey("lavoura.id"), nullable=False)
    lavoura = db.relationship(
        "Lavoura", backref=db.backref("perdas", lazy=True)
    )

    def __repr__(self) -> str:
        return "<Perda %r>" % self.id
