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

    const [friendRequestsLoading, setFriendRequestsLoading] = useState(true)
    const [friendsLoading, setFriendsLoading] = useState(true)

    const [trueFriends, setTrueFriends] = useState([]);
    const [friends, setFriends] = useState([]);
    const [friendRequests, setFriendRequests] = useState([]);

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

                setupFriends(tempFollowers, tempFollowing)
                setFriendsLoading(false)
            }
        }

        getFriends();
    }, [userID])

    // get any friend requests
    useEffect(() => {
        if (userID) {
            createAPIEndpoint(`authors/${userID}/inbox/followers`)
                .get()
                .then(res => {
                    console.log(JSON.stringify(res.data.items))
                    setFriendRequests(res.data.items)
                    setFriendRequestsLoading(false)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }, [userID])

    const setupFriends = (followers, following) => {
        const followersOnly = followers.filter(x => !isIn(following, x._id));
        const followingOnly = following.filter(x => !isIn(followers, x._id));
        const friends = followersOnly.concat(followingOnly);
        const trueFriends = followers.filter(x => isIn(following, x._id));

        setFriends(friends);
        setTrueFriends(trueFriends);
    }

    function isIn(array, id) {
        return array.some(function (el) {
            return el._id === id;
        });
    }

    const acceptFriendRequest = (friendRequest) => {
        var data = {
            "type": "author",
            "id": friendRequest.actor.id,
            "host": friendRequest.actor.host,
            "displayName": friendRequest.actor.displayName,
            "url": friendRequest.actor.url,
            "github": friendRequest.actor.github,
            "profileImage": friendRequest.actor.profileImage
        }

        createAPIEndpoint(`authors/${userID}/followers/${friendRequest.actor._id}`)
                .put(data)
                .then(res => {
                    // reload page
                    createAPIEndpoint(`authors/${userID}/followers/inbox/${friendRequest.actor._id}`)
                    .delete()
                    .then(res => {
                        console.log("Deleting friend request");
                        console.log(res.data);
                    })
                    window.location.reload();
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
    }

    const declineFriendRequest = (friendRequest) => {
        console.log("declining friend request");
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
                                To become true friends with another author, you must both accept each other's friend requests. You can lookup other authors using the Search bar.
                            </Alert>
                        </Grid>

                        <Grid item xs={12}>
                            <Divider />
                        </Grid>

                        {/* show spinner if friendsRequestsLoading is true */}
                        {friendRequestsLoading && (
                            <Grid item xs={12}>
                                <CircularProgress sx={{ marginTop: "50px", marginBottom: "50px" }} />
                            </Grid>
                        )}

                        {/* if friendRequests is length zero, display message */}
                        {!friendRequestsLoading && friendRequests.length === 0 && (
                            <Grid item xs={12}>
                                <Alert severity="info" style={{ textAlign: "left" }}>
                                    No friend requests at this time.
                                </Alert>
                            </Grid>
                        )}

                        {/* if friendRequests is length greater than zero, display list of friend requests */}
                        {!friendRequestsLoading && friendRequests.length > 0 && (
                            friendRequests.map((friendRequest) => (
                                <Grid item xs={12}>
                                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />

                                            <div>
                                                <Typography variant="h6" align="left">@{friendRequest.actor.displayName}</Typography>
                                            </div>
                                        </div>

                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            {/* <Button variant="outlined" startIcon={<CloseIcon />} sx={{ marginRight: "5px" }}>
                                                Reject
                                            </Button> */}
                                            <Button variant="contained" endIcon={<CheckIcon />} onClick={() => {acceptFriendRequest(friendRequest)}}>
                                                Accept
                                            </Button>
                                            <Button variant="contained" endIcon={<CloseIcon />} onClick={() => {declineFriendRequest(friendRequest)}} style={{marginLeft: "0.5em"}}>
                                                Decline
                                            </Button>
                                            
                                        </div>

                                    </div>
                                </Grid>
                            ))
                        )}
                    </Grid>
                </Card>

                <Card>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Typography variant="h6" align="left">All Friends</Typography>
                        </Grid>

                        {/* if loading is true, and followers is null, show loader */}
                        {/* otherwise, show list of followers */}
                        {friendsLoading && (
                            <Grid item xs={12}>
                                <CircularProgress sx={{ marginTop: "50px", marginBottom: "50px" }} />
                            </Grid>
                        )}

                        {/* if trueFriends and friends are both length zero, display message */}
                        {!friendsLoading && trueFriends.length === 0 && friends.length === 0 && (
                            <Grid item xs={12}>
                                <Alert severity="info" style={{ textAlign: "left" }}>
                                    You have no friends yet. To become friends with another author, you must both accept each other's friend requests. You can lookup other authors using the Search bar.
                                </Alert>
                            </Grid>
                        )}

                        {!friendsLoading && (
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