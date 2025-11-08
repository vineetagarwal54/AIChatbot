# post procesing
import re

# Common PII patterns - SSN is an example; keep redact generic
PII_REGEX = re.compile(r"(\d{3}-\d{2}-\d{4})")  # example 123-45-6789
# email regex: make case-insensitive so lowercase emails are matched
EMAIL_REGEX = re.compile(r"(\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b)", re.IGNORECASE)

def secure_output(text: str) -> str:
    text = PII_REGEX.sub("[REDACTED]", text)
    text = EMAIL_REGEX.sub("[REDACTED]", text)
    return text.strip()

