import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="navigation">
      <div className="nav-brand">
        <h2>💰 Wealth Tracker</h2>
      </div>
      <div className="nav-links">
        <Link 
          to="/" 
          className={location.pathname === '/' ? 'nav-link active' : 'nav-link'}
        >
          Dashboard
        </Link>
        <Link 
          to="/add" 
          className={location.pathname === '/add' ? 'nav-link active' : 'nav-link'}
        >
          Add Individual
        </Link>
        <Link 
          to="/view" 
          className={location.pathname === '/view' ? 'nav-link active' : 'nav-link'}
        >
          View All
        </Link>
        <Link 
          to="/ranking" 
          className={location.pathname === '/ranking' ? 'nav-link active' : 'nav-link'}
        >
          Wealth Ranking
        </Link>
        <Link 
          to="/analytics" 
          className={location.pathname === '/analytics' ? 'nav-link active' : 'nav-link'}
        >
          Analytics
        </Link>
      </div>
    </nav>
  );
};

export default Navigation;