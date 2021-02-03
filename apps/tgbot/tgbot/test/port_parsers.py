import asyncio

from ..handlers.default.tcp import TCPCheckerHandler
from ..handlers.base import process_args_for_host_port,\
                            NotEnoughArgs, InvalidPort


try:
    args = "/cmd"
    process_args_for_host_port(args, 443)
except NotEnoughArgs:
    pass
args = "/cmd example.com"
host, port = process_args_for_host_port(args, 443)
assert port == 443

args = "/cmd example.com 42"
host, port = process_args_for_host_port(args, 443)
assert port == "42"  # TODO: FIX THIS SHIT

args = "/cmd example.com:42"
host, port = process_args_for_host_port(args, 443)
assert port == "42"

try:
    args = "/cmd example.com fucktests"
except InvalidPort:
    pass

method = TCPCheckerHandler().process_args


async def test():
    try:
        args = "/cmd"
        await method(args)
        args = "/cmd example.com"
        await method(args)
    except NotEnoughArgs:
        pass

    args = "/cmd example.com 42"
    host, port = await method(args)
    assert port == "42"

    args = "/cmd example.com:42"
    host, port = await method(args)
    assert port == "42"

    try:
        args = "/cmd example.com jdbnjsbndjsd"
        await method(args)
    except InvalidPort:
        pass


asyncio.run(test())
