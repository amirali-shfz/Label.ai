import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

const Contributions = () => {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {
        "CS 348 Project by Kevin Feng, Walker Hildebrand, Bilaal Hussain, Jacob Kim, Amirali Sharifzad "
      }
    </Typography>
  );
}

const drawerWidth = 240;

export default function Login() {
  const classes = useStyles();
  const [open, setOpen] = React.useState(true);
  
  const [pageName, setPageName] = useState("dashboard"); // dashboard, tables

  const [tableName, setTableName] = useState("all"); // all, mislabelled, low

  const handleDrawerOpen = () => {
    setOpen(true);
  };
  const handleDrawerClose = () => {
    setOpen(false);
  };

  
  return (
    <div className={classes.root}>
        <div className={classes.loginContainer}>
            <TextField
            id="outlined-password-input"
            label="Username"
            type="password"
            className="login_input"
            autoComplete="current-password"
            variant="outlined"
            />
            <TextField
            id="outlined-password-input"
            label="Password"
            type="password"
            className="login_input"
            autoComplete="current-password"
            variant="outlined"
            />
            <Button variant="contained" color="primary" className="login_input">
                Login
            </Button>
        </div>

    </div>
  );
}

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    height: "100vh",
    alignIterm: "center"
  },
  loginContainer: {
    display: "flex",
    flexDirection: "column",
  }
}));
