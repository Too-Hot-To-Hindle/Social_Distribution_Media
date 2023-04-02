// React helpers
import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { createAPIEndpoint } from '../api';
import { toast } from 'sonner';

// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Alert, Box, CircularProgress, FormGroup, FormControlLabel, Checkbox, Card, CardActionArea, Typography, Grid, TextField, Button, FormControl, InputLabel, Select, MenuItem, Divider } from "@mui/material";

// Material UI icons
import TextFieldsIcon from '@mui/icons-material/TextFields';
import ImageIcon from '@mui/icons-material/Image';
import NoPhotographyIcon from '@mui/icons-material/NoPhotography';
import DriveFileRenameOutlineIcon from '@mui/icons-material/DriveFileRenameOutline';

function isMarkdown(text) {
    return /^(#+\s|\*\*|__|- \S)/m.test(text);
}

const NewPost = () => {

    const navigate = useNavigate();

    const [uploading, setUpload] = useState(false);
    const [sharing, setSharing] = useState(false);
    const [share,setShare] = useState(true)
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

    const [userID, setUserID] = useState(null);

    useEffect(() => {
        setUserID(localStorage.getItem('author_id'))
    }, [])

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

    const handleAutoShareChange = (event) => {
        setShare(event.target.value);
    };

    const uploadTextPost = async () => {
        setUpload(true);
        if (userID) {
            var data;
            // if post is markdown, make a markdown type post in backend
            if (isMarkdown(postContent)) {
                data = {
                    title: postTitle,
                    description: postDescription,
                    //source: "https://google.com",
                    //origin: "https://google.com",
                    contentType: "text/markdown",
                    content: postContent,
                    categories: postCategories.replace(/\s/g, '').split(','),
                    visibility: selectedPrivacy,
                    unlisted: unlisted
                }


                createAPIEndpoint(`authors/${userID}/posts`)
                    .post(data)
                    .then(res => {

                        let id = res.data.id;
                        let origin = res.data.id;
                        let source = res.data.source;
                        let displayName = res.data.author.displayName;
                        if (share) {
                            var myAuthorData;
                                try {
                                    createAPIEndpoint(`authors/${userID}`)
                                    .get()
                                    .then(res => {
                                        myAuthorData = res.data;
                                        data = {
                                            "type": "post",
                                            "summary": displayName+" shared a post!",
                                            "author": {
                                                "type": "author",
                                                "id": myAuthorData.id,
                                                "host": myAuthorData.host,
                                                "displayName": myAuthorData.displayName,
                                                "url": myAuthorData.url,
                                                "github": myAuthorData.github,
                                                "profileImage": myAuthorData.profileImage
                                            },
                                            "object": {
                                                "type": "post",
                                                "author": {
                                                    "type": "author",
                                                    "id": myAuthorData.id,
                                                    "host": myAuthorData.host,
                                                    "displayName": myAuthorData.displayName,
                                                    "url": myAuthorData.url,
                                                    "github": myAuthorData.github,
                                                    "profileImage": myAuthorData.profileImage
                                                },
                                                "id": id,
                                                "title": postTitle,
                                                "source": source,
                                                "origin": origin,
                                                "description": postDescription,
                                                "contentType": "text/markdown",
                                                "content": postContent,
                                                "categories": postCategories.replace(/\s/g, '').split(','),
                                                "count": 0,
                                                "comments": id + "/comments",
                                                "commentsSrc": {},
                                                "visibility": selectedPrivacy,
                                                "unlisted": unlisted,
                                            }
                                        }

                                        for (let ID of res.data.followers){
                                            try {
                                                createAPIEndpoint(`authors/${ID}/inbox`)
                                                .post(data)
                                                .then(res => {
                                                    //console.log("RESPONSE:",res.data);
                                                })
                                            }
                                            catch (err) {
                                                toast.error('An error has occurred.', {
                                                    description: "Could not post to your followers' inboxes. Please try again later.",
                                                });
                                            }
                                            
                                        }
                                        
                                    })
                                }
                            catch (err) {
                                toast.error('An error has occurred.', {
                                    description: 'Could not retrieve your follower details. Please try again later.',
                                });
                            }
                        }
                        navigate(`/profile/${userID}`)
                        setUpload(false)
                    })
                    .catch(err => {
                        toast.error('An error has occurred.', {
                            description: 'Your post could not be created at this time. Please try again later.',
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

                
                createAPIEndpoint(`authors/${userID}/posts`)
                    .post(data)
                    .then(res => {

                    let id = res.data.id;
                    let origin = res.data.id;
                    let source = res.data.source;
                    let displayName = res.data.author.displayName;
                    if (share) {
                        var myAuthorData;
                            try {
                                createAPIEndpoint(`authors/${userID}`)
                                .get()
                                .then(res => {
                                    myAuthorData = res.data;
                                    data = {
                                        "type": "post",
                                        "summary": displayName+" shared a post!",
                                        "author": {
                                            "type": "author",
                                            "id": myAuthorData.id,
                                            "host": myAuthorData.host,
                                            "displayName": myAuthorData.displayName,
                                            "url": myAuthorData.url,
                                            "github": myAuthorData.github,
                                            "profileImage": myAuthorData.profileImage
                                        },
                                        "object": {
                                            "type": "post",
                                            "author": {
                                                "type": "author",
                                                "id": myAuthorData.id,
                                                "host": myAuthorData.host,
                                                "displayName": myAuthorData.displayName,
                                                "url": myAuthorData.url,
                                                "github": myAuthorData.github,
                                                "profileImage": myAuthorData.profileImage
                                            },
                                            "id": id,
                                            "title": postTitle,
                                            "source": source,
                                            "origin": origin,
                                            "description": postDescription,
                                            "contentType": "text/plain",
                                            "content": postContent,
                                            "categories": postCategories.replace(/\s/g, '').split(','),
                                            "count": 0,
                                            "comments": id + "/comments",
                                            "commentsSrc": {},
                                            "visibility": selectedPrivacy,
                                            "unlisted": unlisted,
                                        }
                                    }

                                    for (let ID of res.data.followers){
                                        try {
                                            createAPIEndpoint(`authors/${ID}/inbox`)
                                            .post(data)
                                            .then(res => {
                                                //console.log("RESPONSE:",res.data);
                                            })
                                        }
                                        catch (err) {
                                            toast.error('An error has occurred.', {
                                                description: "Could not post to your followers' inboxes. Please try again later.",
                                            });
                                        }
                                        
                                    }
                                    
                                })
                            }
                        catch (err) {
                            toast.error('An error has occurred.', {
                                description: 'Could not retrieve your follower details. Please try again later.',
                            });
                        }
                    }






                        navigate(`/profile/${userID}`)
                        setUpload(false)
                    })
                    .catch(err => {
                        toast.error('An error has occurred.', {
                            description: 'Your post could not be created at this time. Please try again later.',
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


            await createAPIEndpoint(`authors/${userID}/posts`)
                .post(data)
                .then(res => {
                    let id = res.data.id;
                    let origin = res.data.id;
                    let source = res.data.source;
                    let displayName = res.data.author.displayName;
                    if (share) {
                        var myAuthorData;
                            try {
                                createAPIEndpoint(`authors/${userID}`)
                                .get()
                                .then(res => {
                                    myAuthorData = res.data;
                                    data = {
                                        "type": "post",
                                        "summary": displayName+" shared a post!",
                                        "author": {
                                            "type": "author",
                                            "id": myAuthorData.id,
                                            "host": myAuthorData.host,
                                            "displayName": myAuthorData.displayName,
                                            "url": myAuthorData.url,
                                            "github": myAuthorData.github,
                                            "profileImage": myAuthorData.profileImage
                                        },
                                        "object": {
                                            "type": "post",
                                            "author": {
                                                "type": "author",
                                                "id": myAuthorData.id,
                                                "host": myAuthorData.host,
                                                "displayName": myAuthorData.displayName,
                                                "url": myAuthorData.url,
                                                "github": myAuthorData.github,
                                                "profileImage": myAuthorData.profileImage
                                            },
                                            "id": id,
                                            "title": postTitle,
                                            "source": source,
                                            "origin": origin,
                                            "description": postDescription,
                                            "contentType": contentTypeToBe,
                                            "content": contentToBe,
                                            "categories": postCategories.replace(/\s/g, '').split(','),
                                            "count": 0,
                                            "comments": id + "/comments",
                                            "commentsSrc": {},
                                            "visibility": selectedPrivacy,
                                            "unlisted": unlisted,
                                        }
                                    }
                                    
                                    for (let ID of res.data.followers){
                                        try {
                                            createAPIEndpoint(`authors/${ID}/inbox`)
                                            .post(data)
                                            .then(res => {
                                                //console.log("RESPONSE:",res.data);
                                            })
                                        }
                                        catch (err) {
                                            toast.error('An error has occurred.', {
                                                description: "Could not post to your followers' inboxes. Please try again later.",
                                            });
                                        }
                                        
                                    }
                                    
                                })
                            }
                        catch (err) {
                            toast.error('An error has occurred.', {
                                description: 'Could not retrieve your follower details. Please try again later.',
                            });
                        }
                    } 
                    setUpload(false);
                    navigate(`/profile`);
                }
                )
                .catch(err => {
                    toast.error('An error has occurred.', {
                        description: 'Your post could not be created at this time. Please try again later.',
                    });
                });

            


            
        }
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
                    {postType === 'Image' && (
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Typography variant="h6" align="left">Post an image</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="body1" fontWeight="500" align="left">Post Title</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth placeholder="Write your title here..." onChange={(event) => { setPostTitle(event.target.value) }} />
                            </Grid>

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="body1" fontWeight="500" align="left">Post Description</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth placeholder="Write your description here..." onChange={(event) => { setPostDescription(event.target.value) }} />
                            </Grid>

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="body1" fontWeight="500" align="left">Post Catgeory</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth placeholder="Denote categories separated by commas" onChange={(event) => { setPostCategories(event.target.value) }} />
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

                            <Grid item xs={12}>
                                <FormControl fullWidth>
                                    <InputLabel id="autoshare-label">Share?</InputLabel>
                                    <Select
                                        label="Privacy"
                                        value={share}
                                        onChange={handleAutoShareChange}
                                    >
                                        <MenuItem value={true}>Share Post Automatically on Creation</MenuItem>
                                        <MenuItem value={false}>Don't Share</MenuItem>
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

                    {/* Text/Markdown Post */}
                    {postType === 'Text' && (
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Typography variant="h6" align="left">What's on your mind?</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="body1" fontWeight="500" align="left">Post Title</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth placeholder="Write your title here..." onChange={(event) => { setPostTitle(event.target.value) }} />
                            </Grid>

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="body1" fontWeight="500" align="left">Post Description</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth placeholder="Write your description here..." onChange={(event) => { setPostDescription(event.target.value) }} />
                            </Grid>

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="body1" fontWeight="500" align="left">Post Catgeory</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth placeholder="Denote categories separated by commas" onChange={(event) => { setPostCategories(event.target.value) }} />
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
                                <FormControl fullWidth>
                                    <InputLabel id="autoshare-label">Share?</InputLabel>
                                    <Select
                                        label="Privacy"
                                        value={share}
                                        onChange={handleAutoShareChange}
                                    >
                                        <MenuItem value={true}>Share Post Automatically on Creation</MenuItem>
                                        <MenuItem value={false}>Don't Share</MenuItem>
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
                                    You can use CommonMark to format your post. <a href="https://commonmark.org/help/" target="_blank" rel="noreferrer" style={{ color: "#499BE9" }}>Click here</a> to learn more.
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
                                    (postTitle === '' || postDescription === '' || postCategories === '' || postContent === '') ? (
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