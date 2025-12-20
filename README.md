# RAG System - Retrieval-Augmented Generation

A production-ready RAG (Retrieval-Augmented Generation) system built with Clean Architecture principles, designed to enable intelligent document search and conversational Q&A capabilities.

## Architecture

This project follows **Clean Architecture** with clear separation of concerns:

```
app/
├── domain/              # Business entities and core logic
│   └── entities/        # Document, Conversation, ChatMessage, Embedding
├── application/         # Use cases and business rules
│   ├── interfaces/      # Abstract interfaces (repositories, services)
│   ├── services/        # Business logic (DocumentService, ChatService)
│   └── dtos/           # Data Transfer Objects
└── infrastructure/      # External adapters and implementations
    ├── database/        # SQLAlchemy models and session management
    ├── repositories/    # Database repository implementations
    ├── llm/            # LLM adapters (OpenAI, SentenceTransformers)
    └── vector_stores/  # Vector database adapters (Pinecone)
```

### Key Design Principles

- **SOLID Principles**: Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion
- **Dependency Injection**: All dependencies are injected through interfaces
- **Repository Pattern**: Abstract data access layer for flexibility
- **Clean Architecture**: Business logic independent of frameworks and external systems

**Database Design:** [View ERD on DrawSQL](https://drawsql.app/teams/mahmuuudtolba/diagrams/rag)

## Technologies Used

### Core Framework

- **Python 3.10+** - Primary language
- **SQLAlchemy (Async)** - ORM with async support
- **PostgreSQL** - Primary database
- **Alembic** - Database migrations

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd RAG-system
   ```

2. **Set up Python environment**

   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   uv pip install -e .
   ```

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

4. **Start the database**

   ```bash
   docker run -d -p 5432:5432 \
       -e POSTGRES_USER=root \
       -e POSTGRES_PASSWORD=password \
       -e POSTGRES_DB=rag \
       -e PGDATA=/var/lib/postgresql/data \
       -v "$(pwd)"/dbstorage:/var/lib/postgresql/data \
       postgres:latest
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

## Project Structure

```
RAG-system/
├── app/
│   ├── domain/
│   │   └── entities/              # Core business entities
│   ├── application/
│   │   ├── interfaces/            # Abstract interfaces
│   │   ├── services/              # Business logic
│   │   └── dtos/                  # Data Transfer Objects
│   └── infrastructure/
│       ├── database/              # Database models & session
│       ├── repositories/          # Repository implementations
│       ├── llm/                   # LLM adapters
│       └── vector_stores/         # Vector DB adapters
├── alembic/
│   └── versions/                  # Database migrations
├── notebooks/                     # Jupyter notebooks for experimentation
├── pyproject.toml                 # Project dependencies
└── alembic.ini                    # Alembic configuration
```

### Phase 3: REST API Development (PLANNED)

**Objectives:**

- Build FastAPI application with RESTful endpoints
- Implement document upload and search endpoints
- Create chat/Q&A endpoints with streaming support
- Add conversation management endpoints
- Configure CORS and middleware
- Generate OpenAPI documentation

### Phase 4: Authentication & Authorization (PLANNED)

**Objectives:**

- Implement user authentication system
- Add JWT token-based authentication
- Create user registration and login endpoints
- Build authorization middleware
- Implement role-based access control

### Phase 5: Testing Infrastructure (PLANNED)

**Objectives:**

- Set up comprehensive testing framework
- Write unit tests for domain entities
- Create integration tests for repositories and APIs
- Build end-to-end RAG pipeline tests
- Set up CI/CD pipeline
- Achieve 80%+ code coverage
