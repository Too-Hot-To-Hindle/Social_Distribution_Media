// Material UI components
import { Typography, Grid, Divider, Avatar } from "@mui/material";

// Material UI icons
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

// Helper functions
// formatLikesString
// takes in array of objects
// returns string of usernames in each object in format "@username1, @username2, @username3"
const formatLikesString = (likes, id) => {
    if (likes.length === 0) {
        return "No one."
    } else {

        const myComments = likes.find(like => like.id === id);

        let likesString = "";
        if (myComments.likes === null || myComments.likes === undefined) {
            likesString += "No one."
            return likesString;
        }

        else if (myComments.likes.length === 0) {
            likesString += "No one."
            return likesString;
        }

        else if (myComments.likes.length === 1) {
            likesString += `@${myComments.likes[0].author.displayName}`;
            return likesString;
        }

        else {
            myComments.likes.forEach((like, index) => {
                if (index === likes.length - 1) {
                    likesString += `@${like.author.displayName}`;
                } else {
                    likesString += `@${like.author.displayName}, `;
                }
            });
            return likesString;
        }
    }
}

const Comment = ({ username, content, likes, id }) => {
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

                {/* Comment likes */}
                <Grid item xs={12}>
                    <Typography variant="body1" align="left">
                        <strong>Liked by:</strong> {formatLikesString(likes, id)}
                    </Typography>
                </Grid>

                {/* Divider */}
                <Grid item xs={12}>
                    <Divider />
                </Grid>

            </Grid>
        </>
    )
}

export default Comment;