// React helpers
import './App.css';
import { createBrowserRouter, RouterProvider } from "react-router-dom";

// Pages
import Stream from './pages/Stream';
import NewPost from './pages/NewPost';

const router = createBrowserRouter([
  {
    path: "/stream",
    element: <Stream/>,
  },

  {
    path: "/post",
    element: <NewPost/>,
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
