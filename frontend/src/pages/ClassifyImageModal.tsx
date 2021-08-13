import iApi from "../services/image/imageApi";

import { useState, useEffect } from "react";
import Button from '@material-ui/core/Button';
import _ from 'lodash';
import { User } from "../services/user/userModel";


const ClassifyImageModal = (props:{user: User, allLabels: Array<{label_id: string}>}) => {

  const {user, allLabels} = props;
  const [labelFilter, setLabelFilter] = useState("");
  const [image, setImage] = useState("");
  const [label, setLabel] = useState<{label_name:string, label_id:string, class_id:string}>({label_name:"", label_id:"",class_id:""});

  useEffect(() => {
    if (image === "") getNewImage();
  }, [image]);

  const getNewImage = async () => {
    const result = await iApi.getClassificationProblem();
    setImage(result?.prompt[0]?.url);
    setLabel(_.sample(result?.prompt[0]?.labels));
  };

  const buttonClick = (isTrueLabel: boolean|null) => {
    iApi.postClassificationSolution(
      isTrueLabel,
      label,
      user
    );
    getNewImage();
  };

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
      <h1 style={{ color: "black" }}>Does this image contain: {label.label_name}</h1>
      <div style={{ textAlign: "center" }}>
        <img
          src={image}
          style={{ maxHeight: "600px", height:"auto", width:"auto"}}
          alt="to classify"
        />
      </div>
      <div style={{ display: "flex" , justifyContent:"center", marginTop: "10px" }}>
        <Button
          onClick={() => { buttonClick(true)}}
          style={Object.assign({}, buttonStyle, { backgroundColor: "green" })}
        >
          Yes
        </Button>
        <Button
          style={Object.assign({}, buttonStyle, { backgroundColor: "red" })}
          onClick={() => { buttonClick(false);}}
        >
          No
        </Button>
        <Button
          style={Object.assign({}, buttonStyle, { backgroundColor: "grey" })}
          onClick={() => { buttonClick(null);}}
        >
          Unsure
        </Button>
      </div>
    </div>
  );
};

const buttonStyle = {
  height: "100%",
  width: "10%",
  cursor: "pointer",
  color: "white",
  padding: "5px 15px",
  borderRadius: "5px",
  marginLeft: "15px",
  marginRight: "15px"
};

export default ClassifyImageModal;
