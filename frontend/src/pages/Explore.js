import { useState, useEffect } from "react";
import { createAPIEndpoint } from '../api';
import { toast } from 'sonner';

// Custom components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";

// Material UI components
import { Card, Typography, Grid, CircularProgress, Alert } from '@mui/material';

// Material UI icons
import PagesIcon from '@mui/icons-material/Pages';
import { all } from "axios";

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

function shuffle(array) {
    let currentIndex = array.length,  randomIndex;

    while (currentIndex != 0) {

      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;

      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
  
    return array;
}  



const Explore = () => {
        const [loading, setLoading] = useState(true)
    
        const [userID, setUserID] = useState(null);
        const [posts, setPosts] = useState([]);


        // useEffect to get the username and user ID from local storage
        useEffect(() => {
            setUserID(localStorage.getItem('author_id'))
        }, [])
    
        // useEffect to get all posts
        useEffect(() => {
            
            const getPosts = async () => {
                if (userID) {
                    try {
                        const response = await createAPIEndpoint(`authors?page=1&size=10`).get()
                        
                        var allPosts = []
                        for (let author of response.data.items) {
                            try {
                                const response = await createAPIEndpoint(`authors/${author._id}/posts`).get()
                                for (const individualPost of response.data.items) {
                                    allPosts.push(individualPost)
                                }
                            }
                            catch (err) {
                                toast.error('An error has occurred.', {
                                    description: "Could not retrieve posts at this time. Please try again later.",
                                })
                            }
                        }
                        //allPosts.sort(sortByDate);
                        shuffle(allPosts);
                        setPosts(allPosts);
                        setLoading(false);
                    }
                    catch (err) {
                        toast.error('An error has occurred.', {
                            description: 'Could not retrieve authors at this time. Please try again later.',
                        });
                    }
                     
                }
            }
    
            getPosts();
        }, [userID])
    



    
    return (
        <>
            <Layout>

            <Alert severity="info" sx={{ marginBottom: "20px" }}>
                    <Typography align="left">The Explore page displays posts from the top 10 authors on our site! To see posts only from users you follow, go to your Stream.</Typography>
                </Alert>
                {loading && (
                    <Card>
                        <CircularProgress sx={{ margin: "auto" }} />
                    </Card>
                )}

                {(!loading && posts.length === 0) && (
                    <Card>
                        <PagesIcon sx={{ fontSize: "60px" }} />
                        <Typography variant="h6" component="h2" sx={{ textAlign: "center" }}>Nothing to Explore!</Typography>
                    </Card>
                )}

                {(!loading && posts.length > 0) && (
                    
                    <Grid container spacing={2}>
                        {posts.map((item, index) => (
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

            </Layout>
        </>
    )
}

export default Explore;