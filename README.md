# 🕒 My First Time Tracker

Aplicação full-stack para controle de ponto e banco de horas.

<img width="1366" height="768" alt="Screenshot" src="https://github.com/user-attachments/assets/a83e4df5-6e0e-46a8-b63e-ed4542242759" />

## 🚀 Tecnologias

- Front-end: React (Vite)
- Back-end: FastAPI (Python)
- DB: SQLite + SQLAlchemy
- Autenticação: JWT no backend (header Authorization)
- HTTP client: Axios

## 🧩 Arquitetura

- `backend/`: API REST
- `frontend/`: SPA React
- `ponto.db`: SQLite (gerada localmente)

## ✅ Funcionalidades atuais

- Cadastro de usuário (`POST /usuarios/cadastro`)
- Login e emissão de token JWT (`POST /usuarios/login`)
- Lançar ponto com entrada+saída (`POST /ponto`)
  - calcula `total_trabalhado` em horas
  - calcula `saldo` (horas trabalhadas - 8) e salva no registro
- Histórico do usuário (`GET /historico-pontos`)
- Deletar ponto do histórico (`DELETE /deletar-ponto/{id}`)
- Saldo acumulado do usuário (`GET /saldo-geral`)
- Saldo global (`GET /usuario/saldo-geral`) (soma de `total_trabalhado`)

## 🔍 Regras de negócio

- Jornada padrão: 8h
- `saldo_dia = total_trabalhado - 8`
- `total_trabalhado` calculado com `saida - entrada` (hora decimal)
- Somatória do saldo por usuário via SQL `SUM(saldo)` (filtrando `owner_id`)

## 🛠️ Instalação e execução

### 1) Backend

```bash
cd backend
python -m venv .venv
. .venv/Scripts/Activate.ps1   # Windows PowerShell
# ou source .venv/bin/activate  # Linux/Mac
pip install fastapi uvicorn sqlalchemy passlib bcrypt python-jose
uvicorn app:app --reload
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3) Uso

1. Cadastre um usuário.
2. Faça login e salve token no localStorage.
3. Acesse dashboard.
4. Lance ponto: data/horário entrada + saída.
5. Veja total, saldo do dia e saldo geral.
6. Exclua registros a partir da tabela.

## 🧾 API Endpoints

| Método | Rota                  | Descrição                      |
| ------ | --------------------- | ------------------------------ |
| POST   | `/usuarios/cadastro`  | cadastrar usuário              |
| POST   | `/usuarios/login`     | login, retorna JWT             |
| POST   | `/ponto`              | registra ponto (entrada/saída) |
| GET    | `/historico-pontos`   | lista pontos do usuário        |
| DELETE | `/deletar-ponto/{id}` | remove registro                |
| GET    | `/saldo-geral`        | soma do `saldo` do usuário     |

## 🛡️ Observações de segurança

- CORS liberado para qualquer origem (`allow_origins=["*"]`) em dev
- Token JWT é exigido nas rotas protegidas (`/historico-pontos`, `/ponto`, `/saldo-geral`)
- Hash de senha com bcrypt
- Chave secreta do JWT (`SECRET_KEY`) carregada via variável de ambiente

## 🔐 Configuração de ambiente (sensible data)

1. Copie `backend/.env.example` para `backend/.env`.
2. Defina uma chave segura (não comite):

```ini
SECRET_KEY=uma_chave_super_secret_comprida
ALGORITHM=HS256
ACESS_TOKEN_EXPIRE_MINUTES=60
```

3. O backend carrega `backend/.env` automaticamente, sem necessidade de `python-dotenv`.
4. Se `.env` não estiver presente, o código usa fallback `SECRET_KEY` de desenvolvimento (`MINHA_CHAVE_SUPERSECRETA_2026`) para evitar quebrar o login.
5. **Não comite** `backend/.env`, `ponto.db`, `.venv/` ou `node_modules/`.

## 📍 Estrutura de arquivos

```
backend/
  app.py
  models.py
  database.py
  security.py
frontend/
  src/
    Dashboard.jsx
    Login.jsx
    App.jsx
```

## 🙋 Desenvolvedora

- Patricia Correia
- Estudante de Sistemas de Informação
- João Pessoa - PB, Brasil

---

> Status atual: funcional e pronto para publicação em repositório com documentação básica de uso e deploy local.

