// React helpers
import { useState, useEffect } from "react";
import { useNavigate, useParams } from 'react-router-dom';
import { createAPIEndpoint, ENDPOINTS } from '../api';
import ReactMarkdown from 'react-markdown';

// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Alert, Box, CircularProgress, Card, Typography, Grid, TextField, Button, FormControl, InputLabel, Select, MenuItem, Divider, FormGroup, FormControlLabel, Checkbox } from "@mui/material";

// Material UI icons
import QuizIcon from '@mui/icons-material/Quiz';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import DriveFileRenameOutlineIcon from '@mui/icons-material/DriveFileRenameOutline';

function isMarkdown(text) {
    return /^(#+\s|\*\*|\_\_|\- \S)/m.test(text);
}

const EditPost = () => {

    const navigate = useNavigate();

    const { authorID, postID } = useParams()
    const [authorData, setAuthorData] = useState(null);
    const [postData, setPostData] = useState(null);
    const [belongsToUser, setBelongsToUser] = useState(false);

    const [postType, setPostType] = useState(null);
    const [postTitle, setPostTitle] = useState("");
    const [postDescription, setPostDescription] = useState("");
    const [postContent, setPostContent] = useState('');
    const [postCategories, setPostCategories] = useState('');
    const [selectedPrivacy, setSelectedPrivacy] = useState('Public');
    const [unlisted, setUnlisted] = useState(false);

    const [uploading, setUpload] = useState(false);

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
                .then(authorRes => {
                    setAuthorData(authorRes.data)

                    // get post information
                    createAPIEndpoint(`authors/${authorID}/posts/${postID}`)
                        .get()
                        .then(res => {
                            setPostData(res.data)
                            setBelongsToUser(authorRes.data["_id"] === userID)
                            setPostType(res.data.contentType)
                            setPostTitle(res.data.title)
                            setPostDescription(res.data.description)
                            setPostContent(res.data.content)
                            setPostCategories(res.data.categories)
                            setSelectedPrivacy(res.data.visibility)
                            setUnlisted(res.data.unlisted)
                        })
                        .catch(err => {
                            // TODO: Add in error handling
                            if (err.response.status === 404) {
                                setPostData({})
                                setBelongsToUser(false)
                            }
                            console.log(err)
                        });
                })
                .catch(err => {
                    // TODO: Add in error handling
                    if (err.response.status === 404) {
                        setPostData({})
                        setBelongsToUser(false)
                    }
                    console.log(err)
                });
        }
    }, [userID]);

    const handlePrivacyChange = (event) => {
        setSelectedPrivacy(event.target.value);
    };

    const editTextPost = async () => {
        setUpload(true);
        if (userID) {
            // if post is markdown, make a markdown type post in backend
            if (isMarkdown(postContent)) {
                var data = new URLSearchParams();
                data.append('title', postTitle);
                data.append('description', postDescription);
                data.append('source', "https://google.com");
                data.append('origin', "https://google.com");
                data.append('contentType', "text/markdown");
                data.append('content', postContent);
                data.append('categories', postCategories.replace(/\s/g, '').split(','));
                data.append('visibility', selectedPrivacy);
                data.append('unlisted', unlisted);

                createAPIEndpoint(`authors/${userID}/posts/${postID}`)
                    .post(data)
                    .then(res => {
                        navigate("/profile")
                        setUpload(false)
                    })
                    .catch(err => {
                        // TODO: Add in error handling
                        console.log(err)
                    });
            }

            // otherwise, create a plaintext post in backend
            else {
                var data = new URLSearchParams();
                data.append('title', postTitle);
                data.append('description', postDescription);
                data.append('source', "https://google.com");
                data.append('origin', "https://google.com");
                data.append('contentType', "text/plain");
                data.append('content', postContent);
                data.append('categories', postCategories.replace(/\s/g, '').split(','));
                data.append('visibility', selectedPrivacy);
                data.append('unlisted', unlisted);

                createAPIEndpoint(`authors/${userID}/posts`)
                    .post(data)
                    .then(res => {
                        navigate("/profile")
                        setUpload(false)
                    })
                    .catch(err => {
                        // TODO: Add in error handling
                        console.log(err)
                    });
            }
        }
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
                        {postData === null && (
                            <CircularProgress sx={{ marginTop: "50px", marginBottom: "50px" }} />
                        )}

                        {(postData !== null && !belongsToUser) && (
                            <>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <QuizIcon sx={{ fontSize: "60px", margin: "20px" }} />
                                        <Typography variant="h6" align="center">Post not found.</Typography>
                                    </Grid>
                                </Grid>
                            </>
                        )}

                        {(postData !== null && belongsToUser) && (
                            <>
                                {/* Image Post */}
                                {/* TODO: setup editing image posts */}
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
                                {(postType === 'text/plain' || postType === "text/markdown") && (
                                    <Grid container spacing={2}>
                                        <Grid item xs={12}>
                                            <Typography variant="h6" align="left">Edit Post</Typography>
                                        </Grid>

                                        {/* Post author */}
                                        <Grid item xs={12}>
                                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                                <div style={{ display: "flex", alignItems: "center" }}>
                                                    <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />

                                                    <div>
                                                        <Typography variant="h6" align="left">@{authorData.displayName}</Typography>
                                                    </div>
                                                </div>
                                            </div>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        {/* Post title and description */}
                                        <Grid item xs={12}>
                                            <Typography variant="body1" fontWeight="500" align="left">Post Title</Typography>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <TextField fullWidth value={postTitle} placeholder="Write your title here..." onChange={(event) => { setPostTitle(event.target.value) }} />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Typography variant="body1" fontWeight="500" align="left">Post Description</Typography>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <TextField fullWidth value={postDescription} placeholder="Write your description here..." onChange={(event) => { setPostDescription(event.target.value) }} />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Typography variant="body1" fontWeight="500" align="left">Post Catgeory</Typography>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <TextField fullWidth value={postCategories} placeholder="Denote categories separated by commas" onChange={(event) => { setPostCategories(event.target.value) }} />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                                <FormControl fullWidth sx={{ marginRight: "15px" }}>
                                                    <InputLabel id="privacy-label">Privacy</InputLabel>
                                                    <Select
                                                        label="Privacy"
                                                        value={selectedPrivacy}
                                                        onChange={handlePrivacyChange}
                                                    >
                                                        <MenuItem value={'PUBLIC'}>Public</MenuItem>
                                                        <MenuItem value={'FRIENDS'}>Friends Only</MenuItem>
                                                    </Select>
                                                </FormControl>

                                                <FormGroup>
                                                    <FormControlLabel control={<Checkbox checked={unlisted} onChange={(event) => { setUnlisted(event.target.checked) }} />} label="Unlisted" />
                                                </FormGroup>
                                            </div>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Typography variant="body1" fontWeight="500" align="left">Content Preview</Typography>
                                        </Grid>

                                        <Grid item xs={12}>
                                            {postContent === "" ? (
                                                <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                                    <DriveFileRenameOutlineIcon sx={{ marginRight: "10px" }} />
                                                    <Typography variant="body2" align="center">Start writing to preview your post</Typography>
                                                </Box>
                                            ) : (
                                                <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", paddingLeft: "10px", paddingRight: "10px", overflowY: "scroll" }}>
                                                    <Typography align="left">
                                                        <ReactMarkdown>{postContent}</ReactMarkdown>
                                                    </Typography>
                                                </Box>
                                            )}
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Alert severity="info">
                                                You can use CommonMark to format your post. <a href="https://commonmark.org/help/" target="_blank" style={{ color: "#499BE9" }}>Click here</a> to learn more.
                                            </Alert>
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
                                                (postTitle === '' || postDescription === '' || postCategories === '' || postContent === '') ? (
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