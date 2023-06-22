import React from 'react';
import { HashRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home'; 
import Queue from './Queue';
import IntroScreen from './IntroScreen';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<IntroScreen />} />
        <Route path="/home" element={<Home />} />
        <Route path="/queue" element={<Queue />} />
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;