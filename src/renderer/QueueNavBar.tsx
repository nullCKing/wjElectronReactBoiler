import React, { useEffect } from 'react';
import { RiFileExcel2Fill } from 'react-icons/ri';
import { states, industries } from './Constants';
import './ExportComponent.css';
import { useNavigate } from 'react-router-dom';
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

export const QueueNavBar = (
    ) => {
    const navigate = useNavigate();

    const handleQueueNavigation = () => {
        navigate('/home');
    }

    return (
    <div className="button-container" style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
        <nav className="menu">
            <div className="menu__bg" onClick={handleQueueNavigation}>
                <svg className="menu__icon menu__icon--hoverable" style={{ cursor: 'pointer', color: '#217346', backgroundColor: 'white', width: '25px', height: '25px' }} fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"></path>
                </svg>    
            </div>

            <div className="menu__bg">
                <RiFileExcel2Fill style={{ cursor: 'pointer', color: '#9CA3AF', backgroundColor: 'white' }} className="menu__icon menu__icon--hoverable"/>
            </div>

            <div className="menu__bg">
                <svg className="menu__icon menu__icon--hoverable" style={{ cursor: 'pointer', color: '#217346', backgroundColor: 'white', width: '25px', height: '25px' }} fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z"></path>
                </svg>
            </div>
        </nav>
    </div>
    );
}

export default QueueNavBar;
