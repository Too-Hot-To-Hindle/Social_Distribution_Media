// React helpers
import { useState } from 'react';

// Material UI components
import { CircularProgress, Card, Typography, Grid, Divider, IconButton, Button, TextField } from "@mui/material";

// Layout component
import Layout from "../components/layouts/Layout";

// Custom components
import Post from "../components/Post";
import Comment from "../components/Comment";

const PostDetails = () => {

    const [commentBody, setCommentBody] = useState("");
    const [commentUploading, setCommentUploading] = useState(false);

    const handleCommentUpload = () => {
        setCommentUploading(true);

        // TODO: upload comment to backend here

        setTimeout(() => {
            setCommentUploading(false);
        }, 1500);
    }

    return (
        <>
            <Layout>
                <Post hideDetailsButton={true} hideEditButton={false} hideCommentButton={true} />

                <Card>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Typography variant="h6" align="left">Comments</Typography>
                        </Grid>

                        <Grid item xs={12}>
                            <Divider/>
                        </Grid>

                        <Grid item xs={12}>
                            <TextField placeholder="Write a comment..." multiline maxRows={Infinity} fullWidth onChange={(event) => {setCommentBody(event.target.value)}}/>
                        </Grid>        

                        <Grid item xs={12}>
                            <Button variant="contained" fullWidth disabled={commentUploading} onClick={handleCommentUpload}>{commentUploading ? <CircularProgress size={21} sx={{ margin: "5px" }} /> : "Comment"}</Button>
                        </Grid>                

                        <Grid item xs={12}>
                            <Divider/>
                        </Grid>

                        <Grid item xs={12}>
                            <Comment />
                        </Grid>
                    </Grid>
                </Card>

            </Layout>
        </>
    )
}

export default PostDetails;