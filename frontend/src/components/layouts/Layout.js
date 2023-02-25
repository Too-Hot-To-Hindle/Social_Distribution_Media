// React helpers
import React from "react"
import { useNavigate } from 'react-router-dom';

// Material UI elements
import { Card, Container, Grid, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography, Button } from "@mui/material"
import { createTheme, ThemeProvider } from "@mui/material/styles"

// Material UI icons
import PublicRoundedIcon from '@mui/icons-material/PublicRounded';
import DynamicFeedRoundedIcon from '@mui/icons-material/DynamicFeedRounded';
import PeopleAltRoundedIcon from '@mui/icons-material/PeopleAltRounded';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';


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

const Layout = ({ children }) => {

    const navigate = useNavigate();

    const pages = ["Stream", "Friends", "New Post"]
    const paths = ["/stream", "/friends", "/post"]
    const icons = [<DynamicFeedRoundedIcon sx={{ fontSize: "32px" }} />, <PeopleAltRoundedIcon sx={{ fontSize: "32px" }} />]

    const pathname = window.location.pathname
    const currentPage = pages[paths.indexOf(pathname)]

    return (
        <ThemeProvider theme={theme}>
            <Container maxWidth="lg" sx={{ marginTop: "10px" }}>
                <Grid container spacing={2}>
                    <Grid item xs={4}>
                        <div style={{ position: "sticky", top: "10px" }}>
                            <Card>
                                <List>
                                    <ListItem>
                                        <ListItemIcon>
                                            <PublicRoundedIcon sx={{ fontSize: "40px", color: "#499BE9" }} />
                                        </ListItemIcon>
                                    </ListItem>

                                    {pages.map((page, index) => {
                                        // if (pathname === paths[index]), then make icon blue and text blue + bold
                                        if (pathname === paths[index]) {
                                            if (page !== "New Post") {
                                                return (
                                                    <ListItem disablePadding key={page}>
                                                        <ListItemButton>
                                                            <ListItemIcon sx={{ color: "#499BE9" }}>
                                                                {icons[index]}
                                                            </ListItemIcon>
                                                            <ListItemText primary={page} primaryTypographyProps={{ fontSize: "24px", fontWeight: "500", color: "#499BE9" }} />
                                                        </ListItemButton>
                                                    </ListItem>
                                                )
                                            }
                                        }
                                        else {
                                            if (page !== "New Post") {
                                                return (
                                                    <ListItem disablePadding key={page}>
                                                        <ListItemButton onClick={() => { navigate(paths[index]) }}>
                                                            <ListItemIcon sx={{ color: "#F5F5F5" }}>
                                                                {icons[index]}
                                                            </ListItemIcon>
                                                            <ListItemText primary={page} primaryTypographyProps={{ fontSize: "24px", color: "#F5F5F5" }} />
                                                        </ListItemButton>
                                                    </ListItem>
                                                )
                                            }
                                        }
                                    })}
                                </List>

                                <Button variant="contained" fullWidth onClick={() => { navigate("/post") }}>Make a Post</Button>

                            </Card>

                            <Card>
                                <List disablePadding>
                                    <ListItem disablePadding>
                                        <ListItemButton>
                                            <ListItemIcon>
                                                <AccountCircleIcon sx={{ fontSize: "40px", color: "#F5F5F5" }} />
                                            </ListItemIcon>
                                            <ListItemText primary="John Smith" primaryTypographyProps={{ fontSize: "24px", color: "#F5F5F5" }} secondary="@johnsmith" secondaryTypographyProps={{ color: "#F5F5F5" }} />
                                        </ListItemButton>
                                    </ListItem>
                                </List>
                            </Card>
                        </div>


                    </Grid>

                    <Grid item xs={8}>
                        <Container sx={{ paddingTop: "30px" }}>
                            <Typography variant="h4" align="left" fontWeight="500">{currentPage}</Typography>
                            <br />
                            {children}
                        </Container>
                    </Grid>
                </Grid>
            </Container>
        </ThemeProvider>
    )
};

export default Layout;