from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.routes.route import route
from contextlib import asynccontextmanager
from app.config.database import connect_db, close_db


def _binary_fix(node):
    # OpenAPI 3.1 'contentMediaType' ko purane 'format: binary' se badlo
    # taaki Swagger UI file arrays (list[UploadFile]) ke liye file-picker dikhaye
    if isinstance(node, dict):
        if node.get("contentMediaType") == "application/octet-stream":
            node.pop("contentMediaType")
            node["format"] = "binary"
        for value in node.values():
            _binary_fix(value)
    elif isinstance(node, list):
        for item in node:
            _binary_fix(item)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_db()
    yield

    # Shutdown
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(route)

# 1. Define the origins that are allowed to make requests to your API
origins = [
    "http://localhost:3000",    # React default port
    "http://localhost:5173",    # Vite/Vue default port
    "https://yourfrontend.com"  # Your production domain
]

# 2. Add the CORSMiddleware to your FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Allows requests from specified origins
    allow_credentials=True,         # Allows cookies to be included in requests
    allow_methods=["*"],            # Allows all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],            # Allows all request headers
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version="3.0.3",
        routes=app.routes,
    )
    _binary_fix(schema)
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi
