// React helpers
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { createAPIEndpoint } from '../api';

// Layout components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";

// Material UI elements
import { Grid, Card, Typography, CircularProgress, Chip, Divider, Dialog, DialogContent, DialogTitle, DialogActions, Button } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import FaceIcon from '@mui/icons-material/Face';
import PagesIcon from '@mui/icons-material/Pages';
import ErrorIcon from '@mui/icons-material/Error';

// Helper functions
// getPostIDFromURL
// takes in a URL, say of example https://social-distribution-media.herokuapp.com/author/abc123/posts/def456
// and returns the post ID, here, def456
const getPostIDFromURL = (url) => {
    // make sure "posts" is in url
    // if last character in string is a '/', remove it first
    if (url[url.length - 1] === "/") {
        url = url.slice(0, -1)
    }

    if (url.includes("posts")) {
        const urlSplit = url.split("/")
        console.log(urlSplit[urlSplit.length - 1])
        return urlSplit[urlSplit.length - 1]
    }
}

// checkIfFollower
// looks at authorFollowerDetails to see if object with authorID === ownUserID exists
// if authorFollowerDetails is null, returns true -- so that we don't render the follow button
const checkIfFollower = (authorFollowerDetails, ownUserID) => {
    if (authorFollowerDetails) {
        for (let i = 0; i < authorFollowerDetails.length; i++) {
            if (authorFollowerDetails[i].id.includes(ownUserID)) {
                return true
            }
        }
        return false
    }
    else {
        return true
    }
}

const GlobalProfile = () => {

    const navigate = useNavigate();

    const { authorURL } = useParams()
    // decode authorURL from URL encoded
    const authorURLDecoded = decodeURIComponent(authorURL)

    const [loading, setLoading] = useState(true);

    const [ownUsername, setOwnUsername] = useState(null);
    const [ownUserID, setOwnUserID] = useState(null);
    const [ownAuthorDetails, setOwnAuthorDetails] = useState(null);


    const [showFollowers, setShowFollowers] = useState(false);
    const [followersLoading, setFollowersLoading] = useState(true);

    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState(null);

    const [authorDetails, setAuthorDetails] = useState(null);
    const [authorPosts, setAuthorPosts] = useState(null);
    const [authorServer, setAuthorServer] = useState(null);
    const [authorFollowerDetails, setAuthorFollowerDetails] = useState(null);

    const [sentFollowRequest, setSentFollowRequest] = useState(false);
    const [sendingFollowRequest, setSendingFollowRequest] = useState(false);

    // useEffect to get own username and user ID from localStorage
    useEffect(() => {
        setOwnUsername(localStorage.getItem('username'))
        setOwnUserID(localStorage.getItem('author_id'))
    }, [])

    // useEffect to get own author details once ownUserID is set
    useEffect(() => {
        if (ownUserID) {
            createAPIEndpoint(`authors/${ownUserID}`)
                .get()
                .then(res => {
                    setOwnAuthorDetails(res.data)
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });
        }
    }, [ownUserID])

    // useEffect to retrieve author details and author posts for author we're viewing on current page
    // may be redundant for own author details, can revisit later
    useEffect(() => {

        // first, set loading to true
        setLoading(true)

        // if authorURLDecoded is undefinfed, show error message
        if (authorURLDecoded === undefined) {
            setError(true)
            setErrorMessage("User not found.")
            setLoading(false)
        }

        // otherwise, if authorURL decoded doesn't start with http, use createAPIEndpoint to get author details + recent posts locally
        else if (!authorURLDecoded.startsWith("http")) {
            createAPIEndpoint(`authors/${authorURLDecoded}`)
                .get()
                .then(res => {
                    setAuthorDetails(res.data)
                    setAuthorServer("Local")

                    createAPIEndpoint(`authors/${authorURLDecoded}/posts`)
                        .get()
                        .then(res => {
                            setAuthorPosts(res.data.items)
                            setLoading(false)
                        })
                        .catch(err => {
                            // TODO: Add in error handling
                            console.log(err)
                            setError(true)
                            setErrorMessage("An unexpected error occurred loading profile content.")
                            setLoading(false)
                        });
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                    setError(true)
                    setErrorMessage("An unexpected error occurred loading profile content.")
                    setLoading(false)
                });
        }

        // otherwise, if authorURLDecoded starts with https://social-distribution-media.herokuapp.com, use createAPIEndpoint to get author details + recent posts
        else if (authorURLDecoded.startsWith("https://social-distribution-media.herokuapp.com")) {
            createAPIEndpoint(`authors/${authorURLDecoded}`)
                .get()
                .then(res => {
                    setAuthorDetails(res.data)
                    setAuthorServer("Remote Clone")

                    createAPIEndpoint(`authors/${authorURLDecoded}/posts`)
                        .get()
                        .then(res => {
                            setAuthorPosts(res.data.items)
                            setLoading(false)
                        })
                        .catch(err => {
                            // TODO: Add in error handling
                            console.log(err)
                            setError(true)
                            setErrorMessage("An unexpected error occurred loading profile content.")
                            setLoading(false)
                        });
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                    setError(true)
                    setErrorMessage("An unexpected error occurred loading profile content.")
                    setLoading(false)
                });

        }

        // otherwise, if authorURLDecoded does not start with https://social-distribution-media.herokuapp.com, make request some other way
        else if (!authorURLDecoded.startsWith("https://social-distribution-media.herokuapp.com")) {
            createAPIEndpoint(`authors/${encodeURIComponent(authorURL)}`)
                .get()
                .then(res => {
                    setAuthorDetails(res.data)
                    setAuthorServer("Remote")

                    createAPIEndpoint(`authors/${encodeURIComponent(authorURL)}/posts`)
                        .get()
                        .then(res => {
                            setAuthorPosts(res.data.items)
                            setLoading(false)
                        })
                        .catch(err => {
                            // TODO: Add in error handling
                            console.log(err)
                            setError(true)
                            setErrorMessage("An unexpected error occurred loading profile content.")
                            setLoading(false)
                        });
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                    setError(true)
                    setErrorMessage("An unexpected error occurred loading profile content.")
                    setLoading(false)
                });
        }

        // otherwise, show error message
        else {
            setError(true)
            setErrorMessage("User not found.")
            setLoading(false)
        }
    }, [])

    // useEffect to retreive followers for author we're viewing on current page
    useEffect(() => {
        if (authorDetails) {
            createAPIEndpoint(`authors/${encodeURIComponent(authorDetails.id)}/followers`)
                .get()
                .then(res => {
                    setAuthorFollowerDetails(res.data.items)
                })
                .catch(err => {
                    console.log(err)
                })
        }
    }, [authorDetails])



    async function sendFollowRequest() {
        setSendingFollowRequest(true);

        const data = {
            type: "follow",
            summary: `${ownUsername} wants to follow ${authorDetails.displayName}.`,
            actor: {
                id: ownAuthorDetails.id,
                type: "author",
                host: ownAuthorDetails.host,
                displayName: ownAuthorDetails.displayName,
                url: ownAuthorDetails.url,
                github: ownAuthorDetails.github,
                profileImage: ownAuthorDetails.profileImage
            },
            object: {
                id: authorDetails.id,
                type: "author",
                host: authorDetails.host,
                displayName: authorDetails.displayName,
                url: authorDetails.url,
                github: authorDetails.github,
                profileImage: authorDetails.profileImage
            }
        }

        console.log(data)

        createAPIEndpoint(`authors/${encodeURIComponent(authorDetails.id)}/inbox`)
            .post(data)
            .then(res => {
                setSendingFollowRequest(false);
                setSentFollowRequest(true);
                console.log(res)
            })
            .catch(err => {
                console.log(err)
            })
    }

    return (
        <>
            <Layout>
                <Dialog open={showFollowers} style={{ padding: "20px" }} maxWidth="xl">
                    <DialogTitle>Followers</DialogTitle>

                    {authorFollowerDetails !== null &&
                        <DialogContent>
                            {authorFollowerDetails.map((follower, index) => {
                                return (
                                    <Grid container key={index} spacing={2}>
                                        <Grid item xs={12}>
                                            <div style={{ display: "flex", justifyContent: "space-between", width: "400px" }}>
                                                <div style={{ display: "flex", alignItems: "center" }}>
                                                    <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                                    <div>
                                                        <Typography variant="h6" align="left">@{follower.displayName}</Typography>
                                                    </div>
                                                </div>

                                                <Button variant="contained" onClick={() => { window.location.href = `/profile/${encodeURIComponent(follower.id)}` }}>View</Button>

                                            </div>
                                        </Grid>

                                        <Grid item xs={12}>
                                            <Divider />
                                        </Grid>
                                    </Grid>
                                )
                            })}
                        </DialogContent>
                    }

                    <DialogActions>
                        <Button variant="contained"  sx={{margin: "5px"}} fullWidth onClick={() => { setShowFollowers(false) }}>Close</Button>
                    </DialogActions>
                </Dialog>

                <Grid container spacing={2}>
                    {loading &&
                        <Grid item xs={12}>
                            <Card>
                                <CircularProgress />
                            </Card>
                        </Grid>
                    }

                    {!loading && error &&
                        <Grid item xs={12}>
                            <Card>
                                <ErrorIcon sx={{ fontSize: "60px" }} />
                                <Typography variant="h6" component="h2" sx={{ textAlign: "center" }}>{errorMessage}</Typography>
                            </Card>
                        </Grid>
                    }

                    {!loading && !error &&
                        <>
                            <Grid item xs={12}>
                                <Card>
                                    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                            <Typography variant="h6" align="left">@{authorDetails.displayName}</Typography>
                                        </div>

                                        <Chip label={authorServer} />
                                    </div>
                                </Card>
                            </Grid>

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="h6" align="left">Followers</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                {authorFollowerDetails === null &&
                                    <Card>
                                        <CircularProgress />
                                    </Card>
                                }

                                {authorFollowerDetails !== null &&
                                    <Card>
                                        {authorFollowerDetails.length === 0 &&
                                            <Typography variant="body1" align="left">No followers.</Typography>
                                        }

                                        {authorFollowerDetails.length > 0 &&
                                            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                                                <Typography variant="h6" align="left">{authorFollowerDetails.length}</Typography>

                                                <Chip label="View All" clickable onClick={() => { setShowFollowers(true) }} />
                                            </div>
                                        }
                                    </Card>
                                }
                            </Grid>

                            {ownUsername !== null && ownUsername !== authorDetails.displayName && (checkIfFollower(authorFollowerDetails, ownUserID) === false) &&
                                <>
                                    <Grid item xs={12}>
                                        <Divider />
                                    </Grid>

                                    <Grid item xs={12}>
                                        {sendingFollowRequest &&
                                            <Button fullWidth variant="contained" disabled>
                                                <CircularProgress size="30px" />
                                            </Button>
                                        }

                                        {!sendingFollowRequest && !sentFollowRequest &&
                                            <Button fullWidth variant="contained" onClick={() => { sendFollowRequest() }}>Send Follow Request</Button>
                                        }

                                        {!sendingFollowRequest && sentFollowRequest &&
                                            <Button fullWidth variant="contained" disabled>Follow Request Sent</Button>
                                        }
                                    </Grid>
                                </>
                            }

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="h6" align="left">Posts</Typography>
                            </Grid>

                            {authorPosts.length === 0 &&
                                <Grid item xs={12}>
                                    <Card>
                                        <Typography variant="body1" align="left">No posts to show.</Typography>
                                    </Card>
                                </Grid>
                            }

                            {authorPosts.map((post, index) => (
                                <Grid item xs={12} key={index}>
                                    <Post
                                        id={getPostIDFromURL(post["id"])}
                                        title={post.title}
                                        description={post.description}
                                        source={post.source}
                                        origin={post.origin}
                                        categories={post.categories}
                                        type={post.contentType}
                                        content={post.content}
                                        authorDisplayName={authorDetails.displayName}
                                        authorID={authorDetails.id}
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
                                        hideLink={true}
                                    />
                                </Grid>
                            ))}
                        </>
                    }

                </Grid>
            </Layout>
        </>
    )
}

export default GlobalProfile;