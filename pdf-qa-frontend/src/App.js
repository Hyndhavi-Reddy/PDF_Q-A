import logo from "./logo.svg";
import "./App.css";
import React from "react";
import UploadFile from "./components/UploadFile";
import AskQuestion from "./components/AskQuestion";

function App() {
  return (
    <div>
      <h1>PDF Q&A App</h1>
      <UploadFile />
      <AskQuestion />
    </div>
  );
}

export default App;
