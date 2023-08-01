import React, { useEffect, useState } from 'react';
import Lottie from 'lottie-react';
import spinnerAnimation from './sync-icon.json';
import './IntroScreen.css';
import { useNavigate } from 'react-router-dom';

function IntroScreen() {
  const navigate = useNavigate(); // get the navigate function
  const [loadingText, setLoadingText] = useState("Loading content...");
  const [loading, setLoading] = useState(true); // New state variable

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage('check-dependencies');  // trigger the check dependencies event

    const listener = (message) => {
      setLoadingText(message); // update the loading text with the Python script's output
      if (message === 'All dependencies up-to-date.') { // Replace this with the actual message you expect when all dependencies are installed
        setLoading(false); // Loading is done
      }
    };

    const removeListener = window.electron.ipcRenderer.on('check-dependencies-reply', listener);

    // cleanup function to remove the listener when the component unmounts
    return removeListener;
  }, []); // Empty dependency array, no need to listen to 'navigate'

  useEffect(() => {
    if (!loading) {
      const timer = setTimeout(() => {
        navigate('/home'); // navigate to /home after 5.5 seconds
      }, 5000); // time in milliseconds

      // cleanup function to clear the timer when the component unmounts
      return () => {
        clearTimeout(timer);
      };
    }
  }, [loading, navigate]); // Run this effect when 'loading' changes

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
            <span>{loadingText}</span> {/* Display the loading text */}
        </div>
    </div>
  );
}

export default IntroScreen;