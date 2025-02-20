from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/crawl",
    responses={404: {"description": "Not found"}},
)


class Response(BaseModel):
    start_url: str
    total: int
    visited_urls: list[str]


@router.get("/", response_model=Response)
async def start_crawl() -> Response:
    return Response(start_url="url_request.url", total=100, visited_urls=["eisisi"])
