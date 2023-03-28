// React helpers
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'
import { createAPIEndpoint, ENDPOINTS } from '../api';
import { v4 as uuidv4 } from 'uuid';

// Material UI components
import { CircularProgress, Card, Typography, Grid, Divider, IconButton, Button, TextField, LinearProgress } from "@mui/material";

// Material UI icons
import QuizIcon from '@mui/icons-material/Quiz';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

// Layout component
import Layout from "../components/layouts/Layout";

// Custom components
import Post from "../components/Post";
import Comment from "../components/Comment";

// Helper functions
// getPostIDFromURL
// takes in a URL, say of example https://social-distribution-media.herokuapp.com/author/abc123/posts/def456
// and returns the post ID, here, def456
const getPostIDFromURL = (url) => {
    // make sure "posts" is in url
    // if last character in string is a '/', remove it first
    if (url[url.length - 1] === "/") {
        url = url.slice(0, -1)
    }

    if (url.includes("posts")) {
        const urlSplit = url.split("/")
        console.log(urlSplit[urlSplit.length - 1])
        return urlSplit[urlSplit.length - 1]
    }
}

const PostDetails = () => {

    const { authorID, postID } = useParams()

    const [commentsLoading, setCommentsLoading] = useState(true);
    const [comments, setComments] = useState([]);

    const [likesLoading, setLikesLoading] = useState(true);
    const [likes, setLikes] = useState([]);

    const [commentLikesLoading, setCommentLikesLoading] = useState(true);
    const [commentLikes, setCommentLikes] = useState(null); // array of objects that contain arrays of the likes for each comment

    const [myProfile, setMyProfile] = useState(null);
    const [notFound, setNotFound] = useState(null)
    const [authorData, setAuthorData] = useState(null);
    const [postData, setPostData] = useState(null);

    const [commentBody, setCommentBody] = useState("");
    const [commentUploading, setCommentUploading] = useState(false);

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    // useEffect to get username and user ID for user currently logged in
    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    // useEffect to get user profile for user currently logged in
    useEffect(() => {
        if (userID) {
            createAPIEndpoint(`authors/${encodeURIComponent(userID)}`)
                .get()
                .then(res => {
                    setMyProfile(res.data)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }, [userID])

    // useEffect to get post and author data for post details we're currently viewing
    useEffect(() => {
        if (userID) {
            // get post author information
            createAPIEndpoint(`authors/${encodeURIComponent(authorID)}`)
                .get()
                .then(res => {
                    setAuthorData(res.data)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    if (err.response.status === 404) {
                        setNotFound(true)
                    }
                    console.log(err)
                });

            // get post information
            createAPIEndpoint(`authors/${encodeURIComponent(authorID)}/posts/${encodeURIComponent(postID)}`)
                .get()
                .then(res => {
                    setPostData(res.data)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    if (err.response.status === 404) {
                        setNotFound(true)
                    }
                    console.log(err)
                });
        }
    }, [userID]);

    // useEffect to get comments for post we're currently viewing
    useEffect(() => {
        const getAllCommentLikes = async (comments) => {
            var allCommentLikes = []
            // then, for each comment, get the likes
            for (let comment of comments) {
                const response = await createAPIEndpoint(`authors/${encodeURIComponent(authorID)}/posts/${encodeURIComponent(postID)}/comments/${encodeURIComponent(comment.id)}/likes`).get()
                const commentWithLikes = {
                    id: comment.id,
                    likes: response.data.items
                }

                allCommentLikes.push(commentWithLikes)
            }
            setCommentLikes(allCommentLikes)
            setCommentLikesLoading(false)
        }

        createAPIEndpoint(`authors/${encodeURIComponent(authorID)}/posts/${encodeURIComponent(postID)}/comments`)
            .get()
            .then(res => {
                setCommentsLoading(false)
                setComments(res.data.items)
                getAllCommentLikes(res.data.items)
            })
            .catch(err => {
                // TODO: Add in error handling
                if (err.response.status === 404) {
                    setCommentsLoading(false)
                    setComments([])
                }
                console.log(err)
            });
    }, [])

    // useEffect to get likes for post we're currently viewing
    useEffect(() => {
        createAPIEndpoint(`authors/${encodeURIComponent(authorID)}/posts/${encodeURIComponent(postID)}/likes`)
            .get()
            .then(res => {
                setLikesLoading(false)
                setLikes(res.data.items)
            })
            .catch(err => {
                // TODO: Add in error handling
                if (err.response.status === 404) {
                    setLikesLoading(false)
                    setLikes([])
                }
                console.log(err)
            });
    }, [])


    const handleCommentUpload = () => {
        setCommentUploading(true);
        var data = {
            "type": "comment",
            "summary": `${myProfile.displayName} commented on your post!`,
            "actor": {
                "type": "author",
                "id": myProfile.id,
                "host": myProfile.host,
                "displayName": myProfile.displayName,
                "url": myProfile.url,
                "github": myProfile.github,
                "profileImage": myProfile.profileImage
            },
            "object": {
                "type": "comment",
                "summary": `${myProfile.displayName} commented on your post!`,
                "author": {
                    "type": "author",
                    "id": myProfile.id,
                    "host": myProfile.host,
                    "displayName": myProfile.displayName,
                    "url": myProfile.url,
                    "github": myProfile.github,
                    "profileImage": myProfile.profileImage
                },
                "id": postData.id + "/comments/" + uuidv4(),
                "comment": commentBody,
                "contentType": "text/plain",
                "object": postData.id
            }
        }

        console.log(data)

        createAPIEndpoint(`authors/${encodeURIComponent(authorID)}/inbox`)
            .post(data)
            .then(res => {
                // refresh page
                window.location.reload();
            })
            .catch(err => {
                console.log(err)
            })


    }

    return (
        <>
            <Layout>
                {(notFound) ? (
                    <>
                        <Card>
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <QuizIcon sx={{ fontSize: "60px", margin: "20px" }} />
                                    <Typography variant="h6" align="center">Post not found.</Typography>
                                </Grid>
                            </Grid>
                        </Card>
                    </>

                ) : (
                    <>
                        {((postData === null || authorData === null || myProfile === null))
                            ? <Card><CircularProgress /></Card>
                            : <Post
                                id={postData["id"]}
                                title={postData.title}
                                description={postData.description}
                                source={postData.source}
                                origin={postData.origin}
                                categories={postData.categories}
                                type={postData.contentType}
                                content={postData.content}
                                authorDisplayName={authorData.displayName}
                                authorID={authorID}
                                link={postData.id}

                                // Hide details button
                                hideDetailsButton={true}
                                hideCommentButton={true}
                                hideDeleteButton={(postData.author.id !== myProfile.id)}
                            />
                        }

                        <Card>
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <Typography variant="h6" align="left">Likes</Typography>
                                </Grid>

                                <Grid item xs={12}>
                                    <Divider />
                                </Grid>

                                {likesLoading &&
                                    <Grid item xs={12}>
                                        <CircularProgress />
                                    </Grid>
                                }

                                {!likesLoading && likes.length === 0 &&
                                    <Grid item xs={12}>
                                        <Typography variant="body1" align="center">No likes yet.</Typography>
                                    </Grid>
                                }

                                {!likesLoading && likes.length > 0 &&
                                    likes.map((like, index) => (
                                        <Grid item xs={12} key={index}>
                                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                                <div style={{ display: "flex", alignItems: "center" }}>
                                                    <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />

                                                    <div>
                                                        <Typography variant="h6" align="left">@{like.author.displayName}</Typography>
                                                    </div>
                                                </div>

                                            </div>
                                        </Grid>
                                    ))
                                }
                            </Grid>
                        </Card>

                        <Card>

                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <Typography variant="h6" align="left">Comments</Typography>
                                </Grid>

                                <Grid item xs={12}>
                                    <Divider />
                                </Grid>


                                <Grid item xs={12}>
                                    <TextField placeholder="Write a comment..." multiline maxRows={Infinity} fullWidth onChange={(event) => { setCommentBody(event.target.value) }} />
                                </Grid>

                                <Grid item xs={12}>
                                    {(commentBody === "")
                                        ? <Button variant="contained" fullWidth disabled>Comment</Button>
                                        : <Button variant="contained" fullWidth disabled={commentUploading} onClick={handleCommentUpload}>{commentUploading ? <CircularProgress size={21} sx={{ margin: "5px" }} /> : "Comment"}</Button>}
                                </Grid>

                                <Grid item xs={12}>
                                    <Divider />
                                </Grid>

                                {(commentsLoading || commentLikes === null) &&
                                    <Grid item xs={12}>
                                        <CircularProgress />
                                    </Grid>
                                }

                                {!commentsLoading && comments.length === 0 &&
                                    <Grid item xs={12}>
                                        <Typography variant="h6" align="center">No comments yet.</Typography>
                                    </Grid>
                                }

                                {!commentsLoading && comments.length > 0 && commentLikes !== null &&
                                    comments.map((comment) => (
                                        <Grid item xs={12}>
                                            <Comment username={comment.author.displayName} content={comment.comment} likes={commentLikes} id={comment.id} />
                                        </Grid>
                                    ))
                                }

                            </Grid>
                        </Card>
                    </>

                )}
            </Layout>
        </>
    )
}

export default PostDetails;