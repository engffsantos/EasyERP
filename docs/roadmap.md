# 🗺️ Roadmap de Desenvolvimento - EasyERP

Este documento apresenta o plano de evolução do EasyERP com base nas necessidades dos usuários, validações de mercado e diretrizes técnicas da EasyData360. O roadmap é organizado por marcos (milestones) e versões incrementais.

---

## ✅ Versão 1.0 - Lançamento Inicial (MVP)

**Status:** ✅ Finalizado  
**Data prevista:** Março 2025

### Funcionalidades entregues:

- [x] Autenticação JWT e login via API
- [x] Módulo Core (Usuários, Perfis, Permissões)
- [x] Módulo Financeiro (Contas, Lançamentos, Conciliação)
- [x] Módulo Vendas & CRM (Clientes, Oportunidades, Produtos)
- [x] Módulo Estoque (Movimentações, Inventário, Armazéns)
- [x] Módulo Service Desk (Tickets, Ativos, Integração GLPI)
- [x] Geração de relatórios em PDF (Balanço, Giro de Estoque)
- [x] Tarefas agendadas com APScheduler (backup, lembretes)
- [x] Estrutura modular com Flask + PostgreSQL + Docker
- [x] Testes unitários e de integração com pytest

---

## 🔜 Versão 1.1 - Aprimoramentos e Estabilidade

**Status:** 🔧 Em andamento  
**Previsão:** Maio 2025

### Melhorias previstas:

- [x] Dashboard de BI com gráficos (D3.js, Chart.js)
- [x] Filtros avançados por período, perfil e status
- [x] Exportação de dados CSV/Excel por módulo
- [x] Upload e visualização de anexos em tickets e clientes
- [x] Auditoria visual em interface administrativa
- [x] Confirmação por e-mail para novo usuário
- [x] Melhorias nos testes automatizados (CI/CD)

---

## 🧩 Versão 2.0 - API Pública & Integrações

**Status:** 🔜 Planejada  
**Previsão:** Julho 2025

### Funcionalidades planejadas:

- [ ] Publicação da API REST externa com chave de acesso
- [ ] Webhooks para sincronização com terceiros (ex: NF-e, CRM)
- [ ] SDK Python para integração com a API
- [ ] Single Sign-On (SSO) com Google e Microsoft
- [ ] Integração nativa com Power BI e Google Sheets

---

## ☁️ Versão 2.1 - Escalabilidade e Multiempresa

**Status:** 🔜 Planejada  
**Previsão:** Setembro 2025

- [ ] Suporte a múltiplas empresas por instância
- [ ] Isolamento de dados por tenant (multi-tenant)
- [ ] Limites por plano de uso (freemium / SaaS)
- [ ] Monitoramento de performance e alertas

---

## 💡 Ideias futuras (Backlog)

- [ ] Assistente por IA para análise de vendas e finanças
- [ ] Notificações push em tempo real com WebSocket
- [ ] App mobile (PWA + Android nativo)
- [ ] OCR de notas fiscais em lançamentos financeiros
- [ ] Módulo de folha de pagamento e RH
- [ ] CRM visual estilo kanban
- [ ] Reconhecimento facial para login interno

---

## 📬 Sugestões

Tem sugestões ou quer priorizar uma funcionalidade?  
Envie para: **contato@easydata360.com.br**

---

© 2025 EasyData360 — Todos os direitos reservados.
