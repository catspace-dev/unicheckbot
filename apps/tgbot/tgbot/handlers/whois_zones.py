from whois.parser import WhoisEntry, PywhoisError, EMAIL_REGEX


class WhoisCf(WhoisEntry):
    """Whois parser for .cf domains
    """
    regex = {
        'domain_name':                    'Domain name:\n*(.+)\n',
        'org':                            'Organisation:\n *(.+)',
        'emails':                         EMAIL_REGEX,
    }

    def __init__(self, domain, text):
        if 'The domain you requested is not known in Freenoms database' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)


ZONES = {
    "cf": WhoisCf
}