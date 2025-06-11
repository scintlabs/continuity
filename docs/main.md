# Main Entry Point

The service is started from `base/main.py`. This file builds the FastAPI
application and wires together configuration and all API routes.

## Configuration

`base.config.Settings` is used to load environment variables via
`pydantic-settings`. Important fields include `PROJECT_NAME` for the title and
`API_V1_STR` which prefixes all routes and the OpenAPI document. The class also
builds a list of allowed CORS origins via the `all_cors_origins` property.

## Application Setup

`base/main.py` constructs a `FastAPI` instance with a custom function for
OpenAPI operation IDs:

```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)
```

If any CORS origins are configured, `CORSMiddleware` is attached so that those
origins are permitted and all methods/headers are allowed.

Finally, the API router defined in `base.api` is mounted under the versioned
prefix:

```python
app.include_router(api_router, prefix=settings.API_V1_STR)
```

`custom_generate_unique_id` formats each route's operation ID as
`"{tag}-{name}"`, ensuring consistent names in the OpenAPI schema.

No additional startup hooks are defined; the application is ready once the
module is imported by an ASGI server such as `uvicorn`.
