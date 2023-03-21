import requests
from requests_cache import CachedSession


class RemoteConnection():
    def __init__(self, remote_base_url):
        if (remote_base_url == "http://127.0.0.1:8000/"):
            self.connection = TeamTESTConnection(
                username="eric",  # read from .env
                password="password",  # read from .env
                base_url=remote_base_url + "api/"
            )

        else:
            raise Exception("Invalid remote base URL")


class TeamTESTConnection():
    def __init__(self, username, password, base_url):
        # TODO: configure username, password, and base_url
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = CachedSession(
            "teamTEST_cache", backend="sqlite", expire_after=300)
        self.session.auth = (self.username, self.password)

    # URL: ://service/authors/
    def get_authors(self):
        url = self.base_url + "authors"
        response = self.session.get(url)

        if response.status_code != 200:
            # TODO: handle error
            # look in cache?
            pass

        else:
            response_authors = response.json().get("items")
            if response_authors is None:
                # TODO: handle error
                pass

            else:
                cleaned_authors = []
                for author in response_authors:
                    # TODO: set default value for missing field?
                    cleaned_authors.append({
                        "type": author.get("type", "N/A"),
                        "id": author.get("id", "N/A"),
                        "url": author.get("url", "N/A"),
                        "host": author.get("host", "N/A"),
                        "displayName": author.get("displayName", "N/A"),
                        "github": author.get("github", "N/A"),
                        "profileImage": author.get("profileImage", "N/A"),
                    })

                return {
                    "type": "authors",
                    "items": cleaned_authors
                }

    # URL: ://service/authors/{AUTHOR_ID}/
    def get_single_author(self, author_id):
        url = self.base_url + "authors/" + author_id
        response = self.session.get(url)

        if response.status_code != 200:
            # TODO: handle error
            # look in cache?
            pass

        else:
            response_author = response.json()
            if response_author is None:
                # TODO: handle error
                pass

            else:
                return {
                    "type": response_author.get("type", "N/A"),
                    "id": response_author.get("id", "N/A"),
                    "host": response_author.get("host", "N/A"),
                    "displayName": response_author.get("displayName", "N/A"),
                    "url": response_author.get("url", "N/A"),
                    "github": response_author.get("github", "N/A"),
                    "profileImage": response_author.get("profileImage", "N/A"),
                }

    # URL: ://service/authors/{AUTHOR_ID}/followers
    def get_author_followers(self, author_id):
        url = self.base_url + "authors/" + author_id + "/followers"
        response = self.session.get(url)

        if response.status_code != 200:
            # TODO: handle error
            # look in cache?
            pass

        else:
            response_followers = response.json().get("items")
            if response_followers is None:
                # TODO: handle error
                pass

            else:
                cleaned_followers = []
                for author in response_followers:
                    # TODO: set default value for missing field?
                    cleaned_followers.append({
                        "type": author.get("type", "N/A"),
                        "id": author.get("id", "N/A"),
                        "url": author.get("url", "N/A"),
                        "host": author.get("host", "N/A"),
                        "displayName": author.get("displayName", "N/A"),
                        "github": author.get("github", "N/A"),
                        "profileImage": author.get("profileImage", "N/A"),
                    })

                return {
                    "type": "followers",
                    "items": cleaned_followers
                }

    # URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    def check_if_follower(self, author_id, follower_id):
        url = self.base_url + "authors/" + author_id + "/followers/" + follower_id
        response = self.session.get(url)

        if response.status_code != 200:
            # TODO: handle error
            # look in cache?
            pass

        else:
            response = response.json()
            if response is None:
                # TODO: handle error
                pass

            else:
                return {
                    "isFollower": response.get("isFollower", False)
                }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    def get_single_post(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id
        response = self.session.get(url)

        if response.status_code != 200:
            # TODO: handle error
            # look in cache?
            pass

        else:
            response_post = response.json()
            if response_post is None:
                # TODO: handle error
                pass

            else:
                comments = []
                for comment in response_post.get("comments", []):
                    comments.append({
                        "type": comment.get("type", "N/A"),
                        "author": {
                            "type": comment.get("author", {}).get("type", "N/A"),
                            "id": comment.get("author", {}).get("id", "N/A"),
                            "host": comment.get("author", {}).get("host", "N/A"),
                            "displayName": comment.get("author", {}).get("displayName", "N/A"),
                            "url": comment.get("author", {}).get("url", "N/A"),
                            "github": comment.get("author", {}).get("github", "N/A"),
                            "profileImage": comment.get("author", {}).get("profileImage", "N/A"),
                        },
                        "comment": comment.get("comment", "N/A"),
                        "contentType": comment.get("contentType", "N/A"),
                        "published": comment.get("published", "N/A"),
                        "id": comment.get("id", "N/A"),
                    })

                return {
                    "type": response_post.get("type", "N/A"),
                    "title": response_post.get("title", "N/A"),
                    "id": response_post.get("id", "N/A"),
                    "source": response_post.get("source", "N/A"),
                    "origin": response_post.get("origin", "N/A"),
                    "description": response_post.get("description", "N/A"),
                    "contentType": response_post.get("contentType", "N/A"),
                    "content": response_post.get("content", "N/A"),
                    "author": {
                        "type": response_post.get("author", {}).get("type", "N/A"),
                        "id": response_post.get("author", {}).get("id", "N/A"),
                        "host": response_post.get("author", {}).get("host", "N/A"),
                        "displayName": response_post.get("author", {}).get("displayName", "N/A"),
                        "url": response_post.get("author", {}).get("url", "N/A"),
                        "github": response_post.get("author", {}).get("github", "N/A"),
                        "profileImage": response_post.get("author", {}).get("profileImage", "N/A"),
                    },
                    "categories": response_post.get("categories", "N/A"),
                    "count": response_post.get("count", "N/A"),
                    "comments": response_post.get("comments", "N/A"),
                    "commentsSrc": {
                        "type": response_post.get("commentsSrc", {}).get("type", "N/A"),
                        "page": response_post.get("commentsSrc", {}).get("page", "N/A"),
                        "size": response_post.get("commentsSrc", {}).get("size", "N/A"),
                        "post": response_post.get("commentsSrc", {}).get("post", "N/A"),
                        "id": response_post.get("commentsSrc", {}).get("id", "N/A"),
                        "comments": comments
                    },
                    "published": response_post.get("published", "N/A"),
                    "visibility": response_post.get("visibility", "N/A"),
                    "unlisted": response_post.get("unlisted", "N/A"),
                }

    # URL: ://service/authors/{AUTHOR_ID}/posts/
    def get_recent_posts(self, author_id):
        url = self.base_url + "authors/" + author_id
        response = self.session.get(url)

        if response.status_code != 200:
            # TODO: handle error
            # look in cache?
            pass

        else:
            response_posts = response.json()
            if response_posts is None:
                # TODO: handle error
                pass

            else:
                posts = []
                for post in response_posts:
                    comments = []
                    for comment in post.get("comments", []):
                        comments.append({
                            "type": comment.get("type", "N/A"),
                            "author": {
                                "type": comment.get("author", {}).get("type", "N/A"),
                                "id": comment.get("author", {}).get("id", "N/A"),
                                "host": comment.get("author", {}).get("host", "N/A"),
                                "displayName": comment.get("author", {}).get("displayName", "N/A"),
                                "url": comment.get("author", {}).get("url", "N/A"),
                                "github": comment.get("author", {}).get("github", "N/A"),
                                "profileImage": comment.get("author", {}).get("profileImage", "N/A"),
                            },
                            "comment": comment.get("comment", "N/A"),
                            "contentType": comment.get("contentType", "N/A"),
                            "published": comment.get("published", "N/A"),
                            "id": comment.get("id", "N/A"),
                        })

                    posts.append({
                        "type": post.get("type", "N/A"),
                        "title": post.get("title", "N/A"),
                        "id": post.get("id", "N/A"),
                        "source": post.get("source", "N/A"),
                        "origin": post.get("origin", "N/A"),
                        "description": post.get("description", "N/A"),
                        "contentType": post.get("contentType", "N/A"),
                        "content": post.get("content", "N/A"),
                        "author": {
                            "type": post.get("author", {}).get("type", "N/A"),
                            "id": post.get("author", {}).get("id", "N/A"),
                            "host": post.get("author", {}).get("host", "N/A"),
                            "displayName": post.get("author", {}).get("displayName", "N/A"),
                            "url": post.get("author", {}).get("url", "N/A"),
                            "github": post.get("author", {}).get("github", "N/A"),
                            "profileImage": post.get("author", {}).get("profileImage", "N/A"),
                        },
                        "categories": post.get("categories", "N/A"),
                        "count": post.get("count", "N/A"),
                        "comments": post.get("comments", "N/A"),
                        "commentsSrc": {
                            "type": post.get("commentsSrc", {}).get("type", "N/A"),
                            "page": post.get("commentsSrc", {}).get("page", "N/A"),
                            "size": post.get("commentsSrc", {}).get("size", "N/A"),
                            "post": post.get("commentsSrc", {}).get("post", "N/A"),
                            "id": post.get("commentsSrc", {}).get("id", "N/A"),
                            "comments": comments
                        },
                        "published": post.get("published", "N/A"),
                        "visibility": post.get("visibility", "N/A"),
                        "unlisted": post.get("unlisted", "N/A"),
                    })

                return posts

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
    def get_image_post(self, author_id, post_id):
        # TODO: implement this method
        pass

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    def get_comments(self, author_id, post_id):
        # TODO: implement this method
        pass

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_like(self, author_id):
        # TODO: implement this method
        pass

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    def get_post_likes(self, author_id, post_id):
        # TODO: implement this method
        pass

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    def get_comment_likes(self, author_id, post_id, comment_id):
        # TODO: implement this method
        pass

    # URL: ://service/authors/{AUTHOR_ID}/liked
    def get_author_likes(self, author_id):
        # TODO: implement this method
        pass

    # URL: ://service/authors/{AUTHOR_ID}/inbox
    def send_to_inbox(self, author_id):
        # TODO: implement this method
        pass