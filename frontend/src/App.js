// React helpers
import './App.css';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { Toaster } from 'sonner';

// Pages
import Stream from './pages/Stream';
import NewPost from './pages/NewPost';
import PostDetails from './pages/PostDetails';
import EditPost from './pages/EditPost';
import Friends from './pages/Friends';
import Profile from './pages/Profile';
import SearchResults from './pages/SearchResults';
import Auth from './pages/Auth';
import Explore from './pages/Explore';
import GlobalProfile from './pages/GlobalProfile';

const router = createBrowserRouter([
  // need to change to splash screen/login
  {
    path: "/",
    element: <Auth />,
    key: Math.random(),
  },
  {
    path: "/stream",
    element: <Stream />,
    key: Math.random(),
  },
  {
    path: "/post",
    element: <NewPost />,
    key: Math.random(),
  },
  {
    path: ":authorID/post/:postID",
    element: <PostDetails />,
    key: Math.random(),
  },
  {
    path: ":authorID/post/:postID/edit",
    element: <EditPost />,
    key: Math.random(),
  },
  {
    path: "/friends",
    element: <Friends />,
    key: Math.random(),
  },
  {
    path: "/profile",
    element: <Profile />,
    key: Math.random(),
  },
  {
    path: "/profile/:authorURL",
    element: <GlobalProfile />,
    key: Math.random(),
  },
  {
    path: "/searchresults/:query",
    element: <SearchResults />,
    key: Math.random(),
  },
  {
    path: "/auth",
    element: <Auth />,
    key: Math.random(),
  },
  {
    path: "/explore",
    element: <Explore />,
    key: Math.random(),
  },
]);

const theme = createTheme({

  palette: {
    mode: 'dark',
  },

  typography: {
    h1: {
      fontFamily: 'Roboto',
      fontWeight: 'bold',
      color: "#F5F5F5"
    },
    h2: {
      fontFamily: 'Roboto',
      fontWeight: 'bold',
      color: "#F5F5F5"
    },
    h3: {
      fontFamily: 'Roboto',
      fontWeight: 'bold',
      color: "#F5F5F5"
    },
    h4: {
      fontFamily: 'Roboto',
      fontWeight: 'bold',
      color: "#F5F5F5"
    },
    h5: {
      fontFamily: 'Roboto',
      fontWeight: 'bold',
      color: "#F5F5F5"
    },
    h6: {
      fontFamily: 'Roboto',
      fontWeight: 'bold',
      color: "#F5F5F5"
    },
    subtitle1: {
      fontFamily: 'Roboto',
    },
    subtitle2: {
      fontFamily: 'Roboto',
    },
    body1: {
      fontFamily: 'Roboto',
    },
    body2: {
      fontFamily: 'Roboto',
    },
    button: {
      fontFamily: 'Roboto',
    },
    caption: {
      fontFamily: 'Roboto',
    },
    overline: {
      fontFamily: 'Roboto',
    }
  },

  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          background: "#444653",
          boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.25)",
          marginBottom: "10px",
          padding: "20px",
          transition: "box-shadow .3s",
          ":hover": {
            boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.50)"
          }
        }
      }
    },

    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: "30px",
          textTransform: 'none',
          fontSize: "18px"
        }
      }
    }
  }
});

function App() {
  return (
    <div className="App">
      <Toaster richColors style={{textAlign: "left"}}/>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </div>
  );
}

export default App;
