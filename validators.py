import re
from wtforms.validators import Regexp, ValidationError, HostnameValidation



class URL(Regexp):
    """
    Simple regexp based url validation. Much like the email validator, you
    probably want to validate the url later by other means if the url must
    resolve.

    :param require_tld:
        If true, then the domain-name portion of the URL must contain a .tld
        suffix.  Set this to false if you want to allow domains like
        `localhost`.
    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, require_tld=True, message=None):
        regex = (
            r"^[a-z]+://"
            r"(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )
        super().__init__(regex, re.IGNORECASE, message)
        self.validate_hostname = HostnameValidation(
            require_tld=require_tld, allow_ip=True
        )

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext("Invalid URL.")

        match = super().__call__(form, field, message)
        if not self.validate_hostname(match.group("host")):
            raise ValidationError(message)