import React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import { createAPIEndpoint, ENDPOINTS } from '../api';
import { useNavigate } from 'react-router';
import CSRFTOKEN from '../api/csrftoken';

export default function SignUp() {
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        createAPIEndpoint(ENDPOINTS.authRegister)
            .post(data)
            .then(res => {
                navigate("/stream")
            })
            .catch(err => {
                // TODO: Add in error handling
                console.log(err)
            });
    };

  return (
    <Grid container component="main" sx={{ height: '100vh' }}
    >
        <Grid item             
            xs={12} 
            sm={12} 
            md={12} 
            component={Paper} 
            elevation={6} 
            square 
            sx={{
                display: 'flex', 
                justifyContent: 'center',
            }}
        >
            <Box
                sx={{
                    marginTop: '10%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    alignContent: 'center',
                    justifyContent: 'center',
                    height: '100%'
                }}
            >
                <Typography component="h1" variant="h5">
                    Sign up
                </Typography>
                <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3, height: '100%', alignItems: 'center', }}>
                    <CSRFTOKEN/>
                    <Grid container spacing={2}>
                        { /*TODO: Do we need more info? */}
                        {/* <Grid item xs={12} sm={6}>
                            <TextField
                                autoComplete="given-name"
                                name="firstName"
                                required
                                fullWidth
                                id="firstName"
                                label="First Name"
                                autoFocus
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                required
                                fullWidth
                                id="lastName"
                                label="Last Name"
                                name="lastName"
                                autoComplete="family-name"
                            />
                        </Grid> */}
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                id="username"
                                label="Username"
                                name="username"
                                autoComplete="username"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                autoComplete="new-password"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            {/* <FormControlLabel
                                control={<Checkbox value="allowExtraEmails" color="primary" />}
                                label="Do you consent to having your data stolen."
                            /> */}
                        </Grid>
                    </Grid>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Sign Up
                        </Button>
                    <Grid container justifyContent="flex-end">
                        <Grid item xs={12}>
                            <Link href="/" variant="body2">
                                Already have an account? Sign in
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Grid>
    </Grid>
  );
}