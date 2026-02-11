# MoveBrasil (MVP Educacional)

Projeto fullstack simples para consulta de informações básicas do transporte público de **Maceió - AL**.

## Objetivo

Ajudar a população a visualizar:
- linhas de ônibus
- paradas
- horários de saída e chegada
- nível de lotação por parada (baixa, média, alta)
- status do trânsito (livre, moderado, intenso)
- mapa interativo com pontos das paradas

> Os dados são simulados (mock) para fins de estudo.

## Stack

- **Backend**: Python + FastAPI + SQLite + SQLAlchemy
- **Frontend**: HTML + CSS + JavaScript puro + Leaflet (OpenStreetMap)
- **Infraestrutura**: Docker + Docker Compose

## Estrutura do projeto

```bash
.
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Como executar

Pré-requisito: Docker e Docker Compose instalados.

```bash
docker compose up --build
```

Após subir os containers:

- Frontend: http://localhost:8080
- API Backend: http://localhost:8000
- Documentação automática do FastAPI (Swagger): http://localhost:8000/docs

## Endpoints principais

- `GET /` - status da API
- `GET /linhas` - lista linhas com horários, parada, lotação e trânsito
- `GET /paradas` - lista paradas com lotação e coordenadas (`lat`, `lng`)
- `GET /paradas/mapa` - retorno compacto para renderização de pontos no mapa
- `GET /horarios` - lista horários cadastrados

## Mapa interativo

A interface web agora exibe um mapa interativo com marcadores para as paradas simuladas de Maceió.
Os pontos são alimentados pelo endpoint `GET /paradas/mapa`, contendo:

- `id`
- `nome`
- `linha_id`
- `lat`
- `lng`
- `lotacao`
- `transito`

## Próximos passos (evolução)

- Integrar dados reais da prefeitura/concessionárias.
- Adicionar autenticação para operadores.
- Incluir geolocalização em tempo real dos ônibus.
- Criar histórico e previsão de lotação.
