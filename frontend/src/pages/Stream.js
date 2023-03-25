// React helpers
import { useState, useEffect } from "react";
import { createAPIEndpoint, ENDPOINTS } from '../api';

// Custom components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";
import SharedPost from "../components/SharedPost";

// Material UI components
import { Card, Typography, CircularProgress, Grid } from '@mui/material';

// Material UI icons
import PagesIcon from '@mui/icons-material/Pages';

const Stream = () => {
    const [loading, setLoading] = useState(true)
    const [posts, setPosts] = useState([]);

    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(null);

    const [postAuthorIDs, setPostAuthorIDs] = useState([]);

    /*
    useEffect(() => {
        setTimeout(() => {
            setLoading(false)
        }, 2000)
    }, [])*/

    useEffect(() => {   //is this needed?
        setUsername(localStorage.getItem('username'))
        setUserID(localStorage.getItem('author_id'))
    }, [])

    useEffect(() => {

        const getPosts = async () => {
            if (userID) {

                setPosts([]);

                await createAPIEndpoint(`authors/${userID}`).get()
                    .then(res => {
                        console.log(res.data.following)
                        setPostAuthorIDs(res.data.following);
                        console.log("postAuthorIDs:",postAuthorIDs);
                    })

                



                /*
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
                setFriendsLoading(false)*/

            }
        }

        getPosts();
    }, [userID])

    useEffect(() => {
        let currPosts = [];
        if (postAuthorIDs.length > 0) {
            currPosts = posts;
            for (let postAuthor in postAuthorIDs){
                createAPIEndpoint(`authors/${postAuthor}/posts`)
                .get()
                .then(res => {
                    console.log("DATA:",res.data)
                    console.log("for author",postAuthor,"posts:",JSON.stringify(res.data))
                    //currPosts.push(res.data?)
                    //setPosts()
                })
            }
            /*
            createAPIEndpoint(`authors/${userID}/posts`)
                .get()
                .then(res => {
                    setPosts(res.data.items)
                    setLoading(false)
                    console.log(JSON.stringify(res.data))
                })
                .catch(err => {
                    // TODO: Add in error handling
                    console.log(err)
                });*/
        }
    }, [userID])

    return (
        <>
            <Layout>
                {loading && (
                    <Card>
                        <CircularProgress sx={{ margin: "auto" }} />
                    </Card>
                )}

                {(posts.length === 0 && !loading) && (
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
                    
                )}


            </Layout>
        </>
    )
}

export default Stream;