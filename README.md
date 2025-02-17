# FIPE-PYTHON: Web Crawler para Consulta de Veículos na [Tabela FIPE](https://veiculos.fipe.org.br/)
## Autor: [Felipe Alves de Morais](https://github.com/FelipeTr00)

Este é o back-end do projeto **FIPE-PYTHON**, implementado em Python com FastAPI. O servidor busca dados do site da [**FIPE - fipe.org.br**](https://veiculos.fipe.org.br/), utiliza cache (opcional) armazenado em um **banco de dados SQLite** e expõe endpoints para consulta de **tipos**, **marcas**, **modelos**, **anos** e **detalhes** de **carros**, **motos** e **caminhões**.

---

## ÍNDICE

1. [OBJETIVOS](#OBJETIVOS)  
2. [APP](#APP)  
3. [SERVER](#SERVER)  
4. [LICENÇA](#LICENÇA)  
5. [NOTAS E CONSIDERAÇÕES](#NOTAS-E-CONSIDERAÇÕES)

---

## OBJETIVOS

1. **Coletar Dados Atualizados**  
   - Implementar um web crawler eficiente para extrair os preços de veículos diretamente da fonte oficial da Tabela FIPE.
   - Automatizar o processo de atualização dos dados para garantir que sempre estejam atualizados.

2. **Armazenamento Estruturado**  
   - Armazenar os dados coletados em um formato estruturado, como JSON, CSV ou banco de dados SQL/NoSQL.
   - Garantir integridade e consistência dos dados coletados.

3. **Facilidade de Consulta e Análise**  
   - Criar uma API ou interface para facilitar o acesso e consulta aos dados coletados.
   - Permitir filtragem e análise dos preços de veículos por categoria, modelo, ano e outros critérios relevantes.

4. **Automatização e Escalabilidade**  
   - Desenvolver um sistema que possa rodar periodicamente e ser escalado conforme a necessidade.
   - Implementar boas práticas de web scraping para evitar bloqueios e manter a eficiência do crawler.

5. **Documentação e Manutenção**  
   - Produzir uma documentação clara e objetiva sobre o funcionamento do web crawler e do sistema em geral.
   - Definir estratégias para manutenção e evolução do projeto, garantindo sua continuidade e confiabilidade.

O projeto **FIPE-Python** busca oferecer uma solução automatizada, confiável e eficiente para a coleta e análise de preços da Tabela FIPE, facilitando a obtenção de informações atualizadas sobre veículos no mercado brasileiro.


---
## APP 

### Em desenvolvimento...

## SERVER 

### Estrutura do Servidor/API
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
    py -m server.src.main

### Port
    http://localhost:8000/v1


---
### Endpoints

| **Método** | **Endpoint** | **Descrição** |
|------------|----------------------------------|------------------------------------------------------------|
| `GET` | `/v1/types` | Retorna os tipos de veículos disponíveis. |
| `GET` | `/v1/brands/{type}` | Retorna as marcas disponíveis para um tipo de veículo. |
| `GET` | `/v1/models/{type}/{brand}` | Retorna os modelos de uma marca específica. |
| `GET` | `/v1/years/{type}/{brand}/{model}` | Retorna os anos disponíveis para um modelo específico. |
| `GET` | `/v1/details/{type}/{brand}/{model}/{year}` | Retorna os detalhes do veículo com base nos 4 parâmetros informados. |
| `GET` | `/v1` | Extra, retorna a versão da API. |
|

* **Mais detalhes: [Documentação do Servidor](server/README.md)**

## LICENÇA

### Distribuído sob a [Licença MIT](LICENCE.txt).

## NOTAS E CONSIDERAÇÕES

Este projeto foi baseado e inspirado no trabalho de [Olavo Mello](https://github.com/olavomello/fipe-api). Agradeço pelo projeto original que serviu como modelo para esta implementação.

