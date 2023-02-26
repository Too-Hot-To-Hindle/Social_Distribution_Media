// React helpers
import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';

// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { CircularProgress, Card, Typography, Grid, TextField, Button, FormControl, InputLabel, Select, MenuItem, Divider } from "@mui/material";

// Material UI icons
import QuizIcon from '@mui/icons-material/Quiz';

const EditPost = () => {

    const navigate = useNavigate();

    const [postData, setPostData] = useState("null");
    const [belongsToUser, setBelongsToUser] = useState(false);
    const [uploading, setUpload] = useState(false);
    const [postType, setPostType] = useState("Text");
    const [postContent, setPostContent] = useState(`Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla augue nisi, pharetra at risus et, gravida tempus purus. Ut euismod elit eget nisl luctus, eget euismod sapien fermentum. Mauris bibendum, felis eget lacinia auctor, tortor odio ornare orci, sit amet volutpat arcu eros ac est. Pellentesque non purus vel lectus dictum gravida quis a felis. In sed quam nulla. Sed sollicitudin mi felis, sed molestie sem dignissim in. Etiam nec blandit mi. Curabitur vel feugiat velit. Sed bibendum purus eu nunc vulputate, sed auctor nisl fermentum. Vivamus laoreet ex mauris, at interdum arcu vehicula nec. Donec sodales tortor a dui placerat, sit amet pharetra elit aliquam. Praesent eget urna mauris. Nunc varius lectus quis sodales posuere. Suspendisse bibendum ex id dolor lacinia, in consectetur ipsum pellentesque. Aliquam imperdiet pulvinar metus vitae bibendum. Curabitur ut elementum augue, eget interdum libero.`);
    const [selectedPrivacy, setSelectedPrivacy] = useState('Public');

    useEffect(() => {
        // TODO: on page load, retrieve post data from backend
        // and fill in state hooks with data
    }, [])

    const handlePrivacyChange = (event) => {
        setSelectedPrivacy(event.target.value);
    };

    const editTextPost = async () => {
        setUpload(true);
        // TODO: Upload text post to backend
        // TODO: Redirect to Stream page
        // navigate("/stream")
    }

    const editImagePost = async () => {
        setUpload(true);
        // TODO: Upload image post to backend
        // TODO: Redirect to Stream page
        // navigate("/stream")
    }

    return (
        <>
            <Layout>
                <Card>
                    <>
                        {/* Post type selector */}
                        {postData === null && (
                            <CircularProgress sx={{ marginTop: "50px", marginBottom: "50px" }} />
                        )}

                        {(postData!== null && !belongsToUser) && (
                            <>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <QuizIcon sx={{fontSize: "60px", margin: "20px"}}/>
                                        <Typography variant="h6" align="center">Post not found.</Typography>
                                    </Grid>
                                </Grid>
                            </>
                        )}

                        {(postData !== null && belongsToUser) && (
                            <>
                                {/* Image Post */}
                                {/* TODO: show existing image */}
                                {postType === 'Image' && (
                                    <Grid container spacing={2}>
                                        <Grid item xs={12}>
                                            <Typography variant="h6" align="left" onChange={(event) => { setPostContent(event.target.value) }}>Upload an image</Typography>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <FormControl fullWidth>
                                                <InputLabel id="privacy-label">Privacy</InputLabel>
                                                <Select
                                                    label="Privacy"
                                                    value={selectedPrivacy}
                                                    onChange={handlePrivacyChange}
                                                >
                                                    <MenuItem value={'Public'}>Public</MenuItem>
                                                    <MenuItem value={'Friends Only'}>Friends Only</MenuItem>
                                                </Select>
                                            </FormControl>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Button variant="contained" fullWidth>Upload Image</Button>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Button>Or, set an image URL</Button>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        <Grid item xs={12}>
                                            {/* If uploading === true, display button with CircularProgress spinner inside */}
                                            {uploading ? (
                                                <Button variant="contained" fullWidth disabled>
                                                    <CircularProgress size={30} sx={{ margin: "5px" }} />
                                                </Button>
                                            ) : (
                                                <Button variant="contained" fullWidth onClick={() => { editImagePost() }}>Save Edits</Button>
                                            )}
                                        </Grid>
                                    </Grid>
                                )}

                                {/* Text/Markdown Post */}
                                {postType === 'Text' && (
                                    <Grid container spacing={2}>
                                        <Grid item xs={12}>
                                            <Typography variant="h6" align="left">Edit Post</Typography>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <FormControl fullWidth>
                                                <InputLabel id="privacy-label">Privacy</InputLabel>
                                                <Select
                                                    label="Privacy"
                                                    value={selectedPrivacy}
                                                    onChange={handlePrivacyChange}
                                                >
                                                    <MenuItem value={'Public'}>Public</MenuItem>
                                                    <MenuItem value={'Friends Only'}>Friends Only</MenuItem>
                                                </Select>
                                            </FormControl>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <TextField fullWidth multiline rows={6} placeholder="Write your post here..." value={postContent} onChange={(event) => { setPostContent(event.target.value) }} />
                                        </Grid>

                                        <Grid item xs={12}>
                                            {/* If uploading === true, display button with CircularProgress spinner inside */}
                                            {uploading ? (
                                                <Button variant="contained" fullWidth disabled>
                                                    <CircularProgress size={30} sx={{ margin: "5px" }} />
                                                </Button>
                                            ) : (
                                                // If postContent is empty, disable button
                                                postContent === '' ? (
                                                    <Button variant="contained" fullWidth disabled>Post</Button>
                                                ) : (
                                                    <Button variant="contained" fullWidth onClick={() => { editTextPost() }}>Save Edits</Button>
                                                )
                                            )}
                                        </Grid>
                                    </Grid>
                                )}
                            </>
                        )}
                    </>
                </Card>
            </Layout>
        </>
    )
}

export default EditPost;