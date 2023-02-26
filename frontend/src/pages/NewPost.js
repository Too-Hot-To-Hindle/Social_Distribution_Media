// React helpers
import { useState } from "react";
import { useNavigate } from 'react-router-dom';

// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { CircularProgress, Card, CardActionArea, Typography, Grid, TextField, Button, FormControl, InputLabel, Select, MenuItem, Divider } from "@mui/material";

// Material UI icons
import TextFieldsIcon from '@mui/icons-material/TextFields';
import ImageIcon from '@mui/icons-material/Image';

const NewPost = () => {

    const navigate = useNavigate();

    const [uploading, setUpload] = useState(false);
    const [postType, setPostType] = useState(null);
    const [postContent, setPostContent] = useState('');
    const [selectedPrivacy, setSelectedPrivacy] = useState('Public');

    const handlePrivacyChange = (event) => {
        setSelectedPrivacy(event.target.value);
    };

    const uploadTextPost = async () => {
        setUpload(true);
        // TODO: Upload text post to backend
        // TODO: Redirect to Stream page
        // navigate("/stream")
    }

    const uploadImagePost = async () => {
        setUpload(true);
        // TODO: Upload image post to backend
        // TODO: Redirect to Stream page
        // navigate("/stream")
    }

    return (
        <>
            <Layout>
                <Card>
                    {/* Post type selector */}
                    {postType === null && (
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Typography variant="h6" align="left">What would you like to post?</Typography>
                            </Grid>

                            <Grid item xs={6}>
                                <Card sx={{ padding: "0px", backgroundColor: "#343540" }}>
                                    <CardActionArea sx={{ padding: "10px" }} onClick={() => { setPostType('Text') }}>
                                        <TextFieldsIcon sx={{ fontSize: "60px" }} />
                                        <Typography variant="h6" align="center">Text/Markdown</Typography>
                                    </CardActionArea>
                                </Card>
                            </Grid>

                            <Grid item xs={6}>
                                <Card sx={{ padding: "0px", backgroundColor: "#343540" }}>
                                    <CardActionArea sx={{ padding: "10px" }} onClick={() => { setPostType('Image') }}>
                                        <ImageIcon sx={{ fontSize: "60px" }} />
                                        <Typography variant="h6" align="center">Image</Typography>
                                    </CardActionArea>
                                </Card>
                            </Grid>
                        </Grid>
                    )}

                    {/* Image Post */}
                    {/* TODO: show preview of image once uploaded/linked */}
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
                                    <Button variant="contained" fullWidth onClick={() => { uploadImagePost() }}>Post</Button>
                                )}
                            </Grid>
                        </Grid>
                    )}

                    {/* Text/Markdown Post */}
                    {postType === 'Text' && (
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Typography variant="h6" align="left">What's on your mind?</Typography>
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
                                <TextField fullWidth multiline rows={6} placeholder="Write your post here..."  onChange={(event) => {setPostContent(event.target.value) }}/>
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
                                        <Button variant="contained" fullWidth onClick={() => { uploadTextPost() }}>Post</Button>
                                    )
                                )}
                            </Grid>
                        </Grid>
                    )}
                </Card>
            </Layout>
        </>
    )
}

export default NewPost;