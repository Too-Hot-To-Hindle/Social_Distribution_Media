// React helpers
import { useState, useEffect } from "react";
import { createAPIEndpoint, ENDPOINTS } from '../api';

// Layout components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";

// Material UI components
import { Card, Typography, Grid, Button, Divider, TextField, InputAdornment, CircularProgress } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import FaceIcon from '@mui/icons-material/Face';
import PagesIcon from '@mui/icons-material/Pages';


const Profile = () => {

    const [loading, setLoading] = useState(true);
    const [posts, setPosts] = useState([]);

    const [firstName, setFirstName] = useState("John");
    const [lastName, setLastName] = useState("Doe");
    const [editing, setEditing] = useState(false);
    const [uploading, setUploading] = useState(false);

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    const handleProfileEdit = async () => {
        setUploading(true);
        // after 2 seconds, set uploading to false
        setTimeout(() => {
            setUploading(false);
            setEditing(false);
        }, 2000);

        // otherwise, make API call here to update user profile
    }

    useEffect(() => {
        if (userID) {
            createAPIEndpoint(`authors/${userID}/posts`)
                .get()
                .then(res => {
                    setPosts(res.data)
                    setLoading(false)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }, [userID])

    return (
        <>
            <Layout>
                <Grid container spacing={2}>

                    {!editing && (
                        <Grid item xs={12}>
                            <Card>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <Typography variant="h6" align="left">About Me</Typography>
                                    </Grid>

                                    <Grid item xs={12}>
                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                            <div>
                                                <Typography variant="h6" align="left">@{username}</Typography>
                                            </div>
                                        </div>
                                    </Grid>

                                    {/* <Grid item xs={12}>
                                        <Button fullWidth variant="contained" onClick={() => { setEditing(true) }}>Edit Profile</Button>
                                    </Grid> */}
                                </Grid>
                            </Card>
                        </Grid>
                    )}

                    {editing && (
                        <Grid item xs={12}>
                            <Card>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <Typography variant="h6" align="left">Editing Profile Information</Typography>
                                    </Grid>

                                    <Grid item xs={6}>
                                        <TextField
                                            fullWidth
                                            value={firstName}
                                            onChange={(event) => { setFirstName(event.target.value) }}
                                            placeholder="First Name"
                                            style={{ backgroundColor: '#F4F4F4', borderRadius: "40px" }}
                                            variant="outlined"
                                            InputProps={{ style: { color: 'black', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><FaceIcon sx={{ color: "black" }} /></InputAdornment>) }}
                                        >
                                        </TextField>
                                    </Grid>

                                    <Grid item xs={6}>
                                        <TextField
                                            fullWidth
                                            value={lastName}
                                            onChange={(event) => { setLastName(event.target.value) }}
                                            placeholder="Last Name"
                                            style={{ backgroundColor: '#F4F4F4', borderRadius: "40px" }}
                                            variant="outlined"
                                            InputProps={{ style: { color: 'black', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><FaceIcon sx={{ color: "black" }} /></InputAdornment>) }}
                                        >
                                        </TextField>
                                    </Grid>

                                    <Grid item xs={12}>
                                        {/* If uploading === true, display button with CircularProgress spinner inside */}
                                        <Button fullWidth variant="contained" disabled={uploading} onClick={() => { handleProfileEdit() }}>{uploading ? <CircularProgress size={30} /> : "Save Changes"}</Button>
                                    </Grid>
                                </Grid>
                            </Card>
                        </Grid>
                    )}

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    <Grid item xs={12}>
                        <Typography variant="h6" align="left">My Posts</Typography>
                    </Grid>

                    {loading && (
                        <Grid item xs={12}>
                            <Card>
                                <CircularProgress sx={{ margin: "auto" }} />
                            </Card>
                        </Grid>
                    )}

                    {(posts.length === 0 && !loading) && (
                        <Grid item xs={12}>
                            <Card>
                                <PagesIcon sx={{ fontSize: "60px" }} />
                                <Typography variant="h6" component="h2" sx={{ textAlign: "center" }}>No posts to show.</Typography>
                            </Card>
                        </Grid>
                    )}

                    {(posts.length > 0 && !loading) && (
                        <>
                            {posts.map((post, index) => (
                                <Grid item xs={12} key={index}>
                                    <Post 
                                        id={post["_id"]} 
                                        title={post.title}
                                        description={post.description}
                                        source={post.source}
                                        origin={post.origin}
                                        categories={post.categories}
                                        type={post.contentType} 
                                        content={post.content}
                                        authorDisplayName={username} 
                                        authorID={userID}
                                        link={post.id} 

                                        // Hide edit button + extra information
                                        hideEditButton={true}
                                        hideSource={true}
                                        hideOrigin={true}
                                        hideCategories={true} 
                                        hideLikeButton={true}
                                        hideCommentButton={true}
                                        hideShareButton={true}
                                        hideDeleteButton={true}
                                        />
                                </Grid>
                            ))}
                        </>
                        
                    )}



                </Grid>
            </Layout>
        </>
    )
}

export default Profile;