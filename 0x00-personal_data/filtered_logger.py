#!/user/bin/env python3
"""
A function that returns the log massage obfuscated
"""
import re

def filter_datum(fields, redation, message, seperator):
    """"""
    pattern = f"({'|'.join(fields)})=([^ {seperator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redation}", message)