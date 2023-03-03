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

    const [followers, setFollowers] = useState([]);
    const [following, setFollowing] = useState([]);
    const [trueFriends, setTrueFriends] = useState([]);
    const [friends, setFriends] = useState([]);

    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    useEffect(() => {

        const getFriends = async () => {
            if (userID) {

                // reset trueFriends and friends - for debugging purposes
                setTrueFriends([]);
                setFriends([]);

                const authorDetails = await createAPIEndpoint(`authors/${userID}`).get()
                const followerIDs = authorDetails.data.followers;
                const followingIDs = authorDetails.data.following;

                // get all followers
                var tempFollowers = [];
                for (const followerID of followerIDs) {
                    const res = await createAPIEndpoint(`authors/${followerID}`).get()
                    tempFollowers.push(res.data)
                }

                // get all following
                var tempFollowing = [];
                for (const followingID of followingIDs) {
                    const res = await createAPIEndpoint(`authors/${followingID}`).get()
                    tempFollowing.push(res.data)
                }

                findTrueFriends(tempFollowers, tempFollowing);
                findRegularFriends(tempFollowers, tempFollowing);
                setLoading(false)
            }
        }

        getFriends();
    }, [userID])

    const findTrueFriends = (followers, following) => {
        // for every follower in followers, check if they are also in following
        // and if so, add them to trueFriends
        for (let i = 0; i < followers.length; i++) {
            for (let j = 0; j < following.length; j++) {
                if (followers[i].id === following[j].id) {
                    setTrueFriends(prevState => [...prevState, followers[i]])
                }
            }
        }

        console.log(trueFriends)
    }

    const findRegularFriends = (followers, following) => {
        // for every follower in followers, check if they are not in following
        // and if so, add them to friends
        for (let i = 0; i < followers.length; i++) {
            for (let j = 0; j < following.length; j++) {
                if (followers[i].id !== following[j].id) {
                    setFriends(prevState => [...prevState, followers[i]])
                }
            }
        }
    }

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
                            <Divider />
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
                        {loading && (
                            <Grid item xs={12}>
                                <CircularProgress sx={{ marginTop: "50px", marginBottom: "50px" }} />
                            </Grid>
                        )}

                        {!loading && (
                            <>
                                {trueFriends.map((follower, index) => {
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
                                                        <Chip label="True Friend" sx={{ marginRight: "10px" }} />
                                                        {/* <IconButton>
                                                            <CloseIcon />
                                                        </IconButton> */}
                                                    </div>
                                                </div>
                                            </Grid>

                                            <Grid item xs={12}>
                                                <Divider />
                                            </Grid>
                                        </>
                                    )
                                })}

                                {friends.map((follower, index) => {
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
                                                        {/* <IconButton>
                                                            <CloseIcon />
                                                        </IconButton> */}
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