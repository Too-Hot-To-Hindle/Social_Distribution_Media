// React helpers
import { createTheme, ThemeProvider } from "@mui/material/styles"
import { useState } from "react";

// Material UI elements
import { Card, Typography, Grid, Button, Divider, TextField, InputAdornment, CircularProgress, IconButton } from "@mui/material";

// Material UI icons
import PublicRoundedIcon from '@mui/icons-material/PublicRounded';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import PasswordIcon from '@mui/icons-material/Password';
import FaceIcon from '@mui/icons-material/Face';

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

const Auth = () => {

    const [authType, setAuthType] = useState("signin");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSignIn = () => {
        setLoading(true);
        setTimeout(() => {
            setLoading(false);
        }, 3000);
    }

    const handleSignUp = () => {
        setLoading(true);
        setTimeout(() => {
            setLoading(false);
        }, 3000);
    }

    return (
        <>
            <ThemeProvider theme={theme}>

                {authType === "signin" &&
                    <Card sx={{ padding: "20px", width: "300px", position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }}>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <IconButton>
                                    <PublicRoundedIcon sx={{ fontSize: "80px", color: "#499BE9" }} />
                                </IconButton>
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="h4" align="center">Sign In</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    value={username}
                                    onChange={(event) => { setUsername(event.target.value) }}
                                    placeholder="Username"
                                    style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                                    variant="outlined"
                                    InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><AccountCircleIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                                >
                                </TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    value={password}
                                    onChange={(event) => { setPassword(event.target.value) }}
                                    placeholder="Password"
                                    style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                                    variant="outlined"
                                    InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><PasswordIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                                >
                                </TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                {(username === "" || password === "") ? (
                                    <Button disabled variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }}>Sign In</Button>
                                ) : (
                                    <>
                                        {loading ? <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }}><CircularProgress size="30px" /></Button> : <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }} onClick={() => { handleSignIn() }}>Sign In</Button>}
                                    </>
                                )}
                            </Grid>

                            <Grid item xs={12}>
                                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                    <Typography variant="subtitle2" align="center">Don't have an account?</Typography>
                                    <Button onClick={() => { setAuthType("signup") }}>Sign Up</Button>
                                </div>
                            </Grid>

                        </Grid>
                    </Card>
                }

                {authType === "signup" &&
                    <Card sx={{ padding: "20px", width: "300px", position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }}>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <IconButton>
                                    <PublicRoundedIcon sx={{ fontSize: "80px", color: "#499BE9" }} />
                                </IconButton>
                            </Grid>

                            <Grid item xs={12}>
                                <Typography variant="h4" align="center">Sign Up</Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    value={firstName}
                                    onChange={(event) => { setFirstName(event.target.value) }}
                                    placeholder="First Name"
                                    style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                                    variant="outlined"
                                    InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><FaceIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                                >
                                </TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    value={lastName}
                                    onChange={(event) => { setLastName(event.target.value) }}
                                    placeholder="Last Name"
                                    style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                                    variant="outlined"
                                    InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><FaceIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                                >
                                </TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    value={username}
                                    onChange={(event) => { setUsername(event.target.value) }}
                                    placeholder="Username"
                                    style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                                    variant="outlined"
                                    InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><AccountCircleIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                                >
                                </TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    value={password}
                                    onChange={(event) => { setPassword(event.target.value) }}
                                    placeholder="Password"
                                    style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                                    variant="outlined"
                                    InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><PasswordIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                                >
                                </TextField>
                            </Grid>

                            <Grid item xs={12}>
                                <Divider />
                            </Grid>

                            <Grid item xs={12}>
                                {(firstName === "" || lastName === "" || username === "" || password === "") ? (
                                    <Button disabled variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }}>Sign Up</Button>
                                ) : (
                                    <>
                                        {loading ? <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }}><CircularProgress size="30px" /></Button> : <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }} onClick={() => { handleSignUp() }}>Sign Up</Button>}
                                    </>
                                )}
                            </Grid>

                            <Grid item xs={12}>
                                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                    <Typography variant="subtitle2" align="center">Already have an account?</Typography>
                                    <Button onClick={() => { setAuthType("signin") }}>Sign In</Button>
                                </div>
                            </Grid>

                        </Grid>
                    </Card>
                }
            </ThemeProvider>
        </>
    )
}

export default Auth;