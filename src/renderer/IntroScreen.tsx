import React, { useEffect } from 'react';
import Lottie from 'lottie-react';
import spinnerAnimation from './sync-icon.json';
import './IntroScreen.css';
import { useNavigate } from 'react-router-dom';

function IntroScreen() {
  const navigate = useNavigate(); // get the navigate function

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/home'); // navigate to /home after 5.5 seconds
    }, 5000); // time in milliseconds

    // cleanup function to clear the timer when the component unmounts
    return () => clearTimeout(timer);
  }, [navigate]); // dependency array

  return (
    <div className="parent-container">
      <div className="container">
        <div className="box">
        <div style={{ height: '100px' }}></div>
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
        <div className="sync-files">
          <Lottie
              animationData={spinnerAnimation}
              style={{ height: '30px', width: '30px' }}
            />
            <span>Loading content...</span> {/* Add your text */}
        </div>
    </div>
  );
}

export default IntroScreen;