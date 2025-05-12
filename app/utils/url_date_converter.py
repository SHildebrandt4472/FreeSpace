
from werkzeug.routing import BaseConverter, ValidationError
from datetime import datetime

class UrlDateConverter(BaseConverter):
    """Extracts a ISO8601 date from the url path and validates it."""

    regex = r'\d{4}-\d{2}-\d{2}|today'

    def to_python(self, value):
        if value == "today":
            return get_localtime().date()
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')
