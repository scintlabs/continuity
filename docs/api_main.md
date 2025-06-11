## base/api/main.py

This module defines the top level FastAPI router used by the application.

### Responsibilities

- Create an `APIRouter` instance.
- Mount the endpoint definitions from `base.api.routes` onto that router.
- Expose the router as `api_router` for use in the main application.

### Usage

The router is imported by `base/main.py` where the FastAPI `app` is created. The app
includes this router under the version prefix configured via `settings.API_V1_STR` and
applies any CORS configuration defined in `base.config.Settings`.

### Configuration points

- `settings.PROJECT_NAME` – used as the FastAPI application title.
- `settings.API_V1_STR` – prefix for all API routes.
- `settings.all_cors_origins` – enables CORS middleware when not empty.

The final app is assembled in `base/main.py` with a custom unique ID generator for
OpenAPI definitions and by mounting `api_router`:

```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
```
