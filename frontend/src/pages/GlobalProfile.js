// React helpers
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { createAPIEndpoint } from '../api';

// Layout components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";

// Material UI elements
import { Grid, Card, Typography, CircularProgress, Chip, Divider, Dialog, DialogContent, DialogTitle } from "@mui/material";

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
    if (url.includes("posts")) {
        const urlSplit = url.split("/")
        return urlSplit[urlSplit.length - 1]
    }
}

const GlobalProfile = () => {

    const navigate = useNavigate();

    const { authorURL } = useParams()
    // decode authorURL from URL encoded
    const authorURLDecoded = decodeURIComponent(authorURL)

    const [loading, setLoading] = useState(true);

    const [showFollowers, setShowFollowers] = useState(false);
    const [followersLoading, setFollowersLoading] = useState(true);

    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState(null);

    const [authorDetails, setAuthorDetails] = useState(null);
    const [authorPosts, setAuthorPosts] = useState(null);
    const [authorServer, setAuthorServer] = useState(null);
    const [authorFollowerDetails, setAuthorFollowerDetails] = useState(null);

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
                            setAuthorPosts(res.data)
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

        // otherwise, show error message
        else {
            setError(true)
            setErrorMessage("User not found.")
            setLoading(false)
        }
    }, [])

    async function loadFollowers() {
        setShowFollowers(true)

        if (authorURLDecoded.startsWith("https://social-distribution-media.herokuapp.com")) {
            // TODO: get local author followers
            var allLocalFollowers = []
            for (let follower of authorDetails.followers) {
                const response = await createAPIEndpoint(`authors/${follower}`).get()
                allLocalFollowers.push(response.data.items)
            }

            setAuthorFollowerDetails(allLocalFollowers)
            setFollowersLoading(false)
        }

        else if (!authorURLDecoded.startsWith("https://social-distribution-media.herokuapp.com")) {
            // TODO: get remote author followers
        }
    }

    return (
        <>
            <Layout>
                {/* <Dialog open={showFollowers} style={{ padding: "20px" }}>
                    <DialogTitle>Followers</DialogTitle>

                    <DialogContent>
                        <Grid container spacing={2}>
                            {followersLoading &&
                                <Grid item xs={12}>
                                    <CircularProgress sx={{ margin: "20px" }} />
                                </Grid>
                            }

                            {!followersLoading &&
                                <>
                                    {authorFollowerDetails.map((follower, index) => (
                                        <Grid item xs={12}>
                                            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                                                <Typography sx={{marginRight: "100px"}}>{follower.displayName}</Typography>

                                                <Chip label="View" clickable onClick={() => {navigate(`/profile/${encodeURIComponent(follower.url)}`, {replace: true}); window.location.reload();}}/>
                                            </div>
                                        </Grid>
                                    ))}
                                </>
                            }
                        </Grid>
                    </DialogContent>
                </Dialog> */}

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

                            {/* <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="h6" align="left">Followers</Typography>
                            </Grid> */}

                            {/* <Grid item xs={12}>
                                <Card>
                                    {authorDetails.followers.length === 0 &&
                                        <Typography variant="body1" align="left">No followers.</Typography>
                                    }

                                    {authorDetails.followers.length > 0 &&
                                        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                                            <Typography variant="h6" align="left">{authorDetails.followers.length}</Typography>

                                            <Chip label="View All" clickable onClick={() => { loadFollowers() }} />
                                        </div>
                                    }
                                </Card>
                            </Grid> */}

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