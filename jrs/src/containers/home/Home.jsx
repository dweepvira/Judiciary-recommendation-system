import React from 'react';

import ai from '../../assets/ai.png';
import './home.css';

const Home = () => (
  <div className="jrs__header section__padding" id="home">
    <div className="jrs__header-content">
      <h1 className="gradient__text">Judiciary Recommendation System</h1>
      <p>The e-Committee, welcomes you to this portal showcasing the information and initiatives adopted by the judicial system. This is an end to end solution for judiciary officials to create a workflow of the cases filed and reviewed.</p>
      
      <div className="jrs_get">
      <a href="/register"><button type="button">Get Started &nbsp;</button></a>
      </div>
      
    </div>

    <div className="jrs__header-image">
      <img src={ai} alt="AI" />
    </div>
  </div>
);

export default Home;
