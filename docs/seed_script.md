## Seed Script

`scripts/seed.py` sends documents to the ingestion service so they can be stored and indexed. The script expects the ingestion endpoint to be running locally at `http://localhost:8000/ingest`.

### Usage

```bash
python scripts/seed.py path/to/file1.txt path/to/file2.txt
```

Pass one or more file paths as arguments. Each file is read and posted to the ingestion endpoint with JSON fields `text` and `type`.

### Asynchronous Calls

The script uses `asyncio` and `aiohttp` to send requests concurrently:

1. `seed_file(path)` reads a file and performs an asynchronous `POST` using `aiohttp.ClientSession`.
2. `main(paths)` gathers all `seed_file` coroutines with `asyncio.gather`, allowing multiple uploads to occur in parallel.
3. `asyncio.run(main(sys.argv[1:]))` starts the event loop when the script is executed directly.

This approach lets multiple documents be uploaded efficiently without waiting for each request to finish before starting the next.
