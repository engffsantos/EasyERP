# EasyERP

**EasyERP**  é um sistema de gestão empresarial modular desenvolvido pela EasyData360 com foco em pequenas e médias empresas que buscam uma solução flexível, segura e escalável. Desenvolvido em Python com Flask, banco de dados PostgreSQL e infraestrutura em nuvem, o sistema é estruturado com arquitetura MVC e oferece APIs RESTful para integração com outras plataformas. O módulo Core é responsável pelo controle de usuários, autenticação JWT, hierarquia entre usuários (supervisor_id), gestão de perfis de acesso com RBAC, permissões e logs de auditoria. Inclui campos padrão como ativo, criado_em e atualizado_em para controle de ciclo de vida. O módulo Financeiro permite o cadastro de contas bancárias, categorias de receitas e despesas, lançamentos financeiros com recorrência, códigos de barras, NF-e, e controle de saldos. Suporta transferências entre contas, conciliação bancária e geração de relatórios financeiros. O módulo de Vendas & CRM possibilita o cadastro de clientes e leads, registro de interações (e-mail, ligação, reunião), oportunidades de venda com probabilidade de conversão, histórico de mudanças de status, associação de produtos às oportunidades e atribuição de responsáveis comerciais. O módulo de Estoque permite o cadastro de armazéns, controle de inventário com estoques mínimos e máximos, movimentações de entrada, saída, transferência e ajustes, além de registrar compras de fornecedores e itens adquiridos. Todos os módulos possuem campos de auditoria e seguem boas práticas de normalização e integridade referencial. O módulo de Segurança & Conformidade oferece criptografia de dados sensíveis, backup automático em nuvem, aceites de termos de uso e relatórios de conformidade com LGPD/GDPR. O módulo de Business Intelligence disponibiliza dashboards com filtros por data, usuário, cliente ou categoria, além de exportação em CSV, Excel ou PDF e integração com ferramentas externas como Power BI ou Python. A infraestrutura é preparada para containerização com Docker e deployment em AWS, Azure ou GCP, permitindo escalabilidade horizontal e monitoramento via ferramentas especializadas. Todas as funcionalidades do EASYERP são acessíveis via web, com interface responsiva e suporte a personalizações white-label.

---

## 🚀 Visão Geral

O EasyERP permite o controle centralizado e eficiente de áreas como:

- Financeiro
- Vendas & CRM
- Estoque
- Segurança & Conformidade
- Business Intelligence

Com um design modular, cada empresa ativa apenas os módulos necessários, reduzindo complexidade e custos.

---

## 🧩 Funcionalidades Principais

### 1. Módulo CORE (Sistema Base)

**Gestão de Usuários**

* Cadastro com hierarquia (supervisor/subordinado)
* Ativação e desativação de contas (soft delete)
* Redefinição de senha com envio de e-mail de confirmação

**Controle de Acesso (RBAC)**

* Criação de perfis customizáveis
* Atribuição granular de permissões (CRUD por módulo)
* Validação dinâmica de permissões por rota e operação

**Auditoria**

* Log de alterações em tabelas críticas
* Rastreamento de atividades por usuário e endereço IP

---

### 2. Módulo FINANCEIRO

**Contas Bancárias**

* Cadastro de contas com saldo inicial
* Atualização automática de saldos via trigger

**Lançamentos Financeiros**

* Receitas e despesas com recorrência
* Agendamento de lançamentos periódicos
* Geração automática no fechamento mensal

**Conciliação Bancária**

* Importação de extratos OFX/CSV com validação de duplicatas

**Fluxo de Caixa e DRE**

* Projeção de receitas/despesas futuras
* Geração de relatório DRE (Demonstração de Resultados)

**Transferências**

* Transferência entre contas com registro automático nos extratos
* Emissão de comprovante em PDF

**Alertas e Notificações**

* Notificações de vencimentos por e-mail ou sistema

---

### 3. Módulo VENDAS & CRM

**Pipeline de Vendas**

* Kanban visual por estágio (prospecção → fechamento)
* Cálculo automático de probabilidade com base em regras
* Alertas automáticos para follow-up

**Gestão de Clientes**

* Visão 360° com histórico consolidado de interações
* Classificação por potencial (A/B/C)
* Importação de listas de contatos via planilha

**Orçamentos e Propostas**

* Geração de propostas em PDF
* Aprovação eletrônica com assinatura digital integrada
* Conversão automática de proposta em pedido

---

### 4. Módulo ESTOQUE

**Controle de Inventário**

* Estoque por múltiplos armazéns/localizações
* Níveis de estoque mínimo e máximo por produto

**Movimentações**

* Entradas via compras (integração com NF-e)
* Saídas vinculadas a oportunidades de venda
* Transferências entre armazéns com validação em duas etapas

**Rastreabilidade**

* Controle por lote, validade e histórico de movimentações
* Relatório de giro de estoque com base FIFO

---

### 5. Funcionalidades Transversais

**Segurança**

* Criptografia AES-256 para dados sensíveis
* Backup automatizado diário em múltiplas cópias na nuvem
* Mascaramento de dados com base no perfil do usuário

**Integrações via API REST**

* Gateway de pagamentos (Pix, boleto)
* Correios (cálculo de frete e rastreamento)
* Sefaz (consulta de CNPJ e NF-e)

**Business Intelligence**

* Painéis interativos com filtros dinâmicos
* Indicadores de desempenho: lucratividade, CAC, conversão
* Curva ABC de produtos e clientes

---

### 6. Workflows Específicos

**Fechamento Mensal**

* Bloqueio de lançamentos retroativos
* Geração automatizada de arquivos SPED (Fiscal e Contábil)

**Aprovação de Compras**

* Fluxo hierárquico por alçada de valor
* Comparativo automático com até 3 cotações

**Onboarding de Clientes**

* Checklist de documentos (KYC)
* Validação automática de crédito

---

## 🛠️ Arquitetura

- **Backend:** Python 3.10+, Flask, SQLAlchemy
- **Frontend:** HTML5, CSS3, JS (Bootstrap/jQuery)
- **Banco de Dados:** PostgreSQL
- **Infraestrutura:** Docker, compatível com AWS, Azure e GCP
- **Padrão:** MVC + RESTful API

---

## ⚙️ Requisitos

- Python 3.10+
- PostgreSQL 13+
- Docker e Docker Compose (opcional)
- Make (Linux/macOS) ou WSL (Windows)

---

## 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/easydata360/easyerp.git
cd easyerp

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Configure variáveis de ambiente (exemplo no .env.example)
cp .env.example .env

# Inicie a aplicação
flask run
```
📁 Estrutura do Projeto
```
erp_easydata360/
│
├── app/                             # Código-fonte principal da aplicação
│   ├── __init__.py                  # Inicialização da aplicação Flask
│   ├── config.py                    # Configurações gerais
│   ├── extensions.py                # Inicialização de extensões Flask (JWT, DB, Migrate)
│
│   ├── core/                        # Módulo CORE (usuários, permissões, RBAC)
│   │   ├── controllers/
│   │   │   ├── auth_controller.py
│   │   │   ├── user_controller.py
│   │   │   └── profile_controller.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── profile.py
│   │   │   └── permission.py
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── user_routes.py
│   │   │   └── profile_routes.py
│   │   ├── schemas/
│   │   │   └── user_schema.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   └── user_service.py
│   │   ├── utils/
│   │   │   ├── decorators.py
│   │   │   └── audit_logger.py
│   │   ├── templates/core/
│   │   │   ├── auth/login.html
│   │   │   ├── auth/register.html
│   │   │   ├── users/list.html
│   │   │   └── users/edit.html
│   │   └── static/core/
│   │       └── js/user_validation.js
│
│   ├── financeiro/
│   │   ├── controllers/
│   │   │   ├── account_controller.py
│   │   │   └── transaction_controller.py
│   │   ├── models/
│   │   │   ├── account.py
│   │   │   └── transaction.py
│   │   ├── routes/
│   │   │   └── financeiro_routes.py
│   │   ├── schemas/
│   │   │   └── transaction_schema.py
│   │   ├── services/
│   │   │   └── reconciliation_service.py
│   │   ├── reports/
│   │   │   ├── balance_report.py
│   │   │   └── templates/balance_sheet.pdf.jinja2
│   │   └── jobs/
│   │       └── vencimento_notifier.py
│
│   ├── vendas/
│   │   ├── controllers/
│   │   │   ├── cliente_controller.py
│   │   │   └── oportunidade_controller.py
│   │   ├── models/
│   │   │   ├── cliente.py
│   │   │   └── oportunidade.py
│   │   ├── viewmodels/
│   │   │   └── opportunity_vm.py
│   │   ├── integrations/
│   │   │   └── email_integration.py
│   │   └── schemas/
│   │       └── oportunidade_schema.py
│
│   ├── estoque/
│   │   ├── models/
│   │   │   ├── inventory.py
│   │   │   ├── movement.py
│   │   │   └── fornecedor.py
│   │   ├── controllers/
│   │   │   └── estoque_controller.py
│   │   ├── routes/
│   │   │   └── estoque_routes.py
│   │   ├── triggers/
│   │   │   └── update_stock.sql
│   │   └── reports/
│   │       └── giro_estoque.py
│
│   ├── service_desk/
│   │   ├── models/
│   │   │   ├── ticket.py
│   │   │   └── asset.py
│   │   ├── workflows/
│   │   │   └── sla_rules.py
│   │   └── integrations/
│   │       └── glpi_api.py
│
│   ├── api/                         # Rotas da API RESTful (versãoada)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth_api.py
│   │       ├── financeiro_api.py
│   │       ├── vendas_api.py
│   │       └── estoque_api.py
│
│   ├── shared/
│   │   ├── exceptions/
│   │   │   ├── business_rules.py
│   │   │   └── api_errors.py
│   │   ├── validators/
│   │   │   └── cnpj_validator.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   └── components/
│   │   │       ├── notification_toast.html
│   │   │       └── data_table.html
│   │   └── logging/
│   │       ├── config.py
│   │       └── handlers.py
│
│   ├── jobs/
│   │   ├── scheduler.py
│   │   ├── backup_job.py
│   │   └── email_reminder.py
│
│   └── hooks/
│       └── post_user_create.py
│
├── migrations/
│   └── versions/
│
├── tests/
│   ├── unit/
│   │   ├── core/test_user_model.py
│   │   └── financeiro/test_transactions.py
│   ├── integration/
│   │   └── test_api_endpoints.py
│   └── conftest.py
│
├── scripts/
│   ├── deploy/cloud_setup.sh
│   └── data/seed_database.py
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── docs/
│   ├── arquitetura.md
│   ├── api_reference.md
│   ├── casos_de_uso.md
│   └── roadmap.md
│
├── instance/
│   └── config.py
│
├── .env.sample
├── .flake8
├── .pre-commit-config.yaml
├── pyproject.toml
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── README.md
└── run.py                        # Ponto de entrada principal

```
___


## 📄 Licença
Este projeto está licenciado sob a MIT License.

## 📬 Contato
Desenvolvido por EasyData360
📧 contato@easydata360.com.br
🌐 www.easydata360.com.br
