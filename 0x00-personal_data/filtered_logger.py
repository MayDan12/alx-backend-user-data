#!/user/bin/env python3
"""
A function that returns the log massage obfuscated
"""
import re


def filter_datum(fields, redaction, message, separator=" "):
    pattern = r"(?:" + separator + r"(?:(?:" + "|".join(fields) + r") \b.+?))"
    return re.sub(pattern, redaction, message)
