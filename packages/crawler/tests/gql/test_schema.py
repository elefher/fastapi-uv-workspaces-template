import pytest
from crawler.gql.schema import CrawlerQuery


@pytest.mark.asyncio
async def test_schema_execution() -> None:
    """Test executing the GraphQL query"""
    import strawberry

    schema = strawberry.Schema(query=CrawlerQuery)

    query = """
        query {
            getDomains
        }
    """

    result = await schema.execute(query)

    assert result.errors is None
    assert result.data is not None
    assert "getDomains" in result.data
    assert isinstance(result.data["getDomains"], list)
    assert all(isinstance(domain, str) for domain in result.data["getDomains"])
    assert "domain1" in result.data["getDomains"]
    assert "domain2" in result.data["getDomains"]
