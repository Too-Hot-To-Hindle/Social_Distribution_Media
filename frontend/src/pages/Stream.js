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
                var allPosts = [];
                await createAPIEndpoint(`authors/${userID}`).get()
                    .then(res => {
                        console.log(res.data.following);
                        setPostAuthorIDs(res.data.following);
                        

                        if (res.data.following.length > 0) {
                            console.log("length greater than 0")
                            
                            for (const postAuthor of res.data.following){
                                createAPIEndpoint(`authors/${postAuthor}/posts`)
                                .get()
                                .then(res => {
                                    console.log("DATA:",res.data.items)
                                    console.log("for author",postAuthor,"posts:",JSON.stringify(res.data.items))
                                    for (const index in res.data.items){
                                        console.log("in loop, item:",res.data.items[index]);
                                        allPosts.push(res.data.items[index]);
                                    }
                                })
                                .catch(err => {
                                    console.log("Error in getting posts: ",err)
                                });
                            }

                        } else {
                            //TO DO
                            console.log("no posts");
                        }
                    })
                    .catch(err => {
                        console.log("Error in getting following: ",err)
                    });


                    
                console.log("all posts:",allPosts);
                setPosts(allPosts);
                setLoading(false);
            }

        }
        getPosts();
    }, [userID]);


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