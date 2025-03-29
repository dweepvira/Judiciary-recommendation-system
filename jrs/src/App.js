import React from 'react';
import { Routes, Route } from 'react-router-dom';


import Review from './containers/review/Review'
import Register from './containers/register/Register'
import Home from './containers/home/Home'
import Navbar from './containers/navbar/Navbar'


import './App.css';


const App = () => (
  <div className="App">
    <div className="gradient__bg">
      <Navbar />
      
      <Routes>
      <Route exact path="/" element={<Home/>} />
      <Route exact path="/register" element={<Register/>} />
      <Route exact path="/review" element={<Review/>} />
      
    </Routes>
      
    
    </div>
    
  </div>
  
  
    
);



export default App;
