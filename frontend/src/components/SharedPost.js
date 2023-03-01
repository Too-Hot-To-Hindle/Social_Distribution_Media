// React helpers
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Material UI components
import { Card, Typography, Grid, Divider, IconButton, Button, TextField } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ReadMoreIcon from '@mui/icons-material/ReadMore';
import EditIcon from '@mui/icons-material/Edit';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import CommentIcon from '@mui/icons-material/Comment';
import RepeatIcon from '@mui/icons-material/Repeat';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';

const SharedPost = ({ hideDetailsButton, hideEditButton, hideLikeButton, hideCommentButton, hideShareButton, hideDeleteButton, hideLink }) => {

    const navigate = useNavigate();

    const [liked, setLiked] = useState(false);

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
                                    <Typography variant="h6" align="left">John Smith</Typography>
                                    <Typography variant="body1" align="left">@johnsmith</Typography>
                                </div>
                            </div>

                            {!hideDetailsButton &&
                                <IconButton onClick={() => { navigate("/post/123") }}>
                                    <ReadMoreIcon />
                                </IconButton>
                            }

                            {!hideEditButton &&
                                <IconButton onClick={() => { navigate("/post/123/edit") }}>
                                    <EditIcon />
                                </IconButton>
                            }
                        </div>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    {/* Post content */}
                    <Grid item xs={12}>
                        <Typography variant="body1" align="left">
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla augue nisi, pharetra at risus et, gravida tempus purus.
                            Ut euismod elit eget nisl luctus, eget euismod sapien fermentum. Mauris bibendum, felis eget lacinia auctor,
                            tortor odio ornare orci, sit amet volutpat arcu eros ac est. Pellentesque non purus vel lectus dictum gravida quis a felis.
                            In sed quam nulla. Sed sollicitudin mi felis, sed molestie sem dignissim in. Etiam nec blandit mi. Curabitur vel feugiat velit.
                            Sed bibendum purus eu nunc vulputate, sed auctor nisl fermentum. Vivamus laoreet ex mauris, at interdum arcu vehicula nec.
                            Donec sodales tortor a dui placerat, sit amet pharetra elit aliquam. Praesent eget urna mauris. Nunc varius lectus quis sodales posuere.
                            Suspendisse bibendum ex id dolor lacinia, in consectetur ipsum pellentesque. Aliquam imperdiet pulvinar metus vitae bibendum. Curabitur
                            ut elementum augue, eget interdum libero.
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    {/* Share details */}
                    <Grid item xs={12}>
                        <div style={{ display: "flex", justifyContent: "space-between" }}>
                            <div style={{ display: "flex", alignItems: "center" }}>
                                <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />

                                <div>
                                    <Typography variant="body1" align="left">shared from:</Typography>
                                    <Typography variant="h6" align="left">Jane Doe</Typography>
                                    <Typography variant="body1" align="left">@janedoe</Typography>
                                </div>
                            </div>

                            <Button>See Original</Button>
                        </div>
                    </Grid>

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
                                    <Button startIcon={<DeleteForeverIcon />}>Delete</Button>
                                </div>
                            }
                        </div>
                    </Grid>

                    {!hideLink &&
                        <Grid item xs={12}>
                            <TextField fullWidth label="Shareable Link" value={"https://abc123.com/post/abc123"}></TextField>
                        </Grid>
                    }

                </Grid>
            </Card>
        </>
    )
}

export default SharedPost;