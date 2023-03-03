// React helpers
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'
import { createAPIEndpoint, ENDPOINTS } from '../api';

// Material UI components
import { CircularProgress, Card, Typography, Grid, Divider, IconButton, Button, TextField } from "@mui/material";

// Material UI icons
import QuizIcon from '@mui/icons-material/Quiz';

// Layout component
import Layout from "../components/layouts/Layout";

// Custom components
import Post from "../components/Post";
import Comment from "../components/Comment";

const PostDetails = () => {

    const { authorID, postID } = useParams()

    const [commentsLoading, setCommentsLoading] = useState(true);
    const [comments, setComments] = useState([]);
    const [myProfile, setMyProfile] = useState(null);
    const [notFound, setNotFound] = useState(null)
    const [authorData, setAuthorData] = useState(null);
    const [postData, setPostData] = useState(null);

    const [commentBody, setCommentBody] = useState("");
    const [commentUploading, setCommentUploading] = useState(false);

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    useEffect(() => {
        if (userID) {
            createAPIEndpoint(`authors/${userID}`)
                .get()
                .then(res => {
                    //console.log(res.data)
                    setMyProfile(res.data)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }, [userID])

    useEffect(() => {
        if (userID) {
            // get post author information
            createAPIEndpoint(`authors/${authorID}`)
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
            createAPIEndpoint(`authors/${authorID}/posts/${postID}`)
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

    // get comments for post
    useEffect(() => {
        createAPIEndpoint(`authors/${authorID}/posts/${postID}/comments`)
            .get()
            .then(res => {
                console.log(res.data)
                setCommentsLoading(false)
                setComments(res.data)
            })
            .catch(err => {
                // TODO: Add in error handling
                if (err.response.status === 404) {
                    setNotFound(true)
                }
                console.log(err)
            });
    }, [])

    const handleCommentUpload = () => {
        setCommentUploading(true);
        var data = {
            "comment": commentBody,
            "contentType": "text/plain",
            "author": {
                "type": "author",
                "id": myProfile.id,
                "host": myProfile.host,
                "displayName": myProfile.displayName,
                "url": myProfile.url,
                "github": myProfile.github,
                "profileImage": myProfile.profileImage
            }
        }

        createAPIEndpoint(`authors/${authorID}/posts/${postID}/comments`)
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
                        {((postData === null || authorData === null))
                            ? <Card><CircularProgress /></Card>
                            : <Post
                                id={postData["_id"]}
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
                            />
                        }

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

                                {commentsLoading &&
                                    <Grid item xs={12}>
                                        <CircularProgress />
                                    </Grid>
                                }

                                {!commentsLoading && comments.length === 0 &&
                                    <Grid item xs={12}>
                                        <Typography variant="h6" align="center">No comments yet.</Typography>
                                    </Grid>
                                }

                                {!commentsLoading && comments.length > 0 &&
                                    comments.map((comment) => (
                                        <Grid item xs={12}>
                                            <Comment username={comment.author.displayName} content={comment.comment} />
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