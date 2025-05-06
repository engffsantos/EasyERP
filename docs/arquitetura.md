# 🧩 Arquitetura do Sistema EasyERP

O EasyERP é um sistema modular de gestão empresarial desenvolvido pela **EasyData360**, projetado para atender pequenas e médias empresas com foco em **flexibilidade, segurança, escalabilidade e integração** com outras plataformas.

---

## 🏗️ Visão Geral da Arquitetura

O sistema é baseado na **arquitetura MVC (Model-View-Controller)** com suporte a APIs RESTful e interface web. Ele é composto por múltiplos módulos (Core, Financeiro, Vendas, Estoque, etc.), cada um isolado logicamente e com responsabilidade clara.

### 🔧 Tecnologias Utilizadas

| Camada         | Tecnologia                            |
|----------------|----------------------------------------|
| Backend        | Python 3, Flask, Flask-SQLAlchemy      |
| Banco de Dados | PostgreSQL                             |
| Autenticação   | JWT (Flask-JWT-Extended)               |
| Agendamento    | APScheduler                            |
| Background Jobs| Scripts Python, CronJobs               |
| Templates      | Jinja2 (HTML5 + CSS3)                  |
| Deploy         | Docker, Docker Compose, Gunicorn       |
| Front-end Web  | HTML, CSS, JavaScript (Progressive)    |
| Cloud Ready    | AWS / GCP / Azure                      |

---

## 🗂️ Estrutura de Diretórios
```
EasyERP/
│
├── app/ # Código-fonte principal
│ ├── core/ # Autenticação, usuários, RBAC
│ ├── financeiro/ # Contas, lançamentos, relatórios
│ ├── vendas/ # CRM, clientes, oportunidades
│ ├── estoque/ # Inventário, movimentações
│ ├── service_desk/ # Tickets, SLAs, integração GLPI
│ ├── api/ # Endpoints RESTful
│ ├── shared/ # Templates, validações, exceções, logs
│ ├── jobs/ # Tarefas agendadas e rotinas
│ └── hooks/ # Ações automáticas pós-eventos
│
├── tests/ # Testes unitários e de integração
├── scripts/ # Deploy, setup, seed do banco
├── docs/ # Documentação
├── requirements/ # Requisitos de ambientes
├── migrations/ # Histórico de migrações Alembic
├── instance/ # Configurações específicas do ambiente
└── run.py # Ponto de entrada da aplicação

```

---

## 🧱 Camadas da Aplicação

### 1. **Model**
Responsável por representar as entidades do domínio da aplicação com SQLAlchemy. Inclui lógica de negócio simples, relacionamentos e campos padrão como `criado_em`, `atualizado_em`, `ativo`.

### 2. **Controller**
Gerencia as regras de negócio e interações do usuário com a aplicação via interface web (views Jinja2) ou REST (via Blueprints).

### 3. **Routes**
Define os endpoints expostos para consumo via navegador ou API, registrando os métodos disponíveis por rota (GET, POST, etc.).

### 4. **Services**
Camada intermediária de lógica de aplicação reutilizável, especialmente para regras complexas ou que envolvam múltiplas entidades.

### 5. **Schemas**
Utiliza `marshmallow` para serialização/deserialização de dados entre objetos Python e JSON.

---

## 🔐 Segurança e Autenticação

- Tokens JWT são utilizados para autenticação e autorização via API.
- RBAC (controle baseado em perfis/permissões) está implementado no módulo Core.
- Logs de auditoria são registrados automaticamente em ações sensíveis.

---

## ☁️ Preparado para Nuvem

O EasyERP é completamente **containerizado** com Docker e pronto para deployment em ambientes como:

- **AWS ECS/Fargate**
- **GCP Cloud Run / App Engine**
- **Azure Web Apps**
- **VPS (DigitalOcean, Linode, etc.)**

Inclui:
- `Dockerfile` e `docker-compose.yml`
- `cloud_setup.sh` para provisionamento rápido
- Configuração de backup e agendamento de jobs

---

## 📊 Integrações

- **GLPI** para gestão de ativos e chamados.
- **Power BI** ou Python via CSV/Excel/PDF para dashboards.
- Webhooks e APIs REST versionadas para integrações externas.

---

## 🧪 Testes

- Testes unitários com `pytest` e `pytest-flask`.
- Testes de integração com banco em memória (`sqlite://`).
- Cobertura via `coverage`.

---

## 📈 Evolução

Consulte o arquivo `docs/roadmap.md` para visualizar as próximas fases de desenvolvimento.

---

© 2025 EasyData360 — Todos os direitos reservados.