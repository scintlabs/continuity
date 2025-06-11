# Continuity

A reactive memory layer for LLM-driven agents that gives each call a rich, human-like “memory” context.

## Features

- [ ] **Cached Context Object**: Retrieves a ready-to-use `Context` (Preferences, Related Threads, Current Thread) from a Redict for ultra-low latency.
- [ ] **Chronological History**: Every message or event is stored in Postgres with timestamps, speaker metadata, and raw text.
- [ ] **Threaded Organization**: Events are grouped into semantically and temporally coherent Thread objects.
- [ ] **Preferences Extraction**: Contextually derived user preferences (language, style, habits) are updated only when needed.
- [ ] **Adaptive Context Sizing**: Token-budgeted: each section shrinks or expands via summarization triggers to keep context sharp.
- [ ] **Related-Threads**: Qdrant-backed semantic search finds threads “like this one,” returns their summaries + IDs for on-demand expansion.

## Memory Management Strategies

- [ ] **Hierarchical Summaries**: Aggregate older messages into parent summaries to keep deep history available at a glance.
- [ ] **Hybrid Retrieval**: Combine vector similarity with timestamp filters or metadata conditions in Postgres for precision.
- [ ] **Dynamic Linking**: On new notes, link semantically related thread summaries for richer recall.
- [ ] **Token Budgeting**: Count tokens of each section; when over budget, prioritize shrinking “Related Threads” first, then Preferences, then Current Thread.

## Tech Stack

| Layer            | Technology       | Purpose                                 |
|------------------|------------------|-----------------------------------------|
| Persistence      | Postgres         | Raw messages, thread metadata, indexes  |
| Vector Store     | Qdrant           | Embeddings for messages and thread      |
| Cache            | Redict           | Store last-seen `Context` objects       |
| API              | FastAPI          | Expose `/memory/context` endpoint       |
| LLM Client       | OpenAI (LLM API) | Summaries, context compression, queries |

## Creating Continuity

- New message arrives
- If it has no correlation id, create a new thread
- If it does have a correlation id, use the id to pull context
- Append the message to the selected thread
- Create current convo slice from thread summary and last `n` message
- Embed convo slice, top-k results from Qdrant
- Use results from Qdrant to pull historical threads and preferences
- If necessary, update preferences using convo embedding
- Store context and return to caller

## Maintainging Continuity

- Background worker triggers hierarchical summarization on threads older than threshold
- Obsolete events get compressed or archived

## Context Object Schema

Rendered as:

```md
# Context

System Prompt

## Preferences

User prefers a professional but informal tone in technical discussions. They want information to be clear, direct, and free of overly promotional language or unnecessary embellishment.
User prefers concise, actionable responses for direct factual queries but detailed breakdowns when exploring new or complex technical subjects.

## Related Threads

a1b2c3: In past conversations from May 2025, the user has been architecting a multi-agent system utilizing LLMs, implementing a port-graph-based structure, and refining an agentic framework for AI-driven orchestration. They discussed structuring their project with a hierarchical system of contexts, threads, protocols, and activities, ensuring efficient execution of tasks while maintaining contextual memory. The user explored ways to improve an asynchronous event-driven architecture by balancing centralized and decentralized control, extending protocols, and building message brokering mechanisms. Discussions covered leveraging indexes, data storage, and hybrid memory models for maintaining long-term relevance in user sessions. They also experimented with refining LLM query optimization via structured schema generation and adaptive tool selection.
d4e5f6: In a past conversation on May 7, 2025, the user discussed a project dispute where their client failed to pay for completed work related to an AI-driven legal case review system. The user sought advice on handling non-payment, considering measures such as final notices, open-sourcing the project, and making a public repository outlining the work done. They outlined that the case files used were public domain and embedded as structured data for analysis and retrieval. Their situation involved extensive unpaid development efforts, including full-stack implementations for reviewing visa petitions, front-end interfaces, and database-backed semantic search capabilities.

## Current Thread

Summary [13:42]: Designing the ingestion, cache, and orchestration layers for context generation.
User [14:10]: Can you decouple read/write...
System [14:11]: Sure, here’s a mermaid diagram...
```
