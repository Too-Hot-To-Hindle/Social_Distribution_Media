import React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { createAPIEndpoint, ENDPOINTS } from '../api';
import { useNavigate } from 'react-router';


export default function SignInSide() {
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        createAPIEndpoint(ENDPOINTS.authorsAuth)
            .post(data)
            .then(res => {
                console.log(res)
                navigate("/stream")
            })
            .catch(err => {
                // TODO: Add in error handling
                console.log(err)
            });
    };

  return (
    <Grid container component="main" sx={{ height: '100vh' }}>
        {/* Keep this in for now just in-case we wanna spice up the login later? */}
        <Grid
            item
            xs={false}
            sm={4}
            md={7}
            sx={{
                backgroundImage: 'url(https://source.unsplash.com/random)',
                backgroundRepeat: 'no-repeat',
                backgroundColor: (t) =>
                    t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
                backgroundSize: 'cover',
                backgroundPosition: 'center',
            }}
        />
        <Grid item 
            xs={12} 
            sm={8} 
            md={5} 
            component={Paper} 
            elevation={6} 
            square 
            sx={{
                display: 'flex', 
                justifyContent: 'center'
            }}
        >
            <Box
                sx={{
                    my: 8,
                    mx: 4,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '80%'
                }}
            >
                <Typography component="h1" variant="h5">
                    Sign in
                </Typography>
                <Box 
                    component="form" 
                    noValidate 
                    onSubmit={handleSubmit} 
                    sx={{ 
                        mt: 1,
                        display: 'flex',
                        flexDirection: 'column',
                        width: '70%',
                        alignItems: 'center'
                    }}
                >
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        autoComplete="username"
                        autoFocus
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        autoComplete="current-password"
                    />
                    {/* <FormControlLabel
                        control={<Checkbox value="remember" color="primary" />}
                        label="Remember me"
                    /> */}
                    <Button
                        type="submit"
                        variant="contained"
                        sx={{ 
                            mt: 3, 
                            mb: 2,
                            width: '50%'
                        }}
                    >
                        Sign In
                    </Button>
                    <Grid container>
                        {/* <Grid item xs={6}>
                            <Link href="#" variant="body2">
                            Forgot password?
                            </Link>
                        </Grid> */}
                        <Grid item xs={12}>
                            <Link href="/signup" variant="body2">
                                {"Don't have an account? Sign Up"}
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Grid>
    </Grid>
  );
}