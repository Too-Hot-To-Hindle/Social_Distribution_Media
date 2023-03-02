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

const Post = ({ 
    id, 
    type,
    title,
    description,
    categories,
    origin,
    source, 
    text, 
    imageURL, 
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

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    const handleDelete = () => {
        if (userID) {
            setDeleting(true);
            createAPIEndpoint(`authors/${userID}/posts/${id}`)
                .delete()
                .then(res => {
                    console.log(res.data)
                    navigate("/profile");
                    window.location.reload();
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }

    return (
        <>
            <Card>
                <Grid container spacing={2}>
                    {/* Post details */}
                    <Grid item xs={12}>
                        <div style={{ display: "flex", justifyContent: "space-between" }}>
                            <div style={{ display: "flex", alignItems: "center" }}>
                                <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />

                                <div>
                                    <Typography variant="h6" align="left">@{authorDisplayName}</Typography>
                                </div>
                            </div>

                            {!hideDetailsButton &&
                                <IconButton onClick={() => { navigate(`/${authorID}/post/${id}`) }}>
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
                        <Grid item xs={12}>
                            <Typography align="left">
                                <ReactMarkdown>{text}</ReactMarkdown>
                            </Typography>
                        </Grid>
                    }

                    {/* TODO: BASE64 text only? */}

                    {/* Image post content */}
                    {(type === "image/png;base64" || type === "image/jpeg;base64") &&
                        <Grid item xs={12}>
                            <Box sx={{ backgroundColor: "#343540", height: "300px", borderRadius: "5px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                                <img src={imageURL} alt="Image Preview" style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "5px" }} />
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
                                    <Button startIcon={liked ? <FavoriteIcon /> : <FavoriteBorderIcon />} onClick={() => { setLiked(!liked) }}>Like</Button>
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
                        <Grid item xs={12}>
                            <TextField fullWidth label="Shareable Link" value={link}></TextField>
                        </Grid>
                    }

                </Grid>
            </Card>
        </>
    )
}

export default Post;