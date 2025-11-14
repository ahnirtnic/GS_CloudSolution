#!/bin/bash
set -e

# ========= CONFIGURAÇÕES =========
RG="rg-gs-giovana-cs"
PLAN="plan-gs-giovana-cs"
WEBAPP="webapp-gs-giovana-cs"
LOCATION="brazilsouth"
RUNTIME="PYTHON:3.12"
# ==================================

echo "Verificando login no Azure..."
az account show >/dev/null 2>&1 || az login

echo "Criando Resource Group..."
az group create \
  --name $RG \
  --location $LOCATION

echo "Criando App Service Plan (Linux B1)..."
az appservice plan create \
  --name $PLAN \
  --resource-group $RG \
  --is-linux \
  --sku B1

echo "Criando WebApp Python 3.12..."
az webapp create \
  --resource-group $RG \
  --plan $PLAN \
  --name $WEBAPP \
  --runtime "$RUNTIME"

echo "Infraestrutura criada com sucesso!"
echo "URL: https://$WEBAPP.azurewebsites.net"