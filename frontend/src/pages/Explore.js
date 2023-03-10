// React helpers
import { useState, useEffect } from "react";
import { createAPIEndpoint, ENDPOINTS } from '../api';

// Custom components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";
import SharedPost from "../components/SharedPost";

// Material UI components
import { Card, Typography, Grid } from '@mui/material';

// Material UI icons
import PagesIcon from '@mui/icons-material/Pages';

const Explore = () => {
    
    return (
        <>
            <Layout>
                <Grid item xs={12}>
                    <Card>
                        <PagesIcon sx={{ fontSize: "60px" }} />
                        <Typography variant="h6" component="h2" sx={{ textAlign: "center" }}>Coming soon!</Typography>
                    </Card>
                </Grid>
            </Layout>
        </>
    )
}

export default Explore;