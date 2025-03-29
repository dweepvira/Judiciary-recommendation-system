import React, { useState } from 'react';
import court from '../../assets/court.jpg';
import { RiMenu3Line, RiCloseLine } from 'react-icons/ri';
import './navbar.css';

const Navbar = () => {
  const [toggleMenu, setToggleMenu] = useState(false);

  return (
    <div className="gpt3__navbar">
      <div className="gpt3__navbar-links_logo">
          <img src={court} alt=""/>
        </div>
      <div className="gpt3__navbar-links">
        
        <div className="gpt3__navbar-links_container">
          <p><a href="/">HOME</a></p>
          <p><a href="#wgpt3"></a></p>
          <p><a href="/register">IPC SECTIONS</a></p>
          <p><a href="/review">SIMILAR CASES</a></p>
          <p><a href="/case"></a></p>
        </div>
      </div>
      
      
      
      <div className="gpt3__navbar-menu">
      {toggleMenu
          ? <RiCloseLine color="#fff" size={27} onClick={() => setToggleMenu(false)} />
          : <RiMenu3Line color="#fff" size={27} onClick={() => setToggleMenu(true)} />}
          
        {toggleMenu && (
        <div className="gpt3__navbar-menu_container scale-up-center">
          <div className="gpt3__navbar-menu_container-links">
            <p><a href="/home">HOME</a></p>
            <p><a href="#"></a></p>
            <p><a href="/register">IPC SECTIONS</a></p>
            <p><a href="/review">SIMILAR CASES</a></p>
            <p><a href="/case"></a></p>
          </div>
          
        </div>
        )}
      </div>
    </div>
  );
};

export default Navbar;
