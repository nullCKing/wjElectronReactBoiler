import React, { useEffect } from 'react';
import { RiFileExcel2Fill } from 'react-icons/ri';
import { states, industries } from './Constants';

type CheckboxArray = boolean[];

interface Props 
{
    stateCheckboxes: CheckboxArray;
    industryCheckboxes: CheckboxArray;
    unlistedIndustry: boolean;
    unlistedLocation: boolean;
    unlistedPrice: boolean;
    sunbeltNetwork: boolean;
    synergy: boolean;
    minGrossRevenue: number;
    maxGrossRevenue: number;
    minCashFlow: number;
    maxCashFlow: number;
    minListingPrice: number;
    maxListingPrice: number;
}

export const ExportComponent: React.FC<Props> = (
    {
      stateCheckboxes, 
      industryCheckboxes, 
      unlistedIndustry, 
      unlistedLocation, 
      unlistedPrice, 
      sunbeltNetwork, 
      synergy,
      minGrossRevenue,
      maxGrossRevenue,
      minCashFlow,
      maxCashFlow,
      minListingPrice,
      maxListingPrice
    }) => {
    useEffect(() => {
        const unsubscribe = window.electron.ipcRenderer.on('select-directory-reply', (result) => {
            console.log(result);
        });

        return () => {
            unsubscribe();
        };
        }, []);

        const handleClick = () => {
            let checkedStates = states.filter((_, i) => stateCheckboxes[i]);
            let checkedIndustries = industries.filter((_, i) => industryCheckboxes[i]);
            window.electron.ipcRenderer.sendMessage(
              'select-directory', 
              'button clicked', 
              checkedStates, 
              checkedIndustries,
              unlistedIndustry,
              unlistedLocation,
              unlistedPrice,
              sunbeltNetwork,
              synergy,
              minGrossRevenue,
              maxGrossRevenue,
              minCashFlow,
              maxCashFlow,
              minListingPrice,
              maxListingPrice
            );
          };

        return (
        <div className="button-container" style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
            <button style={{ backgroundColor: '#217346', color: 'white' }} onClick={handleClick}>
                <RiFileExcel2Fill />
                Export
            </button>
        </div>
        );
}