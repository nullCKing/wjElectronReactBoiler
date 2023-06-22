import React, {useState, ReactNode, useEffect } from 'react';
import ReactDOM from 'react-dom';
import {TiChevronLeftOutline, TiChevronRightOutline} from 'react-icons/ti';
import './Queue.scss'
import { QueueNavBar } from './QueueNavBar';
import { RiFileExcel2Fill } from 'react-icons/ri';
import { fetchData } from '../main/firebase';


const CARDS = 10;
const MAX_VISIBILITY = 3;

type CardProps = {
  date: string;
  time: string;
  industryQuantity: number;  
  stateQuantity: number;     
  VR: boolean;
  sunbelt: boolean;

};

type CarouselProps = {
    children: ReactNode[];
  };
  
  const Card: React.FC<CardProps & { isActive?: boolean }> = ({ date, time, industryQuantity, stateQuantity, VR, sunbelt, isActive }) => (
    <div className='card'>
        {!isActive && <RiFileExcel2Fill size="2em" color="white"/>}
        <h2>{date} {time}</h2>
        <div className='card-body-text'> States/Territories Filtered: {stateQuantity} </div>
        <div className='card-body-text'> Industries Filtered: {industryQuantity} </div>
        <div className='card-body-text'> Sunbelt Enabled: {sunbelt ? 'true' : 'false'} </div>
        <div className='card-body-text'> VR Enabled: {VR ? 'true' : 'false'} </div>
    </div>
    );
    
    const Carousel: React.FC<CarouselProps> = ({ children }) => {
        const [active, setActive] = useState(2);
        const count = React.Children.count(children);
        
        return (
          <div className='carousel-body'>
              <div className='carousel'>
              {active > 0 && <button className='nav left' onClick={() => setActive(i => i - 1)}><TiChevronLeftOutline/></button>}
              {React.Children.map(children, (child, i) => {
                  // Check if the child is a valid React element before cloning
                  if (React.isValidElement(child)) {
                    return (
                      <div 
                        className='card-container' 
                        style={{
                            '--active': i === active ? 1 : 0,
                            '--offset': (active - i) / 3,
                            '--direction': Math.sign(active - i),
                            '--abs-offset': Math.abs(active - i) / 3,
                            'pointer-events': active === i ? 'auto' : 'none',
                            'opacity': Math.abs(active - i) >= MAX_VISIBILITY ? '0' : '1',
                            'display': Math.abs(active - i) > MAX_VISIBILITY ? 'none' : 'block',
                        } as any}>
                        {React.cloneElement(child as any, { isActive: i === active })}
                      </div>
                    );
                  }
                  return child;
              })}
              {active < count - 1 && <button className='nav right' onClick={() => setActive(i => i + 1)}><TiChevronRightOutline/></button>}
              </div>
          </div>
        );
      };

    const Queue = () => {
      const [data, setData] = useState<CardProps[]>([]);
    
      useEffect(() => {
        fetchData()
          .then((fetchedData) => {
            console.log(fetchedData);
            setData(fetchedData.map(log => ({
              date: log.date,
              time: log.time,
              stateQuantity: log.stateQuantity,
              industryQuantity: log.industryQuantity,
              VR: log.VR,
              sunbelt: log.sunbelt,
            })))
          })
          .catch((error) => console.error('Failed to fetch data: ', error));
      }, []);
        
        return (
        <div className='parent-queue'>
            <div className='queue-body'>
            <QueueNavBar/>
            <div className='log-title'> Export Log </div>
                <Carousel>
                {data.map((card, i) => (
                <Card 
                    key={i} 
                    date={card.date}
                    time={card.time}
                    stateQuantity={card.stateQuantity}
                    industryQuantity={card.industryQuantity}
                    sunbelt={card.sunbelt}
                    VR={card.VR}
                />
                ))}
                </Carousel>
            </div>
        </div>
        );
    }
  

export default Queue;