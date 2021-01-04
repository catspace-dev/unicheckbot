from httpx import AsyncClient, Timeout, Response, ConnectError
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
        try:
            async with AsyncClient(timeout=Timeout(timeout=100.0)) as client:
                result = await client.get(
                    f"{node.address}/{endpoint}", params=data
                )
        except ConnectError:
            # We yield 500 response when backend is offline
            result = Response(500)
        yield result
