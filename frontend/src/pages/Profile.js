// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Card, Typography } from "@mui/material";

const Profile = () => {
    return (
        <>
            <Layout>
                <Card sx={{height: "300px"}}>
                    <Typography>Lorem ipsum dolor...</Typography>
                </Card>
            </Layout>
        </>
    )
}

export default Profile;