// React helpers
import { useState } from "react";
import { createAPIEndpoint, ENDPOINTS, BASIC_AUTH_COOKIE_NAME } from '../api';
import { useNavigate } from 'react-router';
import Cookies from 'js-cookie';
import { toast } from 'sonner';

// Material UI elements
import { Card, Typography, Grid, Button, Divider, TextField, InputAdornment, CircularProgress, IconButton } from "@mui/material";

// Material UI icons
import PublicRoundedIcon from '@mui/icons-material/PublicRounded';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import PasswordIcon from '@mui/icons-material/Password';
import FaceIcon from '@mui/icons-material/Face';


const Auth = () => {
    const navigate = useNavigate();

    const [authType, setAuthType] = useState("signin");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSignIn = (event) => {
        event.preventDefault();
        setLoading(true);
        let data = {
            "username": username,
            "password": password
        }

        createAPIEndpoint(ENDPOINTS.auth)
            .post(data)
            .then(res => {

                // TODO: instead of just setting the object, set a JWT token
                // (and maybe store it somewhere better than local storage?)
                localStorage.setItem('username', res.data.username); // capture logged in author username
                localStorage.setItem('author_id', res.data.id); // capture logged in author id

                let authData = window.btoa(username + ':' + password);
                Cookies.set(BASIC_AUTH_COOKIE_NAME, authData);

                navigate("/stream")
            })
            .catch(err => {
                setLoading(false);
                toast.error('An error has occurred.', {
                    description: 'Invalid sign-in credentials. Please try again.',
                });
            });
    }

    const handleSignUp = (event) => {
        event.preventDefault();
        setLoading(true);
        let data = {
            "username": username,
            "password": password
        }

        createAPIEndpoint(ENDPOINTS.authRegister)
            .post(data)
            .then(res => {
                let authData = window.btoa(username + ':' + password);
                Cookies.set(BASIC_AUTH_COOKIE_NAME, authData);
                console.log(res)
                setAuthType("signin")
                setLoading(false);
            })
            .catch(err => {
                setLoading(false);
                toast.error('An error has occurred.', {
                    description: 'Sign-up could not be completed at this time. Please try again later.',
                });
            });
    }

    return (
        <>
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
                                type="password"
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
                                    {loading ? <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }}><CircularProgress size="30px" /></Button> : <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }} onClick={handleSignIn}>Sign In</Button>}
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
                                type="password"
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
                                    {loading ? <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }}><CircularProgress size="30px" /></Button> : <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }} onClick={handleSignUp}>Sign Up</Button>}
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
        </>
    )
}

export default Auth;