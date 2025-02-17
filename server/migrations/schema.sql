PRAGMA foreign_keys = OFF;

-- Apaga tabelas antigas, se existirem
DROP TABLE IF EXISTS details;
DROP TABLE IF EXISTS years;
DROP TABLE IF EXISTS models;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS types;

-- TIPOS (ex: carros, motos, caminhões)
CREATE TABLE IF NOT EXISTS types (
  value INTEGER NOT NULL UNIQUE,
  label TEXT NOT NULL
);

INSERT INTO types (value, label) VALUES
(1, 'carros'),
(2, 'motos'),
(3, 'caminhoes');

-- MARCAS
CREATE TABLE IF NOT EXISTS brands (
  Label TEXT NOT NULL,
  Value TEXT NOT NULL,
  codigoTabelaReferencia INTEGER NOT NULL,
  codigoTipoVeiculo INTEGER NOT NULL,
  updatedAt TEXT NOT NULL
);

-- MODELOS
CREATE TABLE IF NOT EXISTS models (
  value INTEGER NOT NULL,      
  label TEXT NOT NULL,
  codigoTabelaReferencia INTEGER,
  codigoTipoVeiculo INTEGER,
  codigoMarca INTEGER,
  updatedAt TEXT
);

-- ANOS
CREATE TABLE IF NOT EXISTS years (
  value TEXT NOT NULL,   -- ex: "1992-1"
  label TEXT NOT NULL,
  codigoTabelaReferencia INTEGER,
  codigoTipoVeiculo INTEGER,
  codigoMarca INTEGER,
  codigoModelo INTEGER,
  updatedAt TEXT
);

-- DETALHES
CREATE TABLE IF NOT EXISTS details (
    Valor TEXT,
    Marca TEXT,
    Modelo TEXT,
    Combustivel TEXT,
    CodigoFipe TEXT,
    MesReferencia TEXT,
    Autenticacao TEXT,
    TipoVeiculo INTEGER,
    SiglaCombustivel TEXT,
    DataConsulta TEXT,
    codigoTabelaReferencia INTEGER,
    codigoTipoVeiculo INTEGER,
    codigoMarca INTEGER,
    codigoModelo INTEGER,
    anoModelo INTEGER,
    codigoTipoCombustivel INTEGER,
    tipoConsulta TEXT,
    updatedAt TEXT
);