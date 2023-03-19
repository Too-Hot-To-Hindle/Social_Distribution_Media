from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse, OpenApiTypes

AUTHOR_1 = {
    "_id": "9610effa-1461-4d11-85fb-45c5d45e199d",
    "type": "author",
    "id": "https://social-distribution-media.herokuapp.com/api/authors/9610effa-1461-4d11-85fb-45c5d45e199d",
    "host": "https://social-distribution-media.herokuapp.com",
    "displayName": "John",
    "url": "https://social-distribution-media.herokuapp.com/authors/9610effa-1461-4d11-85fb-45c5d45e199d",
    "github": "",
    "profileImage": "",
    "followers": [],
    "following": [
        "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc"
    ]
}

AUTHOR_2 = {
    "_id": "9610effa-1461-4d11-85fb-45c5d45e19sdfgsdf",
    "type": "author",
    "id": "https://social-distribution-media.herokuapp.com/api/authors/9610effa-1461-4d11-85fb-45c5d45esdfgdsfg",
    "host": "https://social-distribution-media.herokuapp.com",
    "displayName": "Johnny",
    "url": "https://social-distribution-media.herokuapp.com/authors/9610effa-1461-4d11-85fb-45c5d45esdfgdsfg",
    "github": "",
    "profileImage": "",
    "followers": [],
    "following": [
        "d5a7f5b6-e68c-4e9e-9612-74ddb66sdfggg"
    ]
}

AUTHOR_3 = {

}

POST_1 = {
    "_id": "9df262a7-a75e-481f-8998-bd57f822bd07",
    "type": "post",
    "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/9df262a7-a75e-481f-8998-bd57f822bd07",
    "title": "TestPostFromPOSTRequest",
    "source": "",
    "origin": "",
    "description": "",
    "contentType": "text/plain",
    "content": "",
    "author": {
        "_id": "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "type": "author",
        "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "url": "https://social-distribution-media.herokuapp.com/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "host": "https://social-distribution-media.herokuapp.com",
        "displayName": "Justin",
        "github": "",
        "profileImage": "",
        "remote": False,
        "user": 15,
        "followers": [
            "9610effa-1461-4d11-85fb-45c5d45e199d"
        ],
        "following": []
    },
    "categories": [],
    "count": 0,
    "comments": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/9df262a7-a75e-481f-8998-bd57f822bd07/comments",
    "commentsSrc": {},
    "published": "2023-03-19T04:46:29.073653Z",
    "visibility": "FRIENDS",
    "unlisted": False
}

POST_2 = {
    "_id": "0e5a9893-9607-4f99-9bc5-c08136a6432c",
    "type": "post",
    "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/0e5a9893-9607-4f99-9bc5-c08136a6432c",
    "title": "TestPostFromPOSTRequest",
    "source": "",
    "origin": "",
    "description": "",
    "contentType": "text/plain",
    "content": "",
    "author": {
        "_id": "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "type": "author",
        "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "url": "https://social-distribution-media.herokuapp.com/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "host": "https://social-distribution-media.herokuapp.com",
        "displayName": "Justin",
        "github": "",
        "profileImage": "",
        "remote": False,
        "user": 15,
        "followers": [
            "9610effa-1461-4d11-85fb-45c5d45e199d"
        ],
        "following": []
    },
    "categories": [],
    "count": 0,
    "comments": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/0e5a9893-9607-4f99-9bc5-c08136a6432c/comments",
    "commentsSrc": {},
    "published": "2023-03-16T20:40:01.796602Z",
    "visibility": "FRIENDS",
    "unlisted": False
}

COMMENT_1 = {
    "type": "comment",
    "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/67331d96-321b-4e15-b438-c568c24aed66/comments/3aae7c80-f1ed-4aa3-bc92-4fa8a84fa44f",
    "author": {
        "_id": "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "type": "author",
        "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "host": "https://social-distribution-media.herokuapp.com",
        "displayName": "Justin",
        "url": "https://social-distribution-media.herokuapp.com/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "github": "",
        "profileImage": "",
        "followers": [
            "9610effa-1461-4d11-85fb-45c5d45e199d"
        ],
        "following": []
    },
    "comment": "Comment from postman!",
    "contentType": "text/plain",
    "published": "2023-03-16T20:50:26.377955Z",
    "_post_author_id": "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
    "_post_id": "67331d96-321b-4e15-b438-c568c24aed66"
}

COMMENT_2 = {
    "type": "comment",
    "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/67331d96-321b-4e15-b438-c568c24aed66/comments/2c99de18-8622-4be2-94a6-40db610471c2",
    "author": {
        "_id": "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "type": "author",
        "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "host": "https://social-distribution-media.herokuapp.com",
        "displayName": "Justin",
        "url": "https://social-distribution-media.herokuapp.com/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "github": "",
        "profileImage": "",
        "followers": [
            "9610effa-1461-4d11-85fb-45c5d45e199d"
        ],
        "following": []
    },
    "comment": "Comment from postman!",
    "contentType": "text/plain",
    "published": "2023-03-17T04:57:33.056945Z",
    "_post_author_id": "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
    "_post_id": "67331d96-321b-4e15-b438-c568c24aed66"
}

POST_LIKE_1 = {
    "type": "Like",
    "summary": "Test user likes your post!",
    "author": {
        "_id": "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "type": "author",
        "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "host": "https://social-distribution-media.herokuapp.com",
        "displayName": "Justin",
        "url": "https://social-distribution-media.herokuapp.com/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "github": "",
        "profileImage": "",
        "followers": [
            "9610effa-1461-4d11-85fb-45c5d45e199d"
        ],
        "following": []
    },
    "object": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/67331d96-321b-4e15-b438-c568c24aed66"
}

POST_LIKE_2 = {
    "type": "Like",
    "summary": "Test user likes your post!",
    "author": {
        "_id": "d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "type": "author",
        "id": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "host": "https://social-distribution-media.herokuapp.com",
        "displayName": "Justin",
        "url": "https://social-distribution-media.herokuapp.com/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc",
        "github": "",
        "profileImage": "",
        "followers": [
            "9610effa-1461-4d11-85fb-45c5d45e199d"
        ],
        "following": []
    },
    "object": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/67331d96-321b-4e15-b438-c568c24aed66"
}

COMMENT_LIKE_1 = {
    "type": "Like",
    "summary": "Test user likes your comment!",
    "author": {
        "_id": "1ea5c53a-b0e0-466b-a2be-058fbb6e8b96",
        "type": "author",
        "id": "https://testremotehost.com/api/authors/1ea5c53a-b0e0-466b-a2be-058fbb6e8b96",
        "host": "https://testremotehost.com",
        "displayName": "Test Remote Author",
        "url": "https://testremotehost.com/authors/1ea5c53a-b0e0-466b-a2be-058fbb6e8b96",
        "github": "",
        "profileImage": "",
        "followers": [],
        "following": []
    },
    "object": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/67331d96-321b-4e15-b438-c568c24aed66/comments/3aae7c80-f1ed-4aa3-bc92-4fa8a84fa44f"
}

COMMENT_LIKE_2 = {
    "type": "Like",
    "summary": "Test user likes your comment again! (This was just generated for documentation purposes)",
    "author": {
    "_id": "1ea5c53a-b0e0-466b-a2be-058fbb6e8b96",
    "type": "author",
    "id": "https://testremotehost.com/api/authors/1ea5c53a-b0e0-466b-a2be-058fbb6e8b96",
    "host": "https://testremotehost.com",
    "displayName": "Test Remote Author",
    "url": "https://testremotehost.com/authors/1ea5c53a-b0e0-466b-a2be-058fbb6e8b96",
    "github": "",
    "profileImage": "",
    "followers": [],
    "following": []
    },
    "object": "https://social-distribution-media.herokuapp.com/api/authors/d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc/posts/67331d96-321b-4e15-b438-c568c24aed66/comments/3aae7c80-f1ed-4aa3-bc92-4fa8a84fa44f"
}

EXAMPLE_POST_BODY = {
    "_id": "67331d96-321b-4e15-b438-c568c24aed66",
    "type": "post",
    "id": "https://social-distribution-media.herokuapp.com/api/authors/2b36204c-e37c-4aeb-bbdc-b63b886218f3/posts/67331d96-321b-4e15-b438-c568c24aed66",
    "title": "TestPostFromPUTRequest",
    "source": "",
    "origin": "",
    "description": "",
    "contentType": "text/plain",
    "content": "",
    "author": AUTHOR_3,
    "categories": [],
    "count": 0,
    "comments": "https://social-distribution-media.herokuapp.com/api/authors/2b36204c-e37c-4aeb-bbdc-b63b886218f3/posts/67331d96-321b-4e15-b438-c568c24aed66/comments",
    "commentsSrc": {},
    "published": "2023-03-03T07:15:44.374719Z",
    "visibility": "FRIENDS",
    "unlisted": False
}

EXTEND_SCHEMA_PARAM_AUTHOR_ID = OpenApiParameter(
    name="author_id",
    description="The ID of the author",
    required=True,
    type=str,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            "Example 1", 
            value="d5a7f5b6-e68c-4e9e-9612-74ddb6664cfc", 
            summary="Example author_id"
        )
    ],
)

EXTEND_SCHEMA_PARAM_FOREIGN_AUTHOR_ID = OpenApiParameter(
    name="foreign_author_id",
    description="The ID of the foreign author that is/isn't following the author_id",
    required=True,
    type=str,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            "Example 1", 
            value="deff525c-23ce-4d3b-b975-d6e484d21fb8", 
            summary="Example foreign_author_id"
        )
    ],
)

EXTEND_SCHEMA_PARAM_POST_ID = OpenApiParameter(
    name="post_id",
    description="The ID of the post",
    required=True,
    type=str,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            "Example 1",
            value="67331d96-321b-4e15-b438-c568c24aed66",
            summary="Example post_id"
        )
    ]
)

EXTEND_SCHEMA_PARAM_COMMENT_ID = OpenApiParameter(
    name="comment_id",
    description="The ID of the comment",
    required=True,
    type=str,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            "Example 1",
            value="3aae7c80-f1ed-4aa3-bc92-4fa8a84fa44f",
            summary="Example comment_id"
        )
    ]
)

EXTEND_SCHEMA_RESP_LIST_AUTHORS = OpenApiResponse(
    description="A list of authors and their data that are all following the user given by author_id",
    examples=[
        OpenApiExample(
            "Example Authors",
            summary="List of example authors",
            value=(
                AUTHOR_1,
                AUTHOR_2
            ),
        ),
    ],
    response=OpenApiTypes.OBJECT,
)

EXTEND_SCHEMA_RESP_IS_FOLLOWER = OpenApiResponse(
    description="Response body contains a boolean indicating if foreign_author_id is a follower of author_id",
    examples=[
        OpenApiExample(
            "Example Response",
            summary="An example response",
            value={
                "isFollower": True
            }
        )
    ],
    response=OpenApiTypes.BOOL,
)

EXTEND_SCHEMA_RESP_LIST_POSTS = OpenApiResponse(
    description="Response body contains a list of posts by author_id, ordered by post date with most recent first",
    examples=[
        OpenApiExample(
            "Example Response",
            summary="An example response",
            value=(
                POST_1,
                POST_2,
            )
        )
    ],
    response=OpenApiTypes.OBJECT,
)

EXTEND_SCHEMA_RESP_POST = OpenApiResponse(
    description="Get post_id posted by author_id",
    examples=[
        OpenApiExample(
            "Example",
            summary="Example",
            value=POST_1
        )
    ],
    response=OpenApiTypes.OBJECT,
)

EXTEND_SCHEMA_RESP_LIST_COMMENTS = OpenApiResponse(
    description="Get all comments on post_id posted by author_id",
    examples=[
        OpenApiExample(
            "Example Response",
            summary="List of comments on post_id posted by author_id",
            value=(
                COMMENT_1,
                COMMENT_2
            ),
        ),
    ],
    response=OpenApiTypes.OBJECT,
)

EXTEND_SCHEMA_RESP_LIST_POST_LIKES = OpenApiResponse(
    description="Get all likes on post_id posted by author_id",
    examples=[
        OpenApiExample(
            "Example Response",
            summary="List of likes on post_id posted by author_id",
            value=(
                POST_LIKE_1,
                POST_LIKE_2,
            ),
        ),
    ],
    response=OpenApiTypes.OBJECT,
)

EXTEND_SCHEMA_RESP_LIST_COMMENT_LIKES = OpenApiResponse(
    description="Get all likes of a comment with comment_id on a post_id posted by author_id",
    examples=[
        OpenApiExample(
            "Example Response",
            summary="List of likes on comment_id for post_id posted by author_id",
            value=(
                COMMENT_LIKE_1,
                COMMENT_LIKE_2,
            ),
        ),
    ],
    response=OpenApiTypes.OBJECT,
)

EXTEND_SCHEMA_RESP_LIKED_POSTS = OpenApiResponse(
    description="Get all posts liked by author_id",
    examples=[
        OpenApiExample(
            "Example Response",
            summary="List of posts liked by author_id",
            value=(
                POST_LIKE_1,
                POST_LIKE_2,
            ),
        ),
    ],
    response=OpenApiTypes.OBJECT,
)

EXTEND_SCHEMA_EXAMPLE_INBOX_POST_BODY = OpenApiExample(
    "Example Request for sending a type POST to author_id",
    summary="Send a post to author_id's inbox",
    value=EXAMPLE_POST_BODY
)