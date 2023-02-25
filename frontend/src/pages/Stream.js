// Layout component
import Layout from "../components/layouts/Layout";

// Material UI components
import { Card, Typography } from "@mui/material";

const Stream = () => {
    return (
        <>
            <Layout>
                <Card sx={{height: "300px"}}>
                    <Typography>Lorem ipsum dolor...</Typography>
                </Card>

                <Card sx={{height: "300px"}}>
                    <Typography>Lorem ipsum dolor...</Typography>
                </Card>

                <Card sx={{height: "300px"}}>
                    <Typography>Lorem ipsum dolor...</Typography>
                </Card>

                <Card sx={{height: "300px"}}>
                    <Typography>Lorem ipsum dolor...</Typography>
                </Card>

                <Card sx={{height: "300px"}}>
                    <Typography>Lorem ipsum dolor...</Typography>
                </Card>
            </Layout>
        </>
    )
}

export default Stream;