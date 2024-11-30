import React from 'react';
import Sparkles from './Sparkles';
import './Header.css';

const Header = () => (
    <header className="header">
        <div className="header-container">
            <h1 className="brand-title">AAPlants</h1>
            <nav className="nav">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/shop">Shop</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
            <Sparkles />
        </div>
    </header>
);

export default Header;
