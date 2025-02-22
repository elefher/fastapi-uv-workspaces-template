from contextlib import asynccontextmanager
from typing import Any

import strawberry
from crawler.gql.schema import CrawlerQuery
from crawler.routes import (
    router as crawler_router,
)
from fastapi import FastAPI
from fastapi.routing import APIRoute
from pg.database import init_db as pg_init_db
from strawberry.fastapi import GraphQLRouter


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    session = await pg_init_db()

    yield
    # Shutdown event
    await session.close()


app_ = FastAPI(
    title="FastAPI UV Workspaces Template",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)


@strawberry.type
class Query(CrawlerQuery):
    pass


schema = strawberry.Schema(query=Query)


async def get_context() -> dict[str, Any]:
    # Implement Auth
    user = {"email": "fastapi@example.com"}
    return user


graphql_app: GraphQLRouter[dict[str, Any], Any] = GraphQLRouter(
    schema,
    debug=True,
    context_getter=get_context,
    graphql_ide="graphiql",
)
app_.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

app_.include_router(crawler_router, tags=["crawler"])


@app_.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
