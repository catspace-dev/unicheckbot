from httpx import AsyncClient, Timeout, Response, ConnectError
from typing import List
from core.coretypes import APINode
from ipaddress import ip_address
from contextlib import suppress
from loguru import logger
from tgbot.handlers.metrics import push_api_request_status


def check_int(value) -> bool:
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def validate_local(target: str) -> bool:
    """
    Validates ip or FQDN is localhost

    :return True if localhost find
    """
    if target == "localhost":
        return True
    with suppress(ValueError):
        ip_addr = ip_address(target)
        if any(
                [ip_addr.is_loopback,
                 ip_addr.is_private,
                 ip_addr.is_multicast,
                 ip_addr.is_link_local,
                 ip_addr.is_unspecified]
        ):
            return True
    return False


async def send_api_requests(endpoint: str, data: dict, nodes: List[APINode]):
    for node in nodes:
        data.update(dict(token=node.token))
        try:
            async with AsyncClient(timeout=Timeout(timeout=100.0)) as client:
                result = await client.get(
                    f"{node.address}/{endpoint}", params=data
                )
        except ConnectError as e:
            logger.error(f"Node {node.address} got ConnectionError. Full exception: {e}")
            # TODO: Report problems to admins
            # We yield 500 response when backend is offline
            result = Response(500)
        await push_api_request_status(
            result.status_code,
            endpoint
        )
        yield result
