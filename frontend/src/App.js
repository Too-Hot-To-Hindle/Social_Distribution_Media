// React helpers
import './App.css';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';

// Pages
import Stream from './pages/Stream';
import NewPost from './pages/NewPost';
import PostDetails from './pages/PostDetails';
import EditPost from './pages/EditPost';
import Friends from './pages/Friends';
import Profile from './pages/Profile';
import SearchResults from './pages/SearchResults';
import Auth from './pages/Auth';
import Login from './pages/Login';
import SignUp from './pages/SignUp';

const router = createBrowserRouter([
  // need to change to splash screen/login
  {
    path: "/",
    element: <Auth/>,
  },
  // {
  //   path: "/signup",
  //   element: <SignUp/>,
  // },
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
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </div>
  );
}

export default App;
