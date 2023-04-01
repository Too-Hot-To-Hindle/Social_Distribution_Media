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
    
def extract_id_group_6(prefix: str, id):
    regex = r'.*' + prefix + r'\/([0-9a-f]{8}[0-9a-f]{4}4[0-9a-f]{3}[89ab][0-9a-f]{3}[0-9a-f]{12}).*'
    search = re.search(regex, id)
    if search:
        return search.group(1)
    return ''

def extract_id_if_url_group_6(type: str, id_str: str):
    """Get the uuid out of a url if it is a url for group 6's weird ID system"""
    validate = URLValidator()

    try:
        validate(id_str)
        match type.lower():
            case 'author':
                # return extract_author_uuid(id_str)
                return extract_id_group_6('authors', id_str)
            case 'post':
                # return extract_post_uuid(id_str)
                return extract_id_group_6('posts', id_str)
            case 'comment':
                # return extract_comment_uuid(id_str)
                return extract_id_group_6('comments', id_str)
            case _:
                raise ValueError("Value of the type arguement must be either 'author', 'post', or 'comment'")
    except ValidationError:
        # If not a URL, just return the ID string
        return id_str
    
def extract_id_group_10(prefix:str, id):
    return id.split(prefix + "/")[1]

def extract_id_if_url_group_10(type: str, id_str: str):
    """Get the uuid out of a url if it is a url for group 10's weird ID system"""
    validate = URLValidator()

    try:
        validate(id_str)
        match type.lower():
            case 'author':
                # return extract_author_uuid(id_str)
                return extract_id_group_10('authors', id_str)
            case 'post':
                # return extract_post_uuid(id_str)
                return extract_id_group_10('posts', id_str)
            case 'comment':
                # return extract_comment_uuid(id_str)
                return extract_id_group_10('comments', id_str)
            case _:
                raise ValueError("Value of the type arguement must be either 'author', 'post', or 'comment'")
    
    except ValidationError:
        # If not a URL, just return the ID string
        return id_str
        

    
def is_remote_url(id_str: str):
    validate = URLValidator()
    try:
        validate(id_str)

        # if id_str starts with http://127.0.0.1:8000, return False
        if id_str.startswith('http://127.0.0.1:8000'):
            return False
        
        if id_str.startswith('https://social-distribution-media.herokuapp.com/api/'):
            return False
        
        # otherwise, it's a remote URL, so return True
        else:
            return True
    
    except ValidationError:
        # If not a URL, just return False
        return False
    
def get_remote_url(url: str):
    # gets base API url from a remote hosted URI
    # for example, `https://social-distribution-media.herokuapp.com/authors/1234/posts/5678/comments/91011`
    # would return `https://social-distribution-media.herokuapp.com/`
    # since all URIs start with 'authors'
    return url.split("authors")[0]