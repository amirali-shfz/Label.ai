import React, { useState, useEffect } from "react";
import clsx from "clsx";
import { makeStyles } from "@material-ui/core/styles";
import CssBaseline from "@material-ui/core/CssBaseline";
import Drawer from "@material-ui/core/Drawer";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
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
import Paper from '@material-ui/core/Paper';

import iApi from "../services/image/imageApi";

const Contributions = () => {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {
        "CS 348 Project by Kevin Feng, Walker Hildebrand, Bilaal Hussain, Jacob Kim, Amirali Sharifzad "
      }
    </Typography>
  );
}

const ConfirmedModal = ({label, setLabel, allLabels, data}) => {
  console.log("confirmed modal label/data:", label, data)
  return (
  <div
  style={{
    display: "flex",
    flexDirection: "column",
    textAlign: "center",
    margin: "24px",
    alignItems:"space-between"
  }}
  >
    <FormControl >
      <InputLabel id="select-label">Label</InputLabel>
      <Select
        labelId="simple-select-label"
        id="simple-select"
        value={label}
        onChange={(event) => {setLabel(event.target.value)}}
      >
        {allLabels === undefined ? null : allLabels.map((label) => {return <MenuItem value={label}>{label.name}</MenuItem>})}
      </Select>
    </FormControl>
    {data === undefined ? null : data.map(({url}) => {return <img style={{maxHeight:"500px", height:"auto", width:"auto"}} src={url} alt={`example of ${label}`}/>})}
  </div>)
}

const DEFAULT_COUNT = 10;
const TablesModal = ({tableName: reportName}) => {
  const [allLabels, setAllLabels] = useState(undefined);
  const [label, setLabel] = useState({});
  const [data, setData] = useState([])

  const getLabels = async () => {
    const res = await iApi.getAllLabels()
    setAllLabels(res);
  };

  const getMislabelled = async () => {
    const mislabelled = await iApi.getMislabelledImages()
    setData(mislabelled);
  };

  const getUnderclassified  = async () => {
    const underclassified = await iApi.getUnderclassifiedImages(DEFAULT_COUNT);
    setData(underclassified);
  };
  useEffect(()  => {
    // api calls here based on which tablename is selected
    switch(reportName){
      case "labels":
        if(allLabels !== undefined)
          break;
        getLabels();
        break;
      case "mislabelled":
        getMislabelled();
        break;
      case "underclassified":
        getUnderclassified();
        break;
      default:
    }
  },[allLabels, reportName]);

  useEffect(() => {
    if (label === {} )
      return;
    const populateData = async () => {const res = await iApi.getConfirmedImagesByLabel(label.label_id); console.log("data from get confirmed image", label, res); setData(res)};
    populateData()
  },[label])

  switch(reportName){
    case "labels":
      return (
        <ConfirmedModal 
          allLabels={allLabels}
          label={label}
          setLabel={setLabel}
          data={data}
        />
      )
    case "mislabelled":
    case "underclassified":
      return (data === undefined? null : data.map((item) => <p>{JSON.stringify(item)}</p> ))
    default:
      return null;
  }
  
}

const drawerWidth = 240;

export default function Dashboard() {
  const classes = useStyles();
  const [open, setOpen] = React.useState(true);
  
  const [pageName, setPageName] = useState("dashboard"); // dashboard, tables

  const [tableName, setTableName] = useState("labels"); // labels, mislabelled, underclassified

  const handleDrawerOpen = () => {
    setOpen(true);
  };
  const handleDrawerClose = () => {
    setOpen(false);
  };

  
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
            Dashboard
          </Typography>
          {/* <IconButton color="inherit">
            <Badge badgeContent={4} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton> */}
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
            <ListItem button onClick={() => {setPageName("dashboard")}}>
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Dashboard" />
            </ListItem>
            <ListItem button onClick={() => {setPageName("tables")}}>
              <ListItemIcon>
                <LayersIcon />
              </ListItemIcon>
              <ListItemText primary="Tables" />
            </ListItem>
          </div>
        </List>
          <Divider />
        { pageName === "tables" ? 
        <List>
          <div>
            <ListSubheader inset>Saved reports</ListSubheader>
            <ListItem button onClick={() => {setTableName("labels")}}>
              <ListItemIcon>
                <AssignmentIcon />
              </ListItemIcon>
              <ListItemText primary="All image labels" />
            </ListItem>
            <ListItem button onClick={() => {setTableName("mislabelled")}}>
              <ListItemIcon>
                <AssignmentIcon />
              </ListItemIcon>
              <ListItemText primary="Mislabelled Images" />
            </ListItem>
            <ListItem button onClick={() => {setTableName("underclassified")}}>
              <ListItemIcon>
                <AssignmentIcon />
              </ListItemIcon>
              <ListItemText primary="Low classifications" />
            </ListItem>
          </div>
        </List> : null }
      </Drawer>
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <div
          style={{
            height: "100%",
            width: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "space-between"
          }}
        >
          {pageName === "dashboard" ? <ClassifyImageModal /> : <TablesModal tableName={tableName}/> }
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
