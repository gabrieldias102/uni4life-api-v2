# uni4life-api-v2

API Python com FastAPI para uma rede social simples.

Agora a API usa PostgreSQL via SQLAlchemy e migrations com Alembic. Para producao na Vercel, a recomendacao e apontar `DATABASE_URL` para o banco Neon.

## Como executar

### Configuracao de ambiente

Defina a variavel `DATABASE_URL` no `.env` local e na Vercel:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DBNAME?sslmode=require
```

Se a variavel nao for definida, a aplicacao usa `sqlite:///./uni4life.db` como fallback local.

### Criando as tabelas com Alembic

1. Instale as dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute a migration inicial:
   ```bash
   alembic upgrade head
   ```

### Usando Docker

1. Construa a imagem:
   ```bash
   docker build -t uni4life-api .
   ```
2. Execute o container:
   ```bash
   docker run -p 8000:8000 --env-file .env uni4life-api
   ```

### Usando Docker Compose

1. Inicie o servico:
   ```bash
   docker compose up --build
   ```
2. Acesse a API em `http://127.0.0.1:8000`

## Estrutura

- `app/main.py` - ponto de entrada da aplicacao
- `app/routes.py` - definicao de rotas HTTP
- `app/services.py` - logica de negocio
- `app/repositories.py` - acesso ao banco de dados via SQLAlchemy
- `app/schemas.py` - validacao de payloads e modelos de resposta
- `app/models.py` - modelos ORM da rede social
- `app/config.py` - configuracao da aplicacao
- `app/database.py` - engine e sessoes do banco
- `alembic/` - migrations versionadas

## Endpoints principais

- `GET /users`
- `GET /users/{user_id}`
- `POST /users`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`
- `POST /users/{user_id}/connections/{target_id}`
- `GET /users/{user_id}/connections`
- `GET /users/{user_id}/posts`
- `GET /posts`
- `GET /posts/{post_id}`
- `POST /posts`
- `PUT /posts/{post_id}`
- `DELETE /posts/{post_id}`
- `GET /posts/{post_id}/comments`
- `POST /posts/{post_id}/comments`
- `GET /posts/{post_id}/reposts`
- `POST /posts/{post_id}/reposts`

## Modelo de dominio

- `User` - perfis de usuario com biografia e nome de usuario
- `Post` - publicacoes com conteudo e referencias a repostagens
- `Comment` - comentarios ligados a publicacoes
- `Repost` - repostagens de publicacoes existentes
- `Connection` - conexoes entre usuarios

## Observacoes

Na Vercel, configure `DATABASE_URL` em `Project Settings > Environment Variables` e faca um novo deploy apos qualquer alteracao.
