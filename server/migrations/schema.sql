PRAGMA foreign_keys = ON;

-- Tabela de Tipos (ex: carros, motos, caminhões)
DROP TABLE IF EXISTS types;
CREATE TABLE IF NOT EXISTS types (
    types_id INTEGER PRIMARY KEY AUTOINCREMENT,
    value INTEGER NOT NULL UNIQUE,
    label TEXT NOT NULL
);

INSERT INTO types (value, label) VALUES
(1, 'carros'),
(2, 'motos'),
(3, 'caminhoes');

-- Tabela de Marcas
DROP TABLE IF EXISTS brands;
CREATE TABLE IF NOT EXISTS brands (
  brands_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Label TEXT NOT NULL,
  Value TEXT NOT NULL,
  codigoTabelaReferencia INTEGER NOT NULL,
  codigoTipoVeiculo INTEGER NOT NULL,
  updatedAt TEXT NOT NULL,
  FOREIGN KEY (codigoTipoVeiculo) REFERENCES types(Value)
);

-- Tabela de Modelos
DROP TABLE IF EXISTS models;
CREATE TABLE IF NOT EXISTS models (
    models_id INTEGER PRIMARY KEY AUTOINCREMENT,
    value INTEGER NOT NULL,  -- valor recebido dos endpoints
    label TEXT NOT NULL,
    brand_id INTEGER NOT NULL,  -- referência à marca
    type_id INTEGER NOT NULL,   -- referência ao tipo
    updated_at TEXT,
    UNIQUE (value, brand_id, type_id),
    FOREIGN KEY (brand_id) REFERENCES brands(brands_id),
    FOREIGN KEY (type_id) REFERENCES types(types_id)
);

-- Tabela de Anos (ex: "1992-1")
DROP TABLE IF EXISTS years;
CREATE TABLE IF NOT EXISTS years (
    years_id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT NOT NULL,  -- valor composto recebido dos endpoints (ex: "1992-1")
    label TEXT NOT NULL,
    model_id INTEGER NOT NULL,  -- referência ao modelo
    brand_id INTEGER NOT NULL,  -- referência à marca
    type_id INTEGER NOT NULL,   -- referência ao tipo
    updated_at TEXT,
    UNIQUE (value, model_id, brand_id, type_id),
    FOREIGN KEY (model_id) REFERENCES models(models_id),
    FOREIGN KEY (brand_id) REFERENCES brands(brands_id),
    FOREIGN KEY (type_id) REFERENCES types(types_id)
);

-- Tabela de Detalhes
DROP TABLE IF EXISTS datails;
CREATE TABLE IF NOT EXISTS details (
    details_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER NOT NULL,   -- referência ao tipo
    brand_id INTEGER NOT NULL,  -- referência à marca
    model_id INTEGER NOT NULL,  -- referência ao modelo
    year INTEGER NOT NULL,      -- ano (parte numérica)
    valor TEXT,
    marca TEXT,
    modelo TEXT,
    ano_modelo INTEGER,
    combustivel TEXT,
    codigo_fipe TEXT,
    mes_referencia TEXT,
    autenticacao TEXT,
    tipo_veiculo INTEGER,
    sigla_combustivel TEXT,
    data_consulta TEXT,
    updated_at TEXT,
    UNIQUE (type_id, brand_id, model_id, year),
    FOREIGN KEY (type_id) REFERENCES types(types_id),
    FOREIGN KEY (brand_id) REFERENCES brands(brands_id),
    FOREIGN KEY (model_id) REFERENCES models(models_id)
);

