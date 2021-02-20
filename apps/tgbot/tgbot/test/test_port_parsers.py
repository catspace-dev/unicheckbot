from unittest import TestCase

from ..handlers.default.tcp import TCPCheckerHandler
from ..handlers.base import process_args_for_host_port,\
                            NotEnoughArgs, InvalidPort


class TestArgsProc(TestCase):

    def test_exceptions(self):
        """Test exceptions being raised
        on invalid commands
        """
        cases = [
            ('/cmd', NotEnoughArgs),
            ('/cmd example.com testsarenice', InvalidPort)
        ]
        for cmd, exc in cases:
            with self.subTest(command=cmd):
                self.assertRaises(
                    exc,
                    process_args_for_host_port, cmd, 443
                )
    
    def test_host_port(self):
        """Test that host and port are parsed correctly
        """
        cases = [
            ('/cmd example.com', 'example.com', 443),
            ('/cmd example.com 42', 'example.com', 42),
            ('/cmd example.com:42', 'example.com', 42)
        ]

        for cmd, host, port in cases:
            with self.subTest(cmd=cmd, host=host, port=port):
                test_host, test_port = process_args_for_host_port(cmd, 443)
                self.assertEqual(test_host, host)
                self.assertEqual(test_port, port)


class TestTCPCheckerHandler(TestCase):
    def setUp(self) -> None:
        self.method = TCPCheckerHandler().process_args
        return super().setUp()

    def test_exceptions(self):
        """Test all appropriate excpetions are raised.
        """
        cases = [
            ('/cmd', NotEnoughArgs),
            ('/cmd example.com', NotEnoughArgs),
            ('/cmd example.com jdbnjsbndjsd', InvalidPort)
        ]

        for cmd, exc in cases:
            with self.subTest(cmd=cmd):
                self.assertRaises(
                    exc,
                    self.method, cmd
                )

    def test_host_port(self):
        """Test that host and port are parsed correctly
        """
        cases = [
            ('/cmd example.com 42', 'example.com', 42),
            ('/cmd example.com:65', 'example.com', 65)
        ]

        for cmd, host, port in cases:
            with self.subTest(cmd=cmd, host=host, port=port):
                test_host, test_port = self.method(cmd)
                self.assertEqual(test_host, host)
                self.assertEqual(test_port, port)
