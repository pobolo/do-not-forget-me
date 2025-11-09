import React, { useState, useEffect } from 'react';
import { wealthAPI } from '../services/api';
import './IndividualForm.css';

const IndividualForm = ({ individual, onSave, onCancel, isEdit = false }) => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    company: '',
    title: '',
    net_worth: '',
    industry: '',
    source_of_wealth: '',
    email: '',
    phone: '',
    city: '',
    state: '',
    last_contact_date: new Date().toISOString().split('T')[0]
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const industries = [
    'Technology',
    'Finance',
    'Real Estate',
    'Healthcare',
    'Manufacturing',
    'Retail',
    'Energy',
    'Media',
    'Entertainment',
    'Other'
  ];

  useEffect(() => {
    if (individual && isEdit) {
      setFormData({
        first_name: individual.first_name || '',
        last_name: individual.last_name || '',
        company: individual.company || '',
        title: individual.title || '',
        net_worth: individual.net_worth || '',
        industry: individual.industry || '',
        source_of_wealth: individual.source_of_wealth || '',
        email: individual.email || '',
        phone: individual.phone || '',
        city: individual.city || '',
        state: individual.state || '',
        last_contact_date: individual.last_contact_date ? individual.last_contact_date.split('T')[0] : new Date().toISOString().split('T')[0]
      });
    }
  }, [individual, isEdit]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const submitData = {
        ...formData,
        net_worth: parseFloat(formData.net_worth)
      };

      let result;
      if (isEdit && individual) {
        result = await wealthAPI.updateIndividual(individual.id, submitData);
      } else {
        result = await wealthAPI.createIndividual(submitData);
      }

      if (result.data.success) {
        onSave(result.data.individual);
        if (!isEdit) {
          // Reset form for new entries
          setFormData({
            first_name: '',
            last_name: '',
            company: '',
            title: '',
            net_worth: '',
            industry: '',
            source_of_wealth: '',
            email: '',
            phone: '',
            city: '',
            state: '',
            last_contact_date: new Date().toISOString().split('T')[0]
          });
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save individual');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="individual-form-container">
      <form onSubmit={handleSubmit} className="individual-form">
        <h2>{isEdit ? 'Edit Individual' : 'Add New Individual'}</h2>
        
        {error && <div className="error-message">{error}</div>}

        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="first_name">First Name *</label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="last_name">Last Name *</label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="company">Company *</label>
            <input
              type="text"
              id="company"
              name="company"
              value={formData.company}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="net_worth">Net Worth ($) *</label>
            <input
              type="number"
              id="net_worth"
              name="net_worth"
              value={formData.net_worth}
              onChange={handleChange}
              min="0"
              step="1000000"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="industry">Industry *</label>
            <select
              id="industry"
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              required
            >
              <option value="">Select Industry</option>
              {industries.map(industry => (
                <option key={industry} value={industry}>
                  {industry}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="source_of_wealth">Source of Wealth *</label>
            <input
              type="text"
              id="source_of_wealth"
              name="source_of_wealth"
              value={formData.source_of_wealth}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone">Phone</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="city">City</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="state">State</label>
            <input
              type="text"
              id="state"
              name="state"
              value={formData.state}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="last_contact_date">Last Contact Date</label>
            <input
              type="date"
              id="last_contact_date"
              name="last_contact_date"
              value={formData.last_contact_date}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={onCancel}
            className="btn btn-secondary"
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Saving...' : (isEdit ? 'Update' : 'Add Individual')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default IndividualForm;