// Layout component
import Layout from "../components/layouts/Layout";

// Custom components
import Post from "../components/Post";

const PostDetails = () => {
    return (
        <>
            <Layout>
                <Post hideDetailsButton={true} hideEditButton={false}/>
            </Layout>
        </>
    )
}

export default PostDetails;