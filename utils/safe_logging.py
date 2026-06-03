import re

REDACTED = "***"

SENSITIVE_KEYS = frozenset({
    "password",
    "password_hash",
    "token",
    "secret",
    "api_key",
    "authorization",
    "email",
    "database_url",
    "connection_string",
})

_CONNECTION_STRING_PATTERN = re.compile(
    r"(mysql|postgresql|mariadb|sqlite)(\+[\w]+)?://[^\s]+",
    re.IGNORECASE,
)


def _is_sensitive_key(key):
    key_lower = key.lower()
    return key_lower in SENSITIVE_KEYS or any(
        sensitive in key_lower for sensitive in SENSITIVE_KEYS
    )


def _sanitize_value(key, value):
    if _is_sensitive_key(key):
        return REDACTED
    if isinstance(value, str) and _CONNECTION_STRING_PATTERN.search(value):
        return REDACTED
    return value


def sanitize_details(details):
    if not details:
        return {}
    return {key: _sanitize_value(key, value) for key, value in details.items()}


def format_safe_details(details):
    safe_details = sanitize_details(details)
    if not safe_details:
        return ""
    context = ", ".join(f"{key}={value}" for key, value in safe_details.items())
    return f" ({context})"


def safe_exception_message(exc):
    return type(exc).__name__
