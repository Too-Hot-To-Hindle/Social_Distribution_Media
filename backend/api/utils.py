from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import re

def extract_uuid(prefix: str, id):
    regex = r'.*' + prefix + r'\/([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}).*'
    search = re.search(regex, id)
    if search:
        return search.group(1)
    return ''

def extract_uuid_if_url(type: str, id_str: str):
    """Get the uuid out of a url if it is a url"""
    validate = URLValidator()

    try:
        validate(id_str)
        match type.lower():
            case 'author':
                # return extract_author_uuid(id_str)
                return extract_uuid('authors', id_str)
            case 'post':
                # return extract_post_uuid(id_str)
                return extract_uuid('posts', id_str)
            case 'comment':
                # return extract_comment_uuid(id_str)
                return extract_uuid('comments', id_str)
            case _:
                raise ValueError("Value of the type arguement must be either 'author', 'post', or 'comment'")
    except ValidationError:
        # If not a URL, just return the ID string
        return id_str