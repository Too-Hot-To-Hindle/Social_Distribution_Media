// React helpers
import { useState, useEffect } from "react";
import { useNavigate, useParams } from 'react-router-dom';
import { createAPIEndpoint } from '../api';
import ReactMarkdown from 'react-markdown';
import { toast } from 'sonner';

// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Alert, Box, CircularProgress, Card, Typography, Grid, TextField, Button, FormControl, InputLabel, Select, MenuItem, Divider, FormGroup, FormControlLabel, Checkbox } from "@mui/material";

// Material UI icons
import QuizIcon from '@mui/icons-material/Quiz';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import DriveFileRenameOutlineIcon from '@mui/icons-material/DriveFileRenameOutline';
import NoPhotographyIcon from '@mui/icons-material/NoPhotography';

// Helper functions
function isMarkdown(text) {
    return /^(#+\s|\*\*|__|- \S)/m.test(text);
}

// isMarkdownImage checks if a string is a markdown image
const isMarkdownImage = (str) => {
    return (str.startsWith('![') && str.endsWith(')'));
}

// extractMarkdownImageURL extracts the image URL from a markdown image
const extractMarkdownImageURL = (str) => {
    return str.substring(str.indexOf('(') + 1, str.indexOf(')'));
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

    // image specific state hooks
    const [imageType, setImageType] = useState("upload");
    const [imageFile, setImageFile] = useState(null);
    const [imageBase64, setImageBase64] = useState(null);
    const [imageURL, setImageURL] = useState("");

    const [uploading, setUpload] = useState(false);

    const [userID, setUserID] = useState(null);

    useEffect(() => {
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
                            setPostCategories(res.data.categories.join())
                            setSelectedPrivacy(res.data.visibility)
                            setUnlisted(res.data.unlisted)

                            
                            if (res.data.contentType === "image/png;base64" || res.data.contentType === "image/jpeg;base64" || res.data.contentType === "image/jpg;base64") {
                                // if res.data begins with 'http', consider it a linked image
                                if (res.data.content.startsWith('http')) {
                                    setImageType("url")
                                    setImageURL(res.data.content)
                                }

                                // otherwise, consider it a base64 image
                                else {
                                    setImageType("upload")
                                    setImageBase64(res.data.content)
                                }
                            }

                            if ((res.data.contentType === "text/markdown" || res.data.contentType === "text/plain") && isMarkdownImage(res.data.content)) {
                                setImageType("url")
                                setImageURL(extractMarkdownImageURL(res.data.content))
                            }

                        })
                        .catch(err => {
                            // TODO: Add in error handling
                            if (err.response.status === 404) {
                                setPostData({})
                                setBelongsToUser(false)
                            }
                            toast.error('An error has occurred.', {
                                description: 'There was an error retrieving this post. Please try again later.',
                            });
                        });
                })
                .catch(err => {
                    // TODO: Add in error handling
                    if (err.response.status === 404) {
                        setPostData({})
                        setBelongsToUser(false)
                    }
                    else {
                        toast.error('An error has occurred.', {
                            description: 'There was an error retrieving author information for this post. Please try again later.',
                        });
                    }
                });
        }
    }, [userID, authorID, postID]);

    const handleFileSelect = (event) => {
        setImageFile(event.target.files[0]);

        const reader = new FileReader();
        reader.onloadend = () => {
            // set the state to the base64 string
            setImageBase64(reader.result);
        };

        reader.readAsDataURL(event.target.files[0]);
    };

    const handlePrivacyChange = (event) => {
        setSelectedPrivacy(event.target.value);
    };

    const editTextPost = async () => {
        setUpload(true);
        if (userID) {
            // if post is markdown, make a markdown type post in backend
            var data;
            if (isMarkdown(postContent)) {

                data = {
                    title: postTitle,
                    description: postDescription,
                    contentType: "text/markdown",
                    content: postContent,
                    categories: postCategories.replace(/\s/g, '').split(','),
                    visibility: selectedPrivacy,
                    unlisted: unlisted
                }

                createAPIEndpoint(`authors/${userID}/posts/${postID}`)
                    .post(data)
                    .then(res => {
                        navigate(`/profile/${userID}`)
                        setUpload(false)
                    })
                    .catch(err => {
                        toast.error('An error has occurred.', {
                            description: 'The post could not be edited at this time. Please try again later.',
                        });
                    });
            }

            // otherwise, create a plaintext post in backend
            else {

                data = {
                    title: postTitle,
                    description: postDescription,
                    contentType: "text/plain",
                    content: postContent,
                    categories: postCategories.replace(/\s/g, '').split(','),
                    visibility: selectedPrivacy,
                    unlisted: unlisted
                }

                createAPIEndpoint(`authors/${userID}/posts/${postID}`)
                    .post(data)
                    .then(res => {
                        navigate(`/profile/${userID}`)
                        setUpload(false)
                    })
                    .catch(err => {
                        toast.error('An error has occurred.', {
                            description: 'The post could not be edited at this time. Please try again later.',
                        });
                    });
            }
        }
    }

    const uploadImagePost = async () => {
        setUpload(true);
        if (userID) {
            var data = {}
            var contentTypeToBe = "";
            var contentToBe = "";
            if (imageType === "upload") {
                if (imageFile.type === "image/png") {
                    contentTypeToBe = "image/png;base64";
                    contentToBe = imageBase64;
                } else if (imageFile.type === "image/jpeg") {
                    contentTypeToBe = "image/jpeg;base64";
                    contentToBe = imageBase64;
                } else if (imageFile.type === "image/jpg") {
                    contentTypeToBe = "image/jpg;base64";
                    contentToBe = imageBase64;
                }
            } else if (imageType === "url") {
                contentTypeToBe = "text/markdown";
                contentToBe = `![${imageURL}](${imageURL})`;
            }

            data = {
                title: postTitle,
                description: postDescription,
                contentType: contentTypeToBe,
                content: contentToBe,
                categories: postCategories.replace(/\s/g, '').split(','),
                visibility: selectedPrivacy,
                unlisted: unlisted
            }

            createAPIEndpoint(`authors/${userID}/posts/${postID}`)
                .post(data)
                .then(res => {
                    navigate(`/profile/${userID}`)
                    setUpload(false)
                })
                .catch(err => {
                    toast.error('An error has occurred.', {
                        description: 'The post could not be edited at this time. Please try again later.',
                    });
                });
        }
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
                                {/* Image File Post */}
                                {(postType === 'image/png;base64' || postType === 'image/jpeg;base64' || postType === "image/jpg;base64") && (
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
                                            <FormControl fullWidth>
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
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

                                        {imageType === "upload" && (
                                            <>
                                                <Grid item xs={12}>
                                                    {imageBase64 === null ? (
                                                        <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                                            <NoPhotographyIcon sx={{ marginRight: "10px" }} />
                                                            <Typography variant="body2" align="center">No image uploaded</Typography>
                                                        </Box>
                                                    ) : (
                                                        <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                                            <img src={imageBase64} alt="Preview" style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "5px" }} />
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
                                                            accept="image/jpeg,image/png"
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
                                                            <img src={imageURL} alt="Preview" style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "5px" }} />
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
                                                ((imageURL === '' && imageBase64 === null) || postTitle === '' || postDescription === '' || postCategories === '') ? (
                                                    <Button variant="contained" fullWidth disabled>Post</Button>
                                                ) : (
                                                    <Button variant="contained" fullWidth onClick={() => { uploadImagePost() }}>Post</Button>
                                                )
                                            )}
                                        </Grid>
                                    </Grid>
                                )}

                                {/* Image URL Post */}
                                {((postType === 'text/plain' || postType === "text/markdown") && isMarkdownImage(postContent)) && (
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
                                            <FormControl fullWidth>
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
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>

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
                                                            <img src={imageURL} alt="Preview" style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "5px" }} />
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
                                                ((imageURL === '' && imageBase64 === null) || postTitle === '' || postDescription === '' || postCategories === '') ? (
                                                    <Button variant="contained" fullWidth disabled>Post</Button>
                                                ) : (
                                                    <Button variant="contained" fullWidth onClick={() => { uploadImagePost() }}>Post</Button>
                                                )
                                            )}
                                        </Grid>
                                    </Grid>
                                )}

                                {/* Text/Markdown Post */}
                                {((postType === 'text/plain' || postType === "text/markdown") && !isMarkdownImage(postContent)) && (
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
                                                You can use CommonMark to format your post. <a href="https://commonmark.org/help/" target="_blank" rel="noreferrer" style={{ color: "#499BE9" }}>Click here</a> to learn more.
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