# AI Assistant Platform

> A production-oriented AI assistant platform that combines deterministic computation, agent orchestration, and Large Language Models (LLMs) using modern Python software engineering practices.

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python)
![Poetry](https://img.shields.io/badge/Poetry-Dependency%20Management-60A5FA?logo=poetry)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit)
![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-0A9EDC?logo=pytest)
![License](https://img.shields.io/badge/license-MIT-green)

---

# Overview

AI Assistant Platform is an educational project designed to simulate the architecture of modern AI assistants.

Instead of allowing the language model to perform every task, the system separates responsibilities between specialized agents and deterministic tools.

This architecture improves:

- Reliability
- Testability
- Maintainability
- Scalability
- Security

The project demonstrates software engineering concepts commonly used in production AI systems.

---

# Key Features

- Agent-based architecture
- Deterministic mathematical engine
- Secure AST expression evaluator
- Context-aware conversations
- Multi-provider LLM support
- Provider abstraction layer
- Conversational memory
- Prompt engineering
- Guardrails
- Streamlit interface
- Modular architecture
- Production-oriented design

---

# Architecture

```text
                    User
                      │
                      ▼
             Streamlit Interface
                      │
                      ▼
          Chatbot Orchestrator
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Chat Memory          Context Resolver
                                  │
                                  ▼
                      Mathematical Agent
                                  │
                                  ▼
                      Expression Evaluator
                                  │
                                  ▼
                           Math Result
                                  │
                                  ▼
                           Writer Agent
                                  │
                                  ▼
                            LLM Service
                                  │
                                  ▼
                         Provider Factory
                                  │
                 ┌────────────────┼────────────────┐
                 ▼                ▼                ▼
              OpenAI          Google Gemini      Ollama
```

---

# Core Design Principles

The project follows a deterministic execution model.

The language model is responsible for:

- Intent interpretation
- Language detection
- Human-friendly responses

The application is responsible for:

- Mathematical execution
- State management
- Business rules
- Flow orchestration

Mathematical operations are **never executed by the LLM**.

Expressions are evaluated locally using Python's Abstract Syntax Tree (AST), providing deterministic and secure execution.

---

# Current Features

## Mathematical Assistant

Supported operations:

- Addition
- Subtraction
- Multiplication
- Division
- Parenthesized expressions
- Unary operators
- Operator precedence

---

## Context Resolution

The Context Resolver transforms natural language into structured mathematical context before execution.

Responsibilities include:

- Direct expression extraction
- Intent classification
- Previous result detection
- Language normalization
- LLM fallback

---

## Writer Agent

The Writer Agent converts deterministic results into natural language while preserving the user's language.

Example:

User:

```text
What is 15 × 8?
```

Response:

```text
The result is 120.
```

---

## Multi-provider Support

Supported providers:

- OpenAI
- Google Gemini
- Ollama

Changing providers requires only configuration changes.

---

## Conversational Memory

Conversation history is preserved during the session, allowing follow-up requests such as:

```text
What is 5 + 4?

Now subtract 2.

Multiply the result by 8.
```

---

# Technologies

| Category | Technology |
|-----------|------------|
| Language | Python |
| Package Manager | Poetry |
| Frontend | Streamlit |
| Testing | Pytest |
| Code Quality | Ruff |
| LLM | OpenAI SDK |
| Providers | OpenAI • Gemini • Ollama |
| Parsing | Python AST |
| Architecture | Multi-Agent |
| State | Streamlit Session State |

---

# Software Engineering Concepts

This project demonstrates:

- SOLID Principles
- DRY Principle
- Separation of Concerns
- Layered Architecture
- Dependency Injection
- Factory Pattern
- Provider Abstraction
- Agent Orchestration
- Tool Calling
- Prompt Engineering
- Guardrails
- Conversational Memory
- Modular Design
- Exception Handling
- Static Typing
- Unit Testing

---

# Project Structure

```text
ai_assistant_platform/
│
├── agents/
│   ├── mathematical_agent.py
│   └── writer_agent.py
│
├── core/
│   ├── context_resolver.py
│   └── math_context.py
│
├── llm/
│   ├── llm_service.py
│   ├── provider_factory.py
│   └── providers/
│
├── memory/
│
├── orchestrators/
│
├── prompts/
│
├── tools/
│   ├── expression_evaluator.py
│   └── math_operations.py
│
├── tests/
│
├── app.py
│
└── pyproject.toml
```

---

# Running the Project

Clone the repository:

```bash
git clone https://github.com/your-user/ai_assistant_platform.git

cd ai_assistant_platform
```

Install dependencies:

```bash
poetry install
```

Configure environment variables:

```env
OPENAI_API_KEY=your_api_key

LLM_PROVIDER=openai

MODEL_NAME=gpt-4o-mini
```

Run the application:

```bash
poetry run streamlit run app.py
```

---

# Running Tests

Execute the unit tests:

```bash
poetry run pytest
```

Generate a coverage report:

```bash
poetry run pytest --cov
```

---

# Roadmap

## Completed

- Agent-based architecture
- Mathematical Agent
- Writer Agent
- Context Resolver
- Secure AST evaluator
- Multi-provider support
- Prompt engineering
- Conversational memory
- Streamlit interface
- Poetry migration

## In Progress

- Task 12
- Test suite stabilization
- Context resolution improvements
- Architecture refactoring

## Planned

- Web Search Agent
- SQL Agent
- RAG Pipeline
- Persistent Memory
- Docker
- GitHub Actions
- REST API
- MCP Integration

---

# Why This Project?

Modern AI systems should not rely exclusively on LLM reasoning.

This project follows a hybrid approach:

- LLMs interpret language.
- Deterministic tools execute logic.

This separation improves correctness, security, and maintainability while keeping the architecture modular and easy to extend.

---

# Future Architecture

After the current test suite is stabilized, the architecture will evolve toward a more decoupled design through dependency injection and smaller specialized services, improving maintainability and adherence to SOLID principles.

---

# Author

Developed as a practical AI Engineering project focused on modern agent architectures, deterministic execution, and production-oriented Python software design.