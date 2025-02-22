#!/bin/bash

# Definir nomes dos arquivos
DATABASE_FILE="db.sqlite"
DUMP_FILE="dump.sql"
ZIP_FILE="dump20250221.zip"

# Verificar se o SQLite está instalado
if ! command -v sqlite3 &> /dev/null; then
    echo "Erro: sqlite3 não está instalado ou não está no PATH."
    exit 1
fi

# Criar o dump do banco de dados SQLite
echo "Criando dump do banco de dados..."
sqlite3 "$DATABASE_FILE" .dump > "$DUMP_FILE"

# Verificar se o dump foi criado
if [ ! -f "$DUMP_FILE" ]; then
    echo "Erro: Falha ao criar o dump do banco de dados."
    exit 1
fi

# Compactar o dump para ZIP
echo "Compactando dump para ZIP..."
zip -9 "$ZIP_FILE" "$DUMP_FILE"

# Verificar se o ZIP foi criado
if [ ! -f "$ZIP_FILE" ]; then
    echo "Erro: Falha ao compactar o arquivo."
    exit 1
fi

# Deletar o dump.sql original
echo "Removendo arquivo original..."
rm "$DUMP_FILE"

echo "Processo concluído! Arquivo ZIP criado: $ZIP_FILE"
