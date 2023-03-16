// React helpers
import React, { useState } from "react";
import { createAPIEndpoint, ENDPOINTS } from '../api';
import { useNavigate } from 'react-router';

// Material UI elements
import { Card, Typography, Grid, Button, Divider, TextField, InputAdornment, CircularProgress, IconButton, Tooltip } from "@mui/material";

// Material UI icons
import PublicRoundedIcon from '@mui/icons-material/PublicRounded';
import PersonIcon from '@mui/icons-material/Person';
import AccountIcon from '@mui/icons-material/AccountCircle';
import GroupsIcon from '@mui/icons-material/Groups';
import AddHomeIcon from '@mui/icons-material/AddHome';

const RemoteRequest = () => {
    const navigate = useNavigate();

    const [name, setName] = useState('')
    const [discord, setDiscord] = useState('')
    const [group, setGroup] = useState('')
    const [host, setHost] = useState('')
    const [loading, setLoading] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();
        setLoading(true);
        let data = {name, group, discord, host}

        createAPIEndpoint(ENDPOINTS.remoteRequest)
            .put(data)
            .then(res => {
                console.log(res)

                navigate("/")
            })
            .catch(err => {
                // TODO: Add in error handling
                setLoading(false);
                console.log(err)
            });
    }

    return <>
        <Card sx={{ padding: "20px", width: "300px", position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <IconButton>
                        <PublicRoundedIcon sx={{ fontSize: "80px", color: "#499BE9" }} />
                    </IconButton>
                </Grid>

                <Grid item xs={12}>
                    <Typography variant="h4" align="center">Request Remote Node Access</Typography>
                </Grid>

                <Grid item xs={12}>
                    <TextField
                        fullWidth
                        value={name}
                        onChange={(event) => { setName(event.target.value) }}
                        placeholder="Your Name"
                        style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                        variant="outlined"
                        InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><PersonIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                    >
                    </TextField>
                </Grid>

                <Grid item xs={12}>
                    <TextField
                        fullWidth
                        value={discord}
                        onChange={(event) => { setDiscord(event.target.value) }}
                        placeholder="Discord Username"
                        style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                        variant="outlined"
                        InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><AccountIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                    >
                    </TextField>
                </Grid>

                <Grid item xs={12}>
                    <TextField
                        fullWidth
                        value={group}
                        onChange={(event) => { setGroup(event.target.value) }}
                        placeholder="Group Number"
                        style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                        variant="outlined"
                        InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><GroupsIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                    >
                    </TextField>
                </Grid>

                <Grid item xs={12}>
                    <Tooltip disableTouchListener disableFocusListener title={
                        <React.Fragment>
                            Where API requests for your application come from. For example, ours come from "social-distribution-media.herokuapp.com".
                        </React.Fragment>
                    }>   
                        <TextField
                            fullWidth
                            value={host}
                            onChange={(event) => { setHost(event.target.value) }}
                            placeholder="Host"
                            style={{ backgroundColor: '#535560', borderRadius: "40px" }}
                            variant="outlined"
                            InputProps={{ style: { color: '#FFFFFF', borderRadius: "40px" }, startAdornment: (<InputAdornment position="start"><AddHomeIcon sx={{ color: "#FFFFFF" }} /></InputAdornment>) }}
                        >
                        </TextField>
                    </Tooltip>
                </Grid>

                <Grid item xs={12}>
                    <Divider />
                </Grid>

                <Grid item xs={12}>
                    {([name, discord, group, host].some(e => e === "")) ? (
                        <Button disabled variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }}>Submit</Button>
                    ) : (
                        <>
                            {loading ? <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }}><CircularProgress size="30px" /></Button> : <Button variant="contained" sx={{ width: "100%", backgroundColor: "#499BE9", color: "#FFFFFF" }} onClick={handleSubmit}>Submit</Button>}
                        </>
                    )}
                </Grid>

                
            </Grid>
        </Card>
    
    </>
}

export default RemoteRequest;