# uni4life-api-v2

Exemplo de API Python usando FastAPI para uma rede social simples.

## Como executar

### Usando Docker

1. Construa a imagem:
   ```bash
   docker build -t uni4life-api .
   ```
2. Execute o container:
   ```bash
   docker run -p 8000:8000 uni4life-api
   ```

### Usando Docker Compose

1. Inicie o serviço:
   ```bash
   docker compose up --build
   ```
2. Acesse a API em `http://127.0.0.1:8000`

### Alternativa local sem Docker

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
   ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicie a API:
   ```bash
   uvicorn app.main:app --reload
   ```

## Estrutura

- `app/main.py` - ponto de entrada da aplicação
- `app/routes.py` - definição de rotas HTTP
- `app/services.py` - lógica de negócio
- `app/repositories.py` - armazenamento em memória e manipulação de dados
- `app/schemas.py` - validação de payloads e modelos de resposta
- `app/models.py` - modelos de domínio da rede social
- `app/config.py` - configuração da aplicação

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

## Modelo de domínio

- `User` - perfis de usuário com biografia e nome de usuário
- `Post` - publicações com conteúdo e referências a repostagens
- `Comment` - comentários ligados a publicações
- `Repost` - repostagens de publicações existentes
- `Connection` - conexões entre usuários

## Observações

Essa implementação usa armazenamento em memória para exemplificar os padrões de projeto. Em produção, você pode substituir `app/repositories.py` por repositórios que usam banco de dados relacional, NoSQL ou ORM.
