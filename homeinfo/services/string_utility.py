"""
Author: Edwin S. Cowart
Created: 4/19/22
"""


def format_in_english(some_list: list, conjunction: str) -> str:
    if not some_list:
        return ""
    elif len(some_list) == 1:
        return str(some_list[0])
    elif len(some_list) == 2:
        return f"{some_list[0]} {conjunction} {some_list[1]}"
    else:
        return f"{', '.join(some_list[0:-1])}, {conjunction} {some_list[-1]}"
