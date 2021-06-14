import logo from './logo.svg';
import Button from 'react-bootstrap/Button';
import './App.css';
import cApi from './services/classification/classificationApi';
import uApi from './services/user/userApi';
import {useState, useEffect} from 'react';
import { User } from './services/user/userModel';

const App = () => {
  const [user,setUser] = useState<User|undefined>(undefined);
  useEffect( () => {
    if(user !== undefined)
      return;
    uApi.getUser().then((val) => setUser(val));
  })

  const randomString = ():string => {return Math.random.toString().substring(16)}

  const buttonClick = (isTrueLabel: boolean) => {
    if(!user) return; 
    cApi.postClassificationSolution(
      randomString(),
      randomString(),
      isTrueLabel,
      user);
  }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <>
        <Button variant="primary" 
                onClick= {() =>  {buttonClick(true)}}>
          True
        </Button>
        <Button variant="secondary" onClick={()=>buttonClick(false)}>False</Button>
        </>
      </header>
    </div>
  );
}

export default App;
