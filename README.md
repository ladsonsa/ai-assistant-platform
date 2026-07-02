# AI Assistant Platform

An agent-based AI assistant platform built with modern software engineering practices, deterministic tools, conversational memory, and modular architecture.

This project demonstrates how specialized AI agents can collaborate through an orchestration layer while maintaining clear responsibility boundaries and production-ready design principles.

---

## Highlights

* Multi-agent architecture
* Deterministic mathematical tools
* LLM provider abstraction layer
* Conversational memory
* Streamlit chat interface
* Modular and scalable design
* Production-oriented software architecture
* Testable and extensible components

---

## Demo Architecture

```text
User
 │
 ▼
Streamlit Chat Interface
 │
 ▼
Chatbot Orchestrator
 │
 ├── Mathematical Agent
 │        │
 │        ▼
 │   Math Tools
 │
 └── Writer Agent
          │
          ▼
     LLM Service
          │
          ▼
    Provider Factory
          │
 ┌────────┼────────┐
 ▼        ▼        ▼
OpenAI  Gemini   Ollama
```

---

## Project Goal

The objective of this project is to explore concepts commonly found in modern AI systems and production environments, including:

* Agent orchestration
* Tool calling
* Prompt engineering
* Conversational memory
* Dependency injection
* Provider abstraction
* Software modularization
* AI guardrails

Rather than relying entirely on LLM reasoning, the application combines deterministic computation with natural language generation to improve reliability and maintainability.

---

## Features

### Mathematical Assistant

Supported operations:

* Addition
* Subtraction
* Multiplication
* Division

Unlike traditional chatbots, calculations are never performed by the LLM.

All operations are executed through deterministic Python tools, guaranteeing consistent and accurate results.

---

### Human-Friendly Responses

A dedicated Writer Agent transforms raw numerical results into conversational responses while:

* preserving the user's language;
* improving readability;
* maintaining a professional tone.

---

### Multi-Provider LLM Support

The platform was designed to support multiple providers through an abstraction layer.

Currently supported:

* OpenAI
* Google Gemini
* Ollama

Switching providers requires only configuration changes.

---

### Conversational Memory

The application preserves conversation history during the session, enabling contextual interactions and follow-up questions.

---

## Technologies

| Category         | Technology                            |
| ---------------- | ------------------------------------- |
| Language         | Python                                |
| Frontend         | Streamlit                             |
| LLM Integration  | OpenAI SDK                            |
| Testing          | Pytest                                |
| Architecture     | Multi-Agent                           |
| Patterns         | Factory, Dependency Injection, Router |
| State Management | Streamlit Session State               |

---

## Engineering Concepts Demonstrated

This repository intentionally showcases concepts expected in modern AI engineering roles:

* Clean Architecture
* Separation of Concerns
* Dependency Injection
* Factory Pattern
* Router Pattern
* Agent Orchestration
* Tool Calling
* Prompt Engineering
* Guardrails
* Conversational Memory
* Modular Design
* Exception Handling
* Unit Testing

---

## Project Structure

```text
ai_assistant_platform/
│
├── agents/
│   ├── mathematical_agent.py
│   └── writer_agent.py
│
├── orchestrators/
│   └── chatbot_orchestrator.py
│
├── tools/
│   └── math_operations.py
│
├── llm/
│   ├── llm_service.py
│   ├── provider_factory.py
│   └── providers/
│
├── memory/
│   └── chat_memory.py
│
├── config/
│   └── settings.py
│
├── tests/
│
└── app.py
```

---

## Example Workflow

**Entrada do usuário **

```text
What is 15 multiplied by 8?
```

**Fluxo de Execução **

```text
User
→ Orchestrator
→ Mathematical Agent
→ Mathematical Tool
→ Writer Agent
→ User
```

**Resposta **

```text
The result of 15 multiplied by 8 is 120.
```

---

## Por que este projeto é importante 

Most AI applications today rely heavily on LLM reasoning for every task.

This project demonstrates an alternative and increasingly adopted approach:

> Use LLMs for communication and reasoning, and deterministic tools for execution.

This architecture improves:

* reliability;
* testability;
* scalability;
* maintainability;
* operational costs.

The same principle is widely used in modern AI assistants and agentic systems.

---

## Running Locally

Clone the repository:

```bash
git clone <repository-url>
cd ai_assistant_platform
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```env
OPENAI_API_KEY=your_api_key
MODEL_NAME=gpt-4o-mini
LLM_PROVIDER=openai
```

Start the application:

```bash
streamlit run app.py
```

---

## Future Improvements

Planned extensions include:

* Web Search Agent
* Code Generation Agent
* SQL Agent
* RAG Pipeline
* Vector Database Integration
* Persistent Memory
* Docker Deployment
* CI/CD Pipelines

---

## Author

Developed as a practical study project focused on AI Engineering, Agent Architectures, and Production-Oriented Software Design.
