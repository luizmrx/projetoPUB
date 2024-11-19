#!/bin/bash

# Configurações do MySQL
DB_USER="admin"         # Substitua pelo seu usuário do MySQL
DB_PASSWORD="admin"       # Substitua pela sua senha do MySQL
DB_NAME='tool_manage'       # Substitua pelo nome do seu banco de dados
BACKUP_PATH="."  # Defina o caminho onde o backup será salvo
DATE=$(date +%Y%m%d_%H%M%S)   # Adiciona timestamp ao nome do arquivo de backup

# Cria o backup
mysqldump -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > $BACKUP_PATH/backup_$DB_NAME_$DATE.sql

# Verifica se o backup foi criado com sucesso
if [ $? -eq 0 ]; then
  echo "Backup do banco de dados $DB_NAME realizado com sucesso!"
else
  echo "Erro ao realizar o backup do banco de dados $DB_NAME."
fi