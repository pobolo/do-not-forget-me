import React, { useState } from 'react';
import './IndividualCard.css';

const IndividualCard = ({ individual, onEdit, onDelete }) => {
  const [showDetails, setShowDetails] = useState(false);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getWealthTierColor = (tier) => {
    switch (tier) {
      case 'Ultra High Net Worth':
        return '#e74c3c';
      case 'High Net Worth':
        return '#e67e22';
      case 'Affluent':
        return '#27ae60';
      default:
        return '#95a5a6';
    }
  };

  return (
    <div className="individual-card">
      <div className="card-header">
        <div className="name-section">
          <h3>{individual.first_name} {individual.last_name}</h3>
          <span 
            className="wealth-tier"
            style={{ backgroundColor: getWealthTierColor(individual.wealth_tier) }}
          >
            {individual.wealth_tier}
          </span>
        </div>
        <div className="net-worth">
          {formatCurrency(individual.net_worth)}
        </div>
      </div>

      <div className="card-content">
        <div className="info-row">
          <span className="label">Company:</span>
          <span className="value">{individual.company}</span>
        </div>
        <div className="info-row">
          <span className="label">Title:</span>
          <span className="value">{individual.title}</span>
        </div>
        <div className="info-row">
          <span className="label">Industry:</span>
          <span className="value">{individual.industry}</span>
        </div>
        
        {showDetails && (
          <div className="detailed-info">
            <div className="info-row">
              <span className="label">Source of Wealth:</span>
              <span className="value">{individual.source_of_wealth}</span>
            </div>
            <div className="info-row">
              <span className="label">Email:</span>
              <span className="value">{individual.email}</span>
            </div>
            {individual.phone && (
              <div className="info-row">
                <span className="label">Phone:</span>
                <span className="value">{individual.phone}</span>
              </div>
            )}
            {(individual.city || individual.state) && (
              <div className="info-row">
                <span className="label">Location:</span>
                <span className="value">
                  {[individual.city, individual.state].filter(Boolean).join(', ')}
                </span>
              </div>
            )}
            <div className="info-row">
              <span className="label">Last Contact:</span>
              <span className="value">
                {new Date(individual.last_contact_date).toLocaleDateString()}
              </span>
            </div>
          </div>
        )}
      </div>

      <div className="card-actions">
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="btn btn-outline"
        >
          {showDetails ? 'Hide Details' : 'Show Details'}
        </button>
        <div className="action-buttons">
          <button
            onClick={() => onEdit(individual)}
            className="btn btn-edit"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(individual.id)}
            className="btn btn-delete"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default IndividualCard;