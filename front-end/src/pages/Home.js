import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { wealthAPI } from '../services/api';
import './Home.css';

const Home = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await wealthAPI.getStats();
      if (response.data.success) {
        setStats(response.data.wealth_statistics);
      }
    } catch (err) {
      console.error('Error loading stats:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Wealth Tracker</h1>
        <p>Manage and analyze wealthy individuals data with Redis-powered storage</p>
        <div className="hero-actions">
          <Link to="/add" className="btn btn-primary btn-large">
            Add New Individual
          </Link>
          <Link to="/view" className="btn btn-secondary btn-large">
            View All Individuals
          </Link>
        </div>
      </div>

      {!loading && stats && (
        <div className="quick-stats">
          <h2>Quick Overview</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">{stats.total_individuals}</div>
              <div className="stat-label">Total Individuals</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{formatCurrency(stats.total_wealth)}</div>
              <div className="stat-label">Total Wealth</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{formatCurrency(stats.average_wealth)}</div>
              <div className="stat-label">Average Wealth</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">
                {Object.keys(stats.industry_distribution || {}).length}
              </div>
              <div className="stat-label">Industries</div>
            </div>
          </div>
        </div>
      )}

      <div className="features-section">
        <h2>Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">👤</div>
            <h3>Manage Individuals</h3>
            <p>Add, edit, and delete wealthy individual records with comprehensive information</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💰</div>
            <h3>Wealth Ranking</h3>
            <p>View individuals ranked by net worth with real-time updates</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Analytics</h3>
            <p>Get insights into wealth distribution and industry trends</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Redis Powered</h3>
            <p>Lightning-fast performance with Redis in-memory data storage</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;