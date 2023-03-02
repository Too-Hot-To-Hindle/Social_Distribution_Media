// React helpers
import { useState, useEffect } from "react";
import { createAPIEndpoint, ENDPOINTS } from '../api';

// Custom components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";
import SharedPost from "../components/SharedPost";

// Material UI components
import { Card, Typography, CircularProgress } from '@mui/material';

// Material UI icons
import PagesIcon from '@mui/icons-material/Pages';

const Explore = () => {
    const [loading, setLoading] = useState(true)
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        // createAPIEndpoint(ENDPOINTS.POSTS).fetchAll()
        //     .then(res => {
        //         setPosts(res.data);
        //         setLoading(false);
        //     })
        //     .catch(err => console.log(err))
    }, [])

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
                        <Post hideEditButton={true} hideLink={true} hideDeleteButton={true} />
                        <SharedPost hideEditButton={true} hideLink={true} hideDeleteButton={true} />
                        <Post hideEditButton={true} hideLink={true} hideDeleteButton={true} />
                        <Post hideEditButton={true} hideLink={true} hideDeleteButton={true} />
                        <Post hideEditButton={true} hideLink={true} hideDeleteButton={true} />
                    </>
                )}

            </Layout>
        </>
    )
}

export default Explore;