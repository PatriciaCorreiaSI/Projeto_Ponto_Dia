from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Um usuário pode ter vários registros de ponto
    pontos = relationship("RegistroPonto", back_populates = "owner")

class RegistroPonto(Base):
    __tablename__ = "registro_ponto"

    id = Column(Integer, primary_key=True, index=True)
    entrada = Column(String)
    saida = Column(String)
    total_trabalhado = Column(Float)
    saldo = Column(Float)
    

    # Chave estrageira ligando ao Usuário
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner =  relationship("User", back_populates = "pontos")

    