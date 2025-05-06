---

# 📘 Referência da API REST – EasyERP (v1)

Esta documentação descreve os endpoints disponíveis na versão 1 da API EasyERP. Todas as requisições devem utilizar a rota base:

```
/api/v1/
```

---

## 🔐 Autenticação

A autenticação é feita utilizando **JWT Bearer Token**.

### POST `/login`

Realiza login do usuário e retorna um token de acesso.

**Requisição (Body JSON):**

```json
{
  "email": "admin@easyerp.com",
  "senha": "admin123"
}
```

**Resposta:**

```json
{
  "access_token": "eyJ0eXAi...",
  "usuario": {
    "id": "uuid",
    "nome": "Admin",
    "email": "admin@easyerp.com",
    "perfil_id": "uuid"
  }
}
```

### GET `/me`

Retorna os dados do usuário autenticado.

**Headers obrigatórios:**

```
Authorization: Bearer <token>
```

### GET `/check`

Verifica se o token JWT é válido.

---

## 👥 Usuários

*Requer autenticação e permissões específicas.*

* **GET** `/core/usuarios`
  Lista todos os usuários cadastrados.

* **POST** `/core/usuarios`
  Cria um novo usuário.

* **PUT** `/core/usuarios/<id>`
  Atualiza os dados de um usuário existente.

* **DELETE** `/core/usuarios/<id>`
  Desativa um usuário (soft delete).

---

## 💰 Financeiro

* **GET** `/financeiro/contas`
  Lista todas as contas bancárias cadastradas.

* **GET** `/financeiro/lancamentos`
  Lista os lançamentos financeiros do usuário autenticado.

* **GET** `/financeiro/contas/<id>/conciliacao`
  Executa a conciliação bancária da conta especificada.

---

## 📞 Vendas & CRM

* **GET** `/vendas/clientes`
  Retorna todos os clientes cadastrados.

* **GET** `/vendas/oportunidades`
  Retorna as oportunidades de venda cadastradas.

---

## 📦 Estoque

* **GET** `/estoque/saldo?produto_id=<uuid>&armazem_id=<uuid>`
  Consulta a quantidade atual de um produto em um armazém específico.

* **POST** `/estoque/movimentar`
  Registra uma movimentação de estoque.

**Body JSON exemplo:**

```json
{
  "tipo": "entrada",
  "produto_id": "uuid",
  "quantidade": 10,
  "armazem_destino_id": "uuid",
  "motivo": "Reposição"
}
```

---

## 📅 Jobs Automáticos

* **Backups diários:** `backup_job`
* **Lembretes por e-mail:** `email_reminder`
* **Notificações de vencimento:** `vencimento_notifier`

---

## 🔒 Cabeçalhos Obrigatórios

Todas as requisições (exceto `/login`) devem conter obrigatoriamente os seguintes cabeçalhos HTTP:

```http
Authorization: Bearer <token>
Content-Type: application/json
```

---

## ⚠️ Códigos de Resposta HTTP

| Código | Significado              |
| ------ | ------------------------ |
| 200    | OK                       |
| 201    | Criado com sucesso       |
| 400    | Requisição inválida      |
| 401    | Não autorizado           |
| 403    | Acesso negado            |
| 404    | Recurso não encontrado   |
| 422    | Erro de regra de negócio |
| 500    | Erro interno do servidor |

---

## 📢 Observações Gerais

* Todas as datas estão no formato ISO 8601 (UTC).
* O sistema está preparado para múltiplas versões da API (v1, v2, etc.).
* Todas as respostas de erro seguem o padrão abaixo:

**Exemplo de resposta de erro padrão:**

```json
{
  "erro": {
    "codigo": 400,
    "mensagem": "Mensagem explicativa do erro."
  }
}
```
