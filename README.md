# Capstone-Project
RAG-Powered Enterprise Ticket Resolution System

AI-assisted IT ticket resolution system using Retrieval-Augmented Generation (RAG) and Large Language Models to provide context-aware support within enterprise ticketing workflows.

This project was developed as a Capstone Project for the B.Sc. Design and Computing program at Birla Institute of Technology and Science, Pilani, and implemented during industry work at HCL Technologies.

The system integrates Generative AI with traditional IT service management workflows to assist users and support agents in resolving technical issues efficiently.

Overview

Traditional IT ticketing systems rely heavily on manual effort from support engineers to interpret issues, search documentation, and provide resolutions. This project explores how Generative AI can assist in ticket resolution while maintaining human control over critical actions.

The system introduces an AI-powered conversational assistant integrated within the ticket lifecycle. Using Retrieval-Augmented Generation (RAG), the assistant retrieves relevant knowledge from a vector database and combines it with ticket context to generate accurate and contextual responses.

To ensure reliability in enterprise environments, the system follows a Human-in-the-Loop (HITL) design where AI can suggest actions but final decisions remain with the user.

Key Features
AI-Assisted Ticket Resolution

Conversational assistant integrated with IT ticket workflows

Context-aware responses based on ticket details and conversation history

Retrieval-Augmented Generation (RAG)

Semantic search over a vector knowledge base

Retrieval of relevant historical tickets and documentation

Grounded AI responses to reduce hallucination

Human-in-the-Loop AI

AI suggests ticket updates and resolution actions

Critical actions require explicit user confirmation

Stateful Conversations

Each ticket maintains a persistent conversational thread

Chat history stored and used for context-aware responses

Sentiment-Based Feedback

User messages analyzed using sentiment analysis

Feedback triggered when dissatisfaction is detected

Observability and Debugging

AI interactions traced using monitoring tools

Tool invocation and prompt behavior observable for debugging

System Architecture

The system follows a modular architecture consisting of:

Frontend

HTML

Tailwind CSS

JavaScript

Backend

FastAPI REST APIs

SQLModel ORM

PostgreSQL database

AI Layer

Large Language Model

LangChain / LangGraph orchestration

Retrieval-Augmented Generation pipeline

Data Layer

PostgreSQL for structured data

ChromaDB vector database for embeddings

Observability

LangSmith for tracing AI behavior

Technology Stack
Category	Technologies
Backend	FastAPI, SQLModel
Database	PostgreSQL
Vector Database	ChromaDB
AI Frameworks	LangChain, LangGraph
NLP	NLTK (VADER Sentiment Analysis)
Observability	LangSmith
Frontend	HTML, Tailwind CSS, JavaScript
RAG Pipeline

The Retrieval-Augmented Generation pipeline operates as follows:

User submits a message within a ticket conversation.

The system retrieves ticket context and chat history.

If additional knowledge is required, semantic retrieval is performed on the vector database.

Relevant knowledge is injected into the prompt.

The LLM generates a response grounded in ticket data and retrieved knowledge.

Suggested actions require explicit user confirmation before execution.

Project Structure

Example high-level structure:

project-root
│
├── backend
│   ├── api
│   ├── models
│   ├── services
│   └── chatbot_controller
│
├── rag_pipeline
│   ├── embeddings
│   ├── retrieval
│   └── prompt_construction
│
├── database
│   ├── models
│   └── migrations
│
├── frontend
│   ├── html
│   ├── css
│   └── js
│
└── README.md
Example Workflow

User creates an IT ticket.

The AI assistant becomes available within the ticket interface.

User asks questions or describes the issue.

The system retrieves relevant knowledge using RAG.

AI suggests solutions or troubleshooting steps.

If appropriate, AI suggests ticket status updates.

User confirms the action before it is executed.

Future Improvements

Possible enhancements include:

Integration with enterprise ticketing platforms (ServiceNow, Jira)

Improved retrieval ranking using advanced embeddings

Reinforcement learning from user feedback

Role-based access control and authentication

Deployment on cloud infrastructure

Author

Ashish Khanijo
B.Sc. Design and Computing
Birla Institute of Technology and Science, Pilani

Capstone Project
Industry Mentorship: HCL Technologies
