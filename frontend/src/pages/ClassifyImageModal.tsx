import iApi from "../services/image/imageApi";
import uApi from "../services/user/userApi";
import { useState, useEffect } from "react";
import { User } from "../services/user/userModel";
import _ from 'lodash';

const ClassifyImageModal = () => {
  const [user, setUser] = useState<User | {}>({});
  const [image, setImage] = useState("");
  const [label, setLabel] = useState<{label_name:string, label_id:string, class_id:string}>({label_name:"", label_id:"",class_id:""});

  useEffect(() => {
    uApi.getUser().then((val) => setUser(val));
  }, []);

  useEffect(() => {
    if (image === "") getNewImage();
  }, [image]);

  const getNewImage = async () => {
    const result = await iApi.getClassificationProblem();
    setImage(result?.prompt[0]?.url);
    setLabel(_.sample(result?.prompt[0]?.labels));
  };

  const buttonClick = (isTrueLabel: boolean) => {
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
      <h1 style={{ color: "black" }}>Is this: {label.label_name}</h1>
      <div style={{ textAlign: "center" }}>
        <img
          src={image}
          style={{ maxHeight: "600px", height:"auto", width:"auto"}}
          alt="to classify"
        />
      </div>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <button
          onClick={() => {
            buttonClick(true);
          }}
          style={Object.assign({}, buttonStyle, { backgroundColor: "green" })}
        >
          Yes
        </button>
        <button
          onClick={() => {
            buttonClick(false);
          }}
          style={Object.assign({}, buttonStyle, { backgroundColor: "red" })}
        >
          No
        </button>
        <button
          onClick={() => {
            getNewImage();
          }}
          style={Object.assign({}, buttonStyle, { backgroundColor: "grey" })}
        >
          I Don't Know
        </button>
      </div>
    </div>
  );
};

const buttonStyle = {
  height: "100%",
  width: "30%",
  cursor: "pointer",
  "text-transform": "uppercase",
  color: "white",
  padding: "5px 15px",
  borderRadius: "5px",
};

export default ClassifyImageModal;
