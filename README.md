# AI Assistant Platform

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.59.2-FF4B4B?logo=streamlit&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-2.x-60A5FA?logo=poetry&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Tested-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An AI-powered mathematical assistant built as a modular application, with a clear separation between natural-language understanding and deterministic mathematical execution.

The platform combines Python, FastAPI, Streamlit, Next.js, TypeScript, and LLM integrations to support conversational mathematical interactions, contextual follow-up questions, and structured API access.

> **Current status:** Generation 2 · Backend `1.1.0`

---

## Overview

The project focuses on software engineering practices around AI integration, backend architecture, deterministic business logic, API design, and conversational context.

A core design principle is to keep probabilistic language understanding separate from deterministic computation:

```text
Natural Language
       ↓
LLM Interpretation
       ↓
Mathematical Intent
       ↓
Deterministic Evaluation
       ↓
Mathematical Result
       ↓
Natural Language Response
```

The LLM interprets the user's request, while the application remains responsible for the actual mathematical computation.

---

## Architecture

The current implementation is **Generation 2**.

Generation 2 expands the original Streamlit-centered application with a FastAPI backend and a dedicated Next.js / TypeScript frontend, while retaining Streamlit as an existing interface.

### HTTP Application Flow

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

### Streamlit Application Flow

```text
User
  ↓
Streamlit
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

The two interfaces currently have different entry paths. The FastAPI `/chat` flow uses the application-layer `ChatService`, while the Streamlit entry point continues to interact directly with the `ChatbotOrchestrator`.

This reflects the current implementation without presenting the architecture as more unified than it is.

---

## Key Engineering Decisions

### Deterministic Mathematical Execution

Mathematical expressions are evaluated by the application's deterministic evaluator rather than relying on an LLM to produce the numerical result.

```text
User Request
     ↓
LLM Interpretation
     ↓
Mathematical Expression
     ↓
ExpressionEvaluator
     ↓
Deterministic Result
     ↓
WriterAgent
     ↓
Final Response
```

This keeps numerical computation predictable and testable.

### Application Layer

`ChatService` provides the application-level entry point for the FastAPI `/chat` use case.

The API layer therefore remains focused on HTTP concerns while application orchestration stays outside the router.

### Dependency Injection

Dependencies are explicitly constructed and injected at the application boundaries, reducing direct coupling between components.

### Structured API Contracts

Pydantic schemas define explicit request and response contracts for the HTTP API.

### Conversational Context

Conversation history and message metadata are preserved so that follow-up mathematical requests can use previous results as context.

---

## Capabilities

The current application supports:

- Conversational mathematical interactions
- Context-aware follow-up questions
- Addition
- Subtraction
- Multiplication
- Division
- Parenthesized expressions
- Operator precedence
- Follow-up calculations using previous results
- LLM-assisted intent interpretation
- Deterministic mathematical evaluation
- Multiple LLM providers
- Structured API contracts
- Conversation history and metadata preservation

---

## LLM Providers

The backend currently integrates with:

- OpenAI
- Google Gemini
- Ollama

Provider credentials and model configuration are supplied through the application environment.

---

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python 3.14+ |
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| Validation | Pydantic |
| Package Management | Poetry |
| Interactive Interface | Streamlit |
| Frontend | Next.js / TypeScript |
| LLM Providers | OpenAI, Google Gemini, Ollama |
| Testing | Pytest |
| Linting | Ruff |
| Formatting | Black |
| Containerization | Docker / Docker Compose |

---

## API

### `POST /chat`

Processes a conversational request through the backend application pipeline.

The endpoint uses explicit Pydantic contracts:

- `ChatMessageSchema`
- `ChatRequestSchema`
- `ChatResponseSchema`

A request contains conversation history, including message content and metadata.

A response contains the generated content and associated metadata.

For mathematical interactions, the API can expose the calculated result through the `math_result` metadata field.

Internal orchestration state such as `last_math_result` is used for contextual processing and is not part of the external API contract.

### Interactive Documentation

When the API is running, FastAPI provides interactive documentation at:

```text
http://localhost:8000/docs
```

---

## Getting Started

### Prerequisites

- Python 3.14+
- Poetry
- Docker
- Docker Compose

### Install Dependencies

```bash
poetry install
```

Run commands inside the Poetry environment with:

```bash
poetry run <command>
```

### Configuration

Create the local environment file from:

```text
.env.example
```

Configure the variables required by the selected provider and application environment.

Never commit credentials or other secrets to the repository.

### Run Streamlit

```bash
poetry run streamlit run app.py
```

### Run FastAPI

```bash
poetry run uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

---

## Docker

The project includes Docker Compose configuration for the Generation 2 environment.

Start the configured environment with:

```bash
docker compose up --build
```

The environment includes the backend and Next.js frontend.

| Service | Port |
| --- | --- |
| Backend | `8000` |
| Frontend | `3000` |

The frontend communicates with the backend through:

```text
NEXT_PUBLIC_API_URL
```

---

## Testing and CI

The project uses Pytest for automated testing.

Run the test suite with:

```bash
poetry run pytest
```

The backend CI pipeline validates pull requests through:

1. Dependency installation
2. Ruff
3. Black
4. Pytest

This provides automated validation for code quality, formatting, and tests.

---

## Project Evolution

The AI Assistant Platform evolved through two architectural generations.

### Generation 1 — Conversational Foundation

Generation 1 established the project as a Streamlit-centered AI mathematical assistant.

The main focus was building the conversational experience and the foundations for:

- Natural-language mathematical requests
- Conversational context
- Deterministic expression evaluation
- LLM-assisted interpretation and response generation
- Multiple LLM providers
- Modular components and dependency injection
- Automated testing

The processing flow was centered around the `ChatbotOrchestrator`.

### Generation 2 — API-Oriented Platform

Generation 2 introduced an explicit FastAPI backend and a Next.js / TypeScript frontend while preserving Streamlit as an existing interface.

The main architectural evolution was the introduction of a clear application layer through `ChatService` and an explicit HTTP contract around the `/chat` endpoint.

This transition moves the project from a primarily UI-centered application toward a platform that can support multiple interfaces while keeping core application responsibilities separated.

> **Generation 2 is an architectural stage, not backend version `2.0.0`.**

### Current State

The project is currently in **Generation 2**, and the backend follows independent Semantic Versioning with the current release at **`1.1.0`**.

### Future Direction — Generation 3

Generation 3 is a future architectural direction and is **not part of the current implementation**.

The intended direction is a more backend-centered architecture based on FastAPI, with Streamlit eventually removed from the target application architecture.

This transition is intentionally deferred until the Generation 2 architecture is sufficiently consolidated.

---

## Versioning

The backend follows **Semantic Versioning (SemVer)** independently from the frontend.

Current backend version:

```text
1.1.0
```

Generation labels and release versions have different meanings:

| Concept | Meaning |
| --- | --- |
| Generation 1 | Initial architectural stage |
| Generation 2 | Current architectural stage |
| `1.1.0` | Current backend release |
| `2.0.0` | Not implied by Generation 2 |

---

## Current Scope

The current implementation is **Generation 2** and focuses on:

- Conversational mathematical interaction
- Deterministic mathematical execution
- Contextual follow-up interactions
- FastAPI `/chat` API
- Streamlit interface
- Next.js / TypeScript frontend
- Structured request/response schemas
- Modular application components
- LLM provider integration
- Automated testing and CI
- Docker-based execution

---

## Out of Scope

The following are outside the current Generation 2 implementation:

- Generation 3 implementation
- Replacing Generation 2 with the future architecture
- Removing Streamlit from the current Generation 2 environment
- Moving deterministic mathematical computation to the frontend
- Delegating mathematical execution entirely to an LLM

---

## License

This project is licensed under the **MIT License**.

See `LICENSE` for the complete license text.

---

## Author

**Ladson Sá**

Software Engineering student and backend developer focused on software architecture, Python, AI, and backend engineering.
