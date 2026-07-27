# AI Assistant Platform

A modular AI-powered mathematical assistant built with Python and Streamlit. The project separates intent interpretation, mathematical execution, and response generation into specialized components, following clean software engineering practices.

## Overview

AI Assistant Platform is a portfolio project focused on building a mathematical chatbot with:

* conversation memory
* contextual follow-up support
* multilingual responses
* deterministic mathematical execution
* LLM-based intent interpretation only

The LLM is used to understand the user request and generate the final response text. Mathematical calculations are always executed locally through the application logic.

## Features

* Basic arithmetic operations: addition, subtraction, multiplication, and division
* Parentheses and operator precedence support
* Follow-up calculations using previous results
* Conversation memory with mathematical context
* Multilingual responses
* Multiple LLM providers:

  * OpenAI
  * Google Gemini
  * Ollama
* Secure expression evaluation using Python AST
* Prompt engineering and guardrails
* Automated tests with Pytest
* Streamlit-based user interface

## Architecture

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

### Responsibilities

* **ChatbotOrchestrator**: coordinates the execution flow.
* **ContextResolver**: interprets the user message and extracts mathematical context.
* **MathematicalAgent**: executes validated expressions.
* **ExpressionEvaluator**: safely evaluates arithmetic expressions using AST.
* **WriterAgent**: generates the final response in the user's language.
* **Chat Memory**: stores conversation history and previous mathematical results.
* **LLM Service**: abstracts the configured LLM provider.

## Project Structure

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
└── app.py

tests/
└── ...
```

## Tech Stack

* Python 3.14+
* Streamlit
* Pytest
* Poetry
* OpenAI SDK
* Google Gemini
* Ollama

## Setup

```bash
git clone https://github.com/ladsonsa/ai_assistant_platform.git
cd ai_assistant_platform
poetry install
```

Create a `.env` file with the provider keys and model settings before running the app.

## Usage

Start the application with Streamlit:

```bash
poetry run streamlit run app.py
```

## Testing

Run the complete test suite:

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

**Ladson Sá**
Software Engineering student and backend developer focused on clean, maintainable, and scalable software.
