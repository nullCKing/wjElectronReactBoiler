import React, { useEffect, useState } from 'react';
import './IntroScreen.css';
import ReactDOM from 'react-dom';
import { useNavigate } from 'react-router-dom';

function IntroScreen() {
  return (
    <div className="container">
      <div className="box">
        <div className="title">
          <span className="block"></span>
          <h1>WJ Partners<span></span></h1>
        </div>
        <div className="role">
          <div className="block"></div>
          <p>Spartanburg, SC</p>
        </div>
      </div>
    </div>
  );
}


export default IntroScreen;