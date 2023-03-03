// Material UI components
import { Card, Typography, Grid, Divider, IconButton, Button } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const Comment = ({ username, content }) => {

    return (
        <>
            <Grid container spacing={2}>
                {/* Comment details */}
                <Grid item xs={12}>
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <div style={{ display: "flex", alignItems: "center" }}>
                            <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5", marginRight: "10px" }} />

                            <div>
                                <Typography variant="h6" align="left">@{username}</Typography>
                            </div>
                        </div>

                    </div>
                </Grid>

                {/* Comment content */}
                <Grid item xs={12}>
                    <Typography variant="body1" align="left">
                        {content}
                    </Typography>
                </Grid>

            </Grid>
        </>
    )
}

export default Comment;