import { ipcRenderer } from 'electron';
import './Home.css';
import { RiFileExcel2Fill } from 'react-icons/ri';
import React, { ChangeEvent, useState, useEffect } from 'react';
import IntroScreen from './IntroScreen';
import { ExportComponent } from './ExportComponent';
import { states, industries } from './Constants';

type State = boolean[];
type Industry = boolean[];
type SliderValue = number;

const Home: React.FC = () => {
  const [showIntro, setShowIntro] = useState(true); 
  const [stateCheckboxes, setStateCheckboxes] = useState<State>(Array(states.length).fill(false));
  const [industryCheckboxes, setIndustryCheckboxes] = useState<Industry>(Array(industries.length).fill(false));
  const [allStatesChecked, setAllStatesChecked] = useState<boolean>(false);
  const [allIndustriesChecked, setAllIndustriesChecked] = useState<boolean>(false);
  const [unlistedIndustry, setUnlistedIndustry] = useState(false);
  const [unlistedLocation, setUnlistedLocation] = useState(false);
  const [unlistedGR, setUnlistedGR] = useState(false);
  const [unlistedCF, setUnlistedCF] = useState(false);
  const [unlistedLP, setUnlistedLP] = useState(false);
  const [unlistedPrice, setUnlistedPrice] = useState(false);
  const [sunbeltNetwork, setSunbeltNetwork] = useState(true);
  const [synergy, setSynergy] = useState(true);


  const [minGrossRevenue, setMinGrossRevenue] = useState(0);
  const [maxGrossRevenue, setMaxGrossRevenue] = useState(1000000);
  const [minCashFlow, setMinCashFlow] = useState(0);
  const [maxCashFlow, setMaxCashFlow] = useState(1000000);
  const [minListingPrice, setMinListingPrice] = useState(0);
  const [maxListingPrice, setMaxListingPrice] = useState(1000000);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowIntro(false);
    }, 6500);  // Adjust this to change the delay. 5000ms = 5 seconds

    return () => clearTimeout(timer); // This function clears the timer when the component unmounts.
  }, []);

  const handleStateCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const index = states.indexOf(event.target.name);
    setStateCheckboxes((prev) => {
      const copy = [...prev];
      copy[index] = event.target.checked;
      return copy;
    });
  };

  const handleIndustryCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const index = industries.indexOf(event.target.name);
    setIndustryCheckboxes((prev) => {
      const copy = [...prev];
      copy[index] = event.target.checked;
      return copy;
    });
  };

  const handleSelectAll = () => {
    console.log('Select/Deselect All States button was clicked');
    console.log("Before allStatesChecked", allStatesChecked);
  
    // Switch the flag
    const newStateChecked = !allStatesChecked;
    setAllStatesChecked(newStateChecked);
  
    // Use the newStateChecked directly for creating new checks
    const newChecks = Array(states.length).fill(newStateChecked);
    setStateCheckboxes(newChecks);
  };
  
  const handleSelectAllIndustries = () => {
    console.log("Before allIndustriesChecked", allIndustriesChecked);
  
    // Switch the flag
    const newIndustryChecked = !allIndustriesChecked;
    setAllIndustriesChecked(newIndustryChecked);
  
    // Use the newIndustryChecked directly for creating new checks
    const newChecks = Array(industries.length).fill(newIndustryChecked);
    setIndustryCheckboxes(newChecks);
  };

  const statesPerTile = Math.ceil(states.length / 5);
  const industriesPerTile = Math.ceil(industries.length / 5);

  const tileStyle = {
    display: 'grid',
    gridTemplateColumns: `repeat(${statesPerTile}, 1fr)`,
    gap: '1rem',
    padding: '1rem',
    border: '2px solid black',
    borderRadius: '10px',
    flexBasis: '90%',
    marginBottom: '20px',
  };

  const leftTileStyle = {
    gap: '1rem',
    padding: '1rem',
    border: '2px solid black',
    borderRadius: '10px',
    flexBasis: '35%',
    marginBottom: '20px',
  };

  const secondtileStyle = {
    display: 'grid',
    gridTemplateColumns: `repeat(${industriesPerTile}, 1fr)`,
    gap: '1rem',
    padding: '1rem',
    border: '2px solid black',
    borderRadius: '10px',
    flexBasis: '90%',
    marginBottom: '20px',
  };
  
  return (
    <>
    <div className="parent">

    <ExportComponent 
        stateCheckboxes={stateCheckboxes} 
        industryCheckboxes={industryCheckboxes} 
        unlistedIndustry={unlistedIndustry} 
        unlistedLocation={unlistedLocation} 
        unlistedPrice={unlistedPrice} 
        sunbeltNetwork={sunbeltNetwork} 
        synergy={synergy} 
        minGrossRevenue={minGrossRevenue} 
        maxGrossRevenue={maxGrossRevenue} 
        minCashFlow={minCashFlow} 
        maxCashFlow={maxCashFlow} 
        minListingPrice={minListingPrice} 
        maxListingPrice={maxListingPrice}
    />

    <div className="container-main" style={{ display: 'flex' }}>

      <div className="entry-tile" style={leftTileStyle}>

        <div className="entry" style={{flexDirection: 'column'}}>
          <label>Gross Revenue</label>
          <input 
              className="entry-spacing" 
              type="number" 
              name="minGrossRevenue" 
              placeholder="Minimum" 
              value={minGrossRevenue} 
              onChange={e => setMinGrossRevenue(Number(e.target.value))} 
          />
          <input 
              type="number" 
              name="maxGrossRevenue" 
              placeholder="Maximum" 
              value={maxGrossRevenue} 
              onChange={e => setMaxGrossRevenue(Number(e.target.value))} 
          />      
        </div>

        <div className="entry" style={{flexDirection: 'column'}}>
          <label>Cash Flow</label>
          <input 
              className="entry-spacing" 
              type="number" 
              name="minCashFlow" 
              placeholder="Minimum" 
              value={minCashFlow} 
              onChange={e => setMinCashFlow(Number(e.target.value))} 
          />
          <input 
              type="number" 
              name="maxCashFlow" 
              placeholder="Maximum" 
              value={maxCashFlow} 
              onChange={e => setMaxCashFlow(Number(e.target.value))} 
          />
        </div>

        <div className="entry" style={{flexDirection: 'column'}}>
          <label>Listing Price</label>
          <input 
              className="entry-spacing" 
              type="number" 
              name="minListingPrice" 
              placeholder="Minimum" 
              value={minListingPrice} 
              onChange={e => setMinListingPrice(Number(e.target.value))} 
          />
          <input 
              type="number" 
              name="maxListingPrice" 
              placeholder="Maximum" 
              value={maxListingPrice} 
              onChange={e => setMaxListingPrice(Number(e.target.value))} 
          />
        </div>

        <div className="entry" style={{textAlign: 'center'}}>
          <label>Toggle unlisted properties (off by default)</label>
        </div>

        <div className="entry">
          <div className="checkbox-container">
            <input className="checkbox-input" type="checkbox" id="unlistedIndustry" name="unlistedParameter" checked={unlistedIndustry} onChange={() => setUnlistedIndustry(!unlistedIndustry)} />
            <label className="checkbox-label" htmlFor="unlistedIndustry">Enable unlisted industry parameter</label>
          </div>
          <div className="checkbox-container">
            <input className="checkbox-input" type="checkbox" id="unlistedLocation" name="unlistedParameter" checked={unlistedLocation} onChange={() => setUnlistedLocation(!unlistedLocation)} />
            <label className="checkbox-label" htmlFor="unlistedLocation">Enable unlisted location parameter</label>
          </div>
          <div className="checkbox-container">
            <input className="checkbox-input" type="checkbox" id="unlistedPrice" name="unlistedParameter" checked={unlistedPrice} onChange={() => setUnlistedPrice(!unlistedPrice)} />
            <label className="checkbox-label" htmlFor="unlistedPrice">Enable unlisted price parameter</label>
          </div>
          <div className="checkbox-container">
            <input className="checkbox-input" type="checkbox" id="unlistedGR" name="unlistedParameter" checked={unlistedGR} onChange={() => setUnlistedGR(!unlistedGR)} />
            <label className="checkbox-label" htmlFor="unlistedGR">Enable unlisted gross revenue</label>
          </div>
          <div className="checkbox-container">
            <input className="checkbox-input" type="checkbox" id="unlistedCF" name="unlistedParameter" checked={unlistedCF} onChange={() => setUnlistedCF(!unlistedCF)} />
            <label className="checkbox-label" htmlFor="unlistedCF">Enable unlisted cash flow</label>
          </div>
          <div className="checkbox-container">
            <input className="checkbox-input" type="checkbox" id="unlistedLP" name="unlistedParameter" checked={unlistedLP} onChange={() => setUnlistedLP(!unlistedLP)} />
            <label className="checkbox-label" htmlFor="unlistedLP">Enable unlisted listing price</label>
          </div>
        </div>

        <div className="entry" style={{textAlign: 'center'}}>
          <label>Toggle brokerages (on by default)</label>
        </div>

        <div className="entry">
          <div className="checkbox-container">
            <input className="checkbox-input" type="checkbox" id="sunbeltNetwork" name="networkParameter" checked={sunbeltNetwork} onChange={() => setSunbeltNetwork(!sunbeltNetwork)} />
            <label className="checkbox-label" htmlFor="sunbeltNetwork">Enable Sunbelt Network Collection</label>
          </div>
          <div className="checkbox-container">
            <input className="checkbox-input" type="checkbox" id="synergy" name="networkParameter" checked={synergy} onChange={() => setSynergy(!synergy)} />
            <label className="checkbox-label" htmlFor="synergy">Enable VR Collection </label>
          </div>
        </div>

      </div>

        <div className="right-side-container" style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="states-tile" style={{ ...tileStyle, display: 'flex', flexDirection: 'column' }}>
            <div className="button-container">
              <button onClick={handleSelectAll}>Select/Deselect All</button>
            </div>
            <div className="checkbox-grid">
              {states.map((state, index) => (
                <div key={state}>
                  <label>
                    <input
                      type="checkbox"
                      name={state}
                      checked={stateCheckboxes[index]} 
                      onChange={handleStateCheckboxChange}
                    />
                    {state}
                  </label>
                </div>
              ))}
            </div>
          </div>
          <div className="industry-tile" style={{ ...secondtileStyle, display: 'flex', flexDirection: 'column' }}>
            <div className="button-container">
              <button onClick={handleSelectAllIndustries}>Hi Mom! Select/Deselect All</button>
            </div>
            <div className="checkbox-grid">
              {industries.map((industry, index) => (
                <div key={industry}>
                  <label>
                    <input
                      type="checkbox"
                      name={industry}
                      checked={industryCheckboxes[index]} 
                      onChange={handleIndustryCheckboxChange}
                    />
                    {industry}
                  </label>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
    </>
  );
}

export default Home;
