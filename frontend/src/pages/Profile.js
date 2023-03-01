// React helpers
import { useState } from "react";

// Layout components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";

// Material UI components
import { Card, Typography, Grid, Button, Divider, TextField, InputAdornment, CircularProgress } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import FaceIcon from '@mui/icons-material/Face';

const Profile = () => {

    const [firstName, setFirstName] = useState("John");
    const [lastName, setLastName] = useState("Doe");
    const [editing, setEditing] = useState(false);
    const [uploading, setUploading] = useState(false);

    const handleProfileEdit = async () => {
        setUploading(true);
        // after 2 seconds, set uploading to false
        setTimeout(() => {
            setUploading(false);
            setEditing(false);
        }, 2000);

        // otherwise, make API call here to update user profile
    }

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
                                                <Typography variant="h6" align="left">{firstName} {lastName}</Typography>
                                                <Typography variant="body1" align="left">@johndoe</Typography>
                                            </div>
                                        </div>
                                    </Grid>

                                    <Grid item xs={12}>
                                        <Button fullWidth variant="contained" onClick={() => {setEditing(true)}}>Edit Profile</Button>
                                    </Grid>
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

                    <Grid item xs={12}>
                        <Grid container>
                            <Grid item xs={12}>
                                <Post hideEditButton={true} hideDeleteButton={true} />
                            </Grid>
                        </Grid>
                    </Grid>

                </Grid>
            </Layout>
        </>
    )
}

export default Profile;