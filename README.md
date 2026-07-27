# AI Assistant Platform

An AI-powered assistant for **basic mathematics**, built with Python using a modular multi-agent architecture.

The platform uses a Large Language Model (LLM) only to understand the user's intent. All mathematical operations are executed by a deterministic engine built with Python, ensuring safe, predictable, and reproducible results.

---

# Overview

This project was developed as a software engineering portfolio project to demonstrate how AI applications can separate natural language understanding from business logic.

Instead of allowing the LLM to perform calculations, the system delegates each responsibility to a dedicated component:

- Understand the mathematical request
- Execute the calculation
- Generate a natural language response
- Maintain conversation context

This approach improves maintainability, testability, and security while keeping mathematical execution independent of the language model.

---

# Features

- Basic arithmetic operations
  - Addition
  - Subtraction
  - Multiplication
  - Division
- Parenthesized expressions
- Follow-up calculations using previous results
- Secure expression evaluation using Python AST
- Automatic language detection
- Multi-agent architecture
- Conversation memory
- Multiple LLM providers
  - OpenAI
  - Google Gemini
  - Ollama
- Streamlit web interface
- Dependency Injection
- Automated tests with Pytest
- Structured logging

---

# Example Conversation

```text
User: What is 8 + 4?
Assistant: The result is 12.

User: Multiply that by 3.
Assistant: The result is 36.

User: Divide by 6.
Assistant: The result is 6.
```

---

# Architecture

The application follows a modular architecture where every component has a single responsibility.

```text
                    User
                      │
                      ▼
              Streamlit Interface
                      │
                      ▼
             ChatbotOrchestrator
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 ContextResolver             Conversation Memory
        │
        ▼
 MathematicalAgent
        │
        ▼
 ExpressionEvaluator
        │
        ▼
      Python AST
        │
        ▼
    WriterAgent
        │
        ▼
      Response
```

## Components

| Component | Responsibility |
|-----------|----------------|
| **ChatbotOrchestrator** | Coordinates the execution flow. |
| **ContextResolver** | Interprets user requests and extracts mathematical expressions. |
| **MathematicalAgent** | Executes deterministic calculations. |
| **ExpressionEvaluator** | Safely evaluates expressions using Python AST. |
| **WriterAgent** | Generates responses in the user's language. |
| **ChatMemory** | Stores previous results for follow-up calculations. |
| **LLM Service** | Abstracts different language model providers. |

---

# Request Flow

Every request follows the same deterministic pipeline.

```text
User
  │
  ▼
Streamlit
  │
  ▼
Conversation Memory
  │
  ▼
ChatbotOrchestrator
  │
  ▼
ContextResolver
  │
  ▼
MathematicalAgent
  │
  ▼
ExpressionEvaluator
  │
  ▼
WriterAgent
  │
  ▼
Response
```

The LLM is responsible only for understanding the user's mathematical intent.

It never performs calculations.

---

# Supported Operations

The mathematical engine currently supports:

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Parentheses
- Operator precedence
- Multi-step calculations using previous results

Example:

```text
(5 + 3) * 2
```

---

# Project Structure

```text
ai_assistant_platform/
├── agents/
├── config/
├── core/
├── llm/
├── memory/
├── orchestrators/
├── prompts/
├── tools/
├── tests/
├── app.py
├── pyproject.toml
└── README.md
```

| Directory | Description |
|-----------|-------------|
| **agents** | Mathematical execution and response generation. |
| **core** | Context extraction and domain models. |
| **llm** | LLM abstraction layer and providers. |
| **memory** | Conversation history. |
| **orchestrators** | Coordinates the application flow. |
| **prompts** | Prompt templates. |
| **tools** | Mathematical evaluator and utilities. |
| **tests** | Unit and integration tests. |

---

# Design Principles

The project follows modern software engineering practices:

- SOLID
- Clean Architecture
- Dependency Injection
- Separation of Concerns
- Deterministic Business Logic
- Low Coupling
- High Cohesion

---

# Quick Start

## Clone the repository

```bash
git clone https://github.com/your-username/ai_assistant_platform.git

cd ai_assistant_platform
```

## Install dependencies

```bash
poetry install
```

## Configure the environment

```bash
cp .env.example .env
```

Configure your preferred LLM provider in the `.env` file.

## Run the application

```bash
poetry run streamlit run app.py
```

---

# Testing

Run all tests:

```bash
poetry run pytest
```

Run unit tests:

```bash
poetry run pytest tests/unit
```

Run integration tests:

```bash
poetry run pytest tests/integration
```

Generate coverage:

```bash
poetry run pytest --cov=ai_assistant_platform
```

---

# Roadmap

## Completed

- Multi-agent architecture
- Secure AST evaluator
- Conversation memory
- Multiple LLM providers
- Streamlit interface
- Automated test suite

## Planned

- Exponentiation
- Square roots
- Percentages
- Scientific calculator functions
- REST API
- Docker support
- CI/CD

---

# Contributing

Contributions are welcome.

Before opening a Pull Request, run:

```bash
poetry run ruff check .
poetry run ruff format .
poetry run pytest
```

Please follow:

- Conventional Commits
- PEP 8
- Static typing
- Automated tests for new features

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---

# Acknowledgements

Built with:

- Python
- Streamlit
- OpenAI
- Google Gemini
- Ollama
- Poetry
- Pytest
- Ruff

---

# Author

**Ladson Sá**

Software Engineering student and backend developer passionate about software architecture, Python, AI, and backend engineering.

- GitHub: https://github.com/ladsonsa
- LinkedIn: https://www.linkedin.com/in/ladsonsa

---

If you found this project interesting, consider giving it a ⭐ on GitHub.
