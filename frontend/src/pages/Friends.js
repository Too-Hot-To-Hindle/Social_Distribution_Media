// React helpers
import { useState, useEffect } from "react";
import { createAPIEndpoint } from '../api';
import { toast } from 'sonner';

// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Card, Typography, Grid, Button, Alert, Divider, Chip, CircularProgress } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CloseIcon from '@mui/icons-material/Close';
import CheckIcon from '@mui/icons-material/Check';
import {IconButton} from "@mui/material";

const Friends = () => {

    const [userID, setUserID] = useState(null);

    const [friendRequestsLoading, setFriendRequestsLoading] = useState(true)
    const [friendsLoading, setFriendsLoading] = useState(true)

    const [trueFriends, setTrueFriends] = useState([]);
    const [friends, setFriends] = useState([]);
    const [friendRequests, setFriendRequests] = useState([]);

    useEffect(() => {
        setUserID(localStorage.getItem('author_id'))
    }, [])

    useEffect(() => {
        const setupFriends = (followers, following) => {
            const followersOnly = followers.filter(x => !isIn(following, x._id));
            const followingOnly = following.filter(x => !isIn(followers, x._id));
            const friends = followersOnly.concat(followingOnly);
            const trueFriends = followers.filter(x => isIn(following, x._id));
    
            setFriends(friends);
            setTrueFriends(trueFriends);
        }

        const getFriends = async () => {
            if (userID) {

                // reset trueFriends and friends - for debugging purposes
                setTrueFriends([]);
                setFriends([]);

                var authorDetails;
                try {
                    authorDetails = await createAPIEndpoint(`authors/${userID}`).get()
                }
                catch (err) {
                    toast.error('An error has occurred.', {
                        description: 'Could not retrieve your follower details. Please try again later.',
                    });
                }

                const followerIDs = authorDetails.data.followers;
                const followingIDs = authorDetails.data.following;

                var res;

                // get all followers
                var tempFollowers = [];
                for (const followerID of followerIDs) {
                    try {
                        res = await createAPIEndpoint(`authors/${followerID}`).get()
                    }
                    catch (err) {
                        toast.error('An error has occurred.', {
                            description: 'Could not retrieve your follower details. Please try again later.',
                        });
                    }
                    tempFollowers.push(res.data)
                }

                // get all following
                var tempFollowing = [];
                for (const followingID of followingIDs) {
                    try {
                        res = await createAPIEndpoint(`authors/${followingID}`).get()
                    }
                    catch (err) {
                        toast.error('An error has occurred.', {
                            description: 'Could not retrieve your follower details. Please try again later.',
                        });
                    }
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
                    setFriendRequests(res.data.items)
                    setFriendRequestsLoading(false)
                })
                .catch(err => {
                    toast.error('An error has occurred.', {
                        description: 'Could not retrieve your friend requests. Please try again later.',
                    });
                });
        }
    }, [userID])

    

    function isIn(array, id) {
        return array.some(function (el) {
            return el._id === id;
        });
    }

    const acceptFriendRequest = async (friendRequest) => {
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
                window.location.reload();
            })
            .catch(err => {
                toast.error('An error has occurred.', {
                    description: 'Could not accept the friend request. Please try again later.',
                });
            });

        createAPIEndpoint(`authors/${userID}/inbox/followers/${friendRequest.actor._id}`)
            .delete()
            .then(res => {
                window.location.reload();
            })
            .catch(err => {
                toast.error('An error has occurred.', {
                    description: 'Could not accept the friend request. Please try again later.',
                });
            })
    }



    const declineFriendRequest = (friendRequest) => {
        createAPIEndpoint(`authors/${userID}/inbox/followers/${friendRequest.actor._id}`)
            .delete()
            .then(res => {
                window.location.reload();
            })
            .catch(err => {
                toast.error('An error has occurred.', {
                    description: 'Could not decline the friend request. Please try again later.',
                });
            })
    }

    const removeFriend = (friend) => {
        createAPIEndpoint(`authors/${userID}/followers/${friend._id}`)
            .delete()
            .then(res => {
                //console.log(res.data);
                window.location.reload();
            })
        .catch(err => {
            toast.error('An error has occurred.', {
                description: 'Could not remove this friend. Please try again later.',
            });
        })

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
                                            <Button variant="contained" endIcon={<CheckIcon />} onClick={() => { acceptFriendRequest(friendRequest) }}>
                                                Accept
                                            </Button>
                                            <Button variant="contained" endIcon={<CloseIcon />} onClick={() => { declineFriendRequest(friendRequest) }} style={{ marginLeft: "0.5em" }}>
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
                                                        <span>
                                                            <Typography variant="h6" align="left">@{follower.displayName}</Typography>
                                                        </span>
                                                        <span style={{paddingLeft: "10px"}}>
                                                            <Chip label="True Friend" />
                                                        
                                                        </span>
                                                    </div>
                                                   

                                                    <div style={{ display: "flex", alignItems: "center" }}>
                                                        
                                                        
                                                        <Button variant="contained" endIcon={<CloseIcon />} onClick={() => { removeFriend(follower) }}>
                                                        Remove Friend
                                                        </Button>
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
                                                    <Button variant="contained" endIcon={<CloseIcon />} onClick={() => { removeFriend(follower) }}>
                                                        Remove Friend
                                                     </Button>
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
