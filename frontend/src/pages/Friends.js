// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Card, Typography, Grid, Button, Alert, IconButton, Divider, Chip } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CloseIcon from '@mui/icons-material/Close';
import CheckIcon from '@mui/icons-material/Check';

const Friends = () => {
    return (
        <>
            <Layout>
                <Card>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Typography variant="h6" align="left">Incoming Friend Requests</Typography>
                        </Grid>

                        <Grid item xs={12}>
                            <Alert severity="info" style={{ textAlign: "left" }}>
                                To become true friends with another author, you must both accept each other's friend requests. You can lookup other authors on the Explore page.
                            </Alert>
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
                                    <Button variant="outlined" startIcon={<CloseIcon />} sx={{ marginRight: "5px" }}>
                                        Reject
                                    </Button>
                                    <Button variant="contained" endIcon={<CheckIcon />}>
                                        Accept
                                    </Button>
                                </div>

                            </div>
                        </Grid>
                    </Grid>
                </Card>

                <Card>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Typography variant="h6" align="left">All Friends</Typography>
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
                                    <Chip label="True Friend" sx={{marginRight: "10px"}}/>
                                    <IconButton>
                                        <CloseIcon />
                                    </IconButton>
                                </div>
                            </div>
                        </Grid>

                    </Grid>
                </Card>
            </Layout>
        </>
    )
}

export default Friends;