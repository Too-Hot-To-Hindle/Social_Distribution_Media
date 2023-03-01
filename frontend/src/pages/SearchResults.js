// Layout component
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";

// Material UI components
import { Card, Typography, Grid, IconButton, Chip, Divider, Button } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CloseIcon from '@mui/icons-material/Close';

const SearchResults = () => {
    return (
        <>
            <Layout>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <Card>
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <Typography variant="h6" align="left">Authors</Typography>
                                </Grid>

                                <Grid item xs={12}>
                                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                            <div>
                                                <Typography variant="h6" align="left">Jane Doe</Typography>
                                                <Typography variant="body1" align="left">@janedoe</Typography>
                                            </div>
                                        </div>

                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <Button variant="contained">Send Friend Request</Button>
                                        </div>
                                    </div>
                                </Grid>

                                <Grid item xs={12}>
                                    <Divider />
                                </Grid>

                                <Grid item xs={12}>
                                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                            <div>
                                                <Typography variant="h6" align="left">John Doe</Typography>
                                                <Typography variant="body1" align="left">@johndoe</Typography>
                                            </div>
                                        </div>

                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <IconButton>
                                                <CloseIcon />
                                            </IconButton>
                                        </div>
                                    </div>
                                </Grid>

                                <Grid item xs={12}>
                                    <Divider />
                                </Grid>

                                <Grid item xs={12}>
                                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />
                                            <div>
                                                <Typography variant="h6" align="left">James Appleseed</Typography>
                                                <Typography variant="body1" align="left">@jamesappleseed</Typography>
                                            </div>
                                        </div>

                                        <div style={{ display: "flex", alignItems: "center" }}>
                                            <Chip label="True Friend" sx={{ marginRight: "10px" }} />
                                            <IconButton>
                                                <CloseIcon />
                                            </IconButton>
                                        </div>
                                    </div>
                                </Grid>
                            </Grid>
                        </Card>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    <Grid item xs={12}>
                        <Typography variant="h6" align="left">Posts</Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Grid container>
                            <Grid item xs={12}>
                                <Post hideEditButton={true} hideDeleteButton={true}/>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Layout>

        </>
    )
}

export default SearchResults;