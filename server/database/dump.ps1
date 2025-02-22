# Definir nomes dos arquivos
$databaseFile = "db.sqlite"
$dumpFile = "dump.sql"
$zipFile = "dump20250221.zip"

# Verificar se o SQLite está disponível
if (-Not (Get-Command "sqlite3" -ErrorAction SilentlyContinue)) {
    Write-Output "Erro: sqlite3 não está instalado ou não está no PATH."
    exit 1
}

# Criar o dump do banco de dados SQLite
Write-Output "Criando dump do banco de dados..."
sqlite3 $databaseFile .dump > $dumpFile

# Verificar se o dump foi criado
if (-Not (Test-Path $dumpFile)) {
    Write-Output "Erro: Falha ao criar o dump do banco de dados."
    exit 1
}

# Compactar o dump para ZIP
Write-Output "Compactando dump para ZIP..."
Compress-Archive -Path $dumpFile -DestinationPath $zipFile -CompressionLevel Optimal

# Verificar se o ZIP foi criado
if (-Not (Test-Path $zipFile)) {
    Write-Output "Erro: Falha ao compactar o arquivo."
    exit 1
}

# Deletar o dump.sql original
Write-Output "Removendo arquivo original..."
Remove-Item $dumpFile

Write-Output "Processo concluído! Arquivo ZIP criado: $zipFile"


