# FIPE API - Servidor

Este é o back-end do projeto **FIPE-PYTHON**, implementado em Python com FastAPI. O servidor busca dados do site da [**FIPE**](https://veiculos.fipe.org.br/), utiliza cache (opcional) armazenado em um **banco de dados SQLite** e expõe endpoints para consulta de **tipos**, **marcas**, **modelos**, **anos** e **detalhes** de **carros**, **motos** e **caminhões**.

---

## Índice

1. [Recursos](#recursos)  
2. [Pré-requisitos](#pré-requisitos)  
3. [Instalação](#instalação)  
4. [Configuração](#configuração)  
5. [Servidor](#servidor)  
6. [Notas e Considerações](#notas-e-considerações)

---

## Recursos

- **FastAPI** para criação de endpoints REST.  
- **httpx** para requisições assíncronas à API FIPE.  
- **python-dotenv** para gerenciamento de variáveis de ambiente.  
- **SQLite** como banco de dados para cache.  
- Suporte opcional a cache: ao habilitar, os dados obtidos da FIPE API são salvos localmente.

---

## Pré-requisitos

- **Python 3.8 ou superior**  
- **Pip**

---

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/FelipeTr00/fipe-python.git
   cd fipe-python/server
2. **Crie e ative um ambiente virtual:**

    **Windows**
    ```
    py -m venv venv
    venv\Scripts\activate
3. **Instale as dependências:**
    ```
    py -m pip install -r requirements.txt


---

## Configuração

**Arquivo server/.env**

    DB_URI=database/db.sqlite
    DEBUG=true
    CACHE_ENABLED=true
    FIPE_TABLE=318
    SERVER_PORT=8000
- DB_URI: Caminho para o arquivo SQLite (relativo à raiz do servidor).
- DEBUG: Ativa mensagens de depuração (true/false).
- CACHE_ENABLED: Habilita (true) ou desabilita (false) o cache.
- FIPE_TABLE: Código de referência da tabela FIPE (ex: 318 para fevereiro/2025).
- SERVER_PORT: Porta em que o servidor será executado.

---

## Servidor 

### Estrutura do Servidor
    server/
    ├── database/                # Arquivo SQLite (db.sqlite)
    ├── migrations/              # Scripts de migração (schema.sql, etc.)
    ├── crawler/                 # Scripts de mineração dos dados (models.py, etc.)
    ├── src/
    │   ├── __init__.py          # Inicializador do pacote
    │   ├── main.py              # Ponto de entrada da aplicação FastAPI
    │   ├── routes.py            # Definição das rotas/endpoint
    │   ├── fipe.py              # Lógica de integração com a API FIPE e cache
    │   └── db.py                # Módulo de conexão e operações com o banco SQLite
    ├── .env                     # Variáveis de ambiente
    ├── requirements.txt         # Dependências do Python
    └── SERVER-README.md         # Este arquivo

### Run
    py -m src.main

---
### End Points

- **Types:** GET: /v1/types

   ```
        // http://localhost:8000/v1/types

    {
      "success": true,
      "data": [
       {
          "Value": 1,
          "Label": "carros"
        },
        {
          "Value": 2,
          "Label": "motos"
        },
        {
          "Value": 3,
          "Label": "caminhões"
        }]}

- **Brands:** GET: /v1/brands/1
    ```
    // http://localhost:8000/v1/brands/1

    {
  "success": true,
  "updatedAt": "2025-02-01T00:00:00Z",
  "type": 1,
  "type_label": "carros",
  "data": [
    {
      "Label": "Acura",
      "Value": "1",
      "codigoTabelaReferencia": 318,
      "codigoTipoVeiculo": 1,
      "updatedAt": "2025-02-16T20:17:52.970307Z"
    },
    {
      "Label": "Agrale",
      "Value": "2",
      "codigoTabelaReferencia": 318,
      "codigoTipoVeiculo": 1,
      "updatedAt": "2025-02-16T20:17:52.970307Z"
    },
    {
      "Label": "Alfa Romeo",
      "Value": "3",
      "codigoTabelaReferencia": 318,
      "codigoTipoVeiculo": 1,
      "updatedAt": "2025-02-16T20:17:52.970307Z"
    }
    
    ...
    
    ]}

- **Models:** GET: /v1/models/1/20
    ```
    // http://localhost:8000/v1/models/1/20

    {
      "success": true,
      "updatedAt": "2025-02-01T00:00:00Z",
      "type": 1,
      "type_label": "carros",
      "brand": 20,
      "data": [
        {
          "Label": "296 GTB (Hibrido)",
          "Value": 10159,
          "codigoTabelaReferencia": 318,
          "codigoTipoVeiculo": 1,
          "codigoMarca": 20,
          "updatedAt": "2025-02-16T20:22:17.576745Z"
        },
        {
          "Label": "296 GTS (Híbrido)",
          "Value": 10624,
          "codigoTabelaReferencia": 318,
          "codigoTipoVeiculo": 1,
          "codigoMarca": 20,
          "updatedAt": "2025-02-16T20:22:17.576745Z"
       }]}

- **Years:** GET /v1/years/1/20/10995

    ```
    // http://localhost:8000/v1/years/1/20/10995

    {
    "success": true,
    "updatedAt": "2025-02-01T00:00:00Z",
    "type": 1,
    "type_label": "carros",
    "brand": 20,
    "model": 10995,
    "data": [
        {
          "Label": "32000 Gasolina",
          "Value": "32000-1",
          "codigoTabelaReferencia": 318,
          "codigoTipoVeiculo": 1,
          "codigoMarca": 20,
          "codigoModelo": 10995,
          "updatedAt": "2025-02-16T20:38:47.992667Z"
        },
        {
          "Label": "2024 Gasolina",
          "Value": "2024-1",
          "codigoTabelaReferencia": 318,
          "codigoTipoVeiculo": 1,
          "codigoMarca": 20,
          "codigoModelo": 10995,
          "updatedAt": "2025-02-16T20:38:47.992667Z"
        },
        {
          "Label": "2023 Gasolina",
          "Value": "2023-1",
          "codigoTabelaReferencia": 318,
          "codigoTipoVeiculo": 1,
          "codigoMarca": 20,
          "codigoModelo": 10995,
          "updatedAt": "2025-02-16T20:38:47.992667Z"
        }]}  


- **Details:** GET /v1/details/1/20/10995/2024
    ```
    // http://localhost:8000/v1/details/1/20/10995/2024

    {
      "success": true,
      "updatedAt": "2025-02-01T00:00:00Z",
      "type": 1,
      "type_label": "carros",
      "brand": 20,
      "model": 10995,
      "year": 2024,
      "data": {
        "Valor": "R$ 7.047.843,00",
        "Marca": "Ferrari",
        "Modelo": "PUROSANGUE 6.5 V12 725cv",
        "AnoModelo": 2024,
        "Combustivel": "Gasolina",
        "CodigoFipe": "031056-5",
        "MesReferencia": "fevereiro de 2025 ",
        "Autenticacao": "5zn264d4k9j3yq",
        "TipoVeiculo": 1,
        "SiglaCombustivel": "G",
        "DataConsulta": "domingo, 16 de fevereiro de 2025 17:40",
        "codigoTabelaReferencia": 318,
        "codigoTipoVeiculo": 1,
        "codigoMarca": 20,
        "codigoModelo": 10995,
        "anoModelo": 2024,
        "codigoTipoCombustivel": 1,
        "tipoConsulta": "tradicional",
        "updatedAt": "2025-02-16T20:40:55.355739Z"
      }
    } 




## Notas e Considerações
. . .
