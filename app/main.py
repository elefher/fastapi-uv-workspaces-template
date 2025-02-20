from typing import Any

import strawberry
from crawler.gql.schema import CrawlerQuery
from crawler.routes import (
    router as crawler_router,
)
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

app_ = FastAPI()


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

app_.include_router(crawler_router)


@app_.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
