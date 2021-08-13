/* eslint-disable jsx-a11y/alt-text */
import React, { useState, useEffect } from "react";
import clsx from "clsx";
import { makeStyles } from "@material-ui/core/styles";
import CssBaseline from "@material-ui/core/CssBaseline";
import Drawer from "@material-ui/core/Drawer";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";

import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import ClassifyImageModal from "./ClassifyImageModal";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import ListSubheader from "@material-ui/core/ListSubheader";
import DashboardIcon from "@material-ui/icons/Dashboard";
import LayersIcon from "@material-ui/icons/Layers";
import AssignmentIcon from "@material-ui/icons/Assignment";

import ConfirmedPage from "./ConfirmedReport";
import NewConfidenceTable from "./NewTable";
import uApi from "../services/user/userApi";
import iApi from "../services/image/imageApi";
import FormDialog from "./Dialog";

const Contributions = () => {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {
        "CS 348 Project by Kevin Feng, Walker Hildebrand, Bilaal Hussain, Jacob Kim, Amirali Sharifzad "
      }
    </Typography>
  );
}

const LABEL_FILTERED_PAGES = {"all":true, "confirmed":true}


const DEFAULT_COUNT = 10;
const TablesPage = ({ tableName, allLabels }) => {
  const [labelId, setLabelId] = useState("");
  const [data, setData] = useState([]);

  useEffect(async () => {
    var label_id = tableName in LABEL_FILTERED_PAGES ? labelId : "";
    const res = await iApi.getImages(tableName, DEFAULT_COUNT, label_id);
    setData(res)
  }, [tableName, labelId]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        textAlign: "center",
        margin: "24px",
        alignItems: "space-between",
      }}
    >
      {tableName in LABEL_FILTERED_PAGES ? (
        <ConfirmedPage
          allLabels={allLabels}
          label={labelId}
          setLabel={setLabelId}
          data={data}
          reportName={tableName}
        />
      ) : (
        <NewConfidenceTable
          rows={data === undefined ? [] : data}
        ></NewConfidenceTable>
      )}
    </div>
  );
};

const drawerWidth = 240;

export default function Dashboard() {
  const classes = useStyles();
  const [open, setOpen] = React.useState(true);

  const [pageName, setPageName] = useState("Dashboard"); // dashboard, tables

  const [tableName, setTableName] = useState("all"); // all, confirmed, misclassified, discovered, controversial

  const handleDrawerOpen = () => {
    setOpen(true);
  };
  const handleDrawerClose = () => {
    setOpen(false);
  };

  const [loginModalShow, setLoginModalShow] = useState(false);
  const [user, setUser] = useState({});
  const [allUsers, setAllUsers] = useState({});

  const [allLabels, setAllLabels] = useState(undefined);

  useEffect(() => {
    iApi.getAllLabels().then((res) => {
      // TODO: allLabels performance slow
      setAllLabels(res.sort((a, b) => (a.name < b.name ? -1 : 1)));
    });
  }, []);

  const userLogin = (username, password) => {
    if (!(username in allUsers)) return false;
    setUser({
      username,
      ...allUsers[username],
    });
    setLoginModalShow(false);
    return true;
  };
  useEffect(() => {
    uApi.getUsersMap().then((val) => {
      setAllUsers(val);
    });
  }, []);

  // Prevent re-render of ClassifyImagePage by keeping state up here
  const [image, setImage] = useState("");
  const [label, setLabel] = useState({ label_name: "", label_id: "", class_id: "" });
  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar
        position="absolute"
        className={clsx(classes.appBar, open && classes.appBarShift)}
      >
        <Toolbar className={classes.toolbar}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            className={clsx(
              classes.menuButton,
              open && classes.menuButtonHidden
            )}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            component="h1"
            variant="h6"
            color="inherit"
            noWrap
            className={classes.title}
          >
            {pageName}
          </Typography>

          {user?.username ? (
            <Typography
              edge="end"
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              className={classes.title}
            >
              {"Hello " + user.username}
            </Typography>
          ) : (
            <IconButton
              edge="end"
              color="inherit"
              aria-label="Login"
              onClick={() => {
                setLoginModalShow(!loginModalShow);
              }}
            >
              Login
            </IconButton>
          )}
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        classes={{
          paper: clsx(classes.drawerPaper, !open && classes.drawerPaperClose),
        }}
        open={open}
      >
        <div className={classes.toolbarIcon}>
          <IconButton onClick={handleDrawerClose}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <Divider />
        <List>
          <div>
            <ListItem
              button
              onClick={() => {
                setPageName("Dashboard");
              }}
            >
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Dashboard" />
            </ListItem>
            {!user?.admin ? (
              <ListItem
                button
                onClick={() => {
                  setPageName("Tables");
                }}
              >
                <ListItemIcon>
                  <LayersIcon />
                </ListItemIcon>
                <ListItemText primary="Tables" />
              </ListItem>
            ) : null}
          </div>
        </List>
        <Divider />
        {pageName === "Tables" ? (
          <List>
            <div>
              <ListSubheader inset>Categories</ListSubheader>
              <ListItem button onClick={() => { setTableName("all"); }}>
                <ListItemIcon><AssignmentIcon/></ListItemIcon>
                <ListItemText primary="All" />
              </ListItem>
              <ListItem button onClick={() => { setTableName("confirmed"); }}>
                <ListItemIcon><AssignmentIcon/></ListItemIcon>
                <ListItemText primary="Confirmed" />
              </ListItem>
              <ListItem button onClick={() => { setTableName("misclassified"); }}>
                <ListItemIcon><AssignmentIcon/></ListItemIcon>
                <ListItemText primary="Misclassified" />
              </ListItem>
              <ListItem button onClick={() => { setTableName("discovered"); }}>
                <ListItemIcon><AssignmentIcon/></ListItemIcon>
                <ListItemText primary="Discovered" />
              </ListItem>
              <ListItem button onClick={() => { setTableName("controversial"); }}>
                <ListItemIcon><AssignmentIcon/></ListItemIcon>
                <ListItemText primary="Controversial" />
              </ListItem>
            </div>
          </List>
        ) : null}
      </Drawer>
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <div
          style={{
            height: "100%",
            width: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "space-between",
          }}
        >
          {
            <FormDialog
              login={userLogin}
              setOpenState={setLoginModalShow}
              isOpen={loginModalShow}
            />
          }
          {pageName === "Dashboard" ? (
            <ClassifyImageModal user={user} allLabels={allLabels} image={image} setImage={setImage} label={label} setLabel={setLabel}/>
          ) : (
            <TablesPage tableName={tableName} allLabels={allLabels} />
          )}
          <Contributions />
        </div>
      </main>
    </div>
  );
}

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  root: {
    display: "flex",
    height: "100vh",
  },
  toolbar: {
    paddingRight: 24, // keep right padding when drawer closed
  },
  toolbarIcon: {
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    padding: "0 8px",
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  menuButtonHidden: {
    display: "none",
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: "relative",
    whiteSpace: "nowrap",
    width: drawerWidth,
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: "hidden",
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing(7),
    [theme.breakpoints.up("sm")]: {
      width: theme.spacing(9),
    },
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    display: "flex",
    "flex-flow": "column",
    height: "100%",
    width: "100%",
  },
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
    width: "100%",
    marginLeft: 24,
    marginRight: 24,
  },
  paper: {
    padding: theme.spacing(2),
    display: "flex",
    overflow: "auto",
    flexDirection: "column",
  },
  fixedHeight: {
    height: 240,
  },
}));
