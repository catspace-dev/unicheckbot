from httpx import AsyncClient
from typing import List
from core.coretypes import APINode


def check_int(value) -> bool:
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


async def send_api_requests(endpoint: str, data: dict, nodes: List[APINode]):
    for node in nodes:
        data.update(dict(token=node.token))
        async with AsyncClient() as client:
            result = await client.get(
                f"{node.address}/{endpoint}", params=data
            )
        yield result
