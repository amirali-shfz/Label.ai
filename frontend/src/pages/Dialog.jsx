import  {useState}  from "react";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

export default function FormDialog(props) {
  const {login, setOpenState, isOpen} = props;

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [errorText, setErrorText] = useState("")

  const submit = () => {

    if(!username || !password) {
      setErrorText("Fill all required fields")
      return
    }

    const result = login(username, password)
    
    if(!result) {
      setErrorText("Credential error")
      return
    }

  }

  return (
      <Dialog
        open={isOpen}
        onClose={() => {
          setErrorText(""); 
          setOpenState(false);
        }}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">Login</DialogTitle>
        <DialogContent>
          <DialogContentText>
            If you do not have any login credentials, please contact the system
            administrator
          </DialogContentText>
          <TextField
            error={errorText}
            helperText={errorText}
            autoFocus
            margin="dense"
            id="name"
            label="Username"
            type="text"
            fullWidth
            required
            onChange={(e)=>{setUsername(e.target.value)}}
          />
          <TextField
            autoFocus
            margin="dense"
            id="password"
            label="Password"
            type="password"
            fullWidth
            onChange={(e)=>{setPassword(e.target.value)}}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={()=>{setErrorText(""); setOpenState(false)}} color="primary">
            Cancel
          </Button>
          <Button onClick={submit} color="primary">
            Submit
          </Button>
        </DialogActions>
      </Dialog>
  );
}
