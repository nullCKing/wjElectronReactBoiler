import React, { useEffect, useState } from 'react';
import Lottie from 'lottie-react';
import spinnerAnimation from './sync-icon.json';
import './IntroScreen.css';
import { useNavigate } from 'react-router-dom';
import { storeHwid, fetchHwids } from '../main/firebase';

function IntroScreen() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [loadingText, setLoadingText] = useState("Loading content...");
  const [hwid, setHwid] = useState<string | null>(null);

  useEffect(() => {
    // Request the hwid from the main process
    window.electron.ipcRenderer.sendMessage('get-hwid');

    // Function to handle the response
    const handleHwidResponse = (...args: unknown[]) => {
      // Cast the first argument to a string
      const receivedHwid = args[0] as string;
      setHwid(receivedHwid);
    };

    // Set up the response listener
    const removeListener = window.electron.ipcRenderer.on('get-hwid-response', handleHwidResponse);

    // Clean up the listener when the component unmounts
    return () => {
      removeListener();
    }
}, []);  // Run this effect on mount

useEffect(() => {
  const checkDependencies = async () => {
    // Explicitly check hwid is not null before calling fetchHwids
    if (hwid !== null) {
      const hwidList = await fetchHwids(hwid);

      if (!hwidList.includes(hwid)) {
        // The current HWID is not in the list, store it and download dependencies
        // Explicitly check hwid is not null before calling storeHwid
        if (hwid !== null) {
          await storeHwid(hwid);
        }
        window.electron.ipcRenderer.sendMessage('check-dependencies');
        setLoadingText("Downloading first time dependencies...");
        // Set longer loading time for first time dependencies download
        return 5 * 60 * 1000; // 5 minutes
      } else {
        // The HWID is already in the list, proceed as usual
        return 5000; // 5 seconds
      }
    }
  }

    if (hwid) {
      checkDependencies().then(loadingDuration => {
        // Start the loading timer
        const timer = setTimeout(() => {
          setLoading(false);
        }, loadingDuration);

        // Cleanup function
        return () => {
          clearTimeout(timer);
        };
      });
    }
    
}, [hwid]);  // Run this effect whenever 'hwid' changes

  useEffect(() => {
    if (!loading) {
      const timer = setTimeout(() => {
        navigate('/home'); // navigate to /home after 5.5 seconds
      }, 500); // time in milliseconds

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
        <span>{loadingText}</span>
      </div>
    </div>
  );
}

export default IntroScreen;
