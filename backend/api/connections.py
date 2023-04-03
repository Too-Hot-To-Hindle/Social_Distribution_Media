import requests
from requests_cache import CachedSession
import json
import base64

# define custom exception for resource not found on remote server


class Remote404(Exception):
    "Raised when remote resource retruned a 404"
    pass

# define custom exception for remote server error


class RemoteServerError(Exception):
    "Raised when remote server returned a non-404 error"
    pass


class RemoteConnection():
    def __init__(self, remote_base_url):
        if (remote_base_url == "https://social-distribution-media-2.herokuapp.com/api/"):
            self.connection = TeamCloneConnection(
                username="joshdoe",  # read from .env
                password="SocialDistribution!",  # read from .env
                base_url=remote_base_url
            )

        # Team 6
        elif (remote_base_url == "https://cmput404-group6-instatonne.herokuapp.com/"):
            self.connection = Team6Connection(
                username="Group2",  # read from .env
                password="purplepurple",  # read from .env
                base_url=remote_base_url
            )

        # Team 10
        elif (remote_base_url == "https://socialdistcmput404.herokuapp.com/"):
            self.connection = Team10Connection(
                username="",  # read from .env
                password="",  # read from .env
                base_url=remote_base_url
            )

        # Team 11
        elif (remote_base_url == "https://quickcomm-dev1.herokuapp.com/api/"):
            self.connection = Team11Connection(
                username="Z6cpWvdTQsVSGaKQYFbw",  # read from .env
                password="1LE7jxqA8n3os60mU48v",  # read from .env
                base_url=remote_base_url
            )

        # Team 13
        elif (remote_base_url == "https://group-13-epic-app.herokuapp.com/api/"):
            self.connection = Team13Connection(
                username="group2user",  # read from .env
                password="test",  # read from .env
                base_url=remote_base_url
            )

        else:
            raise Exception("Invalid remote base URL")


class TeamCloneConnection():
    def __init__(self, username, password, base_url):
        # TODO: configure username, password, and base_url
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = CachedSession(
            "teamTEST_cache", backend="sqlite", expire_after=1)
        self.session.auth = (self.username, self.password)

    # URL: ://service/authors/
    def get_authors(self):
        url = self.base_url + "authors"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        authors = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the authors we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting authors from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(
                    response.status_code) + " was received in response.")

            response_authors = response.json()
            if response_authors is None:
                raise RemoteServerError(
                    "Error getting authors from remote server: https://social-distribution-media-2.herokuapp.com/. Response body was empty.")

            items = response_authors.get("items", [])
            authors.extend(items)
            page += 1

        return {
            "type": "authors",
            "items": authors
        }

    # URL: ://service/authors/{AUTHOR_ID}/
    def get_single_author(self, author_id):
        url = self.base_url + "authors/" + author_id
        response = self.session.get(url)

        # if the author is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Author with id " + author_id +
                            " not found on remote server: https://social-distribution-media-2.herokuapp.com/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_author = response.json()

                # if the response body is empty, throw an exception
                if response_author is None:
                    raise RemoteServerError("Error getting author with id " + author_id +
                                            " from remote server: https://social-distribution-media-2.herokuapp.com/. Response body was empty.")

                else:
                    return response_author

            except Exception as e:
                raise RemoteServerError("Error getting author with id " + author_id +
                                        " from remote server: https://social-distribution-media-2.herokuapp.com/. Exception: " + str(e))

    # URL: ://service/authors/{AUTHOR_ID}/followers
    def get_author_followers(self, author_id):
        url = self.base_url + "authors/" + author_id + "/followers"
        response = self.session.get(url)

        # if the author is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Author with id " + author_id +
                            " not found on remote server: https://social-distribution-media-2.herokuapp.com/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting followers for author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_followers = response.json().get("items", [])
                if response_followers is None:
                    raise RemoteServerError("Error getting followers for author with id " + author_id +
                                            " from remote server: https://social-distribution-media-2.herokuapp.com/. Response body was empty.")

                else:
                    cleaned_followers = []
                    for author in response_followers:
                        cleaned_followers.append({
                            "type": author.get("type"),
                            "id": author.get("id"),
                            "url": author.get("url"),
                            "host": author.get("host"),
                            "displayName": author.get("displayName"),
                            "github": author.get("github"),
                            "profileImage": author.get("profileImage"),
                        })

                    return {
                        "type": "followers",
                        "items": cleaned_followers
                    }

            except Exception as e:
                raise RemoteServerError("Error getting followers for author with id " + author_id +
                                        " from remote server: https://social-distribution-media-2.herokuapp.com/. Exception: " + str(e))

    # URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    def check_if_follower(self, author_id, follower_id):
        url = self.base_url + "authors/" + author_id + "/followers/" + follower_id
        response = self.session.get(url)

        if response.status_code != 200:
            return {
                "isFollower": response.get("isFollower", False)
            }

        else:
            response = response.json()
            if response is None:
                raise RemoteServerError("Error checking if author with id " + follower_id + " is a follower of author with id " +
                                        author_id + " from remote server: https://social-distribution-media-2.herokuapp.com/. Response body was empty.")

            else:
                return {
                    "isFollower": response.get("isFollower", False)
                }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    def get_single_post(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id
        response = self.session.get(url)

        # if the author/post is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id +
                            " not found on remote server: https://social-distribution-media-2.herokuapp.com/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_post = response.json()
                if response_post is None:
                    # TODO: handle error
                    pass

                else:
                    comments = []
                    for comment in response_post.get("commentsSrc", {}).get("comments", []):
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
                            "type": response_post.get("commentsSrc", {}).get("type", "comments"),
                            "page": response_post.get("commentsSrc", {}).get("page", 1),
                            "size": response_post.get("commentsSrc", {}).get("size", 0),
                            "post": response_post.get("commentsSrc", {}).get("post", response_post.get("id", "N/A")),
                            "id": response_post.get("commentsSrc", {}).get("id", response_post.get("id", "N/A") + "/comments"),
                            "comments": comments
                        },
                        "published": response_post.get("published", "N/A"),
                        "visibility": response_post.get("visibility", "N/A"),
                        "unlisted": response_post.get("unlisted", "N/A"),
                    }

            except Exception as e:
                raise RemoteServerError("Error getting post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://social-distribution-media-2.herokuapp.com/; exception " + str(e) + " was thrown.")

    # URL: ://service/authors/{AUTHOR_ID}/posts/
    def get_recent_posts(self, author_id):
        url = self.base_url + "authors/" + author_id + "/posts"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        posts = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the posts we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting recent posts from author with id " + author_id +
                                        " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

            response_posts = response.json()
            if response_posts is None:
                raise RemoteServerError("Error getting recent posts from author with id " + author_id +
                                        " from remote server: https://social-distribution-media-2.herokuapp.com/. Response body was empty.")

            items = response_posts.get("items", [])
            posts.extend(items)
            page += 1

        cleaned_posts = []
        for post in posts:
            comments = []
            for comment in post.get("commentsSrc", {}).get("comments", []):
                comments.append({
                    "type": comment.get("type"),
                    "author": {
                        "type": comment.get("author", {}).get("type"),
                        "id": comment.get("author", {}).get("id"),
                        "host": comment.get("author", {}).get("host"),
                        "displayName": comment.get("author", {}).get("displayName"),
                        "url": comment.get("author", {}).get("url"),
                        "github": comment.get("author", {}).get("github"),
                        "profileImage": comment.get("author", {}).get("profileImage"),
                    },
                    "comment": comment.get("comment"),
                    "contentType": comment.get("contentType"),
                    "published": comment.get("published"),
                    "id": comment.get("id"),
                })

            cleaned_posts.append({
                "type": post.get("type"),
                "title": post.get("title"),
                "id": post.get("id"),
                "source": post.get("source"),
                "origin": post.get("origin"),
                "description": post.get("description"),
                "contentType": post.get("contentType"),
                "content": post.get("content"),
                "author": {
                    "type": post.get("author", {}).get("type"),
                    "id": post.get("author", {}).get("id"),
                    "host": post.get("author", {}).get("host"),
                    "displayName": post.get("author", {}).get("displayName"),
                    "url": post.get("author", {}).get("url"),
                    "github": post.get("author", {}).get("github"),
                    "profileImage": post.get("author", {}).get("profileImage"),
                },
                "categories": post.get("categories"),
                "count": post.get("count"),
                "comments": post.get("comments"),
                "commentsSrc": {
                    "type": post.get("commentsSrc", {}).get("type", "comments"),
                    "page": post.get("commentsSrc", {}).get("page", 1),
                    "size": post.get("commentsSrc", {}).get("size", 0),
                    "post": post.get("commentsSrc", {}).get("post", post.get("id")),
                    "id": post.get("commentsSrc", {}).get("id", post.get("id") + "/comments"),
                    "comments": comments
                },
                "published": post.get("published"),
                "visibility": post.get("visibility"),
                "unlisted": post.get("unlisted"),
            })

        return {
            "type": "posts",
            "items": cleaned_posts,
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
    def get_image_post(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/image"
        response = self.session.get(url)

        # if the post doesn't exist, or isn't an image, throw a 404 exception
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id +
                            " from remote server: https://social-distribution-media-2.herokuapp.com/ does not exist, or is not an image.")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting image post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        # otherwise, return the raw image data and the content type
        else:
            return (response.content, response.headers.get("Content-Type"))

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    def get_comments(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/comments"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        comments = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the comments we have/or the empty list
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting comments for post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

            response_comments = response.json()
            if response_comments is None:
                raise RemoteServerError("Error getting comments for post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://social-distribution-media-2.herokuapp.com/; no JSON was received in response.")

            items = response_comments.get("items")
            comments.extend(items)
            page += 1

        return {
            "type": "comments",
            "items": comments
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    def get_post_likes(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/likes"

        likes = []

        response = self.session.get(url)

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; no JSON was received in response.")

        items = response_likes.get("items")
        likes.extend(items)

        return {
            "type": "likes",
            "items": likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    def get_comment_likes(self, author_id, post_id, comment_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + \
            post_id + "/comments/" + comment_id + "/likes"

        likes = []

        response = self.session.get(url)

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for comment with id " + comment_id + " from post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for comment with id " + comment_id + " from post with id " + post_id + " from author with id " +
                                    author_id + " from remote server: https://social-distribution-media-2.herokuapp.com/; no JSON was received in response.")

        items = response_likes.get("items")
        likes.extend(items)

        return {
            "type": "likes",
            "items": likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/liked
    def get_author_liked(self, author_id):
        url = self.base_url + "authors/" + author_id + "/liked"

        likes = []

        response = self.session.get(url)

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; no JSON was received in response.")

        items = response_likes.get("items")
        likes.extend(items)

        return {
            "type": "likes",
            "items": likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/inbox
    def send_post(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox"
        response = self.session.post(url=url, json=body)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                print("Error parsing response from remote server: https://social-distribution-media-2.herokuapp.com/; status code " +
                      str(response.status_code) + " was received in response.")
                return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_like(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox"
        response = self.session.post(url=url, json=body)

        if response.status_code != 201:
            # TODO: handle error
            # look in cache?
            print("error occurred")
            pass

        else:
            # might wanna return something, parse the response...
            print("sent remotely!")
            return response.json()

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_comment(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox"
        response = self.session.post(url=url, json=body)

        if response.status_code != 201:
            # TODO: handle error
            # look in cache?
            print("error occurred")
            pass

        else:
            # might wanna return something, parse the response...
            print("sent remotely!")
            return response.json()

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_follow(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox"
        response = self.session.post(url=url, json=body)

        if response.status_code != 201:
            # TODO: handle error
            # look in cache?
            print("error occurred")
            pass

        else:
            # might wanna return something, parse the response...
            print("sent remotely!")
            return response.json()


class Team6Connection():
    def __init__(self, username, password, base_url):
        # TODO: configure username, password, and base_url
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = CachedSession(
            "team6_cache", backend="sqlite", expire_after=1)
        self.session.auth = (self.username, self.password)

    # URL: ://service/authors/
    def get_authors(self):

        url = self.base_url + "authors?page=1&size=5000"

        authors = []
        response = self.session.get(url)

        # no need to handle the 404 using an exception, just return the authors we have/or the empty array
        if response.status_code == 404:
            authors = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting authors from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " + str(
                response.status_code) + " was received in response.")

        response_authors = response.json()
        if response_authors is None:
            raise RemoteServerError(
                "Error getting authors from remote server: https://cmput404-group6-instatonne.herokuapp.com/. Response body was empty.")

        items = response_authors.get("items", [])
        authors.extend(items)

        return {
            "type": "authors",
            "items": authors
        }

    # URL: ://service/authors/{author_id}
    def get_single_author(self, author_id):
        url = self.base_url + "authors/" + author_id
        response = self.session.get(url)

        # if the author is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Author with id " + author_id +
                            " not found on remote server: https://cmput404-group6-instatonne.herokuapp.com/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting author with id " + author_id +
                                    " from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_author = response.json()

                # if the response body is empty, throw an exception
                if response_author is None:
                    raise RemoteServerError("Error getting author with id " + author_id +
                                            " from remote server: https://cmput404-group6-instatonne.herokuapp.com/. Response body was empty.")

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

            except Exception as e:
                raise RemoteServerError("Error getting author with id " + author_id +
                                        " from remote server: https://cmput404-group6-instatonne.herokuapp.com/. Exception: " + str(e))

    # URL: ://service/authors/{AUTHOR_ID}/followers
    def get_author_followers(self, author_id):
        url = self.base_url + "authors/" + author_id + "/followers"
        response = self.session.get(url)

        if response.status_code != 200:
            # TODO: handle error
            # look in cache?
            pass

        else:
            response_followers = response.json()
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

    # URL: ://service/authors/{AUTHOR_ID}/followers/{hostencoded}/authors/{FOREIGN_AUTHOR_ID}
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
                for comment in response_post.get("commentsSrc", {}).get("comments", []):
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
                        "type": response_post.get("commentsSrc", {}).get("type", "comments"),
                        "page": response_post.get("commentsSrc", {}).get("page", 1),
                        "size": response_post.get("commentsSrc", {}).get("size", 0),
                        "post": response_post.get("commentsSrc", {}).get("post", response_post.get("id", "N/A")),
                        "id": response_post.get("commentsSrc", {}).get("id", response_post.get("id", "N/A") + "/comments"),
                        "comments": comments
                    },
                    "published": response_post.get("published", "N/A"),
                    "visibility": response_post.get("visibility", "N/A"),
                    "unlisted": response_post.get("unlisted", "N/A"),
                }

    # URL: ://service/authors/{AUTHOR_ID}/posts
    def get_recent_posts(self, author_id):
        url = self.base_url + "authors/" + author_id + "/posts"
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
                    for comment in post.get("commentsSrc", {}).get("comments", []):
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
                            "type": post.get("commentsSrc", {}).get("type", "comments"),
                            "page": post.get("commentsSrc", {}).get("page", 1),
                            "size": post.get("commentsSrc", {}).get("size", 0),
                            "post": post.get("commentsSrc", {}).get("post", post.get("id", "N/A")),
                            "id": post.get("commentsSrc", {}).get("id", post.get("id", "N/A") + "/comments"),
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

        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/comments"
        response = self.session.get(url)

        if response.status_code != 200:
            # TODO: handle error
            # look in cache?
            if response.status_code == 404:
                return []

            else:
                pass

        else:
            response = response.json()
            if response is None:
                # TODO: handle error
                pass

            else:
                comments = []
                for comment in response:
                    comments.append({
                        "type": comment.get("type", "N/A"),
                        "id": comment.get("id", "N/A"),
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
                    })

                return comments

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    def get_post_likes(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/likes"
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
                likes = []
                for like in response:
                    likes.append({
                        "type": like.get("type", "N/A"),
                        "summary": like.get("summary", "N/A"),
                        "author": {
                            "type": like.get("author", {}).get("type", "N/A"),
                            "id": like.get("author", {}).get("id", "N/A"),
                            "host": like.get("author", {}).get("host", "N/A"),
                            "displayName": like.get("author", {}).get("displayName", "N/A"),
                            "url": like.get("author", {}).get("url", "N/A"),
                            "github": like.get("author", {}).get("github", "N/A"),
                            "profileImage": like.get("author", {}).get("profileImage", "N/A"),
                        },
                        "object": like.get("object", "N/A"),
                    })

                return likes

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    def get_comment_likes(self, author_id, post_id, comment_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + \
            post_id + "/comments/" + comment_id + "/likes"
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
                likes = []
                for like in response:
                    likes.append({
                        "type": like.get("type", "N/A"),
                        "summary": like.get("summary", "N/A"),
                        "author": {
                            "type": like.get("author", {}).get("type", "N/A"),
                            "id": like.get("author", {}).get("id", "N/A"),
                            "host": like.get("author", {}).get("host", "N/A"),
                            "displayName": like.get("author", {}).get("displayName", "N/A"),
                            "url": like.get("author", {}).get("url", "N/A"),
                            "github": like.get("author", {}).get("github", "N/A"),
                            "profileImage": like.get("author", {}).get("profileImage", "N/A"),
                        },
                        "object": like.get("object", "N/A"),
                    })

                return likes

    # URL: ://service/authors/{hostencoded}/authors/{AUTHOR_ID}/liked
    def get_author_liked(self, author_id):
        url = self.base_url + "authors/" + author_id + "/liked"
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
                likes = []
                for like in response:
                    likes.append({
                        "type": like.get("type", "N/A"),
                        "author": {
                            "type": like.get("author", {}).get("type", "N/A"),
                            "id": like.get("author", {}).get("id", "N/A"),
                            "host": like.get("author", {}).get("host", "N/A"),
                            "displayName": like.get("author", {}).get("displayName", "N/A"),
                            "url": like.get("author", {}).get("url", "N/A"),
                            "github": like.get("author", {}).get("github", "N/A"),
                            "profileImage": like.get("author", {}).get("profileImage", "N/A"),
                        },
                        "object": like.get("object", "N/A"),
                    })

                return likes

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_post(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox/"

        cleaned_body = {
            "type": body.get("object", {}).get("type", "").lower(),
            "id": body.get("object", {}).get("id", ""),
            "title": body.get("object", {}).get("title", ""),
            "source": body.get("object", {}).get("source", ""),
            "origin": body.get("object", {}).get("origin", ""),
            "description": body.get("object", {}).get("description", ""),
            "contentType": body.get("object", {}).get("contentType", ""),
            "content": body.get("object", {}).get("content", ""),
            "author": {
                "type": body.get("object", {}).get("author", {}).get("type", "").lower(),
                "id": body.get("object", {}).get("author", {}).get("id", ""),
                "host": body.get("object", {}).get("author", {}).get("host", ""),
                "displayName": body.get("object", {}).get("author", {}).get("displayName", ""),
                "url": body.get("object", {}).get("author", {}).get("url", ""),
                "github": body.get("object", {}).get("author", {}).get("github", ""),
                "profileImage": body.get("object", {}).get("author", {}).get("profileImage", ""),
            },
            "categories": body.get("object", {}).get("categories", []),
            "count": body.get("object", {}).get("count", 0),
            "comments": body.get("object", {}).get("comments", []),
            "commentsSrc": body.get("object", {}).get("commentsSrc", {}),
            "published": body.get("object", {}).get("published", ""),
            "visibility": body.get("object", {}).get("visibility", ""),
            "unlisted": body.get("object", {}).get("unlisted", False),
        }

        print(cleaned_body)

        response = self.session.post(url=url, json=cleaned_body)

        if response.status_code != 200 and response.status_code != 201 and response.status_code != 204:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201/204, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
                    return {"success": True}

                else:
                    print("Error parsing response from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_like(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox/"

        # Team 6's like POST body is a little different, less redundant w/ the object field, no context attribute
        cleaned_body = {
            "summary": body.get("summary", ""),
            "type": body.get("type", ""),
            "author": {
                "type": body.get("author", {}).get("type", ""),
                "id": body.get("author", {}).get("id", ""),
                "host": body.get("author", {}).get("host", ""),
                "displayName": body.get("author", {}).get("displayName", ""),
                "url": body.get("author", {}).get("url", ""),
                "github": body.get("author", {}).get("github", ""),
                "profileImage": body.get("author", {}).get("profileImage, """),
            },
            "object": body.get("object", {}).get("object", "")
        }

        print(cleaned_body)

        response = self.session.post(url=url, json=cleaned_body)

        if response.status_code != 200 and response.status_code != 201 and response.status_code != 204:
            raise RemoteServerError("Error sending like to author with id " + author_id +
                                    " from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201/204, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
                    return {"success": True}

                else:
                    print("Error parsing response from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " +
                        str(response.status_code) + " was received in response.")
                    return None
        

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_comment(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox/"

        cleaned_comment = {
            "type": "comment",
            "contentType": body.get("object", {}).get("contentType", ""),
            "comment": body.get("object", {}).get("comment", ""),
            "author": body.get("object", {}).get("author", {}),
            "post": body.get("object", {}).get("id", "").split("/comments/")[0]
        }

        print(cleaned_comment)

        response = self.session.post(url=url, json=cleaned_comment)

        if response.status_code != 200 and response.status_code != 201 and response.status_code != 204:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
                    return None

                else:
                    print("Error parsing response from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_follow(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox/"
        response = self.session.post(url=url, json=body)

        if response.status_code != 200 and response.status_code != 201 and response.status_code != 204:
            raise RemoteServerError("Error sending follow to author with id " + author_id +
                                    " from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
                    return {"success": True}

                else:
                    print("Error parsing response from remote server: https://cmput404-group6-instatonne.herokuapp.com/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None


class Team10Connection():
    def __init__(self, username, password, base_url):
        # TODO: configure username, password, and base_url
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = CachedSession(
            "team10_cache", backend="sqlite", expire_after=1)

        # This team uses token auth, need to add it to each individual request 

    # URL: ://service/authors/
    def get_authors(self):
        url = self.base_url + "api/authors"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        authors = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10}, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

            # no need to handle the 404 using an exception, just return the authors we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting authors from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(
                    response.status_code) + " was received in response.")

            response_authors = response.json()
            if response_authors is None:
                raise RemoteServerError(
                    "Error getting authors from remote server: https://socialdistcmput404.herokuapp.com/api/. Response body was empty.")

            items = response_authors.get("items", [])

            # if there are no items, we've reached the end of the list
            if len(items) == 0:
                break

            else:
                authors.extend(items)
                page += 1

        return {
            "type": "authors",
            "items": authors
        }

    # URL: ://service/authors/{AUTHOR_ID}/
    def get_single_author(self, author_id):
        url = self.base_url + "api/authors/" + author_id
        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        # if the author is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Author with id " + author_id +
                            " not found on remote server: https://socialdistcmput404.herokuapp.com/api/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_author = response.json()

                # if the response body is empty, throw an exception
                if response_author is None:
                    raise RemoteServerError("Error getting author with id " + author_id +
                                            " from remote server: https://socialdistcmput404.herokuapp.com/api/. Response body was empty.")

                else:
                    return response_author

            except Exception as e:
                raise RemoteServerError("Error getting author with id " + author_id +
                                        " from remote server: https://socialdistcmput404.herokuapp.com/api/. Exception: " + str(e))

    # URL: ://service/authors/{AUTHOR_ID}/followers
    def get_author_followers(self, author_id):
        url = self.base_url + "api/authors/" + author_id + "/followers"
        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        # if the author is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Author with id " + author_id +
                            " not found on remote server: https://socialdistcmput404.herokuapp.com/api/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting followers for author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_followers = response.json().get("items", [])
                if response_followers is None:
                    raise RemoteServerError("Error getting followers for author with id " + author_id +
                                            " from remote server: https://socialdistcmput404.herokuapp.com/api/. Response body was empty.")

                else:
                    cleaned_followers = []
                    for author in response_followers:
                        cleaned_followers.append({
                            "type": author.get("type"),
                            "id": author.get("id"),
                            "url": author.get("url"),
                            "host": author.get("host"),
                            "displayName": author.get("displayName"),
                            "github": author.get("github"),
                            "profileImage": author.get("profileImage"),
                        })

                    return {
                        "type": "followers",
                        "items": cleaned_followers
                    }

            except Exception as e:
                raise RemoteServerError("Error getting followers for author with id " + author_id +
                                        " from remote server: https://socialdistcmput404.herokuapp.com/api/. Exception: " + str(e))

    # URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    def check_if_follower(self, author_id, follower_id):
        url = self.base_url + "api/authors/" + author_id + "/followers/" + follower_id
        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        if response.status_code != 200:
            return {
                "isFollower": False
            }

        else:
            return {
                "isFollower": True
            }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    def get_single_post(self, author_id, post_id):
        url = self.base_url + "api/authors/" + author_id + "/posts/" + post_id
        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        # if the author/post is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id +
                            " not found on remote server: https://socialdistcmput404.herokuapp.com/api/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_post = response.json()
                if response_post is None:
                    raise RemoteServerError("Error getting post with id " + post_id + " from author with id " +
                                            author_id + " from remote server: https://socialdistcmput404.herokuapp.com/api/. Response body was empty.")

                else:
                    comments = []
                    for comment in response_post.get("commentsSrc", {}).get("comments", []):
                        comments.append({
                            "type": comment.get("type", ""),
                            "author": {
                                "type": comment.get("author", {}).get("type", ""),
                                "id": comment.get("author", {}).get("id", ""),
                                "host": comment.get("author", {}).get("host", ""),
                                "displayName": comment.get("author", {}).get("displayName", ""),
                                "url": comment.get("author", {}).get("url", ""),
                                "github": comment.get("author", {}).get("github", ""),
                                "profileImage": comment.get("author", {}).get("profileImage", ""),
                            },
                            "comment": comment.get("comment", ""),
                            "contentType": comment.get("contentType", ""),
                            "published": comment.get("published", ""),
                            "id": comment.get("id", ""),
                        })

                    return {
                        "type": response_post.get("type", ""),
                        "title": response_post.get("title", ""),
                        "id": response_post.get("id", ""),
                        "source": response_post.get("source", ""),
                        "origin": response_post.get("origin", ""),
                        "description": response_post.get("description", ""),
                        "contentType": response_post.get("contentType", ""),
                        "content": response_post.get("content", ""),
                        "author": {
                            "type": response_post.get("author", {}).get("type", ""),
                            "id": response_post.get("author", {}).get("id", ""),
                            "host": response_post.get("author", {}).get("host", ""),
                            "displayName": response_post.get("author", {}).get("displayName", ""),
                            "url": response_post.get("author", {}).get("url", ""),
                            "github": response_post.get("author", {}).get("github", ""),
                            "profileImage": response_post.get("author", {}).get("profileImage", ""),
                        },
                        "categories": response_post.get("categories", ""),
                        "count": response_post.get("count", ""),
                        "comments": response_post.get("comments", ""),
                        "commentsSrc": {
                            "type": response_post.get("commentsSrc", {}).get("type", ""),
                            "page": response_post.get("commentsSrc", {}).get("page", 1),
                            "size": response_post.get("commentsSrc", {}).get("size", 0),
                            "post": response_post.get("commentsSrc", {}).get("post", response_post.get("id", "")),
                            "id": response_post.get("commentsSrc", {}).get("id", response_post.get("id", "") + "/comments"),
                            "comments": comments
                        },
                        "published": response_post.get("published", ""),
                        "visibility": response_post.get("visibility", ""),
                        "unlisted": response_post.get("unlisted", ""),
                    }

            except Exception as e:
                raise RemoteServerError("Error getting post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://socialdistcmput404.herokuapp.com/api/; exception " + str(e) + " was thrown.")

    # URL: ://service/authors/{AUTHOR_ID}/posts/
    def get_recent_posts(self, author_id):
        url = self.base_url + "api/authors/" + author_id + "/posts"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        posts = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10}, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

            # no need to handle the 404 using an exception, just return the posts we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting recent posts from author with id " + author_id +
                                        " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

            response_posts = response.json()
            if response_posts is None:
                raise RemoteServerError("Error getting recent posts from author with id " + author_id +
                                        " from remote server: https://socialdistcmput404.herokuapp.com/api/. Response body was empty.")

            items = response_posts.get("items", [])

            if len(items) == 0:
                break

            else:
                posts.extend(items)
                page += 1

        cleaned_posts = []
        for post in posts:
            comments = []
            for comment in post.get("commentsSrc", {}).get("comments", []):
                comments.append({
                    "type": comment.get("type", ""),
                    "author": {
                        "type": comment.get("author", {}).get("type", ""),
                        "id": comment.get("author", {}).get("id", ""),
                        "host": comment.get("author", {}).get("host", ""),
                        "displayName": comment.get("author", {}).get("displayName", ""),
                        "url": comment.get("author", {}).get("url", ""),
                        "github": comment.get("author", {}).get("github", ""),
                        "profileImage": comment.get("author", {}).get("profileImage", ""),
                    },
                    "comment": comment.get("comment", ""),
                    "contentType": comment.get("contentType", ""),
                    "published": comment.get("published", ""),
                    "id": comment.get("id", ""),
                })

            cleaned_posts.append({
                "type": post.get("type", ""),
                "title": post.get("title", ""),
                "id": post.get("id", ""),
                "source": post.get("source", ""),
                "origin": post.get("origin", ""),
                "description": post.get("description", ""),
                "contentType": post.get("contentType", ""),
                "content": post.get("content", ""),
                "author": {
                    "type": post.get("author", {}).get("type", ""),
                    "id": post.get("author", {}).get("id", ""),
                    "host": post.get("author", {}).get("host", ""),
                    "displayName": post.get("author", {}).get("displayName", ""),
                    "url": post.get("author", {}).get("url", ""),
                    "github": post.get("author", {}).get("github", ""),
                    "profileImage": post.get("author", {}).get("profileImage", ""),
                },
                "categories": post.get("categories", ""),
                "count": post.get("count", 0),
                "comments": post.get("comments", ""),
                "commentsSrc": {
                    "type": post.get("commentsSrc", {}).get("type", ""),
                    "page": post.get("commentsSrc", {}).get("page", 1),
                    "size": post.get("commentsSrc", {}).get("size", 0),
                    "post": post.get("commentsSrc", {}).get("post", ""),
                    "id": post.get("commentsSrc", {}).get("id", post.get("id", "") + "/comments"),
                    "comments": comments
                },
                "published": post.get("published", ""),
                "visibility": post.get("visibility", ""),
                "unlisted": post.get("unlisted", ""),
            })

        return {
            "type": "posts",
            "items": cleaned_posts,
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
    def get_image_post(self, author_id, post_id):
        url = self.base_url + "api/authors/" + author_id + "/posts/" + post_id + "/image"
        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})
        # if the post doesn't exist, or isn't an image, throw a 404 exception
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id +
                            " from remote server: https://socialdistcmput404.herokuapp.com/api/ does not exist, or is not an image.")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting image post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        # otherwise, return pull out the base64 string, and turn it into binary
        else:
            binary = response.content
            return (binary, "image/png")

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    def get_comments(self, author_id, post_id):
        url = self.base_url + "api/authors/" + author_id + "/posts/" + post_id + "/comments"

        # DON'T DO PAGINATION FOR THEM -- IT'S BORKNE
        page = 1
        comments = []
        
        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        # no need to handle the 404 using an exception, just return the comments we have/or the empty list
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id + " from remote server: https://socialdistcmput404.herokuapp.com/api/ does not exist.")

        elif response.status_code != 200:
            raise RemoteServerError("Error getting comments for post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        response_comments = response.json()
        if response_comments is None:
            raise RemoteServerError("Error getting comments for post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; no JSON was received in response.")

        items = response_comments.get("items", [])
        comments.extend(items)

        cleaned_comments = []
        for comment in comments:
            cleaned_comments.append({
                "type": comment.get("type", ""),
                "author": {
                    "type": comment.get("author", {}).get("type", ""),
                    "id": comment.get("author", {}).get("id", ""),
                    "host": comment.get("author", {}).get("host", ""),
                    "displayName": comment.get("author", {}).get("displayName", ""),
                    "url": comment.get("author", {}).get("url", ""),
                    "github": comment.get("author", {}).get("github", ""),
                    "profileImage": comment.get("author", {}).get("profileImage", ""),
                },
                "comment": comment.get("comment", "Empty comment."),
                "contentType": comment.get("contentType", ""),
                "published": comment.get("published", ""),
                "id": comment.get("id", ""),
            })

        return {
            "type": "comments",
            "items": cleaned_comments
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    def get_post_likes(self, author_id, post_id):
        url = self.base_url + "api/authors/" + author_id + "/posts/" + post_id + "/likes"

        likes = []

        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; no JSON was received in response.")

        items = response_likes.get("items", [])
        likes.extend(items)

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    def get_comment_likes(self, author_id, post_id, comment_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + \
            post_id + "api/comments/" + comment_id + "/likes"

        likes = []

        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for comment with id " + comment_id + " from post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for comment with id " + comment_id + " from post with id " + post_id + " from author with id " +
                                    author_id + " from remote server: https://socialdistcmput404.herokuapp.com/api/; no JSON was received in response.")

        items = response_likes.get("items")
        likes.extend(items)

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/liked
    def get_author_liked(self, author_id):
        url = self.base_url + "api/authors/" + author_id + "/liked"

        likes = []

        response = self.session.get(url, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; no JSON was received in response.")

        items = response_likes.get("items")
        likes.extend(items)

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/inbox
    def send_post(self, author_id, body):
        url = self.base_url + "api/authors/" + author_id + "/inbox/"

        # need to strip out "data" portion of image before sending
        content = body.get("object", {}).get("content", "")
        if content.startswith("data"):
            content = content.split(",")[1]

        cleaned_body = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": body.get("summary", ""),
            "type": body.get("object", {}).get("type", "").lower(),
            "id": body.get("object", {}).get("id", ""),
            "title": body.get("object", {}).get("title", ""),
            "source": "https://social-distribution-media.herokuapp.com",
            "origin": "https://social-distribution-media.herokuapp.com",
            "description": body.get("object", {}).get("description", ""),
            "contentType": body.get("object", {}).get("contentType", ""),
            "content": content,
            "author": {
                "type": body.get("object", {}).get("author", {}).get("type", "").lower(),
                "id": body.get("object", {}).get("author", {}).get("id", ""),
                "host": body.get("object", {}).get("author", {}).get("host", ""),
                "displayName": body.get("object", {}).get("author", {}).get("displayName", ""),
                "url": body.get("object", {}).get("author", {}).get("url", ""),
                "github": body.get("object", {}).get("author", {}).get("github", ""),
                "profileImage": body.get("object", {}).get("author", {}).get("profileImage", ""),
            },
            "categories": ",".join(body.get("object", {}).get("categories", [])),
            "count": body.get("object", {}).get("count", 0),
            "comments": body.get("object", {}).get("comments", []),
            "commentsSrc": body.get("object", {}).get("commentsSrc", {}),
            "published": "2023-03-28T04:42:14.478355Z",
            "visibility": "VISIBLE",
            "unlisted": body.get("object", {}).get("unlisted", False),
        }

        print(cleaned_body)

        response = self.session.post(url=url, json=cleaned_body, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201:
                    return {"success": True}

                else:
                    print("Error parsing response from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_like(self, author_id, body):
        url = self.base_url + "api/authors/" + author_id + "/inbox/"

        cleaned_body = {
            "@context": body.get("@context", ""),
            "summary": body.get("summary", ""),
            "type": "Like", # needs to have uppercase L
            "author": body.get("author", {}),
            "object": body.get("object", {}).get("object", "")
        }

        response = self.session.post(url=url, json=cleaned_body, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201:
                    return None

                else:
                    print("Error parsing response from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_comment(self, author_id, body):
        url = self.base_url + "api/authors/" + author_id + "/inbox/"

        cleaned_body = {
            "id": body.get("object", {}).get("id", ""),
            "type": "comment",
            "comment": body.get("object", {}).get("comment", ""),
            "contentType": body.get("object", {}).get("contentType", ""),
            "author": {
                "id": body.get("actor", {}).get("id", ""),
                "host": body.get("actor", {}).get("host", ""),
                "displayName": body.get("actor", {}).get("displayName", ""),
                "url": body.get("actor", {}).get("url", ""),
                "github": body.get("actor", {}).get("github", ""),
                "profileImage": body.get("actor", {}).get("profileImage", ""),
            }
        }

        print(cleaned_body)

        response = self.session.post(url=url, json=cleaned_body, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201:
                    return None

                else:
                    print("Error parsing response from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_follow(self, author_id, body):
        url = self.base_url + "api/authors/" + author_id + "/inbox/"

        cleaned_body = {
            "type": "Follow", # needs to be capital F
            "summary": body.get("summary", ""),
            "actor": body.get("actor", ""),
            "object": body.get("object", "")
        }

        response = self.session.post(url=url, json=cleaned_body, headers={"Authorization": "Token E579D1E284A7C283C9E2E74C6C2F001D977186FA"})

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201:
                    return {"success": True}

                else:
                    print("Error parsing response from remote server: https://socialdistcmput404.herokuapp.com/api/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None


class Team11Connection():
    def __init__(self, username, password, base_url):
        # TODO: configure username, password, and base_url
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = CachedSession(
            "team11_cache", backend="sqlite", expire_after=1)
        self.session.auth = (self.username, self.password)

    # URL: ://service/authors/
    def get_authors(self):
        url = self.base_url + "authors"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        authors = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the authors we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting authors from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(
                    response.status_code) + " was received in response.")

            response_authors = response.json()
            if response_authors is None:
                raise RemoteServerError(
                    "Error getting authors from remote server: https://quickcomm-dev1.herokuapp.com/. Response body was empty.")

            items = response_authors.get("items", [])
            authors.extend(items)
            page += 1

        # their server can sometimes return null values, so convert them to empty strings
        cleaned_authors = []
        for author in authors:
            cleaned_authors.append({
                "type": author.get("type").lower() if author.get("type") != None else "",
                "id": author.get("id") if author.get("type") != None else "",
                "host": author.get("host") if author.get("host") != None else "",
                "displayName": author.get("displayName") if author.get("displayName") != None else "",
                "url": author.get("url") if author.get("url") != None else "",
                "github": author.get("github") if author.get("github") != None else "",
                "profileImage": author.get("profileImage") if author.get("profileImage") != None else "",
            })

        return {
            "type": "authors",
            "items": cleaned_authors
        }

    # URL: ://service/authors/{AUTHOR_ID}/
    def get_single_author(self, author_id):
        url = self.base_url + "authors/" + author_id
        response = self.session.get(url)

        print(url)
        print(response.json())

        # if the author is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Author with id " + author_id +
                            " not found on remote server: https://quickcomm-dev1.herokuapp.com/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting author with id " + author_id +
                                    " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_author = response.json()

                # if the response body is empty, throw an exception
                if response_author is None:
                    raise RemoteServerError("Error getting author with id " + author_id +
                                            " from remote server: https://quickcomm-dev1.herokuapp.com/. Response body was empty.")

                if response_author.get("type") == "authors":
                    raise RemoteServerError(
                        "Error getting author details from remote server: https://quickcomm-dev1.herokuapp.com/. Invalid proxy usage -- make sure you specify a valid UUID.")

                else:
                    return {
                        "type": response_author.get("type").lower() if response_author.get("type") != None else "",
                        "id": response_author.get("id") if response_author.get("id") != None else "",
                        "host": response_author.get("host") if response_author.get("host") != None else "",
                        "displayName": response_author.get("displayName") if response_author.get("displayName") != None else "",
                        "url": response_author.get("url") if response_author.get("url") != None else "",
                        "github": response_author.get("github") if response_author.get("github") != None else "",
                        "profileImage": response_author.get("github") if response_author.get("github") != None else "",
                    }

            except Exception as e:
                raise RemoteServerError("Error getting author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/. Exception: " + str(e))

    # URL: ://service/authors/{AUTHOR_ID}/followers
    def get_author_followers(self, author_id):
        url = self.base_url + "authors/" + author_id + "/followers"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case their server throws a 404
        page = 1
        followers = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the followers we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting followers for author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

            response_followers = response.json()
            if response_followers is None:
                raise RemoteServerError("Error getting followers for author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/. Response body was empty.")

            items = response_followers.get("items", [])
            followers.extend(items)
            page += 1

        # their server can sometimes return null values, so convert them to empty strings
        cleaned_followers = []
        for author in followers:
            cleaned_followers.append({
                "type": author.get("type").lower() if author.get("type") != None else "",
                "id": author.get("id") if author.get("type") != None else "",
                "host": author.get("host") if author.get("host") != None else "",
                "displayName": author.get("displayName") if author.get("displayName") != None else "",
                "url": author.get("url") if author.get("url") != None else "",
                "github": author.get("github") if author.get("github") != None else "",
                "profileImage": author.get("profileImage") if author.get("profileImage") != None else "",
            })

        return {
            "type": "followers",
            "items": cleaned_followers
        }

    # URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    def check_if_follower(self, author_id, follower_id):
        url = self.base_url + "authors/" + author_id + "/followers/" + follower_id
        response = self.session.get(url)

        # if we got a 404, means they are not a follower, or they don't exist
        if response.status_code == 404:
            return {
                "isFollower": False
            }

        elif response.status_code != 200:
            raise RemoteServerError("Error checking if author with id " + follower_id + " is a follower of author with id " + author_id +
                                    " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            response = response.json()
            if response is None:
                raise RemoteServerError("Error checking if author with id " + follower_id + " is a follower of author with id " +
                                        author_id + " from remote server: https://quickcomm-dev1.herokuapp.com/. Response body was empty.")

            # if we got a 200, means they are a follower
            else:
                return {
                    "isFollower": True
                }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    def get_single_post(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id
        response = self.session.get(url)

        # if the author/post is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id +
                            " not found on remote server: https://quickcomm-dev1.herokuapp.com/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_post = response.json()
                if response_post is None:
                    raise RemoteServerError("Error getting post with id " + post_id + " from author with id " +
                                            author_id + " from remote server: https://quickcomm-dev1.herokuapp.com/. Response body was empty.")

                else:
                    comments = []
                    for comment in response_post.get("commentsSrc", {}).get("comments", []):
                        comments.append({
                            "type": comment.get("type").lower() if comment.get("type") != None else "",
                            "author": {
                                "type": comment.get("author", {}).get("type").lower() if comment.get("author", {}).get("type") != None else "",
                                "id": comment.get("author", {}).get("id") if comment.get("author", {}).get("id") != None else "",
                                "host": comment.get("author", {}).get("host") if comment.get("author", {}).get("host") != None else "",
                                "displayName": comment.get("author", {}).get("displayName") if comment.get("author", {}).get("displayName") != None else "",
                                "url": comment.get("author", {}).get("url") if comment.get("author", {}).get("url") != None else "",
                                "github": comment.get("author", {}).get("github") if comment.get("author", {}).get("github") != None else "",
                                "profileImage": comment.get("author", {}).get("profileImage") if comment.get("author", {}).get("profileImage") != None else "",
                            },
                            "comment": comment.get("comment") if comment.get("comment") != None else "",
                            "contentType": comment.get("commentType") if comment.get("commentType") != None else "",
                            "published": comment.get("published") if comment.get("published") != None else "",
                            "id": comment.get("id") if comment.get("id") != None else "",
                        })

                    return {
                        "type": response_post.get("type").lower() if response_post.get("type") != None else "",
                        "title": response_post.get("title") if response_post.get("title") != None else "",
                        "id": response_post.get("id") if response_post.get("id") != None else "",
                        "source": response_post.get("source") if response_post.get("source") != None else "",
                        "origin": response_post.get("origin") if response_post.get("origin") != None else "",
                        "description": response_post.get("description") if response_post.get("description") != None else "",
                        "contentType": response_post.get("contentType") if response_post.get("contentType") != None else "",
                        "content": response_post.get("content") if response_post.get("content") != None else "",
                        "author": {
                            "type": response_post.get("author", {}).get("type").lower() if response_post.get("author", {}).get("type") != None else "",
                            "id": response_post.get("author", {}).get("id") if response_post.get("author", {}).get("id") != None else "",
                            "host": response_post.get("author", {}).get("host") if response_post.get("author", {}).get("host") != None else "",
                            "displayName": response_post.get("author", {}).get("displayName") if response_post.get("author", {}).get("displayName") != None else "",
                            "url": response_post.get("author", {}).get("url") if response_post.get("author", {}).get("url") != None else "",
                            "github": response_post.get("author", {}).get("url") if response_post.get("author", {}).get("url") != None else "",
                            "profileImage": response_post.get("author", {}).get("url") if response_post.get("author", {}).get("url") != None else "",
                        },
                        "categories": response_post.get("categories") if response_post.get("categories") != None else "",
                        "count": response_post.get("categories") if response_post.get("categories") != None else "",
                        "comments": response_post.get("comments") if response_post.get("comments") != None else "",
                        "commentsSrc": {
                            "type": response_post.get("commentsSrc", {}).get("type").lower() if response_post.get("commentsSrc", {}).get("type") != None else "",
                            "page": response_post.get("commentsSrc", {}).get("page") if response_post.get("commentsSrc", {}).get("page") != None else "",
                            "size": response_post.get("commentsSrc", {}).get("size") if response_post.get("commentsSrc", {}).get("size") != None else "",
                            "post": response_post.get("commentsSrc", {}).get("post") if response_post.get("commentsSrc", {}).get("post") != None else "",
                            "id": response_post.get("commentsSrc", {}).get("id") if response_post.get("commentsSrc", {}).get("id") != None else "",
                            "comments": comments
                        },
                        "published": response_post.get("published") if response_post.get("published") != None else "",
                        "visibility": response_post.get("visibility") if response_post.get("visibility") != None else "",
                        "unlisted": response_post.get("unlisted") if response_post.get("unlisted") != None else "",
                    }

            except Exception as e:
                raise RemoteServerError("Error getting post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://social-distribution-media-2.herokuapp.com/; exception " + str(e) + " was thrown.")

    # URL: ://service/authors/{AUTHOR_ID}/posts/
    def get_recent_posts(self, author_id):
        url = self.base_url + "authors/" + author_id + "/posts"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        posts = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the posts we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting recent posts from author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

            response_posts = response.json()
            if response_posts is None:
                raise RemoteServerError("Error getting recent posts from author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/. Response body was empty.")

            items = response_posts.get("items", [])
            posts.extend(items)
            page += 1

        cleaned_posts = []
        for post in posts:
            comments = []
            for comment in post.get("commentsSrc", {}).get("comments", []):
                comments.append({
                    "type": comment.get("type").lower() if comment.get("type") != None else "",
                    "author": {
                        "type": comment.get("author", {}).get("type").lower() if comment.get("author", {}).get("type") != None else "",
                        "id": comment.get("author", {}).get("id") if comment.get("author", {}).get("id") != None else "",
                        "host": comment.get("author", {}).get("host") if comment.get("author", {}).get("host") != None else "",
                        "displayName": comment.get("author", {}).get("displayName") if comment.get("author", {}).get("displayName") != None else "",
                        "url": comment.get("author", {}).get("url") if comment.get("author", {}).get("url") != None else "",
                        "github": comment.get("author", {}).get("github") if comment.get("author", {}).get("github") != None else "",
                        "profileImage": comment.get("author", {}).get("profileImage") if comment.get("author", {}).get("profileImage") != None else "",
                    },
                    "comment": comment.get("comment") if comment.get("comment") != None else "",
                    "contentType": comment.get("commentType") if comment.get("commentType") != None else "",
                    "published": comment.get("published") if comment.get("published") != None else "",
                    "id": comment.get("id") if comment.get("id") != None else "",
                })

            cleaned_posts.append({
                "type": post.get("type").lower() if post.get("type") != None else "",
                "title": post.get("title") if post.get("title") != None else "",
                "id": post.get("id") if post.get("id") != None else "",
                "source": post.get("source") if post.get("source") != None else "",
                "origin": post.get("origin") if post.get("origin") != None else "",
                "description": post.get("description") if post.get("description") != None else "",
                "contentType": post.get("contentType") if post.get("contentType") != None else "",
                "content": post.get("content") if post.get("content") != None else "",
                "author": {
                    "type": post.get("author", {}).get("type").lower() if post.get("author", {}).get("type") != None else "",
                    "id": post.get("author", {}).get("id") if post.get("author", {}).get("id") != None else "",
                    "host": post.get("author", {}).get("host") if post.get("author", {}).get("host") != None else "",
                    "displayName": post.get("author", {}).get("displayName") if post.get("author", {}).get("displayName") != None else "",
                    "url": post.get("author", {}).get("url") if post.get("author", {}).get("url") != None else "",
                    "github": post.get("author", {}).get("url") if post.get("author", {}).get("url") != None else "",
                    "profileImage": post.get("author", {}).get("url") if post.get("author", {}).get("url") != None else "",
                },
                "categories": post.get("categories") if post.get("categories") != None else "",
                "count": post.get("categories") if post.get("categories") != None else "",
                "comments": post.get("comments") if post.get("comments") != None else "",
                "commentsSrc": {
                    "type": post.get("commentsSrc", {}).get("type").lower() if post.get("commentsSrc", {}).get("type") != None else "",
                    "page": post.get("commentsSrc", {}).get("page") if post.get("commentsSrc", {}).get("page") != None else "",
                    "size": post.get("commentsSrc", {}).get("size") if post.get("commentsSrc", {}).get("size") != None else "",
                    "post": post.get("commentsSrc", {}).get("post") if post.get("commentsSrc", {}).get("post") != None else "",
                    "id": post.get("commentsSrc", {}).get("id") if post.get("commentsSrc", {}).get("id") != None else "",
                    "comments": comments
                },
                "published": post.get("published") if post.get("published") != None else "",
                "visibility": post.get("visibility") if post.get("visibility") != None else "",
                "unlisted": post.get("unlisted") if post.get("unlisted") != None else "",
            })

        return {
            "type": "posts",
            "items": cleaned_posts,
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
    def get_image_post(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/image"
        response = self.session.get(url)

        # if the post doesn't exist, or isn't an image, throw a 404 exception
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id +
                            " from remote server: https://social-distribution-media-2.herokuapp.com/ does not exist, or is not an image.")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting image post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://social-distribution-media-2.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        # otherwise, return the raw image data and the content type
        else:
            return (response.content, response.headers.get("Content-Type"))

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    def get_comments(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/comments"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case their server throws a 404
        page = 1
        comments = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the comments we have/or the empty list
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting comments for post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

            response_comments = response.json()
            if response_comments is None:
                raise RemoteServerError("Error getting comments for post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; no JSON was received in response.")

            items = response_comments.get("comments")
            comments.extend(items)
            page += 1

        cleaned_comments = []
        for comment in comments:
            cleaned_comments.append({
                "type": comment.get("type").lower() if comment.get("type") != None else "",
                "author": {
                    "type": comment.get("author", {}).get("type") if comment.get("author", {}).get("type") != None else "",
                    "id": comment.get("author", {}).get("id") if comment.get("author", {}).get("id") != None else "",
                    "host": comment.get("author", {}).get("host") if comment.get("author", {}).get("host") != None else "",
                    "displayName": comment.get("author", {}).get("displayName") if comment.get("author", {}).get("displayName") != None else "",
                    "url": comment.get("author", {}).get("url") if comment.get("author", {}).get("url") != None else "",
                    "github": comment.get("author", {}).get("github") if comment.get("author", {}).get("github") != None else "",
                    "profileImage": comment.get("author", {}).get("profileImage") if comment.get("author", {}).get("profileImage") != None else "",
                },
                "comment": comment.get("comment") if comment.get("comment") != None else "",
                "contentType": comment.get("commentType") if comment.get("commentType") != None else "",
                "published": comment.get("published") if comment.get("published") != None else "",
                "id": comment.get("id") if comment.get("id") != None else "",
            })

        return {
            "type": "comments",
            "items": cleaned_comments
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    def get_post_likes(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/likes"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case their server throws a 404
        page = 1
        likes = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the likes we have/or the empty list
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting likes for post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

            response_likes = response.json()
            if response_likes is None:
                raise RemoteServerError("Error getting likes for post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; no JSON was received in response.")

            items = response_likes.get("items")
            likes.extend(items)
            page += 1

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    def get_comment_likes(self, author_id, post_id, comment_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + \
            post_id + "/comments/" + comment_id + "/likes"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case their server throws a 404
        page = 1
        likes = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the likes we have/or the empty list
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting likes for comment with id " + comment_id + " from post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

            response_likes = response.json()
            if response_likes is None:
                raise RemoteServerError("Error getting likes for comment with id " + comment_id + " from post with id " + post_id + " from author with id " +
                                        author_id + " from remote server: https://quickcomm-dev1.herokuapp.com/; no JSON was received in response.")

            items = response_likes.get("items")
            likes.extend(items)
            page += 1

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/liked
    def get_author_liked(self, author_id):
        url = self.base_url + "authors/" + author_id + "/liked"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case their server throws a 404
        page = 1
        likes = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the likes we have/or the empty list
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting likes for author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

            response_likes = response.json()
            if response_likes is None:
                raise RemoteServerError("Error getting likes for author with id " + author_id +
                                        " from remote server: https://quickcomm-dev1.herokuapp.com/; no JSON was received in response.")

            items = response_likes.get("items")
            likes.extend(items)
            page += 1

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/inbox
    def send_post(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox/"

        # need to strip out "data" portion of image before sending
        content = body.get("object", {}).get("content", "")
        if content.startswith("data"):
            content = content.split(",")[1]

        cleaned_body = {
            "@context": body.get("@context") if body.get("@context") != "" else "https://google.com",
            "summary": body.get("summary") if body.get("summary") != "" else None,
            "type": body.get("type").lower() if body.get("type") != "" else None,
            "author": {
                "type": body.get("author", {}).get("type") if body.get("author", {}).get("type") != "" else None,
                "id": body.get("author", {}).get("id") if body.get("author", {}).get("id") != "" else None,
                "host": body.get("author", {}).get("host") if body.get("author", {}).get("host") != "" else None,
                "displayName": body.get("author", {}).get("displayName") if body.get("author", {}).get("displayName") != "" else None,
                "url": body.get("author", {}).get("url") if body.get("author", {}).get("url") != "" else None,
                "github": body.get("author", {}).get("github") if body.get("author", {}).get("github") != "" else "https://google.com",
                "profileImage": body.get("author", {}).get("profileImage") if body.get("author", {}).get("profileImage") != "" else "https://google.com",
            },
            "object": {
                "type": body.get("object", {}).get("type") if body.get("object", {}).get("type") != "" else None,
                "id": body.get("object", {}).get("id") if body.get("object", {}).get("id") != "" else None,
                "title": body.get("object", {}).get("title") if body.get("object", {}).get("title") != "" else None,
                "source": body.get("object", {}).get("source") if body.get("object", {}).get("source") != "" else None,
                "origin": body.get("object", {}).get("origin") if body.get("object", {}).get("origin") != "" else None,
                "description": body.get("object", {}).get("description") if body.get("object", {}).get("description") != "" else None,
                "contentType": body.get("object", {}).get("contentType") if body.get("object", {}).get("contentType") != "" else None,
                "content": content,
                "author": {
                    "type": body.get("object", {}).get("author", {}).get("type") if body.get("object", {}).get("author", {}).get("type") != "" else None,
                    "id": body.get("object", {}).get("author", {}).get("id") if body.get("object", {}).get("author", {}).get("id") != "" else None,
                    "host": body.get("object", {}).get("author", {}).get("host") if body.get("object", {}).get("author", {}).get("host") != "" else None,
                    "displayName": body.get("object", {}).get("author", {}).get("displayName") if body.get("object", {}).get("author", {}).get("displayName") != "" else None,
                    "url": body.get("object", {}).get("author", {}).get("url") if body.get("object", {}).get("author", {}).get("url") != "" else None,
                    "github": body.get("object", {}).get("author", {}).get("github") if body.get("object", {}).get("author", {}).get("github") != "" else "https://google.com",
                    "profileImage": body.get("object", {}).get("author", {}).get("profileImage") if body.get("object", {}).get("author", {}).get("profileImage") != "" else "https://google.com",
                },
                "categories": body.get("object", {}).get("categories") if body.get("object", {}).get("categories") != "" else None,
                "count": body.get("object", {}).get("count") if body.get("object", {}).get("count") != "" else None,
                "comments": body.get("object", {}).get("comments") if body.get("object", {}).get("comments") != "" else None,
                "commentsSrc": body.get("object", {}).get("commentsSrc") if body.get("object", {}).get("commentsSrc") != "" else None,
                "published": "2023-03-27T22:15:11.085446-06:00",  # ignored
                "visibility": body.get("object", {}).get("visibility") if body.get("object", {}).get("visibility") != "" else None,
                "unlisted": body.get("object", {}).get("unlisted") if body.get("object", {}).get("unlisted") != "" else None,
            }
        }

        print(cleaned_body)

        response = self.session.post(url=url, json=cleaned_body)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                print("Error parsing response from remote server: https://quickcomm-dev1.herokuapp.com/; status code " +
                      str(response.status_code) + " was received in response.")
                return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_like(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox/"

        # Team 11's like POST body is a little different, less redundant w/ the object field
        cleaned_body = {
            "@context": body.get("@context") if body.get("@context") != "" else None,
            "summary": body.get("summary") if body.get("summary") != "" else None,
            "type": body.get("type") if body.get("type") != "" else None,
            "author": {
                "type": body.get("author", {}).get("type") if body.get("author", {}).get("type") != "" else None,
                "id": body.get("author", {}).get("id") if body.get("author", {}).get("id") != "" else None,
                "host": body.get("author", {}).get("host") if body.get("author", {}).get("host") != "" else None,
                "displayName": body.get("author", {}).get("displayName") if body.get("author", {}).get("displayName") != "" else None,
                "url": body.get("author", {}).get("url") if body.get("author", {}).get("url") != "" else None,
                "github": body.get("author", {}).get("github") if body.get("author", {}).get("github") != "" else None,
                "profileImage": body.get("author", {}).get("profileImage") if body.get("author", {}).get("profileImage") != "" else None,
            },
            "object": body.get("object", {}).get("object") if body.get("object", {}).get("object") != "" else None
        }

        response = self.session.post(url=url, json=cleaned_body)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending like to author with id " + author_id +
                                    " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                print("Error parsing response from remote server: https://quickcomm-dev1.herokuapp.com/; status code " +
                      str(response.status_code) + " was received in response.")
                return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_comment(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox/"

        # Team 11's comment POST body is a little different, less redundant w/ the object field, uses a comment object
        cleaned_body = {
            "@context": body.get("@context") if body.get("@context") != "" else None,
            "summary": body.get("summary") if body.get("summary") != "" else None,
            "type": body.get("type") if body.get("type") != "" else None,
            "author": {
                "type": body.get("actor", {}).get("type") if body.get("actor", {}).get("type") != "" else None,
                "id": body.get("actor", {}).get("id") if body.get("actor", {}).get("id") != "" else None,
                "host": body.get("actor", {}).get("host") if body.get("actor", {}).get("host") != "" else None,
                "displayName": body.get("actor", {}).get("displayName") if body.get("actor", {}).get("displayName") != "" else None,
                "url": body.get("actor", {}).get("url") if body.get("actor", {}).get("url") != "" else None,
                "github": body.get("actor", {}).get("github") if body.get("actor", {}).get("github") != "" else None,
                "profileImage": body.get("actor", {}).get("profileImage") if body.get("actor", {}).get("profileImage") != "" else None,
            },
            "comment": {
                "type": body.get("object", {}).get("type") if body.get("object", {}).get("type") != "" else None,
                "author": {
                    "type": body.get("object", {}).get("author", {}).get("type") if body.get("object", {}).get("author", {}).get("type") != "" else None,
                    "id": body.get("object", {}).get("author", {}).get("id") if body.get("object", {}).get("author", {}).get("id") != "" else None,
                    "host": body.get("object", {}).get("author", {}).get("host") if body.get("object", {}).get("author", {}).get("host") != "" else None,
                    "displayName": body.get("object", {}).get("author", {}).get("displayName") if body.get("object", {}).get("author", {}).get("displayName") != "" else None,
                    "url": body.get("object", {}).get("author", {}).get("url") if body.get("object", {}).get("author", {}).get("url") != "" else None,
                    "github": body.get("object", {}).get("author", {}).get("github") if body.get("object", {}).get("author", {}).get("github") != "" else None,
                    "profileImage": body.get("object", {}).get("author", {}).get("profileImage") if body.get("object", {}).get("author", {}).get("profileImage") != "" else None,
                },
                "id": body.get("object", {}).get("id") if body.get("object", {}).get("id") != "" else None,
                "comment": body.get("object", {}).get("comment") if body.get("object", {}).get("comment") != "" else None,
                "contentType": body.get("object", {}).get("contentType") if body.get("object", {}).get("contentType") != "" else None,
                # this is ignored, needs to be a proper formatted timestamp I guess?
                "published": "2023-03-27T22:15:11.085446-06:00"
            },
            "object": body.get("object", {}).get("object") if body.get("object", {}).get("object") != "" else None,

        }

        print(cleaned_body)

        response = self.session.post(url=url, json=cleaned_body)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending comment to author with id " + author_id +
                                    " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                print("Error parsing response from remote server: https://quickcomm-dev1.herokuapp.com/; status code " +
                      str(response.status_code) + " was received in response.")
                return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_follow(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox/"

        cleaned_body = {
            "@context": body.get("@context") if body.get("@context") != "" else None,
            "summary": body.get("summary") if body.get("summary") != "" else None,
            "type": body.get("type") if body.get("type") != "" else None,
            "actor": {
                "type": body.get("actor", {}).get("type") if body.get("actor", {}).get("type") != "" else None,
                "id": body.get("actor", {}).get("id") if body.get("actor", {}).get("id") != "" else None,
                "host": body.get("actor", {}).get("host") if body.get("actor", {}).get("host") != "" else None,
                "displayName": body.get("actor", {}).get("displayName") if body.get("actor", {}).get("displayName") != "" else None,
                "url": body.get("actor", {}).get("url") if body.get("actor", {}).get("url") != "" else None,
                "github": body.get("actor", {}).get("github") if body.get("actor", {}).get("github") != "" else None,
                "profileImage": body.get("actor", {}).get("profileImage") if body.get("actor", {}).get("profileImage") != "" else None,
            },
            "object": {
                "type": body.get("object", {}).get("type") if body.get("object", {}).get("type") != "" else None,
                "id": body.get("object", {}).get("id") if body.get("object", {}).get("id") != "" else None,
                "host": body.get("object", {}).get("host") if body.get("object", {}).get("host") != "" else None,
                "displayName": body.get("object", {}).get("displayName") if body.get("object", {}).get("displayName") != "" else None,
                "url": body.get("object", {}).get("url") if body.get("object", {}).get("url") != "" else None,
                "github": body.get("object", {}).get("github") if body.get("object", {}).get("github") != "" else None,
                "profileImage": body.get("object", {}).get("profileImage") if body.get("object", {}).get("profileImage") != "" else None,
            }
        }

        response = self.session.post(url=url, json=cleaned_body)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending follow to author with id " + author_id +
                                    " from remote server: https://quickcomm-dev1.herokuapp.com/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                print("Error parsing response from remote server: https://quickcomm-dev1.herokuapp.com/; status code " +
                      str(response.status_code) + " was received in response.")
                return None


class Team13Connection():
    def __init__(self, username, password, base_url):
        # TODO: configure username, password, and base_url
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = CachedSession(
            "team13_cache", backend="sqlite", expire_after=1)

        # AUTH COMMENTED OUT
        # THEY CURRENTLY HAVE IT DISABLED, SUBJECT TO CHANGE
        # self.session.auth = (self.username, self.password)

    # URL: ://service/authors/
    def get_authors(self):
        url = self.base_url + "authors"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        authors = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the authors we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting authors from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(
                    response.status_code) + " was received in response.")

            response_authors = response.json()
            if response_authors is None:
                raise RemoteServerError(
                    "Error getting authors from remote server: https://group-13-epic-app.herokuapp.com/api/. Response body was empty.")

            items = response_authors.get("items", [])

            # if there are no items, we've reached the end of the list
            if len(items) == 0:
                break

            else:
                authors.extend(items)
                page += 1

        return {
            "type": "authors",
            "items": authors
        }

    # URL: ://service/authors/{AUTHOR_ID}/
    def get_single_author(self, author_id):
        url = self.base_url + "authors/" + author_id
        response = self.session.get(url)

        # if the author is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Author with id " + author_id +
                            " not found on remote server: https://group-13-epic-app.herokuapp.com/api/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_author = response.json()

                # if the response body is empty, throw an exception
                if response_author is None:
                    raise RemoteServerError("Error getting author with id " + author_id +
                                            " from remote server: https://group-13-epic-app.herokuapp.com/api/. Response body was empty.")

                else:
                    return response_author

            except Exception as e:
                raise RemoteServerError("Error getting author with id " + author_id +
                                        " from remote server: https://group-13-epic-app.herokuapp.com/api/. Exception: " + str(e))

    # URL: ://service/authors/{AUTHOR_ID}/followers
    def get_author_followers(self, author_id):
        url = self.base_url + "authors/" + author_id + "/followers"
        response = self.session.get(url)

        # if the author is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Author with id " + author_id +
                            " not found on remote server: https://group-13-epic-app.herokuapp.com/api/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting followers for author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_followers = response.json().get("items", [])
                if response_followers is None:
                    raise RemoteServerError("Error getting followers for author with id " + author_id +
                                            " from remote server: https://group-13-epic-app.herokuapp.com/api/. Response body was empty.")

                else:
                    cleaned_followers = []
                    for author in response_followers:
                        cleaned_followers.append({
                            "type": author.get("type"),
                            "id": author.get("id"),
                            "url": author.get("url"),
                            "host": author.get("host"),
                            "displayName": author.get("displayName"),
                            "github": author.get("github"),
                            "profileImage": author.get("profileImage"),
                        })

                    return {
                        "type": "followers",
                        "items": cleaned_followers
                    }

            except Exception as e:
                raise RemoteServerError("Error getting followers for author with id " + author_id +
                                        " from remote server: https://group-13-epic-app.herokuapp.com/api/. Exception: " + str(e))

    # URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    def check_if_follower(self, author_id, follower_id):
        url = self.base_url + "authors/" + author_id + "/followers/" + follower_id
        print(url)
        response = self.session.get(url)

        if response.status_code != 200:
            return {
                "isFollower": False
            }

        else:
            return {
                "isFollower": True
            }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    def get_single_post(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id
        response = self.session.get(url)

        # if the author/post is not found, throw an exception
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id +
                            " not found on remote server: https://group-13-epic-app.herokuapp.com/api/")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_post = response.json()
                if response_post is None:
                    # TODO: handle error
                    pass

                else:
                    comments = []
                    for comment in response_post.get("commentsSrc", {}).get("comments", []):
                        comments.append({
                            "type": comment.get("type", ""),
                            "author": {
                                "type": comment.get("author", {}).get("type", ""),
                                "id": comment.get("author", {}).get("id", ""),
                                "host": comment.get("author", {}).get("host", ""),
                                "displayName": comment.get("author", {}).get("displayName", ""),
                                "url": comment.get("author", {}).get("url", ""),
                                "github": comment.get("author", {}).get("github", ""),
                                "profileImage": comment.get("author", {}).get("profileImage", ""),
                            },
                            "comment": comment.get("comment", ""),
                            "contentType": comment.get("contentType", ""),
                            "published": comment.get("published", ""),
                            "id": comment.get("id", ""),
                        })

                    return {
                        "type": response_post.get("type", ""),
                        "title": response_post.get("title", ""),
                        "id": response_post.get("id", ""),
                        "source": response_post.get("source", ""),
                        "origin": response_post.get("origin", ""),
                        "description": response_post.get("description", ""),
                        "contentType": response_post.get("contentType", ""),
                        "content": response_post.get("content", ""),
                        "author": {
                            "type": response_post.get("author", {}).get("type", ""),
                            "id": response_post.get("author", {}).get("id", ""),
                            "host": response_post.get("author", {}).get("host", ""),
                            "displayName": response_post.get("author", {}).get("displayName", ""),
                            "url": response_post.get("author", {}).get("url", ""),
                            "github": response_post.get("author", {}).get("github", ""),
                            "profileImage": response_post.get("author", {}).get("profileImage", ""),
                        },
                        "categories": response_post.get("categories", ""),
                        "count": response_post.get("count", ""),
                        "comments": response_post.get("comments", ""),
                        "commentsSrc": {
                            "type": response_post.get("commentsSrc", {}).get("type", ""),
                            "page": response_post.get("commentsSrc", {}).get("page", 1),
                            "size": response_post.get("commentsSrc", {}).get("size", 0),
                            "post": response_post.get("commentsSrc", {}).get("post", response_post.get("id", "")),
                            "id": response_post.get("commentsSrc", {}).get("id", response_post.get("id", "") + "/comments"),
                            "comments": comments
                        },
                        "published": response_post.get("published", ""),
                        "visibility": response_post.get("visibility", ""),
                        "unlisted": response_post.get("unlisted", ""),
                    }

            except Exception as e:
                raise RemoteServerError("Error getting post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://group-13-epic-app.herokuapp.com/api/; exception " + str(e) + " was thrown.")

    # URL: ://service/authors/{AUTHOR_ID}/posts/
    def get_recent_posts(self, author_id):
        url = self.base_url + "authors/" + author_id + "/posts"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        posts = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the posts we have/or the empty array
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting recent posts from author with id " + author_id +
                                        " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

            response_posts = response.json()
            if response_posts is None:
                raise RemoteServerError("Error getting recent posts from author with id " + author_id +
                                        " from remote server: https://group-13-epic-app.herokuapp.com/api/. Response body was empty.")

            items = response_posts.get("items", [])

            if len(items) == 0:
                break

            else:
                posts.extend(items)
                page += 1

        cleaned_posts = []
        for post in posts:
            comments = []
            for comment in post.get("commentsSrc", {}).get("comments", []):
                comments.append({
                    "type": comment.get("type", ""),
                    "author": {
                        "type": comment.get("author", {}).get("type", ""),
                        "id": comment.get("author", {}).get("id", ""),
                        "host": comment.get("author", {}).get("host", ""),
                        "displayName": comment.get("author", {}).get("displayName", ""),
                        "url": comment.get("author", {}).get("url", ""),
                        "github": comment.get("author", {}).get("github", ""),
                        "profileImage": comment.get("author", {}).get("profileImage", ""),
                    },
                    "comment": comment.get("comment", ""),
                    "contentType": comment.get("contentType", ""),
                    "published": comment.get("published", ""),
                    "id": comment.get("id", ""),
                })

            cleaned_posts.append({
                "type": post.get("type", ""),
                "title": post.get("title", ""),
                "id": post.get("id", ""),
                "source": post.get("source", ""),
                "origin": post.get("origin", ""),
                "description": post.get("description", ""),
                "contentType": post.get("contentType", ""),
                "content": post.get("content", ""),
                "author": {
                    "type": post.get("author", {}).get("type", ""),
                    "id": post.get("author", {}).get("id", ""),
                    "host": post.get("author", {}).get("host", ""),
                    "displayName": post.get("author", {}).get("displayName", ""),
                    "url": post.get("author", {}).get("url", ""),
                    "github": post.get("author", {}).get("github", ""),
                    "profileImage": post.get("author", {}).get("profileImage", ""),
                },
                "categories": post.get("categories", ""),
                "count": post.get("count", 0),
                "comments": post.get("comments", ""),
                "commentsSrc": {
                    "type": post.get("commentsSrc", {}).get("type", ""),
                    "page": post.get("commentsSrc", {}).get("page", 1),
                    "size": post.get("commentsSrc", {}).get("size", 0),
                    "post": post.get("commentsSrc", {}).get("post", ""),
                    "id": post.get("commentsSrc", {}).get("id", post.get("id", "") + "/comments"),
                    "comments": comments
                },
                "published": post.get("published", ""),
                "visibility": post.get("visibility", ""),
                "unlisted": post.get("unlisted", ""),
            })

        return {
            "type": "posts",
            "items": cleaned_posts,
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
    def get_image_post(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/image"
        response = self.session.get(url)

        # if the post doesn't exist, or isn't an image, throw a 404 exception
        if response.status_code == 404:
            raise Remote404("Post with id " + post_id + " from author with id " + author_id +
                            " from remote server: https://group-13-epic-app.herokuapp.com/api/ does not exist, or is not an image.")

        # if the server returns an error, throw an exception
        elif response.status_code != 200:
            raise RemoteServerError("Error getting image post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        # otherwise, return the raw image data and the content type
        else:
            return (response.content, response.headers.get("Content-Type"))

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    def get_comments(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/comments"

        # handle pagination
        # start at page 1, loop until no items are returned - in which case our server throws a 404
        page = 1
        comments = []
        while True:
            response = self.session.get(url, params={"page": page, "size": 10})

            # no need to handle the 404 using an exception, just return the comments we have/or the empty list
            if response.status_code == 404:
                break

            elif response.status_code != 200:
                raise RemoteServerError("Error getting comments for post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

            response_comments = response.json()
            if response_comments is None:
                raise RemoteServerError("Error getting comments for post with id " + post_id + " from author with id " + author_id +
                                        " from remote server: https://group-13-epic-app.herokuapp.com/api/; no JSON was received in response.")

            items = response_comments.get("comments", [])
            if len(items) == 0:
                break

            else:
                comments.extend(items)
                page += 1

        cleaned_comments = []
        for comment in comments:
            new_comment = {
                "type": comment.get("type", ""),
                "author": {
                    "type": comment.get("author", {}).get("type", ""),
                    "id": comment.get("author", {}).get("id", ""),
                    "host": comment.get("author", {}).get("host", ""),
                    "displayName": comment.get("author", {}).get("displayName", "Unknown"),
                    "url": comment.get("author", {}).get("url", ""),
                    "github": comment.get("author", {}).get("github", ""),
                    "profileImage": comment.get("author", {}).get("profileImage", ""),
                },
                "comment": comment.get("comment", ""),
                "contentType": comment.get("contentType", ""),
                "published": comment.get("published", ""),
                "id": comment.get("id", ""),
            }

            cleaned_comments.append(new_comment)

        return {
            "type": "comments",
            "items": cleaned_comments
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    def get_post_likes(self, author_id, post_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + post_id + "/likes"

        likes = []

        response = self.session.get(url)

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; no JSON was received in response.")

        items = response_likes.get("items", [])
        likes.extend(items)

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "Unknown",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    def get_comment_likes(self, author_id, post_id, comment_id):
        url = self.base_url + "authors/" + author_id + "/posts/" + \
            post_id + "/comments/" + comment_id + "/likes"

        likes = []

        response = self.session.get(url)

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for comment with id " + comment_id + " from post with id " + post_id + " from author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for comment with id " + comment_id + " from post with id " + post_id + " from author with id " +
                                    author_id + " from remote server: https://group-13-epic-app.herokuapp.com/api/; no JSON was received in response.")

        items = response_likes.get("items")
        likes.extend(items)

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/liked
    def get_author_liked(self, author_id):
        url = self.base_url + "authors/" + author_id + "/liked"

        likes = []

        response = self.session.get(url)

        # no need to handle the 404 using an exception, just return the likes we have/or the empty list
        if response.status_code == 404:
            likes = []

        elif response.status_code != 200:
            raise RemoteServerError("Error getting likes for author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        response_likes = response.json()
        if response_likes is None:
            raise RemoteServerError("Error getting likes for author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; no JSON was received in response.")

        items = response_likes.get("items")
        likes.extend(items)

        cleaned_likes = []
        for like in likes:
            cleaned_likes.append({
                "@context": like.get("@context") if like.get("@context") != None else "",
                "summary": like.get("summary") if like.get("summary") != None else "",
                "type": like.get("type").lower() if like.get("type") != None else "",
                "author": {
                    "type": like.get("author", {}).get("type") if like.get("author", {}).get("type") != None else "",
                    "id": like.get("author", {}).get("id") if like.get("author", {}).get("id") != None else "",
                    "host": like.get("author", {}).get("host") if like.get("author", {}).get("host") != None else "",
                    "displayName": like.get("author", {}).get("displayName") if like.get("author", {}).get("displayName") != None else "",
                    "url": like.get("author", {}).get("url") if like.get("author", {}).get("url") != None else "",
                    "github": like.get("author", {}).get("github") if like.get("author", {}).get("github") != None else "",
                    "profileImage": like.get("author", {}).get("profileImage") if like.get("author", {}).get("profileImage") != None else "",
                },
                "object": like.get("object") if like.get("object") != None else "",
            })

        return {
            "type": "likes",
            "items": cleaned_likes
        }

    # URL: ://service/authors/{AUTHOR_ID}/inbox
    def send_post(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox"

        cleaned_body = {
            "type": body.get("object", {}).get("type", "").lower(),
            "id": body.get("object", {}).get("id", ""),
            "title": body.get("object", {}).get("title", ""),
            "source": body.get("object", {}).get("source", ""),
            "origin": body.get("object", {}).get("origin", ""),
            "description": body.get("object", {}).get("description", ""),
            "contentType": body.get("object", {}).get("contentType", ""),
            "content": body.get("object", {}).get("content", ""),
            "author": {
                "type": body.get("object", {}).get("author", {}).get("type", "").lower(),
                "id": body.get("object", {}).get("author", {}).get("id", ""),
                "host": body.get("object", {}).get("author", {}).get("host", ""),
                "displayName": body.get("object", {}).get("author", {}).get("displayName", ""),
                "url": body.get("object", {}).get("author", {}).get("url", ""),
                "github": body.get("object", {}).get("author", {}).get("github", ""),
                "profileImage": body.get("object", {}).get("author", {}).get("profileImage", ""),
            },
            "categories": body.get("object", {}).get("categories", []),
            "count": body.get("object", {}).get("count", 0),
            "comments": body.get("object", {}).get("comments", []),
            "commentsSrc": body.get("object", {}).get("commentsSrc", {}),
            "published": body.get("object", {}).get("published", ""),
            "visibility": body.get("object", {}).get("visibility", ""),
            "unlisted": body.get("object", {}).get("unlisted", False),
        }

        print(cleaned_body)

        response = self.session.post(url=url, json=cleaned_body)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201:
                    return {"success": True}

                else:
                    print("Error parsing response from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_like(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox"

        cleaned_like = {
            "type": "Like",
            "author": body.get("author", {}).get("id", ""),
            "object": body.get("object", {}).get("object", ""),
        }

        print(cleaned_like)

        response = self.session.post(url=url, json=cleaned_like)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201:
                    return None

                else:
                    print("Error parsing response from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_comment(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox"

        cleaned_comment = {
            "type": "comment",
            "contentType": body.get("object", {}).get("contentType", ""),
            "comment": body.get("object", {}).get("comment", ""),
            "author": body.get("object", {}).get("author", {}).get("id", ""),
            "post": body.get("object", {}).get("id", "").split("/comments/")[0]
        }

        print(cleaned_comment)

        response = self.session.post(url=url, json=cleaned_comment)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201:
                    return None

                else:
                    print("Error parsing response from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None

    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    def send_follow(self, author_id, body):
        url = self.base_url + "authors/" + author_id + "/inbox"
        response = self.session.post(url=url, json=body)

        if response.status_code != 200 and response.status_code != 201:
            raise RemoteServerError("Error sending post to author with id " + author_id +
                                    " from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " + str(response.status_code) + " was received in response.")

        else:
            try:
                response_json = response.json()
                return response_json

            # if there was an issue parsing the JSON response but we still got a 200/201, it's likely that we sent
            # the post successfully, and don't need to parse the response
            except Exception as e:
                if response.status_code == 200 or response.status_code == 201:
                    return {"success": True}

                else:
                    print("Error parsing response from remote server: https://group-13-epic-app.herokuapp.com/api/; status code " +
                          str(response.status_code) + " was received in response.")
                    return None
