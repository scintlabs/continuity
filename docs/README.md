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


3. Data Structures & Indexing

3.1. Conversation Log

A simple approach is to keep a conversation log: each turn (user or system) is stored with:
- Turn ID or Time Stamp
- Speaker (user or system)
- Content (text of the utterance or message)
- Metadata (e.g., user ID, topics, relevant tags, or embedding vector)

This log is appended to short-term storage. Periodically or when the conversation ends, you archive it into a longer-term store (e.g., a database table or object storage).

3.2. Knowledge / Fact Entries

For “fact-based” memory (e.g., user preferences, background knowledge, domain facts), it’s often easier to store them in a structured or semi-structured format:
- Knowledge ID
- Summary / Title
- Detailed Content (a text field or chunk of text)
- Embedding (for retrieval by semantic similarity)
- Metadata (tags, creation date, reliability score, etc.)

Storing embeddings (in a vector database such as Pinecone, Qdrant, Weaviate, or in a local FAISS index) allows for similarity-based retrieval that can be used to look up relevant chunks to feed into the LLM context.

3.3. Summaries

To keep older conversation logs accessible but not overwhelming, you can periodically summarize conversation segments. Store these summaries (rather than the raw transcripts) in a long-term store. For instance:
- Session ID or Time Range
- Summary / Embedding
- Key Moments or Highlights

When relevant, you can retrieve the summary, and if needed, the user or system can “drill down” to the original logs.

4. Retrieval Strategy

4.1. Direct Historical Context

When the user is in an ongoing conversation, you can provide the LLM with a window of the last N turns (for instance, the last 5 or 10 user-system exchanges). This is your short-term memory.

4.2. Semantic Retrieval (Long-Term)

If the user’s query might connect to older knowledge or facts (like preferences, prior solutions, or domain data), you do a semantic search in the long-term store. You:
1.	Formulate a search query (e.g., using the user’s prompt or a specialized retrieval prompt).
2.	Query the vector index to find relevant chunks.
3.	Select top-k results (the most relevant).
4.	Inject those into the LLM’s context as additional instructions or knowledge.

4.3. Hybrid Approach

You can combine direct conversation history with semantic retrieval. This ensures the LLM sees both recent context and any relevant longer-term facts.

5. Protocol Lifecycle

Below is an example protocol flow to manage how inputs/outputs move through your system to provide persistent memory.
1.	Receive User Input
- The user says something or triggers an event.
2.	Log the Input (Short-Term Store)
- Append the user’s message to the conversation log in ephemeral storage (e.g., in-memory queue or short-term database record).
3.	Identify or Retrieve Relevant Context
- Look up the session ID / user ID.
- Retrieve the last N messages from the conversation log.
- Perform a semantic search over your long-term knowledge base for relevant data.
4.	Compose the Prompt for the LLM
- Short-Term Context: The last N user and system messages.
- Long-Term Memories: Summaries, facts, or knowledge entries that match the user’s query.
- Possibly include a system message that sets the LLM’s role or instructions on how to respond.
5.	Call the LLM
- Send the composed prompt to the model.
6.	Receive LLM Output
- The LLM returns its generated response.
7.	Update Memory Stores
- Append the LLM’s output (system message) to the short-term conversation log.
- Optionally, run summarization if the conversation is getting too long, or if the user ended the session.
- Save relevant new facts or resolved user input to the long-term store (e.g., “User indicated new preference X”).
8.	Archive / Summarize (As Needed)
- If the session ends or if conversation logs are growing large, create a summary.
- Save the summary (and possibly the entire conversation) in the long-term knowledge store for future retrieval.

6. Access Control & Privacy

In many real-world applications, the LLM needs to maintain separate memories for different users or roles. Consider:
- User Identification: Each user or session has an ID; any memory is tied to that ID.
- Permission Models: Some knowledge entries might be private to a user vs. shared across an organization.
- Data Retention: Decide how long you keep conversation logs or whether you allow users to delete them.

7. Practical Implementation Considerations

7.1. Data Store Choices
- Short-Term Store:
- Could be a simple in-memory data structure, a Redis queue, or a local ephemeral DB table.
- Long-Term Store:
- A vector database (e.g., Pinecone, Weaviate, Qdrant) or local FAISS index for semantic retrieval.
- Possibly also a relational or NoSQL DB for structured data.
- File-based logs for raw transcripts or backups.

7.2. Indexing & Embedding
- You’ll need an embedding model (often a separate model from the LLM, or you can use the LLM if it provides an embeddings API).
- Update embeddings for new chunks of conversation or knowledge.
- Decide on chunk sizes (e.g., 512- to 1,000-token chunks) for indexing so retrieval remains accurate.

7.3. Summarization Logic
- If you summarize conversation turns, store them in the long-term database with embeddings for easy retrieval.
- You can create hierarchical summaries (e.g., daily summary, weekly summary, monthly summary) if you expect very long conversations.

7.4. Scalability
- Think about how many concurrent users you’ll have and how quickly the data store might grow.
- For large-scale usage, a streaming or microservices architecture can help:
- A dedicated microservice for vector indexing.
- A separate service for conversation logging.

8. Example “Memory Protocol” Specification

Below is a pseudo-spec for how your memory protocol might look. You can adapt the data fields and structure to your own needs.

version: 1.0

short_term_memory:
# In-memory or ephemeral store for the active session
storage: "in-memory"  # or ephemeral DB
max_turns: 10         # Keep last 10 turns in direct context
archiving_policy:
# Summarize and archive after 20 turns or session close
trigger: ["session_close", "turn_count >= 20"]

long_term_memory:
# Persistent knowledge store
storage: "vector_db"
vector_db_details:
name: "Pinecone"
index_name: "conversation_index"
summary_store:
# Where summarized logs go
name: "mongo_db"
collection: "conversation_summaries"

protocol:
conversation_flow:
- step: "RECEIVE_USER_INPUT"
    action: "store_in_short_term_memory"
- step: "RETRIEVE_CONTEXT"
    action:
    - "fetch_last_N_turns_from_short_term"
    - "semantic_search_long_term_knowledge"
- step: "COMPOSE_PROMPT"
    action: "merge_context_and_user_input"
- step: "CALL_LLM"
    action: "send_prompt_and_get_response"
- step: "STORE_LLM_OUTPUT"
    action: "append_llm_response_to_short_term"
- step: "CHECK_ARCHIVE"
    action: "if needed, summarize_and_store_in_long_term"

metadata:
# Additional fields that can be stored in each memory record
fields:
- user_id
- timestamp
- conversation_id
- embedding
- tags
- summary

This pseudo-spec outlines the core steps of how data moves through your system, when it’s stored, and how it’s retrieved.

9. Getting Started / Next Steps
1.	Prototype a Simple Conversation Logger
- Store each user/system message with a timestamp and user ID in a simple DB or CSV/log file.
- Provide only the last few turns to the LLM for context.
2.	Add Vector Search for Long-Term Memory
- Choose a vector DB or local embedding-based index.
- Start indexing conversation segments, user facts, and knowledge.
- Implement a function to retrieve top-K relevant chunks given a query.
3.	Implement Summaries
- After the conversation ends or after X turns, auto-summarize using your LLM.
- Store the summary as a separate record with an embedding.
4.	Refine Access & Privacy
- If multi-user, ensure you have a user/session ID to keep memories separated.
- Add encryption or restricted access if needed.
5.	Scale and Optimize
- If usage grows, move to a more robust architecture (microservices, caching strategies, message queues, etc.).

Conclusion

Designing a “memory” or “state” protocol for an LLM involves carefully managing short-term and long-term data stores, deciding what to store, how to store it (structured vs. unstructured, embeddings for semantic retrieval, etc.), and when to retrieve or archive information. By setting up a well-defined pipeline—and potentially a spec or schema for each memory record—you provide the scaffolding that enables the LLM to “remember” critical interactions and knowledge across sessions.

Starting small with a simple conversation log + vector-based retrieval, then expanding with more sophisticated summaries and knowledge management will help you iteratively build a robust memory system for your LLM-based application.
