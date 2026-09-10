# AI Assistant Platform

[![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Poetry](https://img.shields.io/badge/Poetry-2.x-60A5FA?logo=poetry&logoColor=white)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modular AI-powered mathematical assistant built with **Python, FastAPI, Streamlit, and LLM-based natural language processing**.

The platform combines conversational context with deterministic mathematical execution: the LLM is responsible for understanding the user's intent, while mathematical expressions are evaluated deterministically by the application.

---

## About the Project

**AI Assistant Platform** is a conversational assistant focused on mathematical reasoning and contextual interactions.

The current implementation represents **Generation 2**, combining:

* **FastAPI** as the HTTP API layer
* **Streamlit** as the interactive application interface
* **LLM services** for natural-language understanding and response generation
* **Deterministic mathematical evaluation** for numerical expressions
* **Conversation context resolution** for follow-up questions
* **Dependency injection** for application components

The architecture separates natural-language interpretation from deterministic computation, avoiding the use of the LLM as the mathematical execution engine.

---

## Highlights

* Conversational mathematical assistant
* Context-aware follow-up questions
* Deterministic mathematical expression evaluation
* LLM-assisted intent interpretation
* Structured API request and response schemas
* Conversation history and metadata preservation
* FastAPI HTTP interface
* Streamlit interactive interface
* Dependency injection across the API/application flow
* Automated test suite
* Docker-based development environment

---

## Tech Stack

| Area                   | Technology                         |
| ---------------------- | ---------------------------------- |
| Language               | Python 3.14                        |
| API                    | FastAPI                            |
| ASGI Server            | Uvicorn                            |
| Validation             | Pydantic                           |
| Package Management     | Poetry                             |
| Interactive UI         | Streamlit                          |
| LLM Integration        | LLM Service abstraction            |
| Mathematical Execution | Deterministic Expression Evaluator |
| Testing                | Pytest                             |
| Containerization       | Docker / Docker Compose            |

---

# Generation 2 Architecture

The current architecture has two application entry points.

### FastAPI

The HTTP API follows:

```text
Client
  ↓
FastAPI Router
  ↓
ChatService
  ↓
ChatbotOrchestrator
  ↓
ContextResolver
  ↓
MathematicalAgent
  ↓
ExpressionEvaluator
  ↓
WriterAgent
  ↓
Response
```

The **ChatService** is the application-layer entry point for the `/chat` HTTP endpoint.

The router is intentionally kept thin and delegates application behavior to the service layer.

### Streamlit

The Streamlit application currently follows:

```text
User
  ↓
Streamlit Interface
  ↓
ChatbotOrchestrator
  ↓
ContextResolver
  ↓
MathematicalAgent
  ↓
ExpressionEvaluator
  ↓
WriterAgent
  ↓
Response
```

The two entry points therefore share the core orchestration components while exposing different interfaces.

---

## Application Flow

For an HTTP request, the main processing flow is:

```text
HTTP Request
    ↓
ChatRequestSchema
    ↓
Chat Router
    ↓
ChatService
    ↓
ChatbotOrchestrator
    ↓
ContextResolver
    ↓
MathematicalAgent
    ↓
ExpressionEvaluator
    ↓
WriterAgent
    ↓
ChatResponseMapper
    ↓
ChatResponseSchema
    ↓
HTTP Response
```

### Responsibilities

| Component           | Responsibility                                                     |
| ------------------- | ------------------------------------------------------------------ |
| FastAPI Router      | HTTP routing and dependency injection                              |
| ChatService         | Application-layer entry point for `/chat`                          |
| ChatbotOrchestrator | Coordinates the conversational processing pipeline                 |
| ContextResolver     | Resolves conversational context and mathematical references        |
| MathematicalAgent   | Interprets mathematical intent and prepares mathematical execution |
| ExpressionEvaluator | Performs deterministic mathematical evaluation                     |
| WriterAgent         | Generates the final natural-language response                      |
| ChatResponseMapper  | Converts application output into the API response schema           |

---

# Deterministic Mathematical Execution

A core architectural principle of the platform is the separation between **language understanding** and **mathematical execution**.

The LLM may be used to interpret the user's request, but deterministic mathematical operations are handled by the application's expression evaluator.

Conceptually:

```text
Natural Language
      ↓
LLM / Intent Interpretation
      ↓
Mathematical Context
      ↓
Deterministic Expression Evaluation
      ↓
Mathematical Result
      ↓
Natural Language Response
```

This prevents the LLM from being treated as the source of truth for deterministic numerical calculations.

---

# Conversation Context

The platform supports conversational mathematical interactions by preserving conversation history and metadata.

For example, a mathematical result can be stored in response metadata and subsequently used by the context resolution layer when processing a follow-up request.

The external response uses:

```text
math_result
```

for mathematical result metadata.

The orchestration layer may also maintain internal contextual state such as:

```text
last_math_result
```

for resolving references to previous calculations.

Internal context handling is not exposed as an API field.

---

# API

## POST `/chat`

Processes a conversational request through the application pipeline.

### Request

The endpoint receives a `ChatRequestSchema` containing the conversation history.

Conceptually:

```json
{
  "history": [
    {
      "role": "user",
      "content": "What is 25 * 4?",
      "metadata": {}
    }
  ]
}
```

### Response

The endpoint returns a `ChatResponseSchema` containing the generated response and associated metadata.

Conceptually:

```json
{
  "content": "The result is 100.",
  "metadata": {
    "math_result": 100,
    "expression": "25 * 4",
    "language": "en"
  }
}
```

### Official Schemas

The API uses the following schemas:

* `ChatMessageSchema`
* `ChatRequestSchema`
* `ChatResponseSchema`

`ChatMessageSchema` represents an individual conversation message and supports message metadata.

`ChatRequestSchema` contains the conversation history.

`ChatResponseSchema` represents the final API response and its metadata.

---

# Project Structure

```text
ai-assistant-platform/
│
├── ai_assistant_platform/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── routers/
│   │   │   └── chat.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── chat_message.py
│   │       ├── chat_request.py
│   │       └── chat_response.py
│   │
│   ├── agents/
│   │   ├── mathematical_agent.py
│   │   └── writer_agent.py
│   │
│   ├── context/
│   │   └── context_resolver.py
│   │
│   ├── services/
│   │   └── chat_service.py
│   │
│   └── ...
│
├── tests/
│
├── app.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

# Configuration

Environment-specific configuration is provided through environment variables.

The project includes an example environment file:

```text
.env.exemple
```

Create the local environment configuration according to the variables required by the configured LLM service and application environment.

Secrets should not be committed to the repository.

---

# Getting Started

## Prerequisites

Make sure the following tools are available:

* Python 3.14
* Poetry
* Docker
* Docker Compose

---

## Installation

Install the project dependencies with Poetry:

```bash
poetry install
```

Activate the Poetry environment or execute commands through Poetry:

```bash
poetry shell
```

or:

```bash
poetry run <command>
```

---

# Running the Application

## Streamlit

The Streamlit interface is started through:

```bash
streamlit run app.py
```

The application provides an interactive conversational interface.

---

## FastAPI

Start the API with Uvicorn:

```bash
uvicorn main:app --reload
```

The API is exposed on the configured host and port.

The default development configuration uses:

```text
http://localhost:8000
```

---

# API Documentation

FastAPI automatically provides interactive API documentation.

When the API is running, the documentation is available at:

```text
http://localhost:8000/docs
```

The OpenAPI schema is also exposed by FastAPI.

---

# Docker

The project includes Docker support for the development environment.

Build and start the services with:

```bash
docker compose up --build
```

The current Compose configuration includes:

* Backend — FastAPI
* Frontend — Next.js / TypeScript

The backend is exposed on port:

```text
8000
```

The frontend is configured to communicate with the backend through:

```text
NEXT_PUBLIC_API_URL
```

---

# Testing

The project uses **Pytest** for automated testing.

Run the test suite with:

```bash
pytest
```

The test suite covers the implemented application behavior and architectural flows.

---

# Engineering Practices

The project follows several architectural principles:

### Separation of Responsibilities

HTTP concerns, application orchestration, context resolution, mathematical execution, and response generation are separated into dedicated components.

### Dependency Injection

Application dependencies are provided through explicit dependency construction rather than coupling the HTTP layer directly to concrete orchestration behavior.

### Thin API Layer

The FastAPI router is responsible for HTTP concerns and delegates application processing to `ChatService`.

### Deterministic Computation

Mathematical expressions are evaluated by the deterministic expression evaluator rather than relying on LLM-generated numerical results.

### Structured Contracts

Pydantic schemas define the API request and response contracts.

### Context Preservation

Conversation history and message metadata are preserved across the application flow to support contextual interactions.

---

# Current Scope

The current implementation is **Generation 2: Streamlit + FastAPI**.

The project currently focuses on:

* conversational interaction
* mathematical intent interpretation
* deterministic mathematical execution
* contextual follow-up interactions
* FastAPI `/chat` API
* Streamlit interface
* structured request/response schemas
* modular application components
* automated testing
* Docker-based execution

---

# Out of Scope

The following does not belong to the current Generation 2 implementation:

* replacing Streamlit with a FastAPI-only application
* removing the Streamlit interface
* introducing a new application generation
* moving deterministic mathematical computation to the frontend
* delegating mathematical execution entirely to an LLM

The current architecture intentionally preserves **Streamlit + FastAPI** as the Generation 2 application model.

---

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for the complete license text.
