#!/bin/bash

# =============================================
# Script de setup inicial do EasyERP na nuvem
# Autor: EasyData360
# Requisitos: Ubuntu/Debian, sudo, acesso à internet
# =============================================

set -e

echo "🚀 Iniciando setup do servidor..."

# Atualiza pacotes
sudo apt update && sudo apt upgrade -y

# Instala pacotes essenciais
echo "📦 Instalando dependências..."
sudo apt install -y python3 python3-pip python3-venv git curl ufw unzip build-essential libpq-dev

# Instala Docker
echo "🐳 Instalando Docker..."
if ! command -v docker &> /dev/null; then
  curl -fsSL https://get.docker.com | bash
  sudo usermod -aG docker $USER
else
  echo "✔ Docker já instalado"
fi

# Instala Docker Compose (v2)
echo "📦 Instalando Docker Compose..."
DOCKER_COMPOSE_VERSION="2.20.2"
sudo curl -SL https://github.com/docker/compose/releases/download/v$DOCKER_COMPOSE_VERSION/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Configura firewall básico
echo "🛡️ Configurando firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Cria diretório de projeto
echo "📁 Clonando repositório do EasyERP..."
cd ~
if [ ! -d "EasyERP" ]; then
  git clone https://github.com/sua-empresa/easyerp.git EasyERP
else
  echo "✔ Repositório já existente"
fi

cd EasyERP

# Cria arquivo .env
echo "🔧 Criando arquivo .env"
cp .env.sample .env

# Sobe containers
echo "🛠️ Inicializando aplicação com Docker Compose..."
docker-compose up -d --build

echo "✅ Setup concluído! Acesse a aplicação via IP público da instância."
