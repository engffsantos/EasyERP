# app/service_desk/integrations/glpi_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GLPI_API_URL = os.getenv("GLPI_API_URL")
GLPI_APP_TOKEN = os.getenv("GLPI_APP_TOKEN")
GLPI_USER_TOKEN = os.getenv("GLPI_USER_TOKEN")


def iniciar_sessao_glpi():
    """
    Inicia sessão com o GLPI e retorna o token de sessão.
    """
    headers = {
        'App-Token': GLPI_APP_TOKEN,
        'Authorization': f'user_token {GLPI_USER_TOKEN}'
    }
    response = requests.get(f"{GLPI_API_URL}/initSession", headers=headers)

    if response.status_code == 200:
        return response.json().get('session_token')
    else:
        raise Exception(f"Erro ao iniciar sessão GLPI: {response.text}")


def criar_ticket_glpi(titulo, descricao, usuario_nome):
    """
    Cria um novo chamado no GLPI a partir de um ticket do EasyERP.
    """
    session_token = iniciar_sessao_glpi()

    headers = {
        'App-Token': GLPI_APP_TOKEN,
        'Session-Token': session_token,
        'Content-Type': 'application/json'
    }

    payload = {
        "input": {
            "name": titulo,
            "content": descricao,
            "requesttypes_id": 1,  # Tipo: Solicitação
            "status": 1,           # Aberto
            "priority": 3,         # Normal
            "users_id_recipient": 0,
            "_users_id_requester": usuario_nome
        }
    }

    response = requests.post(f"{GLPI_API_URL}/Ticket", json=payload, headers=headers)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Erro ao criar ticket GLPI: {response.text}")


def encerrar_sessao_glpi(session_token):
    """
    Encerra a sessão ativa com o GLPI.
    """
    headers = {
        'App-Token': GLPI_APP_TOKEN,
        'Session-Token': session_token
    }
    requests.get(f"{GLPI_API_URL}/killSession", headers=headers)
