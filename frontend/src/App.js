// React helpers
import './App.css';
import { createBrowserRouter, RouterProvider } from "react-router-dom";

// Pages
import Stream from './pages/Stream';
import NewPost from './pages/NewPost';
import PostDetails from './pages/PostDetails';
import EditPost from './pages/EditPost';

const router = createBrowserRouter([
  // need to change to splash screen/login
  {
    path: "/",
    element: <Stream/>,
  },
  {
    path: "/stream",
    element: <Stream/>,
  },
  {
    path: "/post",
    element: <NewPost/>,
  },
  {
    path: "/post/:id",
    element: <PostDetails/>,
  },
  {
    path: "/post/:id/edit",
    element: <EditPost/>,
  }
]);

function App() {
  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
