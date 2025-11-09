import React, { useState, useEffect } from 'react';
import { wealthAPI } from '../services/api';
import './WealthRanking.css';

const WealthRanking = () => {
  const [ranking, setRanking] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadRanking();
  }, []);

  const loadRanking = async () => {
    try {
      setLoading(true);
      const response = await wealthAPI.getWealthRanking(20);
      if (response.data.success) {
        setRanking(response.data.ranking);
      }
    } catch (err) {
      setError('Failed to load wealth ranking');
      console.error('Error loading ranking:', err);
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

  if (loading) {
    return <div className="loading">Loading wealth ranking...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="wealth-ranking">
      <h2>Wealth Ranking</h2>
      <div className="ranking-list">
        {ranking.map((item, index) => (
          <div key={item.individual.id} className="ranking-item">
            <div className="rank-number">#{index + 1}</div>
            <div className="individual-info">
              <div className="name">
                {item.individual.first_name} {item.individual.last_name}
              </div>
              <div className="company">{item.individual.company}</div>
              <div className="industry">{item.individual.industry}</div>
            </div>
            <div className="wealth-info">
              <div className="net-worth">{formatCurrency(item.net_worth)}</div>
              <div className="wealth-tier">{item.individual.wealth_tier}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WealthRanking;