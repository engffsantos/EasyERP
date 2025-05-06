# 📚 Casos de Uso - EasyERP

Este documento descreve os principais casos de uso do sistema EasyERP, categorizados por módulo. Cada caso de uso inclui o objetivo, pré-condições, fluxo principal e possíveis variações.

---

## 🔐 Módulo Core (Usuários & Perfis)

### 🎯 Caso de Uso: Autenticar usuário
- **Atores:** Usuário
- **Pré-condição:** Conta de usuário criada e ativa
- **Fluxo:**
  1. Usuário acessa `/login`
  2. Insere e-mail e senha
  3. O sistema valida as credenciais e retorna token JWT
- **Exceções:** E-mail inválido, senha incorreta, usuário inativo

---

### 🎯 Caso de Uso: Criar novo usuário
- **Atores:** Administrador
- **Pré-condição:** Estar autenticado com permissão `gerenciar_usuarios`
- **Fluxo:**
  1. Admin acessa a tela de cadastro de usuário
  2. Preenche dados e seleciona perfil
  3. O sistema salva e aciona o hook de pós-criação
  4. Usuário recebe e-mail de boas-vindas

---

## 💰 Módulo Financeiro

### 🎯 Caso de Uso: Registrar lançamento financeiro
- **Atores:** Usuário financeiro
- **Pré-condição:** Conta e categoria cadastradas
- **Fluxo:**
  1. Usuário preenche descrição, valor, tipo, datas e conta
  2. O sistema valida e salva o lançamento
  3. O saldo da conta é atualizado
- **Variações:** Lançamento pode ser recorrente ou ter código de barras

---

### 🎯 Caso de Uso: Conciliar conta bancária
- **Atores:** Usuário financeiro
- **Pré-condição:** Existência de lançamentos e extrato da conta
- **Fluxo:**
  1. Usuário solicita conciliação
  2. O sistema compara lançamentos e gera relatório de diferenças

---

## 📞 Módulo Vendas & CRM

### 🎯 Caso de Uso: Registrar oportunidade de venda
- **Atores:** Vendedor
- **Pré-condição:** Cliente e produtos cadastrados
- **Fluxo:**
  1. Vendedor seleciona cliente e produtos
  2. Define valor estimado, probabilidade e status inicial
  3. O sistema salva e inicia o histórico da oportunidade

---

### 🎯 Caso de Uso: Acompanhar funil de vendas
- **Atores:** Gerente comercial
- **Pré-condição:** Oportunidades registradas
- **Fluxo:**
  1. Usuário acessa dashboard de vendas
  2. Visualiza oportunidades por etapa e responsável

---

## 📦 Módulo Estoque

### 🎯 Caso de Uso: Movimentar estoque
- **Atores:** Almoxarife, Compras
- **Pré-condição:** Produto e armazém cadastrados
- **Fluxo:**
  1. Usuário informa tipo da movimentação (entrada, saída, ajuste, transferência)
  2. Quantidade e motivo são preenchidos
  3. O estoque do produto é atualizado automaticamente via trigger

---

### 🎯 Caso de Uso: Consultar saldo de produto
- **Atores:** Comprador, Estoquista
- **Fluxo:**
  1. Usuário informa produto e armazém
  2. Sistema retorna a quantidade disponível atual

---

## 🛠️ Módulo Service Desk

### 🎯 Caso de Uso: Abrir ticket de suporte
- **Atores:** Funcionário, Cliente interno
- **Fluxo:**
  1. Preenche tipo, descrição, ativo afetado
  2. Sistema cria ticket e aplica regras de SLA
  3. Técnicos são notificados com base na prioridade

---

## 🔄 Integrações

### 🎯 Caso de Uso: Enviar lembretes por e-mail
- **Atores:** Sistema
- **Fluxo:**
  1. Job periódico busca usuários ativos
  2. Dispara e-mails de lembrete agendado
  3. Registra logs de envio

---

## 🔐 Segurança e Conformidade

### 🎯 Caso de Uso: Auditar ações de usuário
- **Atores:** Sistema, Administrador
- **Fluxo:**
  1. A cada ação crítica (login, edição, exclusão)
  2. Um log é registrado com data, usuário e descrição
  3. Logs podem ser exportados para conformidade LGPD/GDPR

---

© 2025 EasyData360 — Todos os direitos reservados.
