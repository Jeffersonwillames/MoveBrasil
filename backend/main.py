"""API FastAPI do MoveBrasil (MVP educacional)."""

from datetime import datetime, timedelta

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MoveBrasil API",
    description="API educacional para consulta de linhas, paradas, horários e lotação em Maceió - AL.",
    version="1.0.0",
)

# Permite consumo do frontend em outro container/porta.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LotacaoOut(BaseModel):
    nivel: str


class ParadaOut(BaseModel):
    id: int
    nome: str
    bairro: str
    lat: float
    lng: float
    lotacao: LotacaoOut | None

    class Config:
        from_attributes = True


class ParadaMapaOut(BaseModel):
    id: int
    nome: str
    linha_id: int
    lat: float
    lng: float
    lotacao: str
    transito: str


class HorarioOut(BaseModel):
    id: int
    parada: ParadaOut
    saida: datetime
    chegada: datetime
    status_transito: str

    class Config:
        from_attributes = True


class LinhaOut(BaseModel):
    id: int
    codigo: str
    nome: str
    horarios: list[HorarioOut]

    class Config:
        from_attributes = True


def seed_data(db: Session) -> None:
    """Popula o banco com dados simulados quando ainda estiver vazio."""
    if db.query(models.Linha).first():
        return

    linhas = [
        models.Linha(codigo="201", nome="Benedito Bentes / Centro"),
        models.Linha(codigo="223", nome="Ponta Verde / Trapiche"),
        models.Linha(codigo="611", nome="UFAL / Centro"),
    ]

    paradas = [
        models.Parada(
            nome="Terminal do Benedito Bentes",
            bairro="Benedito Bentes",
            lat=-9.5563,
            lng=-35.7735,
        ),
        models.Parada(
            nome="Praça Deodoro",
            bairro="Centro",
            lat=-9.6658,
            lng=-35.7350,
        ),
        models.Parada(
            nome="Orla da Ponta Verde",
            bairro="Ponta Verde",
            lat=-9.6632,
            lng=-35.7003,
        ),
        models.Parada(
            nome="Terminal Trapiche",
            bairro="Trapiche da Barra",
            lat=-9.6745,
            lng=-35.7540,
        ),
    ]

    db.add_all(linhas + paradas)
    db.flush()

    lotacoes = [
        models.Lotacao(parada_id=paradas[0].id, nivel="alta"),
        models.Lotacao(parada_id=paradas[1].id, nivel="media"),
        models.Lotacao(parada_id=paradas[2].id, nivel="baixa"),
        models.Lotacao(parada_id=paradas[3].id, nivel="media"),
    ]

    now = datetime.now().replace(second=0, microsecond=0)
    horarios = [
        models.Horario(
            linha_id=linhas[0].id,
            parada_id=paradas[0].id,
            saida=now + timedelta(minutes=10),
            chegada=now + timedelta(minutes=45),
            status_transito="moderado",
        ),
        models.Horario(
            linha_id=linhas[0].id,
            parada_id=paradas[1].id,
            saida=now + timedelta(minutes=20),
            chegada=now + timedelta(minutes=55),
            status_transito="intenso",
        ),
        models.Horario(
            linha_id=linhas[1].id,
            parada_id=paradas[2].id,
            saida=now + timedelta(minutes=15),
            chegada=now + timedelta(minutes=50),
            status_transito="livre",
        ),
        models.Horario(
            linha_id=linhas[1].id,
            parada_id=paradas[3].id,
            saida=now + timedelta(minutes=30),
            chegada=now + timedelta(minutes=65),
            status_transito="moderado",
        ),
        models.Horario(
            linha_id=linhas[2].id,
            parada_id=paradas[1].id,
            saida=now + timedelta(minutes=12),
            chegada=now + timedelta(minutes=42),
            status_transito="moderado",
        ),
    ]

    db.add_all(lotacoes + horarios)
    db.commit()


@app.on_event("startup")
def on_startup() -> None:
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "MoveBrasil API no ar"}


@app.get("/linhas", response_model=list[LinhaOut])
def listar_linhas(db: Session = Depends(get_db)):
    return db.query(models.Linha).all()


@app.get("/paradas", response_model=list[ParadaOut])
def listar_paradas(db: Session = Depends(get_db)):
    return db.query(models.Parada).all()


@app.get("/paradas/mapa", response_model=list[ParadaMapaOut])
def listar_paradas_mapa(db: Session = Depends(get_db)):
    horarios = db.query(models.Horario).all()

    return [
        ParadaMapaOut(
            id=horario.parada.id,
            nome=horario.parada.nome,
            linha_id=horario.linha_id,
            lat=horario.parada.lat,
            lng=horario.parada.lng,
            lotacao=horario.parada.lotacao.nivel if horario.parada.lotacao else "media",
            transito=horario.status_transito,
        )
        for horario in horarios
    ]


@app.get("/horarios", response_model=list[HorarioOut])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(models.Horario).all()
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# Serve arquivos estáticos do frontend
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Home do site
@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

