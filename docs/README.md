# Continuity

### **Continuous State Protocol for Large Language Models**

Continuity is an opinionated framework and protocol for endowing Large Language Models with a persistent sense of “self” and history. By structuring messages, context windows, and retrieval mechanisms into distinct tiers of memory, Continuity lets developers build dynamic, long-lived user experiences that transcend the LLM’s usual token limit. Whether you’re storing conversation turns, archiving key insights, or retrieving facts from extensive knowledge graphs, Continuity offers a blueprint for weaving short- and long-term memory into a cohesive, continuous state.

## Overview

Contuinity organizes state into "snapshots", which is the output sent to a language model to generate responses and actions. It's essentially an aggregate of the current interaction, along with relevant data pulled from various sources to produce a model response that gives the impression of user connection, temporal and contextual awareness, and interaction consistency.

Snapshots can include:

- System prompts and instructions
- A limited number of interactions from the current conversation
- Active file or io data (e.g., a file the assistant is working on)

Additionally, each snapshot contains a summary of semantically-related contextual references that the assistant can activate using its base tools. These references are categorized into either episodic history, or knowledge stores:

- Episodic history: Representations of historical tasks and conversations
- Knowledge stores: Similar to typical RAG implementations

## States as Tiered Memory

At the risk of anthropomorphizing language models, thinking of assistant state as layered or tiered memory in human beings is a useful mnemonic.

### Interaction State

Interaction state encompasses the "working memory," which includes the last few conversation turns and a buffer for data, such as file edits or remote system access.

- Stored ephemerally (key/value memory store, cache, etc.)

### Index State

Index state is a revolving, filterable, parameterized listing and summary of search results representing **semantically related* information. It's built from the current interaction state and—generally speaking—its purpose is to:

- Help massage the assistant's responses
- Provide concise, context-rich "links" the assistant can use to guide its own state

Which is to say, the index state is designed as an implicit "background" layer that models should consider when responding, but not necessarily referenced unless acted upon explicitly by the model.

- Summaries of previous conversations, older knowledge
- Useful to compress large conversation histories or logs to keep them accessible (e.g., via embeddings and retrieval) without ballooning the LLM’s context

### Recall State

The recall state is built from actions an assistant takes on the index state. When the assistant determines that a listing from the index state would be helpful to expand on within its current context, it uses its tools to activate the listing, the system builds the recall state, creates a new snapshot with the recalled information, and resends the snapshot to the model.

- Encoded and parsed historical conversations
- Knowledge bases, knowledge graphs, etc.
- Stored in long-term storage

## Architecture

- Handling input/generation/output
    - Receives user inputs (e.g., messages or instructions)
    - Orchestrates what additional context or memory to retrieve before passing it all to the LLM
- State and context management
    - Structures how data is stored, retrieved, and updated
    - Operates with multiple tiers of memory (short-term vs. long-term)
    - Decides when to archive data and how to retrieve relevant memory
- Calling language models
    - The user’s new message/queries
    - Relevant short-term memory (current conversation context).
    - Relevant long-term memory (facts, knowledge, user profile, etc.)
- Metadata
- Storage and retrieval
    - One or more data stores optimized for different use cases (e.g., relational DB for structured data, vector DB for semantic search, file-based logs for raw transcripts)
