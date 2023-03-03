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
            // get author information
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

    const handleCommentUpload = () => {
        setCommentUploading(true);

        // TODO: upload comment to backend here

        setTimeout(() => {
            setCommentUploading(false);
        }, 1500);
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

                                <Grid item xs={12}>
                                    <Comment />
                                </Grid>
                            </Grid>
                        </Card>
                    </>

                )}
            </Layout>
        </>
    )
}

export default PostDetails;