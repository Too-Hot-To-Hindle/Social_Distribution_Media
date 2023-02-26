// React helpers
import { useState } from "react";
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Alert, Box, CircularProgress, Card, CardActionArea, Typography, Grid, TextField, Button, FormControl, InputLabel, Select, MenuItem, Divider } from "@mui/material";

// Material UI icons
import TextFieldsIcon from '@mui/icons-material/TextFields';
import ImageIcon from '@mui/icons-material/Image';
import NoPhotographyIcon from '@mui/icons-material/NoPhotography';
import DriveFileRenameOutlineIcon from '@mui/icons-material/DriveFileRenameOutline';

const NewPost = () => {

    const navigate = useNavigate();

    const [uploading, setUpload] = useState(false);
    const [postType, setPostType] = useState(null);
    const [postContent, setPostContent] = useState('');
    const [selectedPrivacy, setSelectedPrivacy] = useState('Public');

    // image specific state hooks
    const [imageType, setImageType] = useState("upload");
    const [imageFile, setImageFile] = useState(null);
    const [uploadedImagePreview, setUploadedImagePreview] = useState(null)
    const [imageURL, setImageURL] = useState("");

    const handleFileSelect = (event) => {
        setImageFile(event.target.files[0]);

        const imageObjectURL = URL.createObjectURL(event.target.files[0]);
        setUploadedImagePreview(imageObjectURL);
    };

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
                                <Typography variant="h6" align="left">Post an image</Typography>
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

                            {imageType === "upload" && (
                                <>
                                    <Grid item xs={12}>
                                        {imageFile === null ? (
                                            <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                                <NoPhotographyIcon sx={{ marginRight: "10px" }} />
                                                <Typography variant="body2" align="center">No image uploaded</Typography>
                                            </Box>
                                        ) : (
                                            <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                                <img src={uploadedImagePreview} alt="Image Preview" style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "5px" }} />
                                            </Box>
                                        )}
                                    </Grid>

                                    <Grid item xs={12}>
                                        <Button variant="contained" fullWidth component="label">
                                            Upload Image
                                            <input
                                                type="file"
                                                onChange={handleFileSelect}
                                                hidden
                                                accept="image/*"
                                                multiple={false}
                                                id="upload-image-input"
                                            />
                                        </Button>
                                    </Grid>

                                    <Grid item xs={12}>
                                        <Button onClick={() => { setImageType("url") }}>Or, set an image URL</Button>
                                    </Grid>
                                </>
                            )}

                            {imageType === "url" && (
                                <>
                                    <Grid item xs={12}>
                                        <Typography variant="body1" fontWeight="500" align="left">Image Preview</Typography>
                                    </Grid>

                                    <Grid item xs={12}>
                                        {imageURL === "" ? (
                                            <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                                <NoPhotographyIcon sx={{ marginRight: "10px" }} />
                                                <Typography variant="body2" align="center">No image URL set</Typography>
                                            </Box>
                                        ) : (
                                            <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                                <img src={imageURL} alt="Image Preview" style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "5px" }} />
                                            </Box>
                                        )}
                                    </Grid>

                                    <Grid item xs={12}>
                                        <TextField fullWidth label="Image URL" placeholder="Enter URL" value={imageURL} onChange={(event) => { setImageURL(event.target.value) }} />
                                    </Grid>

                                    <Grid item xs={12}>
                                        <Button onClick={() => { setImageType("upload") }}>Or, upload an image</Button>
                                    </Grid>
                                </>
                            )}

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
                                    (imageURL === '' && imageFile === null) ? (
                                        <Button variant="contained" fullWidth disabled>Post</Button>
                                    ) : (
                                        <Button variant="contained" fullWidth onClick={() => { uploadImagePost() }}>Post</Button>
                                    )
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
                                    You can use CommonMark to format your post. <a href="https://commonmark.org/help/" target="_blank" style={{color: "#499BE9"}}>Click here</a> to learn more.
                                </Alert>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth multiline rows={6} placeholder="Write your post here..." onChange={(event) => { setPostContent(event.target.value) }} />
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