// React helpers
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { createAPIEndpoint, ENDPOINTS } from '../api';

// Material UI components
import { Card, Typography, Grid, Divider, IconButton, Button, TextField, Box, CircularProgress } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ReadMoreIcon from '@mui/icons-material/ReadMore';
import EditIcon from '@mui/icons-material/Edit';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import CommentIcon from '@mui/icons-material/Comment';
import RepeatIcon from '@mui/icons-material/Repeat';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';

// Helper functions
// isMarkdownImage checks if a string is a markdown image
const isMarkdownImage = (str) => {
    return (str.startsWith('![') && str.endsWith(')'));
}

// extractMarkdownImageURL extracts the image URL from a markdown image
const extractMarkdownImageURL = (str) => {
    return str.substring(str.indexOf('(') + 1, str.indexOf(')'));
}

const Post = ({
    id,
    type,
    title,
    description,
    categories,
    origin,
    source,
    content,
    authorDisplayName,
    authorID,
    link,
    hideDetailsButton,
    hideEditButton,
    hideLikeButton,
    hideCommentButton,
    hideShareButton,
    hideDeleteButton,
    hideSource,
    hideOrigin,
    hideCategories,
    hideLink }) => {

    const navigate = useNavigate();

    const [liked, setLiked] = useState(false);
    const [deleting, setDeleting] = useState(false);

    const [likes, setLikes] = useState([]);
    const [myAuthorData, setMyAuthorData] = useState(null);

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])
    /*
    useEffect(() => {
        if (userID) {
            createAPIEndpoint(`authors/${userID}/posts/${id}/likes`)
                .get()
                .then(res => {
                    setLikes(res.data)
                    for (const like of res.data) {
                        if (like.author._id === userID) {
                            setLiked(true)
                        }
                    }

                })
                .catch(err => {
                    console.log(err)
                })
        }
    }, [userID])*/

    // get currently logged in author information
    useEffect(() => {
        if (userID) {
            createAPIEndpoint(`authors/${authorID}`)
                .get()
                .then(res => {
                    setMyAuthorData(res.data)
                })
                .catch(err => {
                    console.log(err)
                })
        }
    }, [userID])

    const handleDelete = () => {
        if (userID) {
            setDeleting(true);
            createAPIEndpoint(`authors/${userID}/posts/${id}`)
                .delete()
                .then(res => {
                    navigate("/profile");
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }

    const handleLike = () => {
        if (userID && myAuthorData) {
            if (!liked) {
                setLiked(true)

                var data = {
                    "type": "like",
                    "summary": `${username} likes your post!`,
                    "author": {
                        "type": "author",
                        "id": myAuthorData.id,
                        "host": myAuthorData.host,
                        "displayName": myAuthorData.displayName,
                        "url": myAuthorData.url,
                        "github": myAuthorData.github,
                        "profileImage": myAuthorData.profileImage
                    },
                    "object": `https://social-distribution-media.herokuapp.com/api/authors/${authorID}/posts/${id}`
                }


                createAPIEndpoint(`authors/${authorID}/inbox`)
                    .post(data)
                    .then(res => {
                        // refresh page
                        window.location.reload();
                    })
                    .catch(err => {
                        console.log(err)
                    })
            }
        }
    }

    //ReactMarkdown accepts custom renderers
    const renderers = {
        //This custom renderer changes how images are rendered
        //we use it to constrain the max width of an image to its container
        image: ({
            alt,
            src,
            title,
        }) => (
            <img
                alt={alt}
                src={src}
                title={title}
                style={{ maxWidth: "100px" }} />
        ),
    };

    return (
        <>
            <Card>
                <Grid container spacing={2}>
                    {/* Post details */}
                    <Grid item xs={12}>
                        <div style={{ display: "flex", justifyContent: "space-between" }}>
                            <div style={{ display: "flex", alignItems: "left" }}>
                                <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />

                                <div>
                                    <Typography variant="h6" align="left">@{authorDisplayName}</Typography>
                                </div>
                            </div>

                            {!hideDetailsButton &&
                                <IconButton onClick={() => { navigate(`/${encodeURIComponent(authorID)}/post/${encodeURIComponent(id)}`) }}>
                                    <ReadMoreIcon />
                                </IconButton>
                            }

                            {!hideEditButton &&
                                <IconButton onClick={() => { navigate(`/${authorID}/post/${id}/edit`) }}>
                                    <EditIcon />
                                </IconButton>
                            }
                        </div>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    {/* Post title and description */}
                    <Grid item xs={12}>
                        <Typography variant="h6" align="left">{title}</Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Typography align="left">{description}</Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    {/* Text post content */}
                    {(type === "text/plain" || type === "text/markdown") &&
                        <>
                            {(isMarkdownImage(content)) ? (
                                <Grid item xs={12}>
                                    <Box sx={{ backgroundColor: "#343540", minHeight: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                        <img src={extractMarkdownImageURL(content)} alt="Image Preview" style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "5px", margin: "20px" }} />
                                    </Box>
                                </Grid>
                            ) :
                                (<Grid item xs={12}>
                                    <Box sx={{ backgroundColor: "#343540", minHeight: "300px", borderRadius: "5px", textAlign: "left", padding: "10px" }}>
                                        <ReactMarkdown>{content}</ReactMarkdown>
                                    </Box>
                                </Grid>)
                            }
                        </>

                    }

                    {/* TODO: BASE64 text only? */}

                    {/* Image post content */}
                    {(type === "image/png;base64" || type === "image/jpeg;base64") &&
                        <Grid item xs={12}>
                            <Box sx={{ backgroundColor: "#343540", minHeight: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                <img src={content} alt="Image Preview" style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "5px", margin: "20px" }} />
                            </Box>
                        </Grid>
                    }

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    {/* Post actions */}
                    <Grid item xs={12}>
                        <div style={{ display: "flex", justifyContent: "space-between" }}>

                            {!hideLikeButton &&
                                <div style={{ display: "flex", alignItems: "center" }}>
                                    <Button startIcon={liked ? <FavoriteIcon /> : <FavoriteBorderIcon />} onClick={() => { handleLike() }}>{liked ? "Like Sent" : "Send Like"}</Button>
                                </div>
                            }

                            {!hideCommentButton &&
                                <div style={{ display: "flex", alignItems: "center" }}>
                                    <Button startIcon={<CommentIcon />}>Comment</Button>
                                </div>
                            }

                            {!hideShareButton &&
                                <div style={{ display: "flex", alignItems: "center" }}>
                                    <Button startIcon={<RepeatIcon />}>Share</Button>
                                </div>
                            }

                            {!hideDeleteButton &&
                                <div style={{ display: "flex", alignItems: "center" }}>
                                    {deleting ? <CircularProgress size="24px" /> : <Button startIcon={<DeleteForeverIcon />} onClick={() => { handleDelete() }}>Delete</Button>}
                                </div>
                            }
                        </div>
                    </Grid>



                    {!hideLink &&
                        <>
                            <Grid item xs={12}>
                                <TextField fullWidth label="Source" value={source}></TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth label="Origin" value={origin}></TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth label="Post URI" value={link}></TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField fullWidth label="Shareable Link" value={`https://social-distribution-media.herokuapp.com/${encodeURIComponent(authorID)}/post/${encodeURIComponent(id)}`}></TextField>
                            </Grid>
                        </>
                    }

                </Grid>
            </Card>
        </>
    )
}

export default Post;