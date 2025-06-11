## Architecture

### Services

| Service      | Port | Purpose |
|--------------|------|---------|
| qdrant       | 6333 | Vector store |
| postgres     | 5432 | Metadata storage |
| redict       | 6379 | Cache + Streams |
| ingest       | 8000 | Ingestion endpoint |
| retrieve     | 8001 | Read-only endpoint `/query` |

## Logical Topology

- **Ingestion service** – write-only; embeds, validates, enqueues.
- **Retrieval service** – read-only; performs hybrid semantic + metadata search and optional re-ranking.
- **Redis Streams** decouple write spikes from DB latency; workers drain the queue and upsert to Qdrant + Postgres.
