Vamos analisar os **commits** do seu repositório para determinar a versão atual do software, seguindo as regras do **Semantic Versioning (SemVer)**. O SemVer define que a versão é composta por **MAJOR.MINOR.PATCH** (ex: `1.2.3`), onde:

- **MAJOR**: Mudanças incompatíveis com versões anteriores (breaking changes).
- **MINOR**: Adição de funcionalidades compatíveis com versões anteriores.
- **PATCH**: Correções de bugs compatíveis com versões anteriores.

---

---

## **Análise dos Commits**

### **1. Commits Iniciais (Base do Projeto)**

- **`7c7cd9df` (Sun May 3 22:00:10 2026)**
  - **Descrição**: Inicialização das rotas, cookies e conexão com SQLite.
  - **Tipo**: **feat** (nova funcionalidade).
  - **Impacto**: Primeiro commit com funcionalidades básicas (rotas, cookies, banco de dados).
  - **Versão sugerida**: **`0.1.0`** (primeira versão com funcionalidades mínimas).

---

- **`1d7eb993` (Mon May 4 01:57:43 2026)**
  - **Descrição**: Refatoração da arquitetura de `posts`:
    - Migração da lógica de negócio para a camada de **Service**.
    - Implementação de **paginação dinâmica** (3 itens por página).
    - Adição de rotas de **deleção e publicação rápida**.
    - Melhoria na validação de campos obrigatórios.
    - Documentação técnica no README.
  - **Tipo**: **refactor** (melhorias na arquitetura, sem breaking changes).
  - **Impacto**: Adição de funcionalidades significativas (paginação, novas rotas, validações).
  - **Versão sugerida**: **`0.2.0`** (nova funcionalidade compatível, **MINOR**).

---

- **`53259a77` (Tue May 5 19:30:12 2026)**
  - **Descrição**: Reestruturação para `src/`, implementação de **autenticação JWT** e suíte de testes:
    - Reorganização da arquitetura.
    - Sistema de **segurança e autenticação** (JWT).
    - Suíte de testes de integração com Pytest.
    - Makefile para automação.
    - Documentação técnica.
  - **Tipo**: **feat** (nova funcionalidade).
  - **Impacto**: Adição de **autenticação** (funcionalidade crítica e compatível).
  - **Versão sugerida**: **`0.3.0`** (nova funcionalidade, **MINOR**).

---

### **2. Commits de Correções e Melhorias**

- **`34f3e655` (Sat May 9 15:16:08 2026)**
  - **Descrição**: Correções e melhorias:
    - Ajuste na lógica de **paginação** (limite padrão de 5 posts).
    - Suporte ao filtro `published` na listagem de posts.
    - **Reforço na segurança JWT** (SECRET key maior, conforme RFC 7518).
    - Melhorias na **DX** (configurações para VS Code, Pyright).
    - Padronização de imports (`typing.Annotated`).
    - Atualização do `.gitignore`.
  - **Tipo**: **fix** (correções e melhorias de segurança).
  - **Impacto**: Correções de bugs e melhorias de segurança (compatíveis).
  - **Versão sugerida**: **`0.3.1`** (correções, **PATCH**).

---

- **`811e3eb3` (Sat May 9 16:40:54 2026)**
  - **Descrição**: Refatoração de arquitetura:
    - Padronização global de nomenclatura (`read_` → `get_`).
    - **Nova arquitetura de erros** (exceções customizadas, Exception Handlers globais para 404, 400, 409).
    - Novos métodos e endpoints de busca para posts (**por ID, Título, Conteúdo**).
    - Suporte a filtros por ID em rotas de listagem.
    - Validações de unicidade (e-mail de usuários, títulos de posts).
    - Expansão da suíte de testes para **21 casos**.
  - **Tipo**: **refact** (melhorias na arquitetura, sem breaking changes).
  - **Impacto**: Adição de **novas funcionalidades de busca e validações** (compatíveis).
  - **Versão sugerida**: **`0.4.0`** (novas funcionalidades, **MINOR**).

---

---

## **Resumo das Versões**

| Commit     | Tipo     | Impacto                                        | Versão Sugerida |
| ---------- | -------- | ---------------------------------------------- | --------------- |
| `7c7cd9df` | feat     | Funcionalidades básicas                        | **0.1.0**       |
| `1d7eb993` | refactor | Paginação, rotas, validações                   | **0.2.0**       |
| `53259a77` | feat     | Autenticação JWT, testes                       | **0.3.0**       |
| `34f3e655` | fix      | Correções de paginação, segurança              | **0.3.1**       |
| `811e3eb3` | refact   | Nova arquitetura de erros, filtros, validações | **0.4.0**       |

---

## **Versão Atual do Software**

Com base nos commits analisados, a versão atual do seu software, seguindo o **Semantic Versioning**, é:

### **`0.4.0`**

---

### **Justificativa Final**

- **`0.1.0`**: Versão inicial com funcionalidades básicas.
- **`0.2.0`**: Adição de paginação, rotas e validações (MINOR).
- **`0.3.0`**: Adição de autenticação JWT e suíte de testes (MINOR).
- **`0.3.1`**: Correções de bugs e melhorias de segurança (PATCH).
- **`0.4.0`**: Nova arquitetura de erros, filtros avançados e validações (MINOR).

---
