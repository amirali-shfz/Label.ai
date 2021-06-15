import Button from 'react-bootstrap/Button';
import './App.css';
import cApi from './services/classification/classificationApi';
import uApi from './services/user/userApi';
import {useState, useEffect} from 'react';
import { User } from './services/user/userModel';

const App = () => {
  const [user,setUser] = useState<User|{}>({});
  const [image,setImage] = useState('');

  useEffect(() => {
      uApi.getUser().then((val) => setUser(val));
  }, [user])

  useEffect(() => {
    if(image === '')
      getNewImage()  
  },[image]);

  const randomString = ():string => {return Math.random.toString().substring(16)}

  const getNewImage = async () => {
    const result = await cApi.getClassificationProblem();
    setImage(result.url);
  }

  const buttonClick = (isTrueLabel: boolean) => {
    cApi.postClassificationSolution(
      randomString(),
      randomString(),
      isTrueLabel,
      user);
      getNewImage()
  };

  
  return (
    <div className="App">
      <header className="App-header">
        <img src={image} />
        <>
        <Button variant="primary" onClick= {() => {buttonClick(true)} }>True</Button>
        <Button variant="secondary" onClick={()=> {buttonClick(false)} }>False</Button>
        <Button variant="secondary" onClick={()=> {getNewImage()} }>I Don't Know</Button>
        </>
      </header>
    </div>
  );
}

export default App;
