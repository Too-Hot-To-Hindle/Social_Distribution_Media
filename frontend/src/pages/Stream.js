// React helpers
import { useState, useEffect } from "react";
import { createAPIEndpoint, ENDPOINTS } from '../api';

// Custom components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";
import SharedPost from "../components/SharedPost";

// Material UI components
import { Card, Typography, CircularProgress, Grid, Alert } from '@mui/material';

// Material UI icons
import PagesIcon from '@mui/icons-material/Pages';

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

const Stream = () => {
    const [loading, setLoading] = useState(true)
    const [posts, setPosts] = useState([]);

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    // const [postAuthorIDs, setPostAuthorIDs] = useState([]);

    // const[authorsLoaded, setAuthorsLoaded] = useState(false);

    const [inboxItems, setInboxItems] = useState(null);



    /*
    useEffect(() => {
        setTimeout(() => {
            setLoading(false)
        }, 2000)
    }, [])*/

    // useEffect to get the username and user ID from local storage
    useEffect(() => {
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    // useEffect to get the inbox items
    useEffect(() => {
        const getInboxItems = async () => {
            if (userID) {
                const response = await createAPIEndpoint(`authors/${userID}/inbox`).get()
                console.log(response.data.items)
                setInboxItems(response.data.items);
                setLoading(false);
            }
        }

        getInboxItems();
    }, [userID])


    // useEffect(() => {
    //     const getAuthors = async () => {
    //         if (userID) {

    //             await createAPIEndpoint(`authors/${userID}`).get()
    //                 .then(res => {
    //                     setPostAuthorIDs(res.data.following);
    //                     if (res.data.following.length > 0) {
    //                         console.log("length greater than 0")

    //                     } else {
    //                         //TO DO
    //                         console.log("no posts");
    //                     }
    //                 })
    //                 .catch(err => {
    //                     console.log(err)
    //                 });
    //             setAuthorsLoaded(true);

    //         }

    //     }
    //     getAuthors();
    // }, [userID]);


    // useEffect(() => {
    //     let allPosts = [];
    //     const getPosts = async () => {
    //         if (authorsLoaded){
    //             for (const postAuthor of postAuthorIDs){
    //                 await createAPIEndpoint(`authors/${postAuthor}/posts`)
    //                 .get()
    //                 .then(res => {
    //                     for (const index in res.data.items){
    //                         allPosts.push(res.data.items[index]);
    //                     }
    //                 })
    //                 .catch(err => {
    //                     console.log(err)
    //                 });
    //             }
    //             setPosts(allPosts);
    //             setLoading(false);

    //         }
    //     }
    //     getPosts();
    // },[postAuthorIDs])


    return (
        <>
            <Layout>
                <Alert severity="info" sx={{marginBottom: "20px"}}>
                    <Typography align="left">At this time, your Stream displays only inbox Post items. To view Likes and Comments on your posts, please head to your Profile page, or to view pending friend requests, head to the friends page.</Typography>
                </Alert>

                {loading && (
                    <Card>
                        <CircularProgress sx={{ margin: "auto" }} />
                    </Card>
                )}

                {(!loading && inboxItems.length === 0) && (
                    <Card>
                        <PagesIcon sx={{ fontSize: "60px" }} />
                        <Typography variant="h6" component="h2" sx={{ textAlign: "center" }}>Nothing's in your inbox!</Typography>
                    </Card>
                )}

                {(!loading && inboxItems.length > 0) && (
                    <Grid container spacing={2}>
                        {inboxItems.map((item, index) => (
                            <Grid item xs={12} key={index}>
                                {item.type === "post" && (
                                    <Post
                                        id={getPostIDFromURL(item["id"])}
                                        title={item.title}
                                        description={item.description}
                                        source={item.source}
                                        origin={item.origin}
                                        categories={item.categories}
                                        type={item.contentType}
                                        content={item.content}
                                        authorDisplayName={item.author.displayName}
                                        authorID={item.author.id}
                                        link={item.id}

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
                                )}
                            </Grid>
                        ))}
                    </Grid>
                )}

                {/* {(posts.length === 0 && !loading) && (
                    <Card>
                        <PagesIcon sx={{ fontSize: "60px" }} />
                        <Typography variant="h6" component="h2" sx={{ textAlign: "center" }}>No posts to show.</Typography>
                    </Card>
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
                    
                )} */}


            </Layout>
        </>
    )
}

export default Stream;