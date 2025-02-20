import strawberry


def get_domains() -> list[str]:
    return ["domain1", "domain2"]


@strawberry.type
class CrawlerQuery:
    get_domains: list[str] = strawberry.field(resolver=get_domains)
