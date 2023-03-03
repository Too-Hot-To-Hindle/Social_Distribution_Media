// React helpers
import { useState, useEffect } from "react";

// Custom components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";
import SharedPost from "../components/SharedPost";

// Material UI components
import { Card, Typography, CircularProgress } from '@mui/material';

// Material UI icons
import PagesIcon from '@mui/icons-material/Pages';

const Stream = () => {
    const [loading, setLoading] = useState(true)
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        setTimeout(() => {
            setLoading(false)
        }, 2000)
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
                    </>
                )}

            </Layout>
        </>
    )
}

export default Stream;