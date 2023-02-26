// Custom components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";

const Stream = () => {
    return (
        <>
            <Layout>
                <Post hideEditButton={true}/>
                <Post hideEditButton={true}/>
                <Post hideEditButton={true}/>
                <Post hideEditButton={true}/>
            </Layout>
        </>
    )
}

export default Stream;