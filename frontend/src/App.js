// React helpers
import './App.css';
import { createBrowserRouter, RouterProvider } from "react-router-dom";

// Pages
import Stream from './pages/Stream';
import NewPost from './pages/NewPost';
import PostDetails from './pages/PostDetails';
import EditPost from './pages/EditPost';
import Friends from './pages/Friends';
import Profile from './pages/Profile';
import SearchResults from './pages/SearchResults';
import Auth from './pages/Auth';

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
  },
  {
    path: "/friends",
    element: <Friends/>,
  },
  {
    path: "/profile",
    element: <Profile/>,
  },
  {
    path: "/searchresults",
    element: <SearchResults/>,
  },
  {
    path: "/auth",
    element: <Auth/>,
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
