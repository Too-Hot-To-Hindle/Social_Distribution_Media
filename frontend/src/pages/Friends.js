// React helpers
import { useState, useEffect } from "react";
import { createAPIEndpoint, ENDPOINTS } from '../api';

// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Card, Typography, Grid, Button, Alert, IconButton, Divider, Chip, CircularProgress } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CloseIcon from '@mui/icons-material/Close';
import CheckIcon from '@mui/icons-material/Check';

const Friends = () => {

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    const [loading, setLoading] = useState(true)

    const [followers, setFollowers] = useState(null);
    const [following, setFollowing] = useState(null);

    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    // retrieve all followers
    useEffect(() => {
        if (userID) {
            createAPIEndpoint(`authors/${userID}/followers`)
                .get()
                .then(res => {
                    setFollowers(res.data)
                    setLoading(false)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }, [userID])

    // TODO: integrate
    // then, to retrieve all following, get user information, and then course through each ID:
    // useEffect(() => {
    //     if (userID) {
    //         createAPIEndpoint(`authors/${userID}`)
    //             .get()
    //             .then(res => {
    //                 console.log(res.data)
    //                 setFollowing(res.data.following)
    //                 setLoading(false)
    //             })
    //             .catch(err => {
    //                 // TODO: Add in error handling
    //                 console.log(err)
    //             });
    //     }
    // }, [userID])

    return (
        <>
            <Layout>
                <Card>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Typography variant="h6" align="left">Incoming Friend Requests</Typography>
                        </Grid>

                        <Grid item xs={12}>
                            <Alert severity="info" style={{ textAlign: "left" }}>
                                To become true friends with another author, you must both accept each other's friend requests. You can lookup other authors on the Explore page.
                            </Alert>
                        </Grid>

                        <Grid item xs={12}>
                            <Divider/>
                        </Grid>

                        <Grid item xs={12}>
                            <Alert severity="info" style={{ textAlign: "left" }}>
                                No friend requests at this time.
                            </Alert>
                        </Grid>

                        {/* <Grid item xs={12}>
                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                <div style={{ display: "flex", alignItems: "center" }}>
                                    <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />

                                    <div>
                                        <Typography variant="h6" align="left">Jane Doe</Typography>
                                        <Typography variant="body1" align="left">@janedoe</Typography>
                                    </div>
                                </div>

                                <div style={{ display: "flex", alignItems: "center" }}>
                                    <Button variant="outlined" startIcon={<CloseIcon />} sx={{ marginRight: "5px" }}>
                                        Reject
                                    </Button>
                                    <Button variant="contained" endIcon={<CheckIcon />}>
                                        Accept
                                    </Button>
                                </div>

                            </div>
                        </Grid> */}
                    </Grid>
                </Card>

                <Card>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Typography variant="h6" align="left">All Friends</Typography>
                        </Grid>

                        {/* if loading is true, and followers is null, show loader */}
                        {/* otherwise, show list of followers */}
                        {(loading && followers === null) && (
                            <Grid item xs={12}>
                                <CircularProgress sx={{ marginTop: "50px", marginBottom: "50px" }} />
                            </Grid>
                        )}

                        {(!loading && followers !== null) && (
                            <>
                                {followers.map((follower, index) => {
                                    return (
                                        <>
                                            <Grid item xs={12}>
                                                <div style={{ display: "flex", justifyContent: "space-between" }}>
                                                    <div style={{ display: "flex", alignItems: "center" }}>
                                                        <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                                        <div>
                                                            <Typography variant="h6" align="left">@{follower.displayName}</Typography>
                                                        </div>
                                                    </div>

                                                    <div style={{ display: "flex", alignItems: "center" }}>
                                                        {/* <Chip label="True Friend" sx={{marginRight: "10px"}}/> */}
                                                        <IconButton>
                                                            <CloseIcon />
                                                        </IconButton>
                                                    </div>
                                                </div>
                                            </Grid>

                                            <Grid item xs={12}>
                                                <Divider />
                                            </Grid>
                                        </>
                                    )
                                })}
                            </>
                        )}


                    </Grid>
                </Card>
            </Layout>
        </>
    )
}

export default Friends;