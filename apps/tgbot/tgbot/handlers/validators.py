from .errors import LocalhostForbidden
from ipaddress import ip_address
from contextlib import suppress


class BaseValidator:

    def __init__(self):
        pass

    def validate(self, target: str, **kwargs):
        pass


class LocalhostValidator(BaseValidator):

    def validate(self, target: str, **kwargs):
        if target == "localhost":
            raise LocalhostForbidden
        with suppress(ValueError):
            ip_addr = ip_address(target)
            if any(
                    [ip_addr.is_loopback,
                     ip_addr.is_private,
                     ip_addr.is_multicast,
                     ip_addr.is_link_local,
                     ip_addr.is_unspecified]
            ):
                raise LocalhostForbidden
