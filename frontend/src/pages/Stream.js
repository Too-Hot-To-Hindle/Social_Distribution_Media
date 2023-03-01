// Custom components
import Layout from "../components/layouts/Layout";
import Post from "../components/Post";
import SharedPost from "../components/SharedPost";

const Stream = () => {
    return (
        <>
            <Layout>
                <Post hideEditButton={true} hideLink={true} hideDeleteButton={true}/>
                <SharedPost hideEditButton={true} hideLink={true} hideDeleteButton={true}/>
                <Post hideEditButton={true} hideLink={true} hideDeleteButton={true}/>
                <Post hideEditButton={true} hideLink={true} hideDeleteButton={true}/>
                <Post hideEditButton={true} hideLink={true} hideDeleteButton={true}/>
            </Layout>
        </>
    )
}

export default Stream;