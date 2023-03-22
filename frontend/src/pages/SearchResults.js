// React helpers
import { useState, useEffect } from "react";
import { createAPIEndpoint, ENDPOINTS } from '../api';
import { useNavigate, useParams } from 'react-router-dom';

// Layout component
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";

// Material UI components
import { Card, Typography, Grid, IconButton, Chip, Divider, Button, CircularProgress } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CloseIcon from '@mui/icons-material/Close';
import PagesIcon from '@mui/icons-material/Pages';

const SearchResults = () => {

    const { query } = useParams()

    const navigate = useNavigate();


    const [localAuthors, setLocalAuthors] = useState(null);
    const [remoteAuthors, setRemoteAuthors] = useState(null);

    const [myProfile, setMyProfile] = useState(null);
    const [following, setFollowing] = useState([]);
    const [sentFriendRequests, setSentFriendRequests] = useState([]);

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    useEffect(() => {
        if (userID) {
            createAPIEndpoint(`authors/${userID}`)
                .get()
                .then(res => {
                    setMyProfile(res.data)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }, [userID])

    useEffect(() => {

        setLocalAuthors(null)
        setRemoteAuthors(null)
        if (userID) {
            // TODO: make pagination better

            createAPIEndpoint(`authors?page=1&size=500`)
                .get()
                .then(res => {
                    setLocalAuthors(res.data.items
                        .filter(author => author["_id"] !== localStorage.getItem('author_id'))
                        .filter(author => author["displayName"].toLowerCase().includes(query.toLowerCase())))
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });

            // our own team's remote URL
            const testRemoteTeamURL = encodeURIComponent("https://social-distribution-media.herokuapp.com/")
            createAPIEndpoint(`remote/authors/${testRemoteTeamURL}`)
                .get()
                .then(res => {
                    setRemoteAuthors(res.data.items
                        .filter(author => author["displayName"].toLowerCase().includes(query.toLowerCase())))
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });

        }

    }, [query, userID])

    function handleFollowRequests(authorToFollow) {
        // add authorToFollow._id to sentFriendRequests
        setSentFriendRequests([...sentFriendRequests, authorToFollow._id])

        var data = {
            "type": "follow",
            "summary": username + " has requested to follow you.",

            "actor": {
                "type": "author",
                "id": myProfile["id"],
                "host": myProfile["host"],
                "displayName": myProfile["displayName"],
                "url": myProfile["url"],
                "github": myProfile["github"],
                "profileImage": myProfile["profileImage"]
            },
            "object": {
                "type": "author",
                "id": authorToFollow["id"],
                "host": authorToFollow["host"],
                "displayName": authorToFollow["displayName"],
                "url": authorToFollow["url"],
                "github": authorToFollow["github"],
                "profileImage": authorToFollow["profileImage"]
            }
        }

        createAPIEndpoint(`authors/${authorToFollow._id}/inbox`)
            .post(data)
            .then(res => {
                console.log(res)
            })
            .catch(err => {
                console.log(err)
            })
    }

    return (
        <>
            <Layout>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <Typography variant="h4" align="left" fontWeight="500">Search Results</Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Card>

                            {(localAuthors === null) &&
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <CircularProgress />
                                    </Grid>
                                </Grid>
                            }

                            {(localAuthors !== null && localAuthors.length === 0) &&
                                <>
                                    <PagesIcon sx={{ fontSize: "60px" }} />
                                    <Typography variant="h6" component="h2" sx={{ textAlign: "center" }}>No local results.</Typography>
                                </>
                            }

                            {(localAuthors !== null && localAuthors.length > 0) &&
                                <>
                                    <Grid container spacing={2}>

                                        <Grid item xs={12}>
                                            <Typography variant="h6" align="left">Local Authors</Typography>
                                        </Grid>

                                        <Grid item xs={12}>
                                            {localAuthors.map((author, index) => {
                                                return (
                                                    <Grid container key={index} spacing={2}>
                                                        <Grid item xs={12}>
                                                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                                                <div style={{ display: "flex", alignItems: "center" }}>
                                                                    <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                                                    <div>
                                                                        <Typography variant="h6" align="left">@{author.displayName}</Typography>
                                                                    </div>
                                                                </div>

                                                                <Button variant="contained" onClick={() => {navigate(`/profile/${author["_id"]}`)}}>View</Button>


                                                                {/* if userID is not in author.followers, show Send Friend Request button */}
                                                                {!author.followers.includes(userID) &&

                                                                    <div style={{ display: "flex", alignItems: "center" }}>
                                                                        {/* if author._id is in sentFriendRequests, show Sent button */}
                                                                        {sentFriendRequests.includes(author._id) &&
                                                                            <Button variant="contained" disabled>Sent</Button>
                                                                        }

                                                                        {/* if author._id is not in sentFriendRequests, show Send Friend Request button */}
                                                                        {!sentFriendRequests.includes(author._id) &&
                                                                            <Button variant="contained" onClick={() => handleFollowRequests(author)}>Send Friend Request</Button>
                                                                        }

                                                                    </div>
                                                                }
                                                            </div>
                                                        </Grid>

                                                        <Grid item xs={12}>
                                                            <Divider />
                                                        </Grid>


                                                    </Grid>
                                                )
                                            })}
                                        </Grid>
                                    </Grid>
                                </>
                            }
                        </Card>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    <Grid item xs={12}>
                        <Card>

                            {(remoteAuthors === null) &&
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <CircularProgress />
                                    </Grid>
                                </Grid>
                            }

                            {(remoteAuthors !== null && remoteAuthors.length === 0) &&
                                <>
                                    <PagesIcon sx={{ fontSize: "60px" }} />
                                    <Typography variant="h6" component="h2" sx={{ textAlign: "center" }}>No remote-self results.</Typography>
                                </>
                            }

                            {(remoteAuthors !== null && remoteAuthors.length > 0) &&
                                <>
                                    <Grid container spacing={2}>

                                        <Grid item xs={12}>
                                            <Typography variant="h6" align="left">Remote-self Authors</Typography>
                                        </Grid>

                                        <Grid item xs={12}>
                                            {remoteAuthors.map((author, index) => {
                                                return (
                                                    <Grid container key={index} spacing={2}>
                                                        <Grid item xs={12}>
                                                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                                                <div style={{ display: "flex", alignItems: "center" }}>
                                                                    <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                                                    <div>
                                                                        <Typography variant="h6" align="left">@{author.displayName}</Typography>
                                                                    </div>
                                                                </div>

                                                                <Button variant="contained" onClick={() => {navigate(`/profile/${encodeURIComponent(author.id)}`)}}>View</Button>

                                                                {/* Need to redo friend request logic for remote authors */}
                                                            </div>
                                                        </Grid>

                                                        <Grid item xs={12}>
                                                            <Divider />
                                                        </Grid>


                                                    </Grid>
                                                )
                                            })}
                                        </Grid>
                                    </Grid>
                                </>
                            }
                        </Card>
                    </Grid>

                    {/* <Grid item xs={12}>
                        <Typography variant="h6" align="left">Posts</Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Grid container>
                            <Grid item xs={12}>
                                <Post hideEditButton={true} hideDeleteButton={true}/>
                            </Grid>
                        </Grid>
                    </Grid> */}
                </Grid>
            </Layout>

        </>
    )
}

export default SearchResults;