"""Modelos de dados do MVP MoveBrasil."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Linha(Base):
    __tablename__ = "linhas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False, index=True)
    nome = Column(String, nullable=False)

    horarios = relationship("Horario", back_populates="linha", cascade="all, delete-orphan")


class Parada(Base):
    __tablename__ = "paradas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    bairro = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    horarios = relationship("Horario", back_populates="parada", cascade="all, delete-orphan")
    lotacao = relationship("Lotacao", back_populates="parada", uselist=False, cascade="all, delete-orphan")


class Horario(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    linha_id = Column(Integer, ForeignKey("linhas.id"), nullable=False)
    parada_id = Column(Integer, ForeignKey("paradas.id"), nullable=False)
    saida = Column(DateTime, nullable=False)
    chegada = Column(DateTime, nullable=False)
    status_transito = Column(String, nullable=False, default="moderado")

    linha = relationship("Linha", back_populates="horarios")
    parada = relationship("Parada", back_populates="horarios")


class Lotacao(Base):
    __tablename__ = "lotacoes"

    id = Column(Integer, primary_key=True, index=True)
    parada_id = Column(Integer, ForeignKey("paradas.id"), unique=True, nullable=False)
    nivel = Column(String, nullable=False, default="media")

    parada = relationship("Parada", back_populates="lotacao")
